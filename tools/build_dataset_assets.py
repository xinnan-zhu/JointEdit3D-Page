#!/usr/bin/env python3
"""Build lightweight project-page dataset assets from SceneEdit3D render folders."""

from __future__ import annotations

import argparse
import json
import math
import os
import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


BASE_DEFAULT = Path("/mnt/shared-storage-user/steai-share/zhuxinnan")
MASK_COLOR = np.array([45, 130, 255], dtype=np.float32)
PROMPT_OVERRIDES = {
    "mix_livingroom_10_task_0010_add_delete_mix_20_SM_Bowl_with_Oranges_x_12_SM_Radio_view_0": (
        "Add a bowl of bright orange fruits onto the front-left wooden coffee table, "
        "and remove the blue vintage radio from the lower cubby of the wooden bookcase."
    ),
}


@dataclass
class Case:
    group: str
    path: Path

    @property
    def id(self) -> str:
        scene = self.path.parent.parent.name
        task = self.path.parent.name
        view = self.path.name
        return f"{self.group}_{scene}_{task}_{view}".replace(".", "_")

    @property
    def short_label(self) -> str:
        labels = {
            "add": "Add",
            "delete": "Removal",
            "move": "Move",
            "mix": "Mixed",
        }
        return labels.get(self.group, self.group.title())

    @property
    def title(self) -> str:
        scene = self.path.parent.parent.name.replace("_", " ").title()
        return f"{self.short_label} in {scene}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=BASE_DEFAULT)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--frame", type=int, default=30)
    parser.add_argument("--video-size", type=int, default=480)
    parser.add_argument("--max-video-frames", type=int, default=49)
    parser.add_argument("--points-per-frame", type=int, default=0)
    parser.add_argument("--point-frames", type=str, default="0,6,12,18,24,30,36,42,48")
    parser.add_argument("--max-model-points", type=int, default=0)
    parser.add_argument("--point-size", type=float, default=0.022)
    parser.add_argument("--depth-max", type=float, default=35.0)
    parser.add_argument("--all-contact-sheet", action="store_true")
    parser.add_argument("--case-token", action="append", default=[])
    parser.add_argument("--skip-token", action="append", default=["diningroom_09"])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base = args.base.resolve()
    out = (args.out or (base / "project_page_asset_staging")).resolve()
    out.mkdir(parents=True, exist_ok=True)

    cases = read_cases(base / "assert_dir.txt", base)
    if args.skip_token:
        cases = [
            case
            for case in cases
            if not any(token and token in str(case.path) for token in args.skip_token)
        ]
    if args.case_token:
        cases = [
            case
            for case in cases
            if any(token in str(case.path) or token in case.id for token in args.case_token)
        ]
    manifest = []

    if args.all_contact_sheet:
        build_contact_sheet(cases, base, out / "candidate_contact_sheet.jpg", args.frame)

    for case in cases:
        print(f"building {case.group}: {case.path}", flush=True)
        case_out = {
            "id": case.id,
            "label": case.short_label,
            "title": case.title,
            "group": case.group,
            "path": str(case.path),
            "prompt": read_prompt(case),
            "usedFixMask": bool(mask_root(case.path, base) != case.path),
        }

        thumb = out / f"{case.id}_thumb.jpg"
        prompt_frame = out / f"{case.id}_prompt_frame.jpg"
        save_thumb(case, base, thumb, args.frame)
        save_prompt_frame(case, base, prompt_frame, args.frame)
        case_out["thumb"] = thumb.name
        case_out["promptFrame"] = prompt_frame.name

        for side, key in (("before", "beforeVideo"), ("after", "afterVideo")):
            video = out / f"{case.id}_{side}_masked_raw.mp4"
            build_masked_video(case.path, base, side, video, args.video_size, args.max_video_frames)
            case_out[key] = video.name

        for side, key in (("before", "sourceModel"), ("after", "editedModel")):
            model = out / f"{case.id}_{side}.glb"
            build_point_glb(
                case.path,
                side,
                model,
                frame_indices=parse_int_list(args.point_frames),
                points_per_frame=args.points_per_frame,
                max_points=args.max_model_points,
                point_size=args.point_size,
                depth_max=args.depth_max,
            )
            case_out[key] = model.name

        manifest.append(case_out)

    (out / "dataset_assets_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote {out}", flush=True)


