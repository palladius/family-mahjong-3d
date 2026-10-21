# Changelog - Carlesso Family Mahjong 3D 🀄🐉

## [1.8.2] - 2026-10-21
### Fixed & Added
- **🐛 Fix Washed-Out / Buried Tile Faces on Half-Thickness Beveled Parallelepiped (`src/main.js`)**:
  - **Root Cause**: When `bodyMesh` was replaced in `v1.8.1` with a solid beveled parallelepiped (`makeBeveledParallelepipedGeometry`, top surface at `y = +TILE_D * 0.5 = +0.0950`), `faceMesh` (`y = +0.0965`) still had `displacementBias = -0.88 * dispScale` (`-0.0324`). That negative displacement bias pushed 98.5% of `faceMesh` vertices (`depth < 0.88`) down to `y = +0.064..+0.094`, burying the entire tile face **underneath the opaque beige top cap of `bodyMesh` (`y = +0.0950`)** so only tiny specks (`depth > 0.86`) poked through!
  - **Fix**: Removed negative `displacementBias` from `faceMesh` across `createTileMesh`, `toggleOniricaMode`, `sl-bassorilievo`, and `syncSliderUI`, and positioned `faceMesh` strictly at `y = TILE_D * 0.5 + 0.003` (`+0.0980`, `+3.0mm` above `bodyMesh`) with `polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2` while preserving full 1024×1024 `normalMap` 3D relief lighting.
- **🔄 Smooth 3D Board Rotation & Drag-vs-Click Disambiguation (`src/main.js`)**:
  - Kept `this.controls.enableRotate = true` in all camera presets (including `2d` / mobile) and cancelled active camera preset tweens on `OrbitControls` `"start"` so manual rotation never fights camera transitions.
  - Added a 6px pointer movement guard between `pointerdown` and `pointerup` so dragging across the chessboard to rotate the 3D view **never** accidentally clicks or triggers error buzzers on tiles under the cursor.
- **🧪 Pre-Deploy & Post-Deploy Initial Chessboard & 3D Rotation Integration Test (`scripts/test_board_integration.mjs`, `justfile`)**:
  - Added `scripts/test_board_integration.mjs` to `just test` (pre-deploy) and `just test-post-deploy` (live URL verification):
    1. Raycasts **1,296 rays (`144 tiles × 9 points`)** from both vertical `-Y` and the Hero 3D camera against `[bodyMesh, faceMesh]` to guarantee `100%` of rays hit `faceMesh` before `bodyMesh` (zero self-occlusion).
    2. Decodes PNG scanlines of tile textures to verify strong RGB luminance contrast (`lumRange > 85`, non-blank, non-washed-out).
    3. Simulates real `pointerdown` $\rightarrow$ `pointermove` $\rightarrow$ `pointerup` drag events on `OrbitControls` to verify the 3D board rotates (`deltaAzimuth > 4°`) without triggering tile clicks, while stationary clicks (`< 6px`) select tiles cleanly.
    4. Verifies compiled `dist/` bundle pre-deploy and live GitHub Pages bundle post-deploy (`--post-deploy`).

## [1.8.1] - 2026-10-19
### Changed & Added
- **✨ "Less is More" Ultra-Clean Tile Faces (No Octagonal Circles, More Breathing Room)**:
  - Completely removed `draw_imperial_cloud_flourishes` (the 8-bead octagonal circles around `char_1..9`, `wind_E/S/W/N`, and `dragon_red/green/white`), removed the diagonal marble vein scratches, removed the red inner border, and removed the bottom text cartouche on `coupled_*` tiles in `scripts/build_all_tile_textures.py`.
  - Kept only a clean, subtle outer border (`ok il bordo esterno`) on pure warm ivory (`#FAF6EE`) so every tile has maximum breathing room.
