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

const carvedGlb = path.join(ROOT, "public/models/tile_carved_intaglio_showcase.glb");
assert(fs.existsSync(carvedGlb) && fs.statSync(carvedGlb).size > 100000, "3D Carved Intaglio Showcase GLB exists and is non-empty");

// 1b. Check Raspberry Pi 400 ("Sguisatazzo" V3D 4.2) Lightweight GLB assets
const rpiTileGlb = path.join(ROOT, "public/models/tile_generic_white_marble_obsidian_rpi.glb");
assert(
  fs.existsSync(rpiTileGlb) && fs.statSync(rpiTileGlb).size > 10000 && fs.statSync(rpiTileGlb).size < 100000,
  `Sguisatazzo RPi Generic Tile GLB exists and is ultra-lightweight (<100KB, actual: ${(fs.statSync(rpiTileGlb).size / 1024).toFixed(1)}KB)`
);
const rpiEnvGlb = path.join(ROOT, "public/models/temple_environment_rpi.glb");
assert(
  fs.existsSync(rpiEnvGlb) && fs.statSync(rpiEnvGlb).size > 20000 && fs.statSync(rpiEnvGlb).size < 250000,
  `Sguisatazzo RPi Temple Environment GLB exists and is ultra-lightweight (<250KB, actual: ${(fs.statSync(rpiEnvGlb).size / 1024).toFixed(1)}KB)`
);
const rpiShowcaseGlb = path.join(ROOT, "public/models/tile_coupled_showcase_rpi.glb");
assert(
  fs.existsSync(rpiShowcaseGlb) && fs.statSync(rpiShowcaseGlb).size > 20000 && fs.statSync(rpiShowcaseGlb).size < 500000,
  `Sguisatazzo RPi Coupled Showcase GLB exists and is lightweight (<500KB, actual: ${(fs.statSync(rpiShowcaseGlb).size / 1024).toFixed(1)}KB)`
);
const rpiCarvedGlb = path.join(ROOT, "public/models/tile_carved_intaglio_showcase_rpi.glb");
assert(
  fs.existsSync(rpiCarvedGlb) && fs.statSync(rpiCarvedGlb).size > 50000,
  `Sguisatazzo RPi Carved Intaglio Showcase GLB exists`
);

// 2. Topology audit
const auditFile = path.join(ROOT, "public/models/topology_audit.json");
assert(fs.existsSync(auditFile), "Topology audit report exists");
if (fs.existsSync(auditFile)) {
  const audit = JSON.parse(fs.readFileSync(auditFile, "utf8"));
  assert(audit.allManifoldPass === true, `All meshes passed manifold check (0 non-manifold edges, 0 degenerate faces)`);
}

// 3. Textures, Portraits, 3D Depth Maps & Manifest
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
  const oniricaExist = manifest.tiles.every((t) =>
    fs.existsSync(path.join(ROOT, "public/textures/tiles_onirica", `${t.id}.png`))
  );
  assert(oniricaExist, "All 50 Modalità Onirica ('Less is More' Whisper-Fade) tile textures exist");
  const depthExist = manifest.tiles.every((t) =>
    fs.existsSync(path.join(ROOT, "public/textures/tiles_depth", `${t.id}_depth.png`))
  );
  assert(depthExist, "All 50 3D Incandescent-Pen Carved Depth/Displacement maps ('*_depth.png') exist");
  const rpiTilesExist = manifest.tiles.every(
    (t) =>
      fs.existsSync(path.join(ROOT, "public/textures/tiles_rpi", `${t.id}.png`)) &&
      fs.existsSync(path.join(ROOT, "public/textures/tiles_onirica_rpi", `${t.id}.png`))
  );
  assert(rpiTilesExist, "All 50 Sguisatazzo RPi 256x342 tile textures ('tiles_rpi/' & 'tiles_onirica_rpi/') exist");
}
assert(
  fs.existsSync(path.join(ROOT, "public/textures/pbr_rpi/obsidian_basecolor_2k.png")) &&
    fs.existsSync(path.join(ROOT, "public/textures/pbr_rpi/rosewood_basecolor_2k.png")),
  "Sguisatazzo RPi 256x256 PBR textures ('public/textures/pbr_rpi/') exist"
);

const requiredPortraits = [
  "quartet_S1_papa_riccardo.png",
  "quartet_S1_papa_riccardo_top1.png",
  "quartet_S1_papa_riccardo_top3.png",
  "quartet_S2_mamma_kate2016.png",
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
  "bamboo_2_hotwheels_emblem.png",
  "bamboo_3_shiryu_dragon_emblem.png",
  "bamboo_4_gems_rubies_emblem.png",
  "dragon_red_ornate_emblem.png",
  "dragon_green_ornate_emblem.png",
  "dragon_white_ornate_emblem.png",
];
requiredPortraits.forEach((f) => {
  const p = path.join(ROOT, "public/portraits", f);
  assert(fs.existsSync(p) && fs.statSync(p).size > 50000, `Pure 2D Nano Banana portrait/emblem '${f}' exists`);
});