def read_cases(assert_file: Path, base: Path) -> list[Case]:
    cases: list[Case] = []
    group = ""
    for line in assert_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        value = line.strip()
        if not value:
            continue
        if value.endswith(":"):
            group = value[:-1]
            continue
        if value.startswith(str(base)):
            path = Path(value).resolve()
            path.relative_to(base)
            if not any(c.path == path for c in cases):
                cases.append(Case(group=group, path=path))
    return cases


def parse_int_list(value: str) -> list[int]:
    return [int(part) for part in value.split(",") if part.strip()]


def mask_root(case_path: Path, base: Path) -> Path:
    rel = case_path.resolve().relative_to(base)
    if len(rel.parts) >= 3 and rel.parts[:2] == ("Imaginarium", "scene_edit_data"):
        fixed = base / "Imaginarium" / "scene_edit_data_mask_fix" / Path(*rel.parts[2:])
        if fixed.exists():
            return fixed
    return case_path


def read_prompt(case: Case) -> str:
    if case.id in PROMPT_OVERRIDES:
        return PROMPT_OVERRIDES[case.id]

    candidates = [case.path / "task_meta.json", case.path.parent / "task_meta.json"]
    for candidate in candidates:
        if not candidate.exists():
            continue
        try:
            meta = json.loads(candidate.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        prompt = meta.get("vlm_edit_prompt") or meta.get("task", {}).get("instruction")
        if prompt:
            return str(prompt)
    return case.path.parent.name.replace("_", " ")


def frame_file(case_path: Path, side: str, index: int) -> Path:
    frames = case_path / side / "frames"
    candidate = frames / f"{index:06d}.png"
    if candidate.exists():
        return candidate
    files = sorted(frames.glob("*.png"))
    return files[min(index, len(files) - 1)]


def mask_file(case_path: Path, base: Path, side: str, index: int) -> Path | None:
    masks = mask_root(case_path, base) / side / "masks"
    candidate = masks / f"frame_{index:04d}.png"
    if candidate.exists():
        return candidate
    files = sorted(masks.glob("*.png"))
    if not files:
        return None
    return files[min(index, len(files) - 1)]


def load_rgb(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"))


def load_mask(path: Path | None, size: tuple[int, int]) -> np.ndarray:
    if path is None:
        return np.zeros((size[1], size[0]), dtype=np.float32)
    mask = Image.open(path).convert("L").resize(size, Image.NEAREST)
    return np.asarray(mask, dtype=np.float32) / 255.0


def blend_mask(rgb: np.ndarray, mask: np.ndarray, alpha: float = 0.38) -> np.ndarray:
    strength = (mask > 0.08).astype(np.float32)[..., None] * alpha
    out = rgb.astype(np.float32) * (1.0 - strength) + MASK_COLOR * strength
    return np.clip(out, 0, 255).astype(np.uint8)


def save_thumb(case: Case, base: Path, out: Path, index: int) -> None:
    rgb = load_rgb(frame_file(case.path, "before", index))
    mask = load_mask(mask_file(case.path, base, "before", index), (rgb.shape[1], rgb.shape[0]))
    blended = Image.fromarray(blend_mask(rgb, mask)).resize((360, 360), Image.LANCZOS)
    blended.save(out, quality=90)


def save_prompt_frame(case: Case, base: Path, out: Path, index: int) -> None:
    before = load_rgb(frame_file(case.path, "before", index))
    after = load_rgb(frame_file(case.path, "after", index))
    mask = load_mask(mask_file(case.path, base, "before", index), (before.shape[1], before.shape[0]))
    before_overlay = blend_mask(before, mask)
    canvas = Image.new("RGB", (720, 360), (255, 255, 255))
    canvas.paste(Image.fromarray(before_overlay).resize((360, 360), Image.LANCZOS), (0, 0))
    canvas.paste(Image.fromarray(after).resize((360, 360), Image.LANCZOS), (360, 0))
    canvas.save(out, quality=90)


def build_contact_sheet(cases: list[Case], base: Path, out: Path, index: int) -> None:
    thumb = 168
    gap = 8
    label_h = 46
    rows = []
    for case in cases:
        before = load_rgb(frame_file(case.path, "before", index))
        after = load_rgb(frame_file(case.path, "after", index))
        mask = load_mask(mask_file(case.path, base, "before", index), (before.shape[1], before.shape[0]))
        panels = [before, after, blend_mask(before, mask)]
        row = Image.new("RGB", (thumb * 3 + gap * 2, thumb + label_h), (255, 255, 255))
        for i, image in enumerate(panels):
            row.paste(Image.fromarray(image).resize((thumb, thumb), Image.LANCZOS), (i * (thumb + gap), label_h))
        draw = ImageDraw.Draw(row)
        title = f"{case.group.upper()} | {case.path.parent.parent.name}/{case.path.parent.name}/{case.path.name}"
        draw.text((4, 3), title[:78], fill=(20, 24, 34))
        draw.text((4, 22), read_prompt(case)[:95], fill=(72, 78, 92))
        rows.append(row)

    sheet = Image.new("RGB", (thumb * 3 + gap * 2, len(rows) * (thumb + label_h + gap)), (242, 244, 248))
    y = 0
    for row in rows:
        sheet.paste(row, (0, y))
        y += row.height + gap
    sheet.save(out, quality=92)


def build_masked_video(case_path: Path, base: Path, side: str, out: Path, size: int, max_frames: int) -> None:
    import cv2

    frames = sorted((case_path / side / "frames").glob("*.png"))[:max_frames]
    if not frames:
        raise FileNotFoundError(f"no frames for {case_path}/{side}")
    writer = cv2.VideoWriter(
        str(out),
        cv2.VideoWriter_fourcc(*"mp4v"),
        12,
        (size, size),
    )
    for frame_path in frames:
        stem = frame_path.stem
        index = int(stem)
        rgb = Image.open(frame_path).convert("RGB").resize((size, size), Image.LANCZOS)
        mask = load_mask(mask_file(case_path, base, side, index), (size, size))
        blended = blend_mask(np.asarray(rgb), mask)
        writer.write(cv2.cvtColor(blended, cv2.COLOR_RGB2BGR))
    writer.release()


def build_point_glb(
    case_path: Path,
    side: str,
    out: Path,
    frame_indices: list[int],
    points_per_frame: int,
    max_points: int,
    point_size: float,
    depth_max: float,
) -> None:
    intr = read_intrinsics(case_path / side / "intrinsics.txt")
    poses = read_poses(case_path / side / "poses.txt")
    points = []
    colors = []
    rng = np.random.default_rng(2026)

    for index in frame_indices:
        frame = frame_file(case_path, side, index)
        depth_file = case_path / side / "depth" / f"{index:06d}.exr"
        if not depth_file.exists() or index not in poses:
            continue
        rgb = load_rgb(frame)
        depth = read_exr_depth(depth_file)
        if depth.ndim == 3:
            depth = depth[..., 0]
        if depth.shape[:2] != rgb.shape[:2]:
            depth = np.asarray(Image.fromarray(depth).resize((rgb.shape[1], rgb.shape[0]), Image.NEAREST))

        valid = np.isfinite(depth) & (depth > 0.05) & (depth < depth_max)
        ys, xs = np.nonzero(valid)
        if len(xs) == 0:
            continue
        if points_per_frame > 0 and points_per_frame < len(xs):
            choice = rng.choice(len(xs), points_per_frame, replace=False)
            xs = xs[choice]
            ys = ys[choice]
        z = depth[ys, xs].astype(np.float32)
        cam = pixels_to_camera(xs, ys, z, intr)
        world = transform_points(cam, poses[index])
        points.append(world)
        colors.append(rgb[ys, xs].astype(np.float32) / 255.0)

    if not points:
        raise RuntimeError(f"no point data generated for {case_path}/{side}")

    point_array = normalize_points(np.concatenate(points, axis=0))
    color_array = np.concatenate(colors, axis=0)
    if max_points > 0 and len(point_array) > max_points:
        choice = rng.choice(len(point_array), max_points, replace=False)
        point_array = point_array[choice]
        color_array = color_array[choice]
    write_point_glb(point_array, color_array, out)


def read_intrinsics(path: Path) -> tuple[float, float, float, float, int, int]:
    values = [float(v) for v in path.read_text().split()]
    return values[0], values[1], values[2], values[3], int(values[4]), int(values[5])


def read_poses(path: Path) -> dict[int, tuple[np.ndarray, np.ndarray]]:
    poses = {}
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) != 8:
            continue
        index = int(parts[0])
        t = np.array([float(v) for v in parts[1:4]], dtype=np.float32)
        q = np.array([float(v) for v in parts[4:8]], dtype=np.float32)
        poses[index] = (t, quat_to_matrix(q))
    return poses


def quat_to_matrix(q: np.ndarray) -> np.ndarray:
    x, y, z, w = q / max(float(np.linalg.norm(q)), 1e-8)
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ],
        dtype=np.float32,
    )


