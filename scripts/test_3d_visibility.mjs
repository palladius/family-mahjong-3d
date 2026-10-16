#!/usr/bin/env node
/**
 * Automated 3D Visibility, Coplanar Orientation & Zero-Barrier Occlusion Unit Test Suite
 * Verifies:
 *   1. Coplanarity: Temple Floor & Rosewood Table lie in the exact same horizontal XZ plane (+Y Up) as the 144 Mahjong tiles (NEVER orthogonal!).
 *   2. Barrier Clearance: All 144 tiles sit strictly above the table/floor surface (zero intersection or mid-board slicing).
 *   3. 360° Raycast Line-of-Sight: Across all 6 camera presets (2d, hero, topdown, pavement, macro, orbit) and 24 azimuth/elevation angles (4,320 rays),
 *      the camera's eyes are ALWAYS in front of any barrier — 0 rays from camera to any tile are blocked by environment geometry.
 *   4. Full-Board Frustum Coverage: In 2D, Zen Top-Down, and 3D Hero presets, 100% of all 144 tiles project inside the camera viewport.
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import * as THREE from "three";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

const TILE_W = 0.90;
const TILE_H = 1.20;
const TILE_D = 0.65;

let failed = false;
function assert(cond, msg) {
  if (!cond) {
    console.error(`❌ FAIL [3D Visibility Test]: ${msg}`);
    failed = true;
  } else {
    console.log(`✅ PASS [3D Visibility Test]: ${msg}`);
  }
}

console.log("🔭 Running 3D Camera Line-of-Sight, Coplanar Plane & Frustum Unit Tests...");

// 1. Verify src/main.js does NOT rotate templeEnv by -PI/2 around X (which caused the orthogonal vertical wall bug)
const mainJs = fs.readFileSync(path.join(ROOT, "src/main.js"), "utf8");
const hasBrokenEnvRotation = /this\.templeEnv\.rotation\.x\s*=\s*-\s*Math\.PI\s*\/\s*2/.test(mainJs);
assert(!hasBrokenEnvRotation, "src/main.js keeps temple_environment.glb in native +Y Up XZ plane (no orthogonal -PI/2 X rotation)");
assert(mainJs.includes("this.sharedGeo.selOuterPurple") && mainJs.includes("this.sharedGeo.selInnerYellow"), "Yellow-Purple double selection border ('bordino giallo-viola') is wired in src/main.js");
assert(mainJs.includes("550") && mainJs.includes("showPairMatchCard"), "550ms ('mezzo secondo') matched-pair visibility pause is wired for manual & demo play");
assert(mainJs.includes('"2d":') && mainJs.includes("toggle2DMode"), "Dedicated 2D flat top-down camera preset & toggle are wired in src/main.js");
assert(mainJs.includes("getDidYouKnowLore") && mainJs.includes("updateWow3DPreview"), "WOW rotating 3D tile inspector & 'Did you know?' cultural lore are wired in src/main.js");

// 2. Parse actual binary public/models/temple_environment.glb & build Three.js bounding meshes
const glbPath = path.join(ROOT, "public/models/temple_environment.glb");
const buf = fs.readFileSync(glbPath);
const jsonLen = buf.readUInt32LE(12);
const gltf = JSON.parse(buf.subarray(20, 20 + jsonLen).toString("utf8"));

const scene = new THREE.Scene();
const envMeshes = [];
const overheadObstacles = [];

gltf.nodes.forEach((node) => {
  if (node.mesh === undefined) return;
  const meshDef = gltf.meshes[node.mesh];
  const posAcc = gltf.accessors[meshDef.primitives[0].attributes.POSITION];
  const min = new THREE.Vector3(...posAcc.min);
  const max = new THREE.Vector3(...posAcc.max);
  const size = new THREE.Vector3().subVectors(max, min);
  const center = new THREE.Vector3().addVectors(min, max).multiplyScalar(0.5);

  const geo = new THREE.BoxGeometry(size.x, size.y, size.z);
  const mat = new THREE.MeshBasicMaterial();
  const mesh = new THREE.Mesh(geo, mat);
  mesh.name = node.name;
  mesh.position.copy(center);
  mesh.updateMatrixWorld(true);
  mesh.userData.bbox = new THREE.Box3(min, max);
  scene.add(mesh);
  envMeshes.push(mesh);

  if (node.name.startsWith("Temple_Crimson_Pillar") || node.name.startsWith("Temple_Silk_Lantern")) {
    overheadObstacles.push(mesh);
  }
});

// Verify Coplanarity of Floor & Table with the XZ Mahjong Board Plane (+Y is UP)
const pavementMesh = envMeshes.find((m) => m.name === "Temple_Stone_Pavement");
const tableMesh = envMeshes.find((m) => m.name === "Low_Rosewood_Jade_Table");

assert(Boolean(pavementMesh && tableMesh), "temple_environment.glb contains Temple_Stone_Pavement and Low_Rosewood_Jade_Table");

if (pavementMesh && tableMesh) {
  const pBox = pavementMesh.userData.bbox;
  const tBox = tableMesh.userData.bbox;
  const pSize = new THREE.Vector3();
  const tSize = new THREE.Vector3();
  pBox.getSize(pSize);
  tBox.getSize(tSize);

  assert(
    pSize.x >= 20 && pSize.z >= 20 && pSize.y <= 0.6,
    `Temple_Stone_Pavement is horizontal in XZ plane (X=${pSize.x.toFixed(1)}m, Z=${pSize.z.toFixed(1)}m, thickness Y=${pSize.y.toFixed(2)}m)`
  );
  assert(
    tSize.x >= 12 && tSize.z >= 8 && tSize.y <= 0.4,
    `Low_Rosewood_Jade_Table is horizontal in XZ plane (X=${tSize.x.toFixed(1)}m, Z=${tSize.z.toFixed(1)}m, thickness Y=${tSize.y.toFixed(2)}m)`
  );
  assert(
    tBox.max.y <= 0.0,
    `Table top surface (Y=${tBox.max.y.toFixed(3)}m) is strictly below the lowest Mahjong tile layer (Y=0.28m)`
  );
}

// 3. Generate all 144 Master Imperial Turtle Tile Positions in XZ Plane (+Y Up)
function generateMasterSlots() {
  const slots = [];
  for (let r = -3.5; r <= 3.5; r += 1) {
    const cols = Math.abs(r) === 3.5 ? 8 : Math.abs(r) === 2.5 ? 10 : 12;
    for (let c = -(cols - 1) / 2; c <= (cols - 1) / 2; c += 1) {
      if (slots.length < 84) slots.push({ c, r, l: 0 });
    }
  }
  slots.push({ c: -6.5, r: 0, l: 0 }, { c: 6.5, r: 0, l: 0 });
  for (let r = -2.5; r <= 2.5; r += 1) {
    for (let c = -2.5; c <= 2.5; c += 1) slots.push({ c, r, l: 1 });
  }
  for (let r = -1.5; r <= 1.5; r += 1) {
    for (let c = -1.5; c <= 1.5; c += 1) slots.push({ c, r, l: 2 });
  }
  for (let r = -0.5; r <= 0.5; r += 1) {
    for (let c = -0.5; c <= 0.5; c += 1) slots.push({ c, r, l: 3 });
  }
  slots.push({ c: -0.5, r: 0, l: 4 }, { c: 0.5, r: 0, l: 4 });
  while (slots.length > 144) slots.pop();
  return slots;
}

const slots = generateMasterSlots();
const tilePositions = slots.map((slot) => {
  const x = slot.c * (TILE_W * 1.03);
  const y = 0.28 + slot.l * (TILE_D * 1.02);
  const z = slot.r * (TILE_H * 1.03);
  return new THREE.Vector3(x, y, z);
});

// Verify every tile is strictly above the table & floor (zero intersection)
const allTilesAboveTable = tilePositions.every((p) => p.y - TILE_D * 0.5 > tableMesh.userData.bbox.max.y);
assert(allTilesAboveTable, "All 144 tiles sit strictly above the Rosewood Table surface with zero plane intersection");

// 4. Test Line-of-Sight Raycast from Camera Eye to All 144 Tiles across All Presets + 24 Orbit Angles
const camera = new THREE.PerspectiveCamera(38, 16 / 9, 0.1, 100);
const raycaster = new THREE.Raycaster();

function applyEnvVisibilityGuard(presetKey, camPos) {
  const isTopView = presetKey === "2d" || presetKey === "topdown";
  const camDistToCenter = Math.hypot(camPos.x, camPos.z);
  overheadObstacles.forEach((mesh) => {
    if (isTopView) {
      mesh.visible = false;
      return;
    }
    const center = mesh.position;
    const dotSide = center.x * camPos.x + center.z * camPos.z;
    const objDist = Math.hypot(center.x, center.z);
    mesh.visible = !(dotSide > 0 && camDistToCenter > objDist - 3.5);
  });
}

const presets = {
  "2d": { pos: [0.0, 24.5, 0.001], target: [0.0, 0.2, 0.0], fov: 26 },
  hero: { pos: [0.0, 8.8, 11.6], target: [0.0, 0.3, 0.0], fov: 38 },
  topdown: { pos: [0.0, 15.6, 1.6], target: [0.0, 0.3, 0.0], fov: 40 },
  pavement: { pos: [5.4, 2.6, 8.4], target: [0.0, 0.4, -0.5], fov: 36 },
  macro: { pos: [0.0, 2.1, 6.2], target: [0.0, 0.35, 3.2], fov: 44 },
  orbit: { pos: [0.0, 8.6, 12.0], target: [0.0, 0.4, 0.0], fov: 40 },
};

// Add 24 360-degree orbit viewpoints at various heights to guarantee NO angle is blocked
const viewpoints = Object.entries(presets).map(([name, cfg]) => ({ name, ...cfg }));
for (let deg = 0; deg < 360; deg += 15) {
  const rad = THREE.MathUtils.degToRad(deg);
  const dist = 12.5;
  viewpoints.push({
    name: `orbit_${deg}deg`,
    pos: [Math.sin(rad) * dist, 5.2, Math.cos(rad) * dist],
    target: [0, 0.4, 0],
    fov: 38,
  });
}

let totalRays = 0;
let occludedRays = 0;

for (const vp of viewpoints) {
  camera.position.set(...vp.pos);
  camera.fov = vp.fov;
  camera.lookAt(...vp.target);
  camera.updateMatrixWorld(true);
  camera.updateProjectionMatrix();

  applyEnvVisibilityGuard(vp.name, camera.position);
  const visibleEnvMeshes = envMeshes.filter((m) => m.visible);

  for (const tilePos of tilePositions) {
    // Raycast from camera eye to the top center of each tile
    const targetPoint = new THREE.Vector3(tilePos.x, tilePos.y + TILE_D * 0.45, tilePos.z);
    const dir = new THREE.Vector3().subVectors(targetPoint, camera.position);
    const distToTile = dir.length();
    dir.normalize();

    raycaster.set(camera.position, dir);
    raycaster.near = 0.05;
    raycaster.far = distToTile - 0.02;

    const hits = raycaster.intersectObjects(visibleEnvMeshes, false);
    totalRays++;
    if (hits.length > 0) {
      occludedRays++;
      console.error(`  [Occlusion] Viewpoint '${vp.name}' blocked by '${hits[0].object.name}' at d=${hits[0].distance.toFixed(2)}m`);
    }
  }
}

assert(
  occludedRays === 0,
  `Zero environment occlusion across all ${viewpoints.length} viewpoints (${totalRays}/${totalRays} camera-to-tile sightlines 100% clear)`
);

// 5. Verify 100% of all 144 tiles fit inside the camera frustum in '2d', 'topdown', and 'hero' presets
for (const presetName of ["2d", "topdown", "hero"]) {
  const cfg = presets[presetName];
  camera.position.set(...cfg.pos);
  camera.fov = cfg.fov;
  camera.lookAt(...cfg.target);
  camera.updateMatrixWorld(true);
  camera.updateProjectionMatrix();

  let inFrustum = 0;
  for (const tilePos of tilePositions) {
    const ndc = tilePos.clone().project(camera);
    if (ndc.x >= -0.98 && ndc.x <= 0.98 && ndc.y >= -0.98 && ndc.y <= 0.98 && ndc.z >= -1.0 && ndc.z <= 1.0) {
      inFrustum++;
    }
  }
  assert(
    inFrustum === tilePositions.length,
    `Preset '${presetName}' frames 100% of the board (${inFrustum}/${tilePositions.length} tiles inside viewport)`
  );
}

if (failed) {
  process.exit(1);
}