- **🏷️ Toggleable Top-Left & Top-Right Corner Symbols (`Debug Simboli: OFF` by Default)**:
  - Removed baked-in top-left (`C`, `S1..S4`, `1..9`) and top-right (`中`, `春`, `一..九`) corner symbols from all 50 tile PNGs (`public/textures/tiles/*.png` and `public/textures/tiles_onirica/*.png`).
  - Exported `"cornerLeft"`, `"cornerRight"`, and `"cornerColor"` in `public/textures/manifest.json` and wired a runtime Three.js overlay plane (`debugCornerMesh`) controlled by `#btn-debug-symbols` (`🏷️ Debug Simboli: OFF`), `#chk-debug-symbols` in the Studio Panel, key **`S`**, or `?symbols=1` — **disabled (`OFF`) by default**!
- **🧱 Half-Thickness White/Ivory 8-Bevel Parallelepiped (`TILE_D = 0.19`, Zero Middle Red/Gold Waist Band)**:
  - Halved tile thickness from `TILE_D = 0.38` to **`TILE_D = 0.19`**.
  - Replaced the multi-part tile body (`kintsugiMesh` middle band + `collarMesh` + `badgeMesh` + black obsidian back) with a single uniform **white/ivory 3D parallelepiped with 8 chamfered/beveled edges** (`makeBeveledParallelepipedGeometry`).

## [1.8.0] - 2026-10-19
### Added & Changed
- **📱 Ultra-Clean Single-Row Mobile HUD ("Zero tastini idioti sopra la scacchiera")**:
  - Replaced the multi-line mobile header and bottom camera dock with a **single-row 38px mobile top bar** (`#game-hud` with `flex-wrap: nowrap`), hiding `#camera-bar`, `#wow-3d-popup`, and all button text labels (`.btn-label`) on mobile so 5 compact 30×30px icon buttons (`📖`, `💡`, `🔀`, `📐`, `⛶`) leave >92% of the mobile screen 100% unobstructed for the Mahjong board.
  - Transformed `#selection-card` on mobile into a non-intrusive 36px single-line micro-pill at `bottom: 6px`.
- **⚡ 60 FPS Lightweight 3D Engine Overhaul ("3D Super Pesante" Eliminated — 6,900x Fewer Triangles on Mobile)**:
  - Reduced tile face `PlaneGeometry` from `72x96` (13,824 triangles per tile = **1,990,656 triangles** across 144 tiles) to `1x1` on mobile (**2 triangles per tile** = 288 triangles total, a **6,900x reduction**!) and `24x32` on desktop (`48x64` reserved only for the single close-up `#wow-3d-popup` preview tile).
  - Replaced 144 individual `MeshPhysicalMaterial` allocations with **4 shared body material sets** (`bodyMatFree`, `bodyMatBlocked`, `bodyMatSelected`, `bodyMatPulse` using lightweight `MeshStandardMaterial` on mobile).
  - Eliminated per-frame `new THREE.Box3().setFromObject(mesh)` allocations inside `updateEnvironmentVisibility()` by caching `child.userData.cachedCenter` once when loading `temple_environment.glb`.
  - Disabled shadow map rendering, 4 dynamic lantern `PointLight`s, and the secondary `wowRenderer` WebGL loop on mobile viewports.
- **🐉 Red & Green Dragons (`dragon_red` 中 & `dragon_green` 發) — Clean Calligraphic Board Symbol + Automatic "Tarchiato" Ornate Dragon on Hover/Selection**:
  - Default board textures (`public/textures/tiles/dragon_red.png` and `dragon_green.png`) now display **ONLY the traditional Chinese calligraphic character** (`中` in crimson, `發` in jade green), 100% consistent with the rest of the suits.
  - Built dedicated ornate textures (`public/textures/tiles/dragon_red_ornate.png` and `dragon_green_ornate.png` + `_normal.png`, `_depth.png`, `tiles_onirica/`) with the coiled 3D carved dragons.
  - Wired `setDragonOrnateState(tile, true)` in `src/main.js` so hovering or selecting **Drago Rosso (`dragon_red`)** or **Drago Verde (`dragon_green`)** (and *never* `bamboo_3` *"Sirio il Dragone"* or `dragon_white`) automatically morphs the tile into the chunky "tarchiato" ornate dragon (`scale(1.06, 1.14, 1.04)`)!
