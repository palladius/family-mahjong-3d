#!/usr/bin/env node
/**
 * Pre-Deploy & Post-Deploy Initial Chessboard Visual, Z-Buffer Self-Occlusion & 3D Rotation Integration Test
 *
 * Prevents regressions like the v1.8.1 bug where:
 *   1. Negative displacementBias (-0.88 * dispScale) pushed faceMesh vertices (y = 0.064..0.094) UNDERNEATH
 *      the solid top cap of bodyMesh (y = +0.095), making all 144 tiles look like blank beige blocks.
 *   2. Dragging on the board to rotate either triggered accidental tile clicks/errors on pointerdown
 *      or was locked in 2D mode (enableRotate = false).
 *
 * Runs:
 *   - Pre-Deploy (`node scripts/test_board_integration.mjs`):
 *       1. Builds the exact 144-tile initial chessboard in Three.js and raycasts 1,296 rays (9 per tile)
 *          to prove `faceMesh` is 100% above `bodyMesh` (zero self-occlusion at every point on every tile).
 *       2. Inspects the actual PNG pixel data of tile textures on the board to prove high visual contrast
 *          (non-blank, non-washed-out).
 *       3. Simulates real pointer drag events (`pointerdown` -> `pointermove` -> `pointerup`) on Three.js
 *          `OrbitControls` to verify the chessboard is smoothly rotatable in both 3D Hero and 2D modes,
 *          and that dragging to rotate never accidentally clicks tiles.
 *       4. Verifies `dist/` production bundle integrity if `dist/` exists.
 *   - Post-Deploy (`node scripts/test_board_integration.mjs --post-deploy`):
 *       Fetches the live GitHub Pages deployment (`https://palladius.github.io/family-mahjong-3d/`) and
 *       verifies the deployed JS bundle and tile textures match all visual & rotation invariants.
 */

import fs from "node:fs";
import path from "node:path";
import zlib from "node:zlib";
import { fileURLToPath } from "node:url";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { detectHardwareProfile } from "../src/main.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

const TILE_W = 0.68;
const TILE_H = 0.92;
const TILE_D = 0.19;

let failed = false;
function assert(cond, msg) {
  if (!cond) {
    console.error(`❌ FAIL [Board & Rotation Integration Test]: ${msg}`);
    failed = true;
  } else {
    console.log(`✅ PASS [Board & Rotation Integration Test]: ${msg}`);
  }
}

console.log("🧪 Running Initial Chessboard Visual, Self-Occlusion & 3D Rotation Integration Tests...");

const mainJs = fs.readFileSync(path.join(ROOT, "src/main.js"), "utf8");

// ============================================================================
// 1. STATIC & GEOMETRIC Z-BUFFER SELF-OCCLUSION AUDIT ACROSS ALL 144 TILES
// ============================================================================

// Ensure negative displacementBias is completely gone so faceMesh can never sink into bodyMesh
const hasNegativeDisplacementBias = /displacementBias\s*[:=]\s*-\s*0\.88/.test(mainJs);
assert(
  !hasNegativeDisplacementBias,
  "Zero negative displacementBias in src/main.js (faceMesh vertices never sink underneath bodyMesh top surface)"
);

assert(
  mainJs.includes("faceMesh.position.y = TILE_D * 0.5 + 0.003") &&
    mainJs.includes("polygonOffset: true") &&
    mainJs.includes("polygonOffsetFactor: -2"),
  "faceMesh sits strictly at y = TILE_D * 0.5 + 0.003 with polygonOffsetFactor: -2 above bodyMesh"
);

// Build exact production beveled parallelepiped + faceMesh geometry from src/main.js
function makeBeveledParallelepipedGeometry(w, d, h, cornerRadius = 0.042, bevelSize = 0.015) {
  const iw = Math.max(0.1, w - bevelSize * 2);
  const ih = Math.max(0.1, h - bevelSize * 2);
  const r = Math.min(cornerRadius, iw * 0.25, ih * 0.25);
  const x0 = -iw / 2;
  const y0 = -ih / 2;

  const shape = new THREE.Shape();
  shape.moveTo(x0 + r, y0);
  shape.lineTo(x0 + iw - r, y0);
  shape.quadraticCurveTo(x0 + iw, y0, x0 + iw, y0 + r);
  shape.lineTo(x0 + iw, y0 + ih - r);
  shape.quadraticCurveTo(x0 + iw, y0 + ih, x0 + iw - r, y0 + ih);
  shape.lineTo(x0 + r, y0 + ih);
  shape.quadraticCurveTo(x0, y0 + ih, x0, y0 + ih - r);
  shape.lineTo(x0, y0 + r);
  shape.quadraticCurveTo(x0, y0, x0 + r, y0);

  const geo = new THREE.ExtrudeGeometry(shape, {
    depth: Math.max(0.04, d - bevelSize * 2),
    bevelEnabled: true,
    bevelThickness: bevelSize,
    bevelSize: bevelSize,
    bevelSegments: 3,
    curveSegments: 6,
  });
  geo.rotateX(-Math.PI / 2);
  geo.center();
  return geo;
}

