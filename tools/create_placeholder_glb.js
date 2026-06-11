const fs = require("fs");
const path = require("path");

const outDir = path.join(__dirname, "..", "assets", "models");
fs.mkdirSync(outDir, { recursive: true });

const scenes = [
  { name: "dataset_removal.glb", seed: 11, moved: false, accent: [0.88, 0.28, 0.2] },
  { name: "dataset_move.glb", seed: 29, moved: true, accent: [0.28, 0.44, 0.82] },
  { name: "dataset_mixed.glb", seed: 47, moved: true, accent: [0.18, 0.58, 0.52] }
];

for (const scene of scenes) {
  fs.writeFileSync(path.join(outDir, scene.name), makeGlb(scene));
}

function makeGlb(scene) {
  const positions = [];
  const colors = [];
  const random = seededRandom(scene.seed);

  addBox(positions, colors, [0, -0.55, 0], [2.4, 0.04, 2.2], [0.68, 0.59, 0.45]);
  addBox(positions, colors, [0, 0.2, -1.1], [2.4, 1.5, 0.04], [0.78, 0.83, 0.84]);
  addBox(positions, colors, [-1.2, 0.18, 0], [0.04, 1.46, 2.2], [0.65, 0.76, 0.77]);
  addBox(positions, colors, [0.15, -0.28, -0.18], [0.78, 0.08, 0.48], [0.2, 0.46, 0.43]);
  addBox(positions, colors, [0.15, -0.48, -0.18], [0.08, 0.4, 0.08], [0.25, 0.27, 0.28]);
  addBox(positions, colors, scene.moved ? [0.55, -0.2, 0.35] : [0.74, -0.2, 0.02], [0.22, 0.44, 0.22], scene.accent);
  addBox(positions, colors, [-0.48, 0.05, -1.08], [0.4, 0.28, 0.04], [0.2, 0.25, 0.62]);
  addBox(positions, colors, [0.6, 0.18, -1.08], [0.32, 0.4, 0.04], [0.92, 0.36, 0.22]);

  for (let i = 0; i < 180; i += 1) {
    const x = random() * 2.15 - 1.08;
    const y = random() * 1.25 - 0.45;
    const z = random() * 1.9 - 1.0;
    addBox(positions, colors, [x, y, z], [0.014, 0.014, 0.014], [0.58 + random() * 0.18, 0.63 + random() * 0.16, 0.64 + random() * 0.12]);
  }

  return packGlb(new Float32Array(positions), new Float32Array(colors));
}

function addBox(positions, colors, center, size, color) {
  const [cx, cy, cz] = center;
  const [sx, sy, sz] = size.map((v) => v / 2);
  const corners = [
    [cx - sx, cy - sy, cz - sz], [cx + sx, cy - sy, cz - sz], [cx + sx, cy + sy, cz - sz], [cx - sx, cy + sy, cz - sz],
    [cx - sx, cy - sy, cz + sz], [cx + sx, cy - sy, cz + sz], [cx + sx, cy + sy, cz + sz], [cx - sx, cy + sy, cz + sz]
  ];
  const faces = [
    [0, 1, 2, 0, 2, 3],
    [5, 4, 7, 5, 7, 6],
    [4, 0, 3, 4, 3, 7],
    [1, 5, 6, 1, 6, 2],
    [3, 2, 6, 3, 6, 7],
    [4, 5, 1, 4, 1, 0]
  ];
  for (const face of faces) {
    for (const idx of face) {
      positions.push(...corners[idx]);
      colors.push(color[0], color[1], color[2], 1);
    }
  }
}

function packGlb(positionArray, colorArray) {
  const positionBuffer = Buffer.from(positionArray.buffer);
  const colorBuffer = Buffer.from(colorArray.buffer);
  const positionOffset = 0;
  const colorOffset = align4(positionBuffer.length);
  const binLength = align4(colorOffset + colorBuffer.length);
  const bin = Buffer.alloc(binLength);
  positionBuffer.copy(bin, positionOffset);
  colorBuffer.copy(bin, colorOffset);

  const count = positionArray.length / 3;
  const bounds = computeBounds(positionArray);
  const gltf = {
    asset: { version: "2.0", generator: "JointEdit3D placeholder generator" },
    extensionsUsed: ["KHR_materials_unlit"],
    scene: 0,
    scenes: [{ nodes: [0] }],
    nodes: [{ mesh: 0 }],
    meshes: [{
      primitives: [{
        attributes: { POSITION: 0, COLOR_0: 1 },
        material: 0,
        mode: 4
      }]
    }],
    materials: [{
      pbrMetallicRoughness: { baseColorFactor: [1, 1, 1, 1], metallicFactor: 0, roughnessFactor: 1 },
      doubleSided: true,
      extensions: { KHR_materials_unlit: {} }
    }],
    buffers: [{ byteLength: binLength }],
    bufferViews: [
      { buffer: 0, byteOffset: positionOffset, byteLength: positionBuffer.length, target: 34962 },
      { buffer: 0, byteOffset: colorOffset, byteLength: colorBuffer.length, target: 34962 }
    ],
    accessors: [
      { bufferView: 0, byteOffset: 0, componentType: 5126, count, type: "VEC3", min: bounds.min, max: bounds.max },
      { bufferView: 1, byteOffset: 0, componentType: 5126, count, type: "VEC4" }
    ]
  };

  const json = Buffer.from(JSON.stringify(gltf), "utf8");
  const jsonPadded = padBuffer(json, 0x20);
  const binPadded = padBuffer(bin, 0x00);
  const totalLength = 12 + 8 + jsonPadded.length + 8 + binPadded.length;
  const glb = Buffer.alloc(totalLength);

  let offset = 0;
  glb.writeUInt32LE(0x46546c67, offset); offset += 4;
  glb.writeUInt32LE(2, offset); offset += 4;
  glb.writeUInt32LE(totalLength, offset); offset += 4;
  glb.writeUInt32LE(jsonPadded.length, offset); offset += 4;
  glb.writeUInt32LE(0x4e4f534a, offset); offset += 4;
  jsonPadded.copy(glb, offset); offset += jsonPadded.length;
  glb.writeUInt32LE(binPadded.length, offset); offset += 4;
  glb.writeUInt32LE(0x004e4942, offset); offset += 4;
  binPadded.copy(glb, offset);
  return glb;
}

function computeBounds(array) {
  const min = [Infinity, Infinity, Infinity];
  const max = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < array.length; i += 3) {
    for (let axis = 0; axis < 3; axis += 1) {
      min[axis] = Math.min(min[axis], array[i + axis]);
      max[axis] = Math.max(max[axis], array[i + axis]);
    }
  }
  return { min, max };
}

function padBuffer(buffer, padByte) {
  const padded = Buffer.alloc(align4(buffer.length), padByte);
  buffer.copy(padded);
  return padded;
}

function align4(value) {
  return (value + 3) & ~3;
}

function seededRandom(seed) {
  let state = seed >>> 0;
  return () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 4294967296;
  };
}
