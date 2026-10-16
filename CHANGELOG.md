# Changelog - Carlesso Family Mahjong 3D 🀄🐉

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