def read_exr_depth(path: Path) -> np.ndarray:
    import OpenEXR
    import Imath

    exr = OpenEXR.InputFile(str(path))
    header = exr.header()
    dw = header["dataWindow"]
    width = dw.max.x - dw.min.x + 1
    height = dw.max.y - dw.min.y + 1
    channels = list(header["channels"].keys())
    preferred = next((c for c in ("Z", "Y", "R") if c in channels), channels[0])
    raw = exr.channel(preferred, Imath.PixelType(Imath.PixelType.FLOAT))
    return np.frombuffer(raw, dtype=np.float32).reshape((height, width))


def pixels_to_camera(
    xs: np.ndarray,
    ys: np.ndarray,
    z: np.ndarray,
    intr: tuple[float, float, float, float, int, int],
) -> np.ndarray:
    fx, fy, cx, cy, _, _ = intr
    x = (xs.astype(np.float32) - cx) * z / fx
    y = -(ys.astype(np.float32) - cy) * z / fy
    return np.stack([x, y, -z], axis=1)


def transform_points(points: np.ndarray, pose: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
    translation, rotation = pose
    return points @ rotation.T + translation[None, :]


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

    bounds_min = points.min(axis=0).astype(float).tolist()
    bounds_max = points.max(axis=0).astype(float).tolist()
    gltf = {
        "asset": {"version": "2.0", "generator": "JointEdit3D point-cloud exporter"},
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
                },
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
                "min": bounds_min,
                "max": bounds_max,
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


def write_cube_point_glb(points: np.ndarray, colors: np.ndarray, out: Path, size: float) -> None:
    positions = []
    vertex_colors = []
    indices = []
    for point, color in zip(points, colors):
        add_indexed_cube(positions, vertex_colors, indices, point, size, color)
    pack_glb(
        np.asarray(positions, dtype=np.float32),
        np.asarray(vertex_colors, dtype=np.float32),
        np.asarray(indices, dtype=np.uint32),
        out,
    )


def add_indexed_cube(
    positions: list[float],
    colors: list[float],
    indices: list[int],
    center: np.ndarray,
    size: float,
    color: np.ndarray,
) -> None:
    cx, cy, cz = center.tolist()
    s = size / 2
    base = len(positions) // 3
    corners = [
        (cx - s, cy - s, cz - s),
        (cx + s, cy - s, cz - s),
        (cx + s, cy + s, cz - s),
        (cx - s, cy + s, cz - s),
        (cx - s, cy - s, cz + s),
        (cx + s, cy - s, cz + s),
        (cx + s, cy + s, cz + s),
        (cx - s, cy + s, cz + s),
    ]
    faces = [
        (0, 1, 2, 0, 2, 3),
        (5, 4, 7, 5, 7, 6),
        (4, 0, 3, 4, 3, 7),
        (1, 5, 6, 1, 6, 2),
        (3, 2, 6, 3, 6, 7),
        (4, 5, 1, 4, 1, 0),
    ]
    rgba = [float(color[0]), float(color[1]), float(color[2]), 1.0]
    for corner in corners:
        positions.extend(corner)
        colors.extend(rgba)
    for face in faces:
        indices.extend(base + idx for idx in face)


def pack_glb(positions: np.ndarray, colors: np.ndarray, indices: np.ndarray, out: Path) -> None:
    positions = positions.reshape((-1, 3))
    colors = colors.reshape((-1, 4))
    indices = indices.reshape((-1,))
    if len(positions) <= 65535:
        indices = indices.astype("<u2")
        index_component_type = 5123
    else:
        indices = indices.astype("<u4")
        index_component_type = 5125

    pos = positions.astype("<f4").tobytes()
    col = colors.astype("<f4").tobytes()
    color_offset = align4(len(pos))
    index_offset = align4(color_offset + len(col))
    idx = indices.tobytes()
    bin_length = align4(index_offset + len(idx))
    binary = bytearray(bin_length)
    binary[: len(pos)] = pos
    binary[color_offset : color_offset + len(col)] = col
    binary[index_offset : index_offset + len(idx)] = idx

    count = len(positions)
    bounds_min = positions.min(axis=0).astype(float).tolist()
    bounds_max = positions.max(axis=0).astype(float).tolist()
    gltf = {
        "asset": {"version": "2.0", "generator": "JointEdit3D dataset asset builder"},
        "extensionsUsed": ["KHR_materials_unlit"],
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [
            {
                "primitives": [
                    {
                        "attributes": {"POSITION": 0, "COLOR_0": 1},
                        "indices": 2,
                        "material": 0,
                        "mode": 4,
                    }
                ]
            }
        ],
        "materials": [
            {
                "pbrMetallicRoughness": {
                    "baseColorFactor": [1, 1, 1, 1],
                    "metallicFactor": 0,
                    "roughnessFactor": 1,
                },
                "doubleSided": True,
                "extensions": {"KHR_materials_unlit": {}},
            }
        ],
        "buffers": [{"byteLength": bin_length}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(pos), "target": 34962},
            {"buffer": 0, "byteOffset": color_offset, "byteLength": len(col), "target": 34962},
            {"buffer": 0, "byteOffset": index_offset, "byteLength": len(idx), "target": 34963},
        ],
        "accessors": [
            {
                "bufferView": 0,
                "byteOffset": 0,
                "componentType": 5126,
                "count": count,
                "type": "VEC3",
                "min": bounds_min,
                "max": bounds_max,
            },
            {
                "bufferView": 1,
                "byteOffset": 0,
                "componentType": 5126,
                "count": count,
                "type": "VEC4",
            },
            {
                "bufferView": 2,
                "byteOffset": 0,
                "componentType": index_component_type,
                "count": len(indices),
                "type": "SCALAR",
            },
        ],
    }
    json_bytes = json.dumps(gltf, separators=(",", ":")).encode("utf-8")
    write_glb(out, gltf, bytes(binary))


def write_glb(out: Path, gltf: dict, binary: bytes) -> None:
    json_padded = pad(json.dumps(gltf, separators=(",", ":")).encode("utf-8"), b" ")
    bin_padded = pad(binary, b"\x00")
    total = 12 + 8 + len(json_padded) + 8 + len(bin_padded)
    with out.open("wb") as fh:
        fh.write(struct.pack("<III", 0x46546C67, 2, total))
        fh.write(struct.pack("<II", len(json_padded), 0x4E4F534A))
        fh.write(json_padded)
        fh.write(struct.pack("<II", len(bin_padded), 0x004E4942))
        fh.write(bin_padded)


def align4(value: int) -> int:
    return (value + 3) & ~3


def pad(data: bytes, byte: bytes) -> bytes:
    return data + byte * (align4(len(data)) - len(data))


if __name__ == "__main__":
    os.environ.setdefault("OPENCV_IO_ENABLE_OPENEXR", "1")
    main()