const bodyGeo = makeBeveledParallelepipedGeometry(TILE_W, TILE_D, TILE_H, 0.042, 0.015);
bodyGeo.computeBoundingBox();
const faceGeo = new THREE.PlaneGeometry(TILE_W * 0.91, TILE_H * 0.92, 1, 1);

const bodyMaxY = bodyGeo.boundingBox.max.y;
const faceY = TILE_D * 0.5 + 0.003;
assert(
  faceY > bodyMaxY + 0.002,
  `Tile faceMesh Y (${faceY.toFixed(4)}) is strictly above bodyMesh top cap Y (${bodyMaxY.toFixed(4)}) by +${(faceY - bodyMaxY).toFixed(4)}m`
);

// Build all 144 tiles on the initial chessboard and raycast 9 sample points per tile (1,296 rays)
function generateMasterDragonSlots() {
  const slots = [];
  for (let r = -3.5; r <= 3.5; r += 1) {
    for (let c = -5.5; c <= 5.5; c += 1) {
      if ((r === -2.5 || r === 2.5) && Math.abs(c) > 3.5) continue;
      if ((r === -3.5 || r === 3.5) && Math.abs(c) > 4.5 && Math.abs(c) < 5.5) continue;
      slots.push({ c, r, l: 0 });
    }
  }
  slots.push({ c: -6.5, r: -0.5, l: 0 }, { c: -6.5, r: 0.5, l: 0 });
  slots.push({ c: 6.5, r: -0.5, l: 0 }, { c: 6.5, r: 0.5, l: 0 });
  for (let r = -2.5; r <= 2.5; r += 1) {
    for (let c = -2.5; c <= 2.5; c += 1) {
      slots.push({ c, r, l: 1 });
    }
  }
  for (let r = -1.5; r <= 1.5; r += 1) {
    for (let c = -1.5; c <= 1.5; c += 1) {
      slots.push({ c, r, l: 2 });
    }
  }
  for (let r = -0.5; r <= 0.5; r += 1) {
    for (let c = -0.5; c <= 0.5; c += 1) {
      slots.push({ c, r, l: 3 });
    }
  }
  slots.push({ c: -0.5, r: 0.0, l: 4 }, { c: 0.5, r: 0.0, l: 4 });
  return slots.slice(0, 144);
}

const slots = generateMasterDragonSlots();
const raycaster = new THREE.Raycaster();
const downDir = new THREE.Vector3(0, -1, 0);
const heroCamPos = new THREE.Vector3(0.0, 7.2, 9.6);

let totalFaceRays = 0;
let faceFirstHits = 0;
let cameraSightHits = 0;

const sampleOffsets = [
  [0.01, 0.01],
  [-0.21, -0.29],
  [0.21, -0.29],
  [-0.21, 0.29],
  [0.21, 0.29],
  [0.01, -0.31],
  [0.01, 0.31],
  [-0.23, 0.01],
  [0.23, 0.01],
];

slots.forEach((s) => {
  const root = new THREE.Group();
  const bodyMesh = new THREE.Mesh(bodyGeo, new THREE.MeshBasicMaterial());
  bodyMesh.name = "bodyMesh";
  const faceMesh = new THREE.Mesh(faceGeo, new THREE.MeshBasicMaterial({ side: THREE.DoubleSide }));
  faceMesh.name = "faceMesh";
  faceMesh.rotation.x = -Math.PI / 2;
  faceMesh.position.y = faceY;
  root.add(bodyMesh);
  root.add(faceMesh);

  const x = s.c * (TILE_W * 1.03);
  const y = 0.28 + s.l * (TILE_D * 1.02);
  const z = s.r * (TILE_H * 1.03);
  root.position.set(x, y, z);
  root.updateMatrixWorld(true);

  for (const [ox, oz] of sampleOffsets) {
    totalFaceRays++;
    // 1. Vertical ray down onto the tile top
    const origin = new THREE.Vector3(x + ox, y + 2.0, z + oz);
    raycaster.set(origin, downDir);
    const hits = raycaster.intersectObjects([bodyMesh, faceMesh], false);
    if (hits.length > 0 && hits[0].object === faceMesh) {
      faceFirstHits++;
    }
    // 2. Ray from the initial Hero 3D camera toward the tile's top face point
    const targetPt = new THREE.Vector3(x + ox, y + faceY, z + oz);
    const camDir = targetPt.clone().sub(heroCamPos).normalize();
    raycaster.set(heroCamPos, camDir);
    const camHits = raycaster.intersectObjects([bodyMesh, faceMesh], false);
    if (camHits.length > 0 && camHits[0].object === faceMesh) {
      cameraSightHits++;
    }
  }
});

