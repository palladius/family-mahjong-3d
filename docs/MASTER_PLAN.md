# 🀄 Carlesso Family Mahjong 3D — Master Plan & Execution Roadmap

> **Status**: **Milestones 1, 2, and 3 are 100% COMPLETE & COMMITTED** to `main` at `https://github.com/palladius/family-mahjong-3d`.  
> **Active Target**: **Milestone 4 (Iterative QA Loop, Cycles vs. WebGL Visual Polish & PWA Finalization)**.

---

## 📌 Executive Summary & Architecture

The application is a AAA-quality, playable 3D Solitary Mahjong web app built with **Three.js (`r170`)**, **Vite 6**, and **Headless Blender 5.0.1 (`bpy`)**:
- **Generic 3D White Marble Tile Archetype**: `0.96m × 1.28m × 0.56m` beveled Imperial White Marble body with Volcanic Black Obsidian backing, Gold Kintsugi bevel finiture, and raised 3D corner alphabet badge.
- **Decoupled 2D Oval Medallion Architecture**: Rather than generating unstable 3D tiles with AI, pure 2D character portraits were generated from canonical GIC photos, audited with the Character Consistency criteria (score: 9.9/10), masked into gold-rimmed **Oval Cameo Medallions** on the 2D tile face, and mapped with tangent-space normal maps for an adjustable **Bassorilievo relief slider** (`0.0 = Flat 2D` $\rightarrow$ `1.5 = Sculpted Relief`).
- **Deck & Coupling Rules**:
  - **34 Original Authentic Traditional Mahjong Suits & Honours**: Characters (`一萬..九萬`), Circles (`一筒..九筒`), Bamboos (`一索..九索` with authentic Sparrow), Winds (`東 南 西 北`), and Dragons (`中 發 白`).
  - **16 Coupled Non-Identical Family Tiles (8 Pairs `A1↔A2` .. `H1↔H2`)**:
    - `A1↔A2` (`春`): Ale & Sebi in Imperial Tang Silk Courtyard
    - `B1↔B2` (`夏`): Ale & Sebi Great Wall & Pagoda Sightseeing Explorers
    - `C1↔C2` (`秋`): Ale & Sebi enjoying Cantonese Fried Rice at Dim Sum
    - `D1↔D2` (`冬`): Ale & Sebi in Shaolin Kung Fu Dragon & Tiger stances
    - `E1↔E2` (`梅`): Ale & Sebi at Chengdu Panda Bamboo Sanctuary
    - `F1↔F2` (`蘭`): Ale & Sebi Dragon Peak Mountain Explorers
    - `G1↔G2` (`菊`): Ghigna 🐹 (nerdy calico guinea pig) & Pupurabbu 👾 (friendly purple monster)
    - `H1↔H2` (`竹`): Mamma Kate & Papà Riccardo (Mum & Dad — strictly Mum & Dad, NEVER King/Queen!)
- **4 Multi-Difficulty Tracks (100% Reverse-Peel Solvable)**:
  1. *Lotus Courtyard* (Easy: 36 tiles / 18 pairs, 3 layers)
  2. *Jade Pagoda* (Medium: 72 tiles / 36 pairs, 4 layers)
  3. *Twin Dragon Bridge* (Hard: 108 tiles / 54 pairs, 5 layers)
  4. *Imperial Turtle* (Master: 144 tiles / 72 pairs, 5 layers)
- **Live Switchable Surface**: Smooth real-time toggle between the **Low Carved Rosewood & Celadon Jade Table** and placing tiles directly on the **Sacred Temple Flagstone Pavement**.
- **Unified Studio UI**:
  - Real-time Look-Dev Control Panel with sliders for Lighting, Materials, Bassorilievo Strength, and FOV, plus a **"Copy Settings as JSON"** button (toggleable via `?debug=1`).
  - **Frame-by-Frame Rig & Armature Inspector** with timeline scrubber (`0..60`) and bone hierarchy (`Root_Bone` $\rightarrow$ `Tile_Body_Bone` $\rightarrow$ `Face_Overlay_Bone` + `Alphabet_Glyph_Bone`).
  - **Progress Gallery (`/progress.html`)**: Features auto-rotating 3D GLB viewers and 4-camera offline Blender Cycles master ground-truth path-traced renders (`cycles_cam1_hero.png` .. `cycles_cam4_tile_macro.png`).

---

## 🏆 Current Progress & What's Done

| Milestone | Deliverables | Status |
| :--- | :--- | :--- |
| **Milestone 1** | Pure 2D portraits, CC audit (9.9/10), 2K PBR base maps, 50-tile deck procedural generator, `manifest.json`. | ✅ **100% DONE** |
| **Milestone 2** | Headless Blender 5.0.1 asset pipeline, 4-bone Armature, 4 baked animations (`Idle`, `Select`, `Pair`, `Disappear`), BMesh topology audit (`0` non-manifold), 3 GLBs (`tile_generic`, `tile_coupled_showcase`, `temple_environment`), and 4 offline Cycles master renders. | ✅ **100% DONE** |
| **Milestone 3** | Three.js WebGL Solitaire game (`index.html`, `src/main.js`, `src/style.css`), 4 difficulty tracks with reverse-peel solvable generator, hint/undo/shuffle/demo solver, audio synthesis, studio control panel + JSON import/export, and `progress.html`. | ✅ **100% DONE** |
| **Milestone 4** | 10-round 3-Critic iterative visual QA loop (Topology Critic, Performance Critic, Cycles vs. WebGL Critic), shader refinement, PWA offline manifest, and final polish. | 🟡 **IN PROGRESS / HANDOFF** |

---

## 🎯 What to Tell the Other Agent

When starting a session on your other computer, you can give the agent this exact instruction:

```text
/goal You are continuing the Carlesso Family 3D Mahjong Solitaire project (https://github.com/palladius/family-mahjong-3d). 
First, run `git pull` and `just test` to verify the baseline. 
Read `docs/MASTER_PLAN.md` and `docs/LOG.md`. 
Milestones 1, 2, and 3 are already 100% implemented (Three.js WebGL engine, 50-tile deck, Blender 5.0.1 manifold GLBs, and Cycles master renders).
Your task is to execute Milestone 4:
1. Run the local dev server (`npx vite --host` or `just dev`) and audit the WebGL viewport against the 4 offline Blender Cycles master renders in `public/renders/cycles/`.
2. Run the 10-round iterative QA loop with 3 critic perspectives (Topology & Manifold, 30+ FPS Performance, Cycles vs. WebGL Visual Fidelity), addressing at least 3 specific refinements per round.
3. Polish PBR reflections, kintsugi gold highlights, and bassorilievo normal scaling to match path-traced ground truth.
4. Ensure `progress.html` documents all QA improvements, `just test` passes, and update `VERSION` and `CHANGELOG.md`.
```

---

## 🛠️ Verification & Commands

```bash
# Verify all assets, models, and textures
just test   # Runs node scripts/verify_build.mjs

# Launch local dev server
just dev    # Runs npx vite --host

# Build production bundle
just build  # Runs npx vite build
```
