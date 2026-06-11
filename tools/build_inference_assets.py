#!/usr/bin/env python3
"""Build project-page inference assets from Gen3R result folders."""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
import subprocess
from pathlib import Path

import numpy as np


BASE_DEFAULT = Path("/mnt/shared-storage-user/steai-share/zhuxinnan")
FFMPEG_DEFAULT = (
    BASE_DEFAULT
    / "miniconda3/envs/trellis/lib/python3.10/site-packages/"
    "imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=BASE_DEFAULT)
    parser.add_argument("--assert-file", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--video-size", type=int, default=560)
    parser.add_argument("--max-points", type=int, default=0)
    parser.add_argument("--ffmpeg", type=Path, default=FFMPEG_DEFAULT)
    parser.add_argument("--case-token", action="append", default=[])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base = args.base.resolve()
    assert_file = args.assert_file or (base / "assert_inference_dir.txt")
    out = (args.out or (base / "project_page_inference_asset_staging")).resolve()
    media_out = out / "media"
    model_out = out / "models"
    thumb_out = out / "thumbs"
    for directory in (media_out, model_out, thumb_out):
        directory.mkdir(parents=True, exist_ok=True)

    all_cases = read_cases(assert_file, base)
    selected_cases = [
        (index, case_dir)
        for index, case_dir in enumerate(all_cases, start=1)
        if not args.case_token or any(token in str(case_dir) or token in case_id_from_path(case_dir) for token in args.case_token)
    ]
    manifest = []
    for output_index, (case_index, case_dir) in enumerate(selected_cases, start=1):
        print(f"[{output_index:02d}/{len(selected_cases):02d}] source #{case_index:02d}: {case_dir}", flush=True)
        meta = json.loads((case_dir / "input_meta.json").read_text(encoding="utf-8"))
        case_id = case_id_from_path(case_dir)
        before_video = media_out / f"{case_id}_source.mp4"
        after_video = media_out / f"{case_id}_edited.mp4"
        thumb = thumb_out / f"{case_id}_thumb.jpg"
        model = model_out / f"{case_id}.glb"

        split_comparison_video(
            args.ffmpeg,
            case_dir / "comparison.mp4",
            before_video,
            after_video,
            thumb,
            args.video_size,
        )
        points, colors = read_ply_points(case_dir / "pcds.ply")
        camera_orbit = camera_orbit_from_average_pose(case_dir / "cameras.json")
        points = normalize_points(points)
        if args.max_points > 0 and len(points) > args.max_points:
            rng = np.random.default_rng(2026 + case_index)
            choice = rng.choice(len(points), args.max_points, replace=False)
            points = points[choice]
            colors = colors[choice]
        write_point_glb(points, colors, model)

        manifest.append(
            {
                "id": case_id,
                "title": title_for_case(meta, case_index),
                "label": label_for_case(meta),
                "prompt": meta.get("edit_prompt") or (case_dir / "prompts.txt").read_text(encoding="utf-8").strip(),
                "source": meta.get("source"),
                "path": str(case_dir),
                "before": before_video.name,
                "after": after_video.name,
                "model": model.name,
                "thumb": thumb.name,
                "cameraOrbit": camera_orbit,
                "modelOrientation": "180deg 0deg 0deg",
            }
        )

    (out / "inference_assets_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    print(f"wrote {out}", flush=True)


def read_cases(assert_file: Path, base: Path) -> list[Path]:
    cases = []
    for line in assert_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        value = line.strip()
        if not value:
            continue
        path = Path(value).resolve()
        path.relative_to(base)
        cases.append(path)
    return cases


def case_id_from_path(case_dir: Path) -> str:
    parts = case_dir.parts
    result_index = parts.index("results")
    useful = parts[result_index + 1 :]
    if len(useful) >= 3:
        useful = (useful[0], useful[2])
    return slug("_".join(useful))


def slug(value: str) -> str:
    value = value.replace(".", "_").replace("-", "_")
    value = re.sub(r"[^A-Za-z0-9_]+", "_", value)
    return re.sub(r"_+", "_", value).strip("_").lower()


def label_for_case(meta: dict) -> str:
    source = meta.get("source")
    if source:
        if source == "my_tests":
            return "Custom"
        if source == "dggt_video":
            return "DGGT Video"
        return str(source).replace("360usid", "360-USID")
    original = str(meta.get("original_video", ""))
    if "appearance_edit" in original:
        return "Appearance"
    if "my_tests" in original or original.startswith("videos/00"):
        return "Custom"
    return "SceneEdit3D"


def title_for_case(meta: dict, index: int) -> str:
    label = label_for_case(meta)
    return f"{label} Example {index:02d}"


def split_comparison_video(
    ffmpeg: Path,
    comparison: Path,
    before: Path,
    after: Path,
    thumb: Path,
    size: int,
) -> None:
    if not comparison.exists():
        raise FileNotFoundError(comparison)
    run_ffmpeg(
        ffmpeg,
        "-i",
        comparison,
        "-vf",
        f"crop=iw/2:ih:0:0,scale={size}:{size}",
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        before,
    )
    run_ffmpeg(
        ffmpeg,
        "-i",
        comparison,
        "-vf",
        f"crop=iw/2:ih:iw/2:0,scale={size}:{size}",
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        after,
    )
    run_ffmpeg(
        ffmpeg,
        "-ss",
        "00:00:02",
        "-i",
        after,
        "-frames:v",
        "1",
        "-q:v",
        "3",
        thumb,
    )


def run_ffmpeg(ffmpeg: Path, *args: object) -> None:
    command = [str(ffmpeg), "-y", "-loglevel", "error", *(str(arg) for arg in args)]
    subprocess.run(command, check=True)


def camera_orbit_from_average_pose(cameras_path: Path) -> str:
    if not cameras_path.exists():
        return "0deg 88deg auto"
    cameras = json.loads(cameras_path.read_text(encoding="utf-8"))
    extrinsics = np.asarray(cameras["extrinsics"], dtype=np.float64)
    forwards = []
    for extrinsic in extrinsics:
        c2w = np.linalg.inv(extrinsic)
        forwards.append(c2w[:3, 2])
    forward = np.mean(np.asarray(forwards), axis=0)
    norm = np.linalg.norm(forward)
    if not np.isfinite(norm) or norm < 1e-8:
        return "0deg 88deg auto"
    forward = forward / norm
    theta = np.degrees(np.arctan2(forward[0], forward[2]))
    polar = np.degrees(np.arccos(np.clip(forward[1], -1.0, 1.0)))
    polar = float(np.clip(polar, 18.0, 88.0))
    return f"{theta:.1f}deg {polar:.1f}deg auto"


def read_ply_points(path: Path) -> tuple[np.ndarray, np.ndarray]:
    data = path.read_bytes()
    marker = b"end_header\n"
    header_end = data.find(marker)
    if header_end < 0:
        marker = b"end_header\r\n"
        header_end = data.find(marker)
    if header_end < 0:
        raise ValueError(f"could not find PLY header end in {path}")

    header = data[:header_end].decode("ascii", errors="replace").splitlines()
    if "format binary_little_endian 1.0" not in header:
        raise ValueError(f"unsupported PLY format in {path}")
    count = 0
    properties: list[tuple[str, str]] = []
    in_vertex = False
    for line in header:
        parts = line.split()
        if len(parts) >= 3 and parts[0] == "element":
            in_vertex = parts[1] == "vertex"
            if in_vertex:
                count = int(parts[2])
            continue
        if in_vertex and len(parts) == 3 and parts[0] == "property":
            properties.append((parts[2], parts[1]))

    dtype = np.dtype([(name, ply_dtype(kind)) for name, kind in properties])
    offset = header_end + len(marker)
    vertices = np.frombuffer(data, dtype=dtype, count=count, offset=offset)
    points = np.column_stack([vertices["x"], vertices["y"], vertices["z"]]).astype(np.float32)
    colors = np.column_stack([vertices["red"], vertices["green"], vertices["blue"]]).astype(np.float32) / 255.0
    return points, colors


def ply_dtype(kind: str) -> str:
    mapping = {
        "char": "i1",
        "uchar": "u1",
        "int8": "i1",
        "uint8": "u1",
        "short": "<i2",
        "ushort": "<u2",
        "int16": "<i2",
        "uint16": "<u2",
        "int": "<i4",
        "uint": "<u4",
        "int32": "<i4",
        "uint32": "<u4",
        "float": "<f4",
        "float32": "<f4",
        "double": "<f8",
        "float64": "<f8",
    }
    return mapping[kind]


def normalize_points(points: np.ndarray) -> np.ndarray:
    center = np.median(points, axis=0)
    points = points - center
    scale = np.percentile(np.linalg.norm(points, axis=1), 94)
    if not np.isfinite(scale) or scale < 1e-5:
        scale = 1.0
    return points / scale


def write_point_glb(points: np.ndarray, colors: np.ndarray, out: Path) -> None:
    points = points.reshape((-1, 3)).astype(np.float32)
    colors = colors.reshape((-1, 3))
    rgba = np.empty((len(colors), 4), dtype=np.uint8)
    rgba[:, :3] = np.clip(colors * 255.0, 0, 255).astype(np.uint8)
    rgba[:, 3] = 255

    pos = points.astype("<f4").tobytes()
    col = rgba.tobytes()
    color_offset = align4(len(pos))
    bin_length = align4(color_offset + len(col))
    binary = bytearray(bin_length)
    binary[: len(pos)] = pos
    binary[color_offset : color_offset + len(col)] = col

    gltf = {
        "asset": {"version": "2.0", "generator": "JointEdit3D inference point-cloud exporter"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [
            {
                "primitives": [
                    {
                        "attributes": {"POSITION": 0, "COLOR_0": 1},
                        "material": 0,
                        "mode": 0,
                    }
                ]
            }
        ],
        "materials": [
            {
                "pbrMetallicRoughness": {
                    "baseColorFactor": [1, 1, 1, 1],
                    "metallicFactor": 0,
                    "roughnessFactor": 0,
                }
            }
        ],
        "buffers": [{"byteLength": bin_length}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(pos), "target": 34962},
            {"buffer": 0, "byteOffset": color_offset, "byteLength": len(col), "target": 34962},
        ],
        "accessors": [
            {
                "bufferView": 0,
                "byteOffset": 0,
                "componentType": 5126,
                "count": len(points),
                "type": "VEC3",
                "min": points.min(axis=0).astype(float).tolist(),
                "max": points.max(axis=0).astype(float).tolist(),
            },
            {
                "bufferView": 1,
                "byteOffset": 0,
                "componentType": 5121,
                "count": len(points),
                "type": "VEC4",
                "normalized": True,
            },
        ],
    }
    write_glb(out, gltf, bytes(binary))


def write_glb(out: Path, gltf: dict, binary: bytes) -> None:
    json_padded = pad(json.dumps(gltf, separators=(",", ":")).encode("utf-8"), b" ")
    bin_padded = pad(binary, b"\x00")
    total = 12 + 8 + len(json_padded) + 8 + len(bin_padded)
    with out.open("wb") as handle:
        handle.write(struct.pack("<III", 0x46546C67, 2, total))
        handle.write(struct.pack("<II", len(json_padded), 0x4E4F534A))
        handle.write(json_padded)
        handle.write(struct.pack("<II", len(bin_padded), 0x004E4942))
        handle.write(bin_padded)


def align4(value: int) -> int:
    return (value + 3) & ~3


def pad(data: bytes, byte: bytes) -> bytes:
    return data + byte * (align4(len(data)) - len(data))


if __name__ == "__main__":
    os.environ.setdefault("OPENCV_IO_ENABLE_OPENEXR", "1")
    main()
