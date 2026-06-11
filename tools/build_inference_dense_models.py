#!/usr/bin/env python3
"""Build dense inference GLBs from all-view Gen3R result folders."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image

from build_inference_assets import (
    BASE_DEFAULT,
    case_id_from_path,
    read_cases,
    read_ply_points,
    write_point_glb,
)


ALL_VIEW_ROOT_DEFAULT = BASE_DEFAULT / "Gen3R/results/assert_rgbframes_gen3r_allview_once"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=BASE_DEFAULT)
    parser.add_argument("--assert-file", type=Path, default=None)
    parser.add_argument("--all-view-root", type=Path, default=ALL_VIEW_ROOT_DEFAULT)
    parser.add_argument("--run", type=str, default="latest")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--max-points", type=int, default=0)
    parser.add_argument("--points-per-frame", type=int, default=60000)
    parser.add_argument("--source", choices=("pointmaps", "ply"), default="pointmaps")
    parser.add_argument("--case-token", action="append", default=[])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base = args.base.resolve()
    assert_file = args.assert_file or (base / "assert_inference_dir.txt")
    all_view_root = args.all_view_root.resolve()
    run_dir = resolve_run_dir(all_view_root, args.run)
    out = (args.out or (base / "project_page_inference_dense_models")).resolve()
    out.mkdir(parents=True, exist_ok=True)

    cases = read_cases(assert_file, base)
    manifest = []
    skipped = []
    for all_view_case in sorted(run_dir.iterdir()):
        if not all_view_case.is_dir():
            continue
        source_index = source_index_from_name(all_view_case.name)
        if source_index is None:
            continue
        if source_index >= len(cases):
            skipped.append({"directory": all_view_case.name, "reason": "source index outside assert list"})
            continue

        original_case = cases[source_index]
        case_id = case_id_from_path(original_case)
        if args.case_token and not any(
            token in case_id or token in str(original_case) or token in all_view_case.name
            for token in args.case_token
        ):
            continue

        ply = all_view_case / "pcds.ply"
        cameras = all_view_case / "cameras.json"
        if not ply.exists() or not cameras.exists():
            skipped.append({"id": case_id, "directory": all_view_case.name, "reason": "incomplete"})
            continue

        print(f"{all_view_case.name} -> {case_id}", flush=True)
        if args.source == "pointmaps":
            points, colors = read_pointmap_points(
                all_view_case,
                points_per_frame=args.points_per_frame,
                seed=2026 + source_index,
            )
        else:
            points, colors = read_ply_points(ply)
        point_count = int(len(points))
        if args.max_points > 0 and len(points) > args.max_points:
            rng = np.random.default_rng(2026 + source_index)
            choice = rng.choice(len(points), args.max_points, replace=False)
            points = points[choice]
            colors = colors[choice]

        points, center = normalize_points_with_center(points)
        model = out / f"{case_id}.glb"
        write_point_glb(points, colors, model)
        manifest.append(
            {
                "id": case_id,
                "sourceIndex": source_index + 1,
                "allViewPath": str(all_view_case),
                "originalPath": str(original_case),
                "model": model.name,
                "cameraOrbit": camera_orbit_from_average_center(cameras, center),
                "modelOrientation": "180deg 0deg 0deg",
                "points": point_count,
                "glbBytes": model.stat().st_size,
                "source": args.source,
            }
        )

    (out / "dense_models_manifest.json").write_text(
        json.dumps({"run": str(run_dir), "models": manifest, "skipped": skipped}, indent=2),
        encoding="utf-8",
    )
    print(f"wrote {len(manifest)} dense models to {out}", flush=True)
    if skipped:
        print(f"skipped {len(skipped)} incomplete/unmatched cases", flush=True)


def resolve_run_dir(root: Path, run: str) -> Path:
    if run != "latest":
        candidate = root / run
        if not candidate.exists():
            raise FileNotFoundError(candidate)
        return candidate
    runs = sorted([path for path in root.iterdir() if path.is_dir()])
    if not runs:
        raise FileNotFoundError(f"no all-view runs under {root}")
    return runs[-1]


def source_index_from_name(name: str) -> int | None:
    match = re.match(r"^(\d+)_", name)
    if not match:
        return None
    return int(match.group(1))


def read_pointmap_points(case_dir: Path, points_per_frame: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    pointmaps = np.load(case_dir / "pointmaps.npy")
    frame_paths = sorted((case_dir / "rgb_frames").glob("*.png"))
    if len(frame_paths) < len(pointmaps):
        raise RuntimeError(f"{case_dir} has {len(pointmaps)} point maps but only {len(frame_paths)} RGB frames")

    rng = np.random.default_rng(seed)
    points = []
    colors = []
    for frame_index, pointmap in enumerate(pointmaps):
        rgb = np.asarray(Image.open(frame_paths[frame_index]).convert("RGB"), dtype=np.float32) / 255.0
        flat_points = pointmap.reshape((-1, 3))
        flat_colors = rgb.reshape((-1, 3))
        valid = np.isfinite(flat_points).all(axis=1) & (np.linalg.norm(flat_points, axis=1) > 1e-6)
        valid_indices = np.flatnonzero(valid)
        if len(valid_indices) == 0:
            continue
        if points_per_frame > 0 and len(valid_indices) > points_per_frame:
            valid_indices = rng.choice(valid_indices, points_per_frame, replace=False)
        points.append(flat_points[valid_indices].astype(np.float32, copy=False))
        colors.append(flat_colors[valid_indices].astype(np.float32, copy=False))

    if not points:
        raise RuntimeError(f"no valid pointmap points in {case_dir}")
    return np.concatenate(points, axis=0), np.concatenate(colors, axis=0)


def normalize_points_with_center(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    center = np.median(points, axis=0)
    points = points - center
    scale = np.percentile(np.linalg.norm(points, axis=1), 94)
    if not np.isfinite(scale) or scale < 1e-5:
        scale = 1.0
    return points / scale, center


def camera_orbit_from_average_center(cameras_path: Path, scene_center: np.ndarray) -> str:
    if not cameras_path.exists():
        return "0deg 88deg auto"
    cameras = json.loads(cameras_path.read_text(encoding="utf-8"))
    extrinsics = np.asarray(cameras["extrinsics"], dtype=np.float64)
    centers = []
    for extrinsic in extrinsics:
        c2w = np.linalg.inv(extrinsic)
        centers.append(c2w[:3, 3])
    camera_center = np.mean(np.asarray(centers), axis=0)
    direction = camera_center - np.asarray(scene_center, dtype=np.float64)
    norm = np.linalg.norm(direction)
    if not np.isfinite(norm) or norm < 1e-8:
        return "0deg 88deg auto"

    # The inference point clouds are displayed with model-viewer orientation
    # "180deg 0deg 0deg", so rotate the desired camera vector the same way.
    direction = np.array([direction[0], -direction[1], -direction[2]], dtype=np.float64) / norm
    theta = np.degrees(np.arctan2(direction[0], direction[2]))
    theta = normalize_degrees(theta + 180.0)
    polar = np.degrees(np.arccos(np.clip(direction[1], -1.0, 1.0)))
    polar = float(np.clip(polar, 18.0, 88.0))
    return f"{theta:.1f}deg {polar:.1f}deg auto"


def normalize_degrees(value: float) -> float:
    return ((value + 180.0) % 360.0) - 180.0


if __name__ == "__main__":
    main()
