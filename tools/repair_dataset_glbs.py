#!/usr/bin/env python3
"""Repair dataset GLB accessors written by an earlier flat-array exporter."""

from __future__ import annotations

import json
import struct
from pathlib import Path

import numpy as np


GLB_MAGIC = 0x46546C67
JSON_CHUNK = 0x4E4F534A
BIN_CHUNK = 0x004E4942


def main() -> None:
    root = Path(__file__).resolve().parents[1] / "assets" / "models" / "dataset"
    for path in sorted(root.glob("*.glb")):
        repair(path)
        print(f"repaired {path.name}")


def repair(path: Path) -> None:
    data = path.read_bytes()
    magic, version, _ = struct.unpack_from("<III", data, 0)
    if magic != GLB_MAGIC or version != 2:
        raise ValueError(f"{path} is not a GLB v2 file")

    offset = 12
    json_length, json_type = struct.unpack_from("<II", data, offset)
    offset += 8
    if json_type != JSON_CHUNK:
        raise ValueError(f"{path} missing JSON chunk")
    gltf = json.loads(data[offset : offset + json_length].decode("utf-8").rstrip(" "))
    offset += json_length

    bin_length, bin_type = struct.unpack_from("<II", data, offset)
    offset += 8
    if bin_type != BIN_CHUNK:
        raise ValueError(f"{path} missing BIN chunk")
    binary = data[offset : offset + bin_length]

    position_view = gltf["bufferViews"][0]
    color_view = gltf["bufferViews"][1]
    position_count = position_view["byteLength"] // (3 * 4)
    color_count = color_view["byteLength"] // (4 * 4)
    if position_count != color_count:
        raise ValueError(f"{path} has mismatched position/color counts")

    pos_offset = position_view.get("byteOffset", 0)
    positions = np.frombuffer(binary[pos_offset : pos_offset + position_view["byteLength"]], dtype="<f4").reshape((-1, 3))

    gltf["accessors"][0]["count"] = position_count
    gltf["accessors"][0]["min"] = positions.min(axis=0).astype(float).tolist()
    gltf["accessors"][0]["max"] = positions.max(axis=0).astype(float).tolist()
    gltf["accessors"][1]["count"] = color_count

    write_glb(path, gltf, binary)


def write_glb(path: Path, gltf: dict, binary: bytes) -> None:
    json_chunk = pad(json.dumps(gltf, separators=(",", ":")).encode("utf-8"), b" ")
    bin_chunk = pad(binary, b"\x00")
    total = 12 + 8 + len(json_chunk) + 8 + len(bin_chunk)
    with path.open("wb") as fh:
        fh.write(struct.pack("<III", GLB_MAGIC, 2, total))
        fh.write(struct.pack("<II", len(json_chunk), JSON_CHUNK))
        fh.write(json_chunk)
        fh.write(struct.pack("<II", len(bin_chunk), BIN_CHUNK))
        fh.write(bin_chunk)


def pad(data: bytes, byte: bytes) -> bytes:
    return data + byte * (((len(data) + 3) & ~3) - len(data))


if __name__ == "__main__":
    main()