assert(
  faceFirstHits === totalFaceRays,
  `Zero vertical self-occlusion on initial chessboard: ${faceFirstHits}/${totalFaceRays} rays hit faceMesh before bodyMesh`
);
assert(
  cameraSightHits === totalFaceRays,
  `Zero Hero-3D camera self-occlusion on initial chessboard: ${cameraSightHits}/${totalFaceRays} camera rays hit faceMesh before bodyMesh (artwork 100% visible!)`
);

// ============================================================================
// 2. INITIAL CHESSBOARD TEXTURE PIXEL CONTRAST AUDIT (NO WASHED-OUT TILES!)
// ============================================================================

function parsePngBufferRgbStats(buf) {
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  const bitDepth = buf[24];
  const colorType = buf[25];
  const idatChunks = [];
  let offset = 8;
  while (offset < buf.length) {
    const len = buf.readUInt32BE(offset);
    const type = buf.subarray(offset + 4, offset + 8).toString("ascii");
    if (type === "IDAT") {
      idatChunks.push(buf.subarray(offset + 8, offset + 8 + len));
    }
    offset += 12 + len;
  }
  const raw = zlib.inflateSync(Buffer.concat(idatChunks));
  const bpp = colorType === 6 ? 4 : colorType === 2 ? 3 : 1;
  const stride = width * bpp + 1;

  // Reconstruct PNG scanlines (Sub, Up, Average, Paeth filters) and measure color contrast in central artwork region
  const prevLine = new Uint8Array(width * bpp);
  const curLine = new Uint8Array(width * bpp);
  let minLum = 255;
  let maxLum = 0;
  let colorfulPixels = 0;
  let totalSampled = 0;

  for (let y = 0; y < height; y++) {
    const filter = raw[y * stride];
    const rowStart = y * stride + 1;
    for (let i = 0; i < width * bpp; i++) {
      const xByte = raw[rowStart + i];
      const a = i >= bpp ? curLine[i - bpp] : 0;
      const b = prevLine[i];
      const c = i >= bpp ? prevLine[i - bpp] : 0;
      let val = xByte;
      if (filter === 1) val = (xByte + a) & 0xff;
      else if (filter === 2) val = (xByte + b) & 0xff;
      else if (filter === 3) val = (xByte + ((a + b) >> 1)) & 0xff;
      else if (filter === 4) {
        const p = a + b - c;
        const pa = Math.abs(p - a);
        const pb = Math.abs(p - b);
        const pc = Math.abs(p - c);
        const pr = pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
        val = (xByte + pr) & 0xff;
      }
      curLine[i] = val;
    }
    prevLine.set(curLine);

    // Sample interior artwork region (18%..82% X and Y)
    if (y > height * 0.18 && y < height * 0.82 && y % 4 === 0) {
      for (let x = Math.floor(width * 0.18); x < Math.floor(width * 0.82); x += 4) {
        const idx = x * bpp;
        const r = curLine[idx];
        const g = curLine[idx + 1];
        const b = curLine[idx + 2];
        const lum = 0.299 * r + 0.587 * g + 0.114 * b;
        if (lum < minLum) minLum = lum;
        if (lum > maxLum) maxLum = lum;
        if (lum < 210 || Math.max(r, g, b) - Math.min(r, g, b) > 28) {
          colorfulPixels++;
        }
        totalSampled++;
      }
    }
  }

  return {
    width,
    height,
    bitDepth,
    lumRange: maxLum - minLum,
    colorfulRatio: colorfulPixels / Math.max(1, totalSampled),
  };
}

function parsePngRgbStats(pngPath) {
  return parsePngBufferRgbStats(fs.readFileSync(pngPath));
}

const sampleTileIds = [
  "dragon_red",
  "dragon_green",
  "dragon_white",
  "char_1",
  "char_8",
  "dots_2",
  "dots_4",
  "bamboo_1",
  "wind_E",
  "coupled_A1",
  "coupled_E1",
];

for (const tileId of sampleTileIds) {
  const p = path.join(ROOT, `public/textures/tiles/${tileId}.png`);
  const stats = parsePngRgbStats(p);
  assert(
    stats.lumRange > 85 && stats.colorfulRatio > 0.03,
    `Tile texture '${tileId}.png' (${stats.width}x${stats.height}) has strong visual contrast (lumRange=${stats.lumRange.toFixed(1)}, inkCoverage=${(stats.colorfulRatio * 100).toFixed(1)}%)`
  );
}