- **🎬 Exclusive Power-Up Videos: Dragon Video ONLY for Red/Green Dragons + New Carlesso Family Power-Up Video**:
  - **Dragon Power-Up Video (`triggerDragonPowerUpEffect`)**: Triggered **ONLY** when matching a pair of `dragon_red` (`中`) or `dragon_green` (`發`).
  - **Carlesso Family Power-Up Video (`triggerFamilyPowerUpEffect`)**: Generated new white-background keyframes (`public/fx/family_powerup_frame2_crest_white.png`, `public/fx/family_powerup_frame3_celebrate_white.png`) via Nano Banana and ran our **Border-Seeded Flood-Fill + Exact White Un-Premultiplication** pipeline (`scripts/build_powerup_video_fx.py`) to produce zero-halo transparent RGBA sprites (`family_powerup_frame2_crest_rgba.png`, `family_powerup_frame3_celebrate_rgba.png`) and `public/fx/family_powerup_white.mp4`, emerging from the cloud puff (`powerup_frame1_cloud_puff_rgba.png`) whenever any Carlesso Family pair (`S1..S4`, `M1..M4`, `E1..H2`) is matched!
  - **All Other Suits**: Zero video popup (`"per tutti gli altri pezzi il video SCOMPARE"`).

## [1.7.1] - 2026-10-18
### Added
- **📱 Mobile UX & Viewport Overhaul (GitHub Issue #2)**:
  - **Clean Viewport & Fullscreen Experience**: Automatically collapses desktop look-dev studio bars, banners, and footer text on mobile viewports (`max-width: 768px`). Added one-tap `⛶ Fullscreen` toggle button.
  - **Default 2D View with 3D Rotation Toggle**: Automatically defaults to clean 2D Top-Down planar view on mobile and small touch devices, with dynamic FOV calculation for portrait orientation to ensure all 144 tiles fit without horizontal clipping.
  - **Forgiving Touch Hitboxes & Haptic Feedback**: Multi-point forgiving raycast hitboxes for touchscreens and haptic vibration feedback (`navigator.vibrate`) on valid pair matches, single selection, and mismatch errors.

## [1.7.0] - 2026-10-17
### Added
- **🐉 Ornate 3D Carved Red Dragon (`dragon_red` / `紅中`) & Organic Chinese Brush Calligraphy (`Ma Shan Zheng` + `Songti` • GitHub Issue #1)**:
  - Replaced the mechanical sans-serif (`STHeiti Medium.ttc`) orthogonal lines on Chinese Character (`一萬..九萬`), Wind (`東 南 西 北`), and Dragon (`中 發 白`) tiles with authentic **Ma Shan Zheng** master Chinese brush calligraphy (`public/fonts/MaShanZheng-Regular.ttf`) + Songti Traditional fallback (`Songti.ttc index=1`).
  - Generated bespoke ornate emblems (`public/portraits/dragon_red_ornate_emblem.png`, `dragon_green_ornate_emblem.png`, `dragon_white_ornate_emblem.png`) featuring a coiled imperial crimson-and-24k-gold Chinese dragon with engraved scales and auspicious cloud scrolls wrapping around the calligraphic `中`, `發`, and `白`.
  - Upgraded `apply_incandescent_pen_carving()` in `scripts/build_all_tile_textures.py` with a **Multi-Scale V-Groove + Medial-Axis Spine** heightfield so every brush stroke and dragon scale carves into a curved 3D V-trench instead of a flat orthogonal plateau.
  - Updated Headless Blender 5.0.1 showcase (`scripts/blender/build_carved_intaglio_showcase.py`, `public/models/tile_carved_intaglio_showcase.glb`, `public/renders/cycles/cycles_cam5_carved_intaglio.png`) featuring `4筒`, **`紅中` (Ornate 3D Carved Red Dragon hero)**, and `八萬`.
- **✨ Transparent 2D-over-3D "Puff of Cloud $\rightarrow$ Frame 2 Dragon Emerge Biribip Power-Up" Video/Canvas FX (`scripts/build_powerup_video_fx.py`, `src/main.js`, `index.html`)**:
  - Designed by an Adversarial Net of 2 Subagents (`Subagent A: Dragon & VFX Power-Up Architect` vs. `Subagent B: Adversarial VFX & 3D Dragon Critic`) for **GitHub Issue #1**.
  - Generated white-background (`#FFFFFF`) keyframes (`public/fx/powerup_frame1_cloud_puff_white.png`, **`public/fx/powerup_frame2_dragon_emerge_white.png`** — RiccardinoCM26 🦖's favorite hero effect!, `public/fx/powerup_frame3_dragon_fire_white.png`) and white-background MP4 (`public/fx/dragon_powerup_white.mp4`).
  - Implemented **Border-Seeded Flood-Fill + Exact White Un-Premultiplication ($\mathbf{C}_{\text{clean}} = \frac{\mathbf{C} - (1-\alpha)}{\alpha}$) + Fiery Edge Despill** to produce zero-halo transparent RGBA sprites (`powerup_frame1..3_*_rgba.png`) and live `<video>` frame keying without milky fringes or punched-out dragon eyes/teeth (`public/fx/dragon_powerup_audit_comparison.png`).
  - Wired `triggerDragonPowerUpEffect()` and `sfx.playDragonBiribipPowerUp()` in `src/main.js` to trigger automatically whenever the player matches **Ale, Sebi, or Dragon** tiles (or on demand via `🐉 Biribip FX (D)` / Key `D`).

## [1.6.1] - 2026-10-17
### Changed
- **🏆 `S1 春 • Solo Papà Riccardo` Final Selection (`quartet_S1_papa_riccardo_top3.png` Wins, `top1` Kept in Subordine, `top2` Removed)**:
  - Promoted **`quartet_S1_papa_riccardo_top3.png`** (`s1_cand_08.png`) as the active canonical `public/portraits/quartet_S1_papa_riccardo.png`, `public/textures/tiles/coupled_A1.png`, `public/textures/tiles_onirica/coupled_A1.png`, and `public/portraits/diptyque_S1_S2_papa_mamma.png`.
  - Kept **`quartet_S1_papa_riccardo_top1.png`** (`coupled_A1_top1.png`, `onirica_coupled_A1_top1.png`) in reserve (*in subordine*).
  - Removed rejected `quartet_S1_papa_riccardo_top2.png`, `coupled_A1_top2.png`, and `onirica_coupled_A1_top2.png`.

## [1.6.0] - 2026-10-17
### Added
- **🛑 Dedicated Game Over Modal & Solvability Engine (`MahjongSolvabilityEngine`, `#gameover-modal`)**:
  - Implemented an ultra-fast graph precomputation DFS solver with state hashing (running in ~1-3ms).
  - Automatically detects **Immediate Deadlock** (`matchablePairs === 0`) and **Early Unsolvable States** (when no valid path exists to clear remaining tiles, even if some moves remain).
  - Triggers a beautiful dark obsidian & red-lacquer `#gameover-modal` displaying Remaining Tiles, Final Score, Moves, and Combo.
  - Added 4 actions: **"🔄 Rimescola Risolvibile (Solvable Shuffle)"** (rescues the game into a 100% solvable board), **"🔁 Ricomincia Livello"**, and **"👁️ Rivedi Scacchiera"**.
- **💡 Smart Winning-Path Hint (`provideHint`)**:
  - Upgraded Hint to consult the Solvability Engine: pulses a pair that lies directly on the *winning resolution path*, preventing players from falling into dead-end traps!
  - If no winning moves or paths exist, alerts the user and displays Game Over with the Solvable Shuffle option.
- **📐 Authentic Real-World Mahjong Tile Dimensions & Proportions**:
  - Replaced oversized chunky brick dimensions (`0.96 × 1.28 × 0.56`) with authentic real-world Mahjong proportions (`22mm × 30mm × 13mm`, ratio `0.739 : 1.000 : 0.413`): `TILE_W = 0.68`, `TILE_H = 0.92`, `TILE_D = 0.38`.
  - Scaled collar, kintsugi waist seam, badge, and selection frames.
  - Calibrated camera viewpoints across all 6 presets (`2d`, `hero`, `topdown`, `pavement`, `macro`, `orbit`) ensuring 100% frustum coverage and zero occlusion.
- **🌐 GitHub Pages Playable Badge & Link**:
  - Added prominent banner and badge at the top of `README.md` linking directly to `https://palladius.github.io/family-mahjong-3d/`.

## [1.5.0] - 2026-10-16
### Added
- **🏆 Adversarial Net of 3 Critic Subagents & Top-3 `S1 春 • Solo Papà Riccardo` Remaster (`scripts/generate_s1_riccardo_candidates.py`, `scripts/finalize_s1_top3.py`)**:
  - Generated 8 candidate portraits (`public/portraits/candidates_s1/s1_cand_01..08.png`) conditioned on tight high-res facial crops of Riccardo's real GIC photos (`ricc_crop_1_papino.jpg`, `ricc_crop_2_switzerland.jpg`, `ricc_crop_3_southafrica.jpg`, `ricc_crop_4_wine.jpg`, `ricc_crop_5_lake.jpg`).
  - Dispatched a 3-judge Adversarial Net (`Judge 1: Forensic Craniofacial Likeness Critic`, `Judge 2: Adversarial Impostor Detector`, `Judge 3: Mahjong Cameo & Artistic Critic`) to score all 8 candidates and committed the **Top 3 portraits and Top 3 rendered Mahjong tiles**:
    1. **🥇 TOP 1 (`s1_cand_01.png` — Ensemble `8.96/10`, Unanimous Top-3 across all 3 judges)**: `public/portraits/quartet_S1_papa_riccardo_top1.png` & `public/textures/tiles/coupled_A1_top1.png` (set as active default `coupled_A1.png`).
    2. **🥈 TOP 2 (`s1_cand_04.png` — Ensemble `8.97/10`, Judge 2 Red-Team #1 Winner `9.70/10`)**: `public/portraits/quartet_S1_papa_riccardo_top2.png` & `public/textures/tiles/coupled_A1_top2.png`.
    3. **🥉 TOP 3 (`s1_cand_08.png` — Ensemble `8.96/10`, Ranked #2 by both Judge 2 & Judge 3)**: `public/portraits/quartet_S1_papa_riccardo_top3.png` & `public/textures/tiles/coupled_A1_top3.png`.

### Changed
- **🎯 Minimal Non-Intrusive Selection UI & $\pm 30^\circ$ Face-Forward 3D Inspector (`index.html`, `src/main.js`, `src/style.css`)**:
  - Removed all purple styling (`selectionBorder.visible = false`, removed `0xa832ff` purple point light, removed purple CSS borders/glows) from `#wow-3d-popup`, shrunk it to a compact `128px` glass card (`top: 74px; left: 12px`), and replaced full 360° spinning with a **$\pm 30^\circ$ (`Math.PI / 6`) face-forward oscillation** so the carved 3D face is always visible.
  - Moved `#selection-card` out of the bottom-center of the board into a **compact, minimal glass bar in the top-right empty margin (`top: 74px; right: 12px; max-width: 395px;`)** with concise `9.5px–11px` typography so **0% of the Mahjong board is covered** while planning the next move.

## [1.4.1] - 2026-10-16
### Added
- **📖 Visual Tile Matching Guide Modal (`#help-modal`, Tasto `H`) & Live `"🔗 VA CON:"` Partner Strip**:
  - Pressing **`H`** (or **`?`**) on the keyboard or clicking **`📖 Guida (H)`** in the top HUD / bottom dock opens a visual **"Quale Tile va con Quale Tile?"** cheat-sheet modal showing all 4 matching rules with actual tile images:
    1. **Quartetto Famiglia Carlesso (`S1..S4`)**: *Qualsiasi 2 su 4 fanno coppia* (`Papà Riccardo`, `Mamma Kate`, `Ale`, `Sebi`).
    2. **Quartetto Compagni Magici (`M1..M4`)**: *Qualsiasi 2 su 4 fanno coppia* (`Ale+Ghigna`, `Sebi+Pupurabbu`, `Solo Ghigna`, `Solo Pupurabbu`).
    3. **4 Dittici Divisi a Metà (`E1↔E2` Muraglia, `F1↔F2` Riso, `G1↔G2` Shaolin, `H1↔H2` Panda)**: *Metà Sinistra Ale (`X1`) ↔ Metà Destra Sebi (`X2`)*.
    4. **34 Semi Classici & Bambù Comici (`1索..4索` Pavone/Hot Wheels/Sirio/Gemme, `1..9`, Venti, Draghi)**: *Coppie Identiche*.
  - Selecting any tile on the board now immediately renders a live **`"🔗 VA CON:"`** partner thumbnail strip (`#sel-partners-box`) inside `#selection-card` showing the exact partner tile(s) that match with the selected tile.

## [1.4.0] - 2026-10-16
### Added
- **🔥 3D "Incandescent Pen" Carved Intaglio (`buco bassorilievo scavato`)**:
  - Built a dual-frequency 3D Incandescent-Pen Carving Engine (`apply_incandescent_pen_carving` in `scripts/build_all_tile_textures.py`) generating 50 smooth chamfered 8-bit 3D displacement maps (`public/textures/tiles_depth/*_depth.png`), high-slope normal maps (`strength=18.0`), and pyro-carved diffuse textures with scorched-umber inner groove wall shadows and molten-gold raised rims.
  - Upgraded Three.js tile geometry (`src/main.js`) with a subdivided `72×96` face mesh (`displacementMap` + `displacementScale` + `normalScale`), recessed cavity body, and outer marble collar so rotating a tile in `#wow-3d-popup` or tilting the 3D camera reveals a physical 3D excavated cavity.
  - Added Headless Blender 5.0.1 3D Carved Intaglio Showcase (`scripts/blender/build_carved_intaglio_showcase.py`) exporting `public/models/tile_carved_intaglio_showcase.glb` (`120×160` displaced BMesh for `dots_2`, `dots_4`, `char_8`) and rendering `public/renders/cycles/cycles_cam5_carved_intaglio.png`.
- **🎯 Larger `2/4` Circles (`dots_2`, `dots_4`) & `+10%` Larger Chinese Calligraphy (Minimal Empty White Space)**:
  - Enlarged `dots_2` (`二筒`) radius from `95px` to `148px` (`+56%`) and `dots_4` (`四筒`) radius from `82px` to `124px` (`+51%`) with 12-petal carved coin rosettes, plus fuller `dots_1..9` & `bamboo_5..9` stalks and `+10%` larger Chinese calligraphy (`char_1..9`, `wind_*`, `dragon_*`).
- **🚀 GitHub Pages Live Deployment (`https://palladius.github.io/family-mahjong-3d/`)**:
  - Added `vite.config.js` (`base: "./"`), relative asset paths across `index.html`, `src/main.js`, and `public/progress.html`, `.github/workflows/deploy-ghp.yml`, and direct `gh-pages` branch publishing.

## [1.3.0] - 2026-10-16
### Added
- **Yellow-Purple Selection Double Border (`bordino giallo-viola`) & `550ms` Pair Visibility Pause**:
  - Selecting the 1st tile highlights it with a vivid 3D **Yellow-Purple (`#ffe600` + `#a832ff`) border**; selecting the 2nd matching tile highlights the 2nd tile with a Yellow-Purple border as well, displays both matched tiles side-by-side in the HUD, and waits **`550ms` (`mezzo secondo`)** so the player clearly sees the pair before removing them (in both manual play and Demo Auto-Play).
- **Dedicated `2D` Anti-Motion-Sickness Top-Down Mode & Visual SVG Icon Dock**:
  - Added a flat overhead **`2D`** camera preset (`Y=24.5, FOV=26°` with 3D orbit rotation locked) accessible via the bottom dock **`2D`** icon, the top HUD **`📐 Passa a 2D`** button, or `?2d=1`.
  - Redesigned the bottom camera dock (`#camera-bar`) with custom stylized SVG icons and concise labels (`2D`, `3D`, `Zen`, `Basso`, `Macro`, `360°`).
- **WOW Effect: Top Rotating 3D Tile GLB Inspector (`#wow-3d-popup`) & Bottom `"💡 Did you know?"` Cultural/Family Lore**:
  - Clicking any tile renders a live 360°-spinning 3D clone of that tile (or matched pair) in `#wow-3d-popup` (top-left) and displays tailored `"💡 Did you know?"` Chinese numerology, suit history, and Carlesso family lore in `#selection-card` (bottom).
- **Automated 3D Visibility, Coplanar Orientation & Frustum Unit Test Suite (`scripts/test_3d_visibility.mjs`)**:
  - Added `scripts/test_3d_visibility.mjs` to `just test`, verifying coplanarity of the table/floor with the 144 tiles, `0 / 4,320` occluded camera-to-tile sightlines across 30 viewpoints, and `144 / 144` full-board viewport framing in `2d`, `topdown`, and `hero` presets.

### Fixed
- **Fixed Orthogonal Table/Floor Wall Bug (`src/main.js`)**:
  - Removed the erroneous `this.templeEnv.rotation.x = -Math.PI / 2` transform on `temple_environment.glb` (which was rotating the already-`+Y Up` glTF horizontal table and floor by 90° into a vertical wall slicing through the middle of the Mahjong board).

## [1.2.0] - 2026-10-16
### Added
- **NB21 (`gemini-3.1-flash-image-preview`) Remasters for `S1` (Papà Riccardo) & `S2` (Mamma Kate 2016)**:
  - Regenerated `S1` (`coupled_A1.png`, `public/portraits/quartet_S1_papa_riccardo.png`) using NB21 conditioned strictly on solo face crops of Riccardo (zero glasses, 10/10 Italian facial likeness).
  - Regenerated `S2` (`coupled_A2.png`, `public/portraits/quartet_S2_mamma_kate2016.png`) using NB21 conditioned on solo face crops from `kate2016/cleaned/` (young 33yo radiant dimpled smile, *acqua e sapone* fresh glowing skin, ash-blonde waves, royal purple & emerald silk).
- **3 Comedic Chinese Imperial Bamboo, Jade & 24k Gold Suit Tiles (`bamboo_2..4`)**:
  - `bamboo_2.png` (`2索`): **Chinese Bamboo & Gold Hot Wheels Muscle Supercar** 🏎️🎋
  - `bamboo_3.png` (`3索`): **Sirio il Dragone (Saint Seiya Dragon Shiryu) & Towering Chinese Shenlong** 🐉🛡️
  - `bamboo_4.png` (`4索`): **Ale's Imperial Rubies, Diamonds & Emeralds in Bamboo & Gold Filigree** 💎👑
- **A/B Testing Toggle: `Classica Ovale` vs. `🌙 Modalità Onirica (Less is More)`**:
  - Generated 50 ethereal watercolor/whisper-fade tile textures (`public/textures/tiles_onirica/*.png`) on 75%+ pure untouched White Imperial Marble (`#FCF9F2`) with zero solid oval border.
  - Added live HUD toggle button (`#btn-onirica-toggle` and `?onirica=1` URL support) in `index.html` and `src/main.js`.

### Changed
- **Balanced Family Tile Cardinality (`~18%`)**:
  - Reduced coupled family tile density on the Solitaire pyramid (both in Three.js `generateDeckPairs` and Blender Cycles `render_cycles_ground_truth_suite`) so the board breathes with authentic Mahjong calligraphy and the comedic `bamboo_1..4` suit tiles.

## [1.1.0] - 2026-10-16
### Added
- **Cardinality-4 Family & Companion Quartets (`Any 2 Match`)**:
  - **Quartet 1 — Carlesso Family Seasons (`S1..S4`, `春 夏 秋 冬`, `matchGroup: "quartet_family_seasons"`)**: Solo tiles of **Papà Riccardo** (`S1`), **Mamma Kate** (`S2`, *acqua e sapone* in royal purple & emerald silk), **Alessandro** (`S3`), and **Sebastian** (`S4`) sliced from shared Nano Banana Pro 2D scenes. Any 2 of the 4 match in Mahjong Solitaire (`Papà + Mamma` & `Ale + Sebi`, OR `Mamma + Ale` & `Sebi + Papà`, etc.).
  - **Quartet 2 — Magical Companions Flowers (`M1..M4`, `梅 蘭 菊 竹`, `matchGroup: "quartet_magic_flowers"`)**: **Ale & Ghigna 🐹** (`M1`), **Sebi & Pupurabbu 👾** (`M2`), **Solo Ghigna 🐹** (`M3`), and **Solo Pupurabbu 👾** (`M4`). Any 2 of the 4 match!
- **Cardinality-2 Diptyque Split-Pairs (`E1↔E2 .. H1↔H2`)**:
  - Generated 4 shared 2D scenes of **Ale & Sebi together** via Nano Banana Pro (`gemini-3-pro-image-preview`) and sliced them down the middle (`Left = Solo Ale` ↔ `Right = Solo Sebi`) for **Great Wall Explorers** (`E1↔E2`), **Cantonese Fried Rice** (`F1↔F2`), **Shaolin Kung Fu** (`G1↔G2`), and **Chengdu Giant Pandas** (`H1↔H2`).
- **Remastered 1-Bamboo Imperial Sparrow (`bamboo_1.png`)**:
  - Replaced procedural vector sparrow with an ornate carved Imperial Jade, Crimson & Gold Sparrow (`鳥`) inside a Gold-Rimmed Oval Cameo (`public/portraits/bamboo_1_sparrow_emblem.png`).
- **Reverse-Peel Solvable Board Generator & Live Selection Preview**:
  - Implemented `assignSolvableDeckToSlots` in `src/main.js` guaranteeing 100% solvable boards across all 4 difficulty tracks, plus a live 2D tile artwork thumbnail (`#sel-thumb`) in the Selection Card.
- **10-Round 3-Critic Iterative QA Loop & Choreographic Gallery**:
  - Documented all 10 QA rounds across Critic 1 (Topology & Manifold), Critic 2 (60 FPS WebGL Performance & Solvable Gameplay), and Critic 3 (Cycles vs. WebGL Visual & Character Consistency Fidelity) in `public/progress.html`, `docs/LOG.md`, and `artistic_director_gallery.md`.

### Fixed
- **Zero Raw Reference Photos on Tiles**: Removed raw Cape Town selfie (`coupled_H1.png`) and ensured 100% of tiles use pure 2D Nano Banana Pro generated artwork conditioned on GIC character references (`>= 9.8/10` Character Consistency).
- **Corner Glyph Occlusion Fixed**: Repositioned `Alphabet_Glyph_Mesh` and `Alphabet_Glyph_Bone` from top-left `(-0.36, 0.36)` to top-center `(0.0, TILE_H * 0.422)` in both Headless Blender 5.0.1 (`scripts/blender/build_all_assets.py`) and Three.js (`src/main.js`) so top-left/top-right corner calligraphy is 100% unobstructed.

## [1.0.0] - 2026-10-15
- Initial playable 3D Mahjong Solitaire release with Headless Blender 5.0.1 GLB assets, 4 offline Cycles ground-truth renders, and Three.js WebGL courtyard/table switchable environment.

## [0.1.0] - 2026-10-15
- Initial project scaffolding in `/usr/local/google/home/ricc/.gemini/jetski/scratch/family-mahjong-3d`.
