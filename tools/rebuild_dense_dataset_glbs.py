#!/usr/bin/env python3
"""Rebuild denser dataset GLB previews without regenerating videos or thumbs."""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from pathlib import Path


BASE_DEFAULT = Path("/mnt/shared-storage-user/steai-share/zhuxinnan")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=BASE_DEFAULT)
    parser.add_argument("--out", type=Path, default=BASE_DEFAULT / "project_page_dense_glbs")
    parser.add_argument("--points-per-frame", type=int, default=0)
    parser.add_argument("--point-frames", type=str, default="0,6,12,18,24,30,36,42,48")
    parser.add_argument("--max-model-points", type=int, default=0)
    parser.add_argument("--point-size", type=float, default=0.022)
    parser.add_argument("--depth-max", type=float, default=35.0)
    parser.add_argument("--skip-token", action="append", default=["diningroom_09"])
    parser.add_argument("--case-token", action="append", default=[])
    return parser.parse_args()


def main() -> None:
    os.environ.setdefault("OPENCV_IO_ENABLE_OPENEXR", "1")
    args = parse_args()
    base = args.base.resolve()
    out = args.out.resolve()
    out.relative_to(base)
    out.mkdir(parents=True, exist_ok=True)

    builder = load_builder(Path(__file__).with_name("project_page_build_dataset_assets_dense.py"))
    frame_indices = builder.parse_int_list(args.point_frames)
    cases = builder.read_cases(base / "assert_dir.txt", base)

    written = 0
    for case in cases:
        case.path.resolve().relative_to(base)
        if any(token and token in str(case.path) for token in args.skip_token):
            continue
        if args.case_token and not any(token in str(case.path) for token in args.case_token):
            continue
        for side in ("before", "after"):
            model = out / f"{case.id}_{side}.glb"
            builder.build_point_glb(
                case.path,
                side,
                model,
                frame_indices=frame_indices,
                points_per_frame=args.points_per_frame,
                max_points=args.max_model_points,
                point_size=args.point_size,
                depth_max=args.depth_max,
            )
            written += 1
            print(f"wrote {model}", flush=True)

    print(f"done: {written} GLBs in {out}", flush=True)


def load_builder(path: Path):
    spec = importlib.util.spec_from_file_location("dataset_asset_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    main()