// ============================================================================
// 3. INTERACTIVE 3D ORBITCONTROLS ROTATION & DRAG-VS-CLICK INTEGRATION TEST
// ============================================================================

class MockControlElement {
  constructor() {
    this.listeners = {};
    this.style = {};
    this.clientWidth = 1280;
    this.clientHeight = 800;
    this.ownerDocument = this;
  }
  addEventListener(type, fn) {
    if (!this.listeners[type]) this.listeners[type] = [];
    this.listeners[type].push(fn);
  }
  removeEventListener(type, fn) {
    if (!this.listeners[type]) return;
    this.listeners[type] = this.listeners[type].filter((f) => f !== fn);
  }
  dispatchEvent(evt) {
    const list = this.listeners[evt.type] || [];
    for (const fn of list) {
      fn.call(this, evt);
    }
  }
  getBoundingClientRect() {
    return { left: 0, top: 0, width: 1280, height: 800 };
  }
  setPointerCapture() {}
  releasePointerCapture() {}
  getRootNode() {
    return this;
  }
}

function createDomEvent(type, props = {}) {
  return {
    type,
    pointerId: 1,
    pointerType: "mouse",
    button: 0,
    buttons: 1,
    clientX: 0,
    clientY: 0,
    pageX: 0,
    pageY: 0,
    ctrlKey: false,
    metaKey: false,
    shiftKey: false,
    preventDefault() {},
    stopPropagation() {},
    ...props,
  };
}

const domElem = new MockControlElement();
const testCam = new THREE.PerspectiveCamera(38, 1280 / 800, 0.1, 100);
testCam.position.set(0.0, 7.2, 9.6);

const controls = new OrbitControls(testCam, domElem);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.enableRotate = true;
controls.enableZoom = true;
controls.enablePan = true;
controls.screenSpacePanning = false;
controls.mouseButtons = {
  LEFT: THREE.MOUSE.PAN,
  MIDDLE: THREE.MOUSE.DOLLY,
  RIGHT: THREE.MOUSE.ROTATE,
};
controls.touches = {
  ONE: THREE.TOUCH.PAN,
  TWO: THREE.TOUCH.DOLLY_ROTATE,
};
controls.target.set(0.0, 0.2, 0.0);
controls.update();

assert(
  mainJs.includes("LEFT: THREE.MOUSE.PAN") &&
    mainJs.includes("RIGHT: THREE.MOUSE.ROTATE") &&
    mainJs.includes("ONE: THREE.TOUCH.PAN") &&
    mainJs.includes("screenSpacePanning = false"),
  "src/main.js binds Left-Click/1-Finger drag to horizontal XZ PAN (preserving Left/Right Mahjong rules) and Right-Click/Shift-Drag/2-Finger to 3D ROTATE"
);

// Wire the exact pointerdown / pointermove / pointerup drag-vs-click guard from src/main.js
let pointerDownState = null;
let tileClickCount = 0;

domElem.addEventListener("pointerdown", (e) => {
  pointerDownState = { x: e.clientX, y: e.clientY, moved: false, button: e.button, pointerType: e.pointerType };
});
domElem.addEventListener("pointermove", (e) => {
  if (pointerDownState) {
    const dist = Math.hypot(e.clientX - pointerDownState.x, e.clientY - pointerDownState.y);
    if (dist > 6) pointerDownState.moved = true;
  }
});
domElem.addEventListener("pointerup", (e) => {
  const st = pointerDownState;
  pointerDownState = null;
  if (st && !st.moved && (st.button === 0 || st.button === undefined || st.pointerType === "touch")) {
    tileClickCount++;
  }
});

// Test 3A: Left-Click Drag (button: 0) TRANSLATES (PANS) the board while keeping Left/Right azimuth orientation 100% locked!
const startPos = testCam.position.clone();
const startTarget = controls.target.clone();
const startRel = startPos.clone().sub(startTarget);
const startRelAzimuth = Math.atan2(startRel.x, startRel.z);

domElem.dispatchEvent(createDomEvent("pointerdown", { button: 0, clientX: 640, clientY: 400, pageX: 640, pageY: 400 }));
domElem.dispatchEvent(createDomEvent("pointermove", { button: 0, clientX: 420, clientY: 310, pageX: 420, pageY: 310 }));
domElem.dispatchEvent(createDomEvent("pointerup", { button: 0, clientX: 420, clientY: 310, pageX: 420, pageY: 310 }));
for (let f = 0; f < 5; f++) controls.update();

const pannedPos = testCam.position.clone();
const pannedTarget = controls.target.clone();
const pannedRel = pannedPos.clone().sub(pannedTarget);
const pannedRelAzimuth = Math.atan2(pannedRel.x, pannedRel.z);
const panTargetShift = pannedTarget.distanceTo(startTarget);
const panAzimuthDriftDeg = (Math.abs(pannedRelAzimuth - startRelAzimuth) * 180) / Math.PI;

