#!/usr/bin/env python3
"""Quantize JointEdit3D point-cloud GLBs while keeping every point."""

from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path

import numpy as np


JSON_CHUNK = 0x4E4F534A
BIN_CHUNK = 0x004E4942


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="*", type=Path)
    parser.add_argument("--list", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path("project_page/assets/models"))
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    inputs = list(args.inputs)
    if args.list:
        inputs.extend(Path(line.strip()) for line in args.list.read_text(encoding="utf-8").splitlines() if line.strip())
    if not inputs:
        raise SystemExit("no input GLBs")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for src in inputs:
        src = resolve_input(src, args.root)
        rel = src.resolve().relative_to(args.root.resolve())
        dst = args.out_dir / rel
        if dst.exists() and not args.force:
            print(f"skip existing {dst}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        before, after, count = quantize_glb(src, dst)
        print(f"{src} -> {dst}  {before / 1048576:.2f}MB -> {after / 1048576:.2f}MB  points={count}")


def resolve_input(src: Path, root: Path) -> Path:
    if src.exists():
        return src
    page_relative = Path("project_page") / src
    if page_relative.exists():
        return page_relative
    root_relative = root / src
    if root_relative.exists():
        return root_relative
    raise FileNotFoundError(src)


def quantize_glb(src: Path, dst: Path) -> tuple[int, int, int]:
    data = src.read_bytes()
    gltf, binary = read_glb(data)
    validate_supported(gltf)

    position_accessor = gltf["accessors"][0]
    color_accessor = gltf["accessors"][1]
    count = int(position_accessor["count"])

    positions = read_positions(gltf, binary, position_accessor)
    colors = read_colors(gltf, binary, color_accessor, count)

    position_min = positions.min(axis=0)
    position_max = positions.max(axis=0)
    extent = position_max - position_min
    extent[extent < 1e-8] = 1.0
    normalized = np.clip((positions - position_min) / extent, 0.0, 1.0)
    quantized_positions = np.rint(normalized * 65535.0).astype("<u2", copy=False)
    rgb_colors = colors[:, :3].astype("u1", copy=False)

    position_bytes = quantized_positions.tobytes(order="C")
    color_offset = len(position_bytes)
    color_bytes = rgb_colors.tobytes(order="C")
    out_binary = pad4(position_bytes + color_bytes)

    gltf = rebuild_gltf(gltf, count, len(position_bytes), color_offset, len(color_bytes), position_min, extent)
    out_data = write_glb(gltf, out_binary)
    dst.write_bytes(out_data)
    return len(data), len(out_data), count


def read_glb(data: bytes) -> tuple[dict, bytes]:
    magic, version, total_length = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF" or version != 2 or total_length != len(data):
        raise ValueError("not a GLB v2 file")
    offset = 12
    chunks = {}
    while offset < len(data):
        chunk_length, chunk_type = struct.unpack_from("<II", data, offset)
        offset += 8
        chunks[chunk_type] = data[offset : offset + chunk_length]
        offset += chunk_length
    if JSON_CHUNK not in chunks or BIN_CHUNK not in chunks:
        raise ValueError("GLB must contain JSON and BIN chunks")
    gltf = json.loads(chunks[JSON_CHUNK].rstrip(b" \t\r\n\0"))
    return gltf, chunks[BIN_CHUNK]


def validate_supported(gltf: dict) -> None:
    accessors = gltf.get("accessors", [])
    buffer_views = gltf.get("bufferViews", [])
    meshes = gltf.get("meshes", [])
    nodes = gltf.get("nodes", [])
    if len(accessors) != 2 or len(buffer_views) != 2 or len(meshes) != 1:
        raise ValueError("expected one point mesh with POSITION and COLOR_0 accessors")
    primitive = meshes[0]["primitives"][0]
    if primitive.get("mode") != 0 or primitive.get("attributes") != {"POSITION": 0, "COLOR_0": 1}:
        raise ValueError("expected POINTS primitive with POSITION/COLOR_0")
    if accessors[0].get("componentType") != 5126 or accessors[0].get("type") != "VEC3":
        raise ValueError("POSITION must be FLOAT VEC3")
    if accessors[1].get("componentType") != 5121 or accessors[1].get("type") != "VEC4":
        raise ValueError("COLOR_0 must be UBYTE VEC4")
    if any(any(key in node for key in ("matrix", "translation", "rotation", "scale")) for node in nodes):
        raise ValueError("node transforms are not supported by this simple quantizer")


def read_positions(gltf: dict, binary: bytes, accessor: dict) -> np.ndarray:
    view = gltf["bufferViews"][accessor["bufferView"]]
    offset = int(view.get("byteOffset", 0)) + int(accessor.get("byteOffset", 0))
    count = int(accessor["count"])
    return np.frombuffer(binary, dtype="<f4", count=count * 3, offset=offset).reshape((count, 3)).copy()


def read_colors(gltf: dict, binary: bytes, accessor: dict, count: int) -> np.ndarray:
    view = gltf["bufferViews"][accessor["bufferView"]]
    offset = int(view.get("byteOffset", 0)) + int(accessor.get("byteOffset", 0))
    return np.frombuffer(binary, dtype="u1", count=count * 4, offset=offset).reshape((count, 4)).copy()


def rebuild_gltf(
    gltf: dict,
    count: int,
    position_length: int,
    color_offset: int,
    color_length: int,
    position_min: np.ndarray,
    extent: np.ndarray,
) -> dict:
    gltf = json.loads(json.dumps(gltf))
    used = set(gltf.get("extensionsUsed", []))
    used.add("KHR_mesh_quantization")
    gltf["extensionsUsed"] = sorted(used)
    required = set(gltf.get("extensionsRequired", []))
    required.add("KHR_mesh_quantization")
    gltf["extensionsRequired"] = sorted(required)
    gltf["buffers"] = [{"byteLength": position_length + color_length}]
    gltf["bufferViews"] = [
        {"buffer": 0, "byteOffset": 0, "byteLength": position_length, "target": 34962},
        {"buffer": 0, "byteOffset": color_offset, "byteLength": color_length, "target": 34962},
    ]
    gltf["accessors"] = [
        {
            "bufferView": 0,
            "byteOffset": 0,
            "componentType": 5123,
            "count": count,
            "type": "VEC3",
            "normalized": True,
            "min": [0.0, 0.0, 0.0],
            "max": [1.0, 1.0, 1.0],
        },
        {
            "bufferView": 1,
            "byteOffset": 0,
            "componentType": 5121,
            "count": count,
            "type": "VEC3",
            "normalized": True,
        },
    ]
    node = gltf["nodes"][0]
    node["translation"] = [float(v) for v in position_min]
    node["scale"] = [float(v) for v in extent]
    gltf["asset"]["generator"] = f"{gltf['asset'].get('generator', 'JointEdit3D point-cloud exporter')} + quantized"
    return gltf


def write_glb(gltf: dict, binary: bytes) -> bytes:
    json_bytes = pad4(json.dumps(gltf, separators=(",", ":")).encode("utf-8"), pad=b" ")
    total_length = 12 + 8 + len(json_bytes) + 8 + len(binary)
    return b"".join(
        [
            struct.pack("<4sII", b"glTF", 2, total_length),
            struct.pack("<II", len(json_bytes), JSON_CHUNK),
            json_bytes,
            struct.pack("<II", len(binary), BIN_CHUNK),
            binary,
        ]
    )


def pad4(data: bytes, pad: bytes = b"\0") -> bytes:
    return data + pad * ((4 - len(data) % 4) % 4)


if __name__ == "__main__":
    main()
