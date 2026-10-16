#!/usr/bin/env node
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

console.log("🔍 Running Carlesso Family 3D Mahjong Verification Suite...");

let failed = false;
function assert(condition, message) {
  if (!condition) {
    console.error(`❌ FAIL: ${message}`);
    failed = true;
  } else {
    console.log(`✅ PASS: ${message}`);
  }
}

// 1. Check GLB assets
const tileGlb = path.join(ROOT, "public/models/tile_generic_white_marble_obsidian.glb");
assert(fs.existsSync(tileGlb) && fs.statSync(tileGlb).size > 100000, "Canonical Generic Tile GLB exists and is non-empty");

const showcaseGlb = path.join(ROOT, "public/models/tile_coupled_showcase.glb");
assert(fs.existsSync(showcaseGlb) && fs.statSync(showcaseGlb).size > 100000, "Coupled Showcase GLB exists and is non-empty");

const envGlb = path.join(ROOT, "public/models/temple_environment.glb");
assert(fs.existsSync(envGlb) && fs.statSync(envGlb).size > 50000, "Temple Environment GLB exists and is non-empty");

// 2. Topology audit
const auditFile = path.join(ROOT, "public/models/topology_audit.json");
assert(fs.existsSync(auditFile), "Topology audit report exists");
if (fs.existsSync(auditFile)) {
  const audit = JSON.parse(fs.readFileSync(auditFile, "utf8"));
  assert(audit.allManifoldPass === true, `All meshes passed manifold check (0 non-manifold edges, 0 degenerate faces)`);
}

// 3. Textures, Portraits & Manifest
const manifestFile = path.join(ROOT, "public/textures/manifest.json");
assert(fs.existsSync(manifestFile), "Tile textures manifest.json exists");
if (fs.existsSync(manifestFile)) {
  const manifest = JSON.parse(fs.readFileSync(manifestFile, "utf8"));
  assert(manifest.tileCount === 50, `Manifest defines exactly 50 tiles (found: ${manifest.tileCount})`);
  assert(manifest.suitsCount === 34, `34 Original Traditional Mahjong suits present`);
  assert(manifest.coupledCount === 16, `16 Coupled Non-Identical Family tiles present`);
  const quartets = manifest.tiles.filter((t) => t.coupled && t.cardinality === 4);
  const diptyques = manifest.tiles.filter((t) => t.coupled && t.cardinality === 2);
  assert(quartets.length === 8, `8 Cardinality-4 Quartet tiles (S1..S4 Family Seasons + M1..M4 Magical Companions) present`);
  assert(diptyques.length === 8, `8 Cardinality-2 Diptyque Split-Pair tiles (E1..H2) present`);
}

const requiredPortraits = [
  "diptyque_S1_S2_papa_mamma.png",
  "diptyque_S3_S4_ale_sebi_tang.png",
  "diptyque_A_great_wall.png",
  "diptyque_B_cantonese_rice.png",
  "diptyque_C_shaolin_kungfu.png",
  "diptyque_D_chengdu_pandas.png",
  "quartet_F1_ale_ghigna.png",
  "quartet_F2_sebi_pupurabbu.png",
  "quartet_F3_solo_ghigna.png",
  "quartet_F4_solo_pupurabbu.png",
  "bamboo_1_sparrow_emblem.png",
];
requiredPortraits.forEach((f) => {
  const p = path.join(ROOT, "public/portraits", f);
  assert(fs.existsSync(p) && fs.statSync(p).size > 50000, `Pure 2D Nano Banana portrait '${f}' exists`);
});

// 4. Cycles Ground Truth Renders
const cyclesRenders = [
  "cycles_cam1_hero.png",
  "cycles_cam2_topdown.png",
  "cycles_cam3_low_pavement.png",
  "cycles_cam4_tile_macro.png",
];
cyclesRenders.forEach((f) => {
  const p = path.join(ROOT, "public/renders/cycles", f);
  assert(fs.existsSync(p) && fs.statSync(p).size > 50000, `Cycles Master Render '${f}' exists`);
});

// 5. Playable App & Progress Gallery
assert(fs.existsSync(path.join(ROOT, "index.html")), "index.html exists");
assert(fs.existsSync(path.join(ROOT, "public/progress.html")), "public/progress.html exists");
assert(fs.existsSync(path.join(ROOT, "docs/LOG.md")), "docs/LOG.md exists");

if (failed) {
  console.error("\n💥 Verification Suite Failed!");
  process.exit(1);
} else {
  console.log("\n🎉 All 3D Mahjong Verification Checks Passed Successfully!");
}