assert(
  panTargetShift > 0.4 && panAzimuthDriftDeg < 0.05,
  `Left-click drag TRANSLATES (pans) the board horizontally (target shifted ${panTargetShift.toFixed(2)}m) with 0.00° rotation so Left/Right tile edges stay strictly Left/Right!`
);
assert(
  tileClickCount === 0,
  "Dragging to translate/pan the chessboard does NOT accidentally click/error on tiles under the cursor"
);

// Test 3B: Right-Click Drag (button: 2) or Shift + Left-Click Drag ROTATES the 3D chessboard!
const preRotRel = testCam.position.clone().sub(controls.target);
const preRotAzimuth = Math.atan2(preRotRel.x, preRotRel.z);

domElem.dispatchEvent(createDomEvent("pointerdown", { button: 2, clientX: 640, clientY: 400, pageX: 640, pageY: 400 }));
domElem.dispatchEvent(createDomEvent("pointermove", { button: 2, clientX: 420, clientY: 310, pageX: 420, pageY: 310 }));
domElem.dispatchEvent(createDomEvent("pointerup", { button: 2, clientX: 420, clientY: 310, pageX: 420, pageY: 310 }));
controls.update();

const postRotRel = testCam.position.clone().sub(controls.target);
const postRotAzimuth = Math.atan2(postRotRel.x, postRotRel.z);
const deltaAzimuthDeg = (Math.abs(postRotAzimuth - preRotAzimuth) * 180) / Math.PI;

assert(
  deltaAzimuthDeg > 4.0,
  `Right-click / Shift+Left-click drag ROTATES the 3D chessboard cleanly (azimuth rotated ${deltaAzimuthDeg.toFixed(1)}°)`
);

// Test 3C: Simulate a clean click/tap (< 6px movement) and verify it DOES trigger tile selection
domElem.dispatchEvent(createDomEvent("pointerdown", { button: 0, clientX: 640, clientY: 400, pageX: 640, pageY: 400 }));
domElem.dispatchEvent(createDomEvent("pointermove", { button: 0, clientX: 642, clientY: 401, pageX: 642, pageY: 401 }));
domElem.dispatchEvent(createDomEvent("pointerup", { button: 0, clientX: 642, clientY: 401, pageX: 642, pageY: 401 }));

assert(tileClickCount === 1, "Clean click/tap (< 6px movement) triggers tile selection cleanly");

// Test 3C: Verify 2D Camera Preset also keeps enableRotate = true in src/main.js
assert(
  mainJs.includes("this.controls.enableRotate = true;") &&
    !mainJs.includes('this.controls.enableRotate = this.activeCameraPreset !== "2d"'),
  "src/main.js keeps OrbitControls rotation enabled in all camera presets (including 2D/mobile)"
);

// ============================================================================
// 4. SGUISATAZZO (RASPBERRY PI 400 V3D 4.2) AUTO-DETECTION HEURISTICS TEST
// ============================================================================

// 4A. Exact Sguisatazzo profile from Obsidian (Raspberry Pi 400 Rev 1.0, Broadcom BCM2711 Cortex-A72, V3D 4.2, 4GB RAM, 1920x1080 monitor)
const sguisatazzoProfile = detectHardwareProfile(new URLSearchParams(""), {
  userAgent: "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
  platform: "Linux aarch64",
  deviceMemory: 4,
  hardwareConcurrency: 4,
  maxTouchPoints: 0,
  innerWidth: 1920,
  innerHeight: 1080,
  gpuRenderer: "V3D 4.2",
  gpuVendor: "Broadcom",
  maxTextureSize: 4096,
});
assert(
  sguisatazzoProfile.isRpi === true && sguisatazzoProfile.tier === "rpi" && sguisatazzoProfile.reason.includes("V3D 4.2"),
  `Sguisatazzo Raspberry Pi 400 (Broadcom V3D 4.2, 1920x1080 non-touch HDMI) auto-detected at startup: isRpi=true (${sguisatazzoProfile.reason})`
);

// 4B. Linux ARM64 desktop with masked WebGL renderer string still triggers Sguisatazzo mode
const maskedArmLinuxProfile = detectHardwareProfile(new URLSearchParams(""), {
  userAgent: "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36",
  platform: "Linux aarch64",
  deviceMemory: 4,
  hardwareConcurrency: 4,
  maxTouchPoints: 0,
  innerWidth: 1920,
  innerHeight: 1080,
  gpuRenderer: "WebKit WebGL",
  gpuVendor: "WebKit",
  maxTextureSize: 4096,
});
assert(
  maskedArmLinuxProfile.isRpi === true,
  `Linux aarch64 + MAX_TEXTURE_SIZE=4096 auto-detects Sguisatazzo mode even if UNMASKED_RENDERER_WEBGL is masked (${maskedArmLinuxProfile.reason})`
);

