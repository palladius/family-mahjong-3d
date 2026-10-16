# Changelog - Carlesso Family Mahjong 3D 🀄🐉

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