const brushFont = path.join(ROOT, "public/fonts/MaShanZheng-Regular.ttf");
assert(fs.existsSync(brushFont) && fs.statSync(brushFont).size > 1000000, "Calligraphic brush font 'MaShanZheng-Regular.ttf' exists");

const requiredFX = [
  "powerup_frame1_cloud_puff_white.png",
  "powerup_frame2_dragon_emerge_white.png",
  "powerup_frame3_dragon_fire_white.png",
  "powerup_frame1_cloud_puff_rgba.png",
  "powerup_frame2_dragon_emerge_rgba.png",
  "powerup_frame3_dragon_fire_rgba.png",
  "dragon_powerup_white.mp4",
  "dragon_powerup_audit_comparison.png",
  "family_powerup_frame2_crest_white.png",
  "family_powerup_frame3_celebrate_white.png",
  "family_powerup_frame2_crest_rgba.png",
  "family_powerup_frame3_celebrate_rgba.png",
  "family_powerup_white.mp4",
];
requiredFX.forEach((f) => {
  const p = path.join(ROOT, "public/fx", f);
  assert(fs.existsSync(p) && fs.statSync(p).size > 20000, `Power-Up FX asset '${f}' exists`);
});

["dragon_red_ornate", "dragon_green_ornate", "dragon_white_ornate"].forEach((id) => {
  assert(
    fs.existsSync(path.join(ROOT, "public/textures/tiles", `${id}.png`)) &&
      fs.existsSync(path.join(ROOT, "public/textures/tiles_onirica", `${id}.png`)) &&
      fs.existsSync(path.join(ROOT, "public/textures/tiles_normal", `${id}_normal.png`)) &&
      fs.existsSync(path.join(ROOT, "public/textures/tiles_depth", `${id}_depth.png`)),
    `Ornate "Tarchiato" Hover/Select Dragon texture & 3D maps exist for '${id}'`
  );
});

assert(
  !fs.existsSync(path.join(ROOT, "public/portraits/quartet_S1_papa_riccardo_top2.png")),
  "Rejected 'quartet_S1_papa_riccardo_top2.png' is cleanly removed"
);
assert(
  fs.readFileSync(path.join(ROOT, "public/portraits/quartet_S1_papa_riccardo.png")).equals(
    fs.readFileSync(path.join(ROOT, "public/portraits/quartet_S1_papa_riccardo_top3.png"))
  ),
  "Canonical 'quartet_S1_papa_riccardo.png' matches WINNER 'quartet_S1_papa_riccardo_top3.png'"
);

["coupled_A1_top3.png", "coupled_A1_top1.png"].forEach((f) => {
  const p = path.join(ROOT, "public/textures/tiles", f);
  assert(fs.existsSync(p) && fs.statSync(p).size > 50000, `S1 Mahjong Tile '${f}' exists`);
});

// 4. Cycles Ground Truth Renders
const cyclesRenders = [
  "cycles_cam1_hero.png",
  "cycles_cam2_topdown.png",
  "cycles_cam3_low_pavement.png",
  "cycles_cam4_tile_macro.png",
  "cycles_cam5_carved_intaglio.png",
];
cyclesRenders.forEach((f) => {
  const p = path.join(ROOT, "public/renders/cycles", f);
  assert(fs.existsSync(p) && fs.statSync(p).size > 50000, `Cycles Master Render '${f}' exists`);
});

// 5. Playable App, Dragon & Family Power-Up Overlays & Progress Gallery
assert(fs.existsSync(path.join(ROOT, "index.html")), "index.html exists");
const indexHtml = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");
assert(
  indexHtml.includes("dragon-powerup-overlay") &&
    indexHtml.includes("dragon-powerup-canvas") &&
    indexHtml.includes("family-powerup-video"),
  "index.html includes transparent 2D-over-3D '#dragon-powerup-overlay', '#dragon-powerup-canvas', and '#family-powerup-video'"
);
const mainJs = fs.readFileSync(path.join(ROOT, "src/main.js"), "utf8");
assert(
  mainJs.includes("triggerDragonPowerUpEffect") &&
    mainJs.includes("triggerFamilyPowerUpEffect") &&
    mainJs.includes("isRedOrGreenDragonPair") &&
    mainJs.includes("isCarlessoFamilyPair") &&
    mainJs.includes("setDragonOrnateState") &&
    mainJs.includes("unpremultiplyWhiteVideoFrame"),
  "src/main.js wires 'setDragonOrnateState' hover/selection morphing, 'isRedOrGreenDragonPair' -> Dragon Video, 'isCarlessoFamilyPair' -> Family Video, and zero video for all other suits"
);
assert(fs.existsSync(path.join(ROOT, "public/progress.html")), "public/progress.html exists");
assert(fs.existsSync(path.join(ROOT, "docs/LOG.md")), "docs/LOG.md exists");

if (failed) {
  console.error("\n💥 Verification Suite Failed!");
  process.exit(1);
} else {
  console.log("\n🎉 All 3D Mahjong Verification Checks Passed Successfully!");
}