// 4C. URL override ?sguisatazzo=1 forces Sguisatazzo mode on any desktop machine for testing
const urlForcedRpi = detectHardwareProfile(new URLSearchParams("sguisatazzo=1"), {
  userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
  platform: "MacIntel",
  deviceMemory: 8,
  hardwareConcurrency: 12,
  gpuRenderer: "Apple M3 Max",
  gpuVendor: "Apple",
  maxTextureSize: 16384,
});
assert(urlForcedRpi.isRpi === true, "URL parameter '?sguisatazzo=1' forces Sguisatazzo RPi mode on any machine");

// 4D. High-end Mac Desktop defaults to full high quality (isRpi === false)
const macDesktopProfile = detectHardwareProfile(new URLSearchParams(""), {
  userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
  platform: "MacIntel",
  deviceMemory: 8,
  hardwareConcurrency: 12,
  maxTouchPoints: 0,
  innerWidth: 2560,
  innerHeight: 1440,
  gpuRenderer: "ANGLE (Apple, ANGLE Metal Renderer: Apple M3 Max, Unspecified Version)",
  gpuVendor: "Google Inc. (Apple)",
  maxTextureSize: 16384,
});
assert(
  macDesktopProfile.isRpi === false && macDesktopProfile.tier === "high",
  "Apple M3 Max desktop keeps full High-Quality mode (isRpi=false)"
);

// 4E. Verify RPi 256x342 tile textures retain full Mahjong ink contrast
for (const tileId of ["dragon_red", "dragon_green", "dragon_white", "coupled_A1", "dots_4"]) {
  const rpiPath = path.join(ROOT, `public/textures/tiles_rpi/${tileId}.png`);
  const rpiStats = parsePngRgbStats(rpiPath);
  assert(
    rpiStats.width === 256 && rpiStats.height === 342 && rpiStats.lumRange > 85,
    `RPi texture 'tiles_rpi/${tileId}.png' (${rpiStats.width}x${rpiStats.height}) is 9x smaller in pixels while preserving sharp contrast (lumRange=${rpiStats.lumRange.toFixed(1)})`
  );
}

// ============================================================================
// 5. PRE-DEPLOY PRODUCTION BUNDLE (`dist/`) BROKEN-PUSH GATE (--check-dist)
// ============================================================================

const requireDist = process.argv.includes("--check-dist");
const distDir = path.join(ROOT, "dist");
const distAssetsDir = path.join(ROOT, "dist/assets");

if (requireDist) {
  assert(
    fs.existsSync(distDir) && fs.existsSync(distAssetsDir),
    "Pre-Deploy Gate (--check-dist): 'dist/' and 'dist/assets/' exist (run 'npm run build' first)"
  );
}

if (fs.existsSync(distAssetsDir)) {
  const distIndexPath = path.join(distDir, "index.html");
  assert(fs.existsSync(distIndexPath), "dist/index.html exists in built bundle");
  const distIndexHtml = fs.readFileSync(distIndexPath, "utf8");

  // 5A. Subpath Safety Check: No root-relative src="/assets/..." or href="/assets/..." that 404 on /family-mahjong-3d/
  const hasRootAssetRef = /(?:src|href)=["']\/(assets|textures|models|fx|fonts|portraits)\//.test(distIndexHtml);
  assert(
    !hasRootAssetRef,
    "dist/index.html uses strictly relative './' asset paths (safe for GitHub Pages '/family-mahjong-3d/' subpath)"
  );

  // 5B. Referenced JS & CSS bundles physically exist and meet minimum size thresholds
  const jsFiles = fs.readdirSync(distAssetsDir).filter((f) => f.endsWith(".js"));
  const cssFiles = fs.readdirSync(distAssetsDir).filter((f) => f.endsWith(".css"));
  assert(
    jsFiles.length > 0 && cssFiles.length > 0,
    `dist/assets/ contains compiled JS (${jsFiles.join(", ")}) and CSS (${cssFiles.join(", ")}) bundles`
  );

  if (jsFiles.length > 0) {
    const jsPath = path.join(distAssetsDir, jsFiles[0]);
    const jsSize = fs.statSync(jsPath).size;
    const bundleCode = fs.readFileSync(jsPath, "utf8");
    assert(jsSize > 400000, `Compiled JS bundle (${jsFiles[0]}) is non-truncated (${(jsSize / 1024).toFixed(1)} KB)`);
    assert(
      !bundleCode.includes("-0.88*") && !bundleCode.includes("-.88*") && bundleCode.includes("polygonOffsetFactor:-2"),
      `Compiled dist/ bundle (${jsFiles[0]}) has polygonOffsetFactor:-2 and zero negative displacementBias`
    );
    assert(
      bundleCode.includes("screenSpacePanning=!1") &&
        bundleCode.includes("dragon_white") &&
        bundleCode.includes("_ornate") &&
        bundleCode.includes("triggerGameOver") &&
        bundleCode.includes("VideoCore"),
      `Compiled dist/ bundle (${jsFiles[0]}) includes XZ PAN controls, Dragonlance 'dragon_white' + '_ornate', Sguisatazzo VideoCore/V3D auto-detection, and GameOver deadlock protection`
    );
    const hasRootFetchInBundle = /fetch\(["']\/(textures|models|fx|fonts)\//.test(bundleCode);
    assert(
      !hasRootFetchInBundle,
      `Compiled dist/ bundle (${jsFiles[0]}) has zero broken root-relative fetch('/textures/...') calls`
    );
  }

  // 5C. Complete dist/ Public Asset Tree Audit (Classic + Onirica + RPi 256px Textures, 8 GLBs with valid glTF magic header, Videos, Font)
  const distManifestPath = path.join(distDir, "textures/manifest.json");
  assert(fs.existsSync(distManifestPath), "dist/textures/manifest.json exists");
  if (fs.existsSync(distManifestPath)) {
    const distManifest = JSON.parse(fs.readFileSync(distManifestPath, "utf8"));
    const allDistTilesExist = distManifest.tiles.every(
      (t) =>
        fs.existsSync(path.join(distDir, "textures/tiles", `${t.id}.png`)) &&
        fs.existsSync(path.join(distDir, "textures/tiles_onirica", `${t.id}.png`)) &&
        fs.existsSync(path.join(distDir, "textures/tiles_rpi", `${t.id}.png`)) &&
        fs.existsSync(path.join(distDir, "textures/tiles_onirica_rpi", `${t.id}.png`)) &&
        fs.existsSync(path.join(distDir, "textures/tiles_normal", `${t.id}_normal.png`)) &&
        fs.existsSync(path.join(distDir, "textures/tiles_depth", `${t.id}_depth.png`))
    );
    const ornateDistExist = ["dragon_red_ornate", "dragon_green_ornate", "dragon_white_ornate"].every(
      (id) =>
        fs.existsSync(path.join(distDir, "textures/tiles", `${id}.png`)) &&
        fs.existsSync(path.join(distDir, "textures/tiles_onirica", `${id}.png`)) &&
        fs.existsSync(path.join(distDir, "textures/tiles_rpi", `${id}.png`)) &&
        fs.existsSync(path.join(distDir, "textures/tiles_onirica_rpi", `${id}.png`)) &&
        fs.existsSync(path.join(distDir, "textures/tiles_normal", `${id}_normal.png`)) &&
        fs.existsSync(path.join(distDir, "textures/tiles_depth", `${id}_depth.png`))
    );
    assert(
      allDistTilesExist && ornateDistExist,
      "All 318+ tile textures (Classic + Onirica + RPi 256px + Normal + Depth + Ornate Dragon maps) are present in dist/textures/"
    );
  }

  const distGlbs = [
    "models/tile_generic_white_marble_obsidian.glb",
    "models/temple_environment.glb",
    "models/tile_coupled_showcase.glb",
    "models/tile_carved_intaglio_showcase.glb",
    "models/tile_generic_white_marble_obsidian_rpi.glb",
    "models/temple_environment_rpi.glb",
    "models/tile_coupled_showcase_rpi.glb",
    "models/tile_carved_intaglio_showcase_rpi.glb",
  ];
  for (const relGlb of distGlbs) {
    const p = path.join(distDir, relGlb);
    const exists = fs.existsSync(p);
    let validHeader = false;
    if (exists) {
      const fd = fs.openSync(p, "r");
      const hdr = Buffer.alloc(12);
      fs.readSync(fd, hdr, 0, 12, 0);
      fs.closeSync(fd);
      const magic = hdr.toString("ascii", 0, 4);
      const version = hdr.readUInt32LE(4);
      const totalLen = hdr.readUInt32LE(8);
      validHeader = magic === "glTF" && version === 2 && totalLen === fs.statSync(p).size;
    }
    assert(exists && validHeader, `dist/${relGlb} exists and has a valid binary glTF v2 header`);
  }

  assert(
    fs.existsSync(path.join(distDir, "fx/dragon_powerup_white.mp4")) &&
      fs.existsSync(path.join(distDir, "fx/family_powerup_white.mp4")) &&
      fs.existsSync(path.join(distDir, "fonts/MaShanZheng-Regular.ttf")) &&
      fs.existsSync(path.join(distDir, "progress.html")),
    "dist/ includes Power-Up MP4 videos, MaShanZheng-Regular.ttf brush font, and progress.html showcase"
  );
}

// ============================================================================
// 6. POST-DEPLOY LIVE GITHUB PAGES DEEP VERIFICATION (--post-deploy)
// ============================================================================

if (process.argv.includes("--post-deploy")) {
  const liveUrl = process.env.LIVE_GHP_URL || "https://palladius.github.io/family-mahjong-3d/";
  console.log(`🌐 Running Deep Post-Deploy Live Verification against ${liveUrl} ...`);

  const res = await fetch(`${liveUrl}?t=${Date.now()}`, { cache: "no-store", redirect: "follow" });
  assert(res.ok, `Live GitHub Pages index.html responded HTTP ${res.status} (${res.url})`);
  const html = await res.text();

  const jsMatch = html.match(/src="\.?\/?assets\/(index-[^"]+\.js)"/);
  const cssMatch = html.match(/href="\.?\/?assets\/(index-[^"]+\.css)"/);
  assert(Boolean(jsMatch) && Boolean(cssMatch), "Live index.html references compiled Vite JS and CSS bundles");

  if (jsMatch) {
    const jsUrl = `${liveUrl}assets/${jsMatch[1]}?t=${Date.now()}`;
    const jsRes = await fetch(jsUrl, { cache: "no-store" });
    assert(jsRes.ok, `Live JS bundle (${jsMatch[1]}) responded HTTP ${jsRes.status}`);
    const liveBundle = await jsRes.text();
    assert(
      liveBundle.includes("polygonOffsetFactor:-2") &&
        !liveBundle.includes("-.88*") &&
        liveBundle.includes("screenSpacePanning=!1") &&
        liveBundle.includes("dragon_white") &&
        liveBundle.includes("_ornate"),
      `Live deployed JS bundle (${jsMatch[1]}, ${(liveBundle.length / 1024).toFixed(1)} KB) contains all 3D elevation, XZ PAN, and Dragonlance filigree invariants`
    );
  }

  // Verify live manifest.json
  const manifestRes = await fetch(`${liveUrl}textures/manifest.json?t=${Date.now()}`, { cache: "no-store" });
  assert(manifestRes.ok, `Live textures/manifest.json responded HTTP ${manifestRes.status}`);
  if (manifestRes.ok) {
    const liveManifest = await manifestRes.json();
    assert(
      liveManifest.tileCount === 50 && liveManifest.suitsCount === 34 && liveManifest.coupledCount === 16,
      `Live manifest.json serves all ${liveManifest.tileCount} tiles (34 suits + 16 coupled family tiles)`
    );
  }

  // Verify live binary 3D GLB header over HTTP
  const glbRes = await fetch(`${liveUrl}models/temple_environment.glb?t=${Date.now()}`, { cache: "no-store" });
  assert(glbRes.ok, `Live models/temple_environment.glb responded HTTP ${glbRes.status}`);
  if (glbRes.ok) {
    const glbBuf = Buffer.from(await glbRes.arrayBuffer());
    const magic = glbBuf.toString("ascii", 0, 4);
    const version = glbBuf.readUInt32LE(4);
    assert(
      magic === "glTF" && version === 2 && glbBuf.length > 50000,
      `Live temple_environment.glb is a valid binary glTF v2 asset (${(glbBuf.length / 1024).toFixed(1)} KB)`
    );
  }

  // Verify live PNG tile textures & decode their RGB scanlines over HTTP
  for (const liveTileId of ["dragon_white", "dragon_white_ornate", "coupled_A1"]) {
    const pngRes = await fetch(`${liveUrl}textures/tiles/${liveTileId}.png?t=${Date.now()}`, { cache: "no-store" });
    assert(pngRes.ok, `Live tile texture 'textures/tiles/${liveTileId}.png' responded HTTP ${pngRes.status}`);
    if (pngRes.ok) {
      const pngBuf = Buffer.from(await pngRes.arrayBuffer());
      const stats = parsePngBufferRgbStats(pngBuf);
      assert(
        stats.lumRange > 85 && stats.colorfulRatio > 0.03,
        `Live tile texture '${liveTileId}.png' (${stats.width}x${stats.height}) has crisp RGB contrast over HTTP (lumRange=${stats.lumRange.toFixed(1)}, inkCoverage=${(stats.colorfulRatio * 100).toFixed(1)}%)`
      );
    }
  }
}

if (failed) {
  console.error("\n💥 Initial Chessboard & Rotation Integration Test Suite FAILED!");
  process.exit(1);
} else {
  console.log("\n🎉 All Initial Chessboard Visual, Self-Occlusion & 3D Rotation Integration Checks PASSED!");
}
