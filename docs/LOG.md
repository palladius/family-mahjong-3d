# 📓 Engineering & Agentic Loop Chronological Log (`docs/LOG.md`)

> **Purpose**: Complete chronological telemetry of prompts, timestamps, human-in-the-loop (`/grill-me`) decisions, subagent dispatches, Character Consistency audits, architectural pivots, and the 10-round 3-Critic QA loop for **RiccardinoCM26 🦖's upcoming technical article**.

---

## 📅 Session Timeline & Agentic Loops (2026-10-15)

### 1. `[2026-10-15T15:00:24+02:00]` — Initial Vision & AAA 3D Family Mahjong Prompt
- **User Prompt (`ricc`)**:
  > *"Build a AAA-quality, playable 3D Family Mahjonng web app from scratch using headless Blender and Three.js, featuring a multi-difficulty classic solitary game on a low pavement / or table inside a 3D Chinese temple setting and a unified UI for camera presets, concept comparisons, and frame-by-frame rig inspection. Coordinate specialized subagents to first generate and select winning reference concepts, then model, rig, and animate all marble / obsidian piece archetypes in parallel under a shared scale and manifold-geometry contract—complete with hierarchical overlays for alphabet baked 2K PBR maps, and custom idle, select, pair, and disaappear animations. Enforce quality through a 10-round iterative QA loop where three independent critic subagents audit 3D topology, 30 FPS runtime performance, and live browser screenshots against offline Cycles master renders, resolving at least three flaws per round until the real-time WebGL viewport matches the path-traced ground truth. To keep things interesting, use the colorful pieces which don’t have to match with Alessandro and Sebastian in similar coupled pose (eg two with Ale and Sebi are in a chinese cloth, another in which they’re dressed for site-seeing, another they are sitting at a restaurant eating cantonese rice). All themes are chinese (or asian if you finish the stereotypes) and usse Character consistency skill to check the quality of the images first, then the tiles. 1. After each milestone, save screenshots from our main camera angles into a `progress.html` gallery... If a GLB is there, make it auto-rotate for me in the attachment. 2. Build an on-screen control panel with sliders for the lighting, textures, and camera angles—plus a 'Copy Settings as JSON' button..."*
- **Agentic Discovery & Setup (`15:00:34` – `15:08:47`)**:
  - Loaded skills: `nano-banana-ricc`, `web-app-development`, `modern-web-guidance`, `run-workflow`, `swarm`, `carlesso-family`, `characterconsistency-family-images`, `audio-for-riccardos-kids`.
  - Located canonical Carlesso family reference photos in `~/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/` (`alessandro`, `sebastian`, `kate-best`, `riccardo`) and magical companions (`Ghigna` 🐹 & `Pupurabbu` 👾) in `carlesso-family/assets/compagni-magici/`.
  - Initialized workspace at `/usr/local/google/home/ricc/.gemini/jetski/scratch/family-mahjong-3d` and provisioned Python 3.11 + **Headless Blender 5.0.1 (`bpy==5.0.1`)**, `pillow`, `numpy`, `scipy`, `google-genai` via `uv`.

---

### 2. `[2026-10-15T15:13:01+02:00]` & `[15:13:30+02:00]` — `/grill-me` Interactive Interview & Corp Registry Bypass
- **User Prompts (`ricc`)**:
  > *"- you should use nano banana to render mocks of the track design, pass them back to me in a chat response or .md file, and wait for my approval*
  > *- you may use nano banana to render textures for specific items*
  > *- you should launch subagents to help with the project*
  > *- you should first make a very comprehensive plan with tasks and milestones*
  > */grill-me ask me questions, then when you're done, give me a plan that I can review and a /goal I can set to keep you running for a long time."*
  > *"use corp skill to bypass npm issues ;)"*
- **Agentic Action (`15:13:40` – `15:44:59`)**:
  - Read `google-computer` skill (`SKILL.md`) for Corp `uv` (`UV_INDEX_URL=https://pypi.org/simple`) and `npm` airlock handling; installed `three` (`r170`) and `vite` (`v6.0`) inside sandbox (`task-109`).
  - Triggered native `ask_question` GUI modal (`conductor_antigravity.md` rule) with 6 structured architectural & creative questions.
- **User `/grill-me` Decisions (`15:44:59`)**:
  1. **Surface**: Low carved rosewood & jade table resting on sacred temple stone pavement, with a control-panel toggle to switch between table and direct-on-pavement play.
  2. **Deck**: 8+ Ale & Sebi coupled Asian themes + family honour tiles + classic carved suits.
  3. **Materials**: *"sorry tiles should be ALL marble/.white, you can use obsidian or black for the finiture/rigs/sfumature if any, you decide."*
  4. **Alphabet Overlays**: Raised 3D corner glyph with shared Theme Letter + Pose Sub-index (`A1` matches `A2`, `B1` matches `B2`) plus matching border accent color.
  5. **Themes**: All 5 selected (Tang Silk, Sightseeing Explorers, Cantonese Rice Restaurant, Shaolin Kung Fu & Dragon Dance, Chengdu Panda Sanctuary & Terracotta Expedition with Ghigna & Pupurabbu cameos).
  6. **Tracks**: 4 Solitaire Track Layouts — *Easy (36-tile Lotus)*, *Medium (72-tile Pagoda)*, *Hard (108-tile Twin Dragon Bridge)*, and *Master (144-tile Imperial Turtle)* — all 100% reverse-peel solvable.

---

### 3. `[2026-10-15T15:58:52+02:00]` – `[16:08:04+02:00]` — Subagent Wave 1: Nano Banana Concept Mocks & Character Consistency Audit
- **Subagents Spawned**:
  - `cd5d0268-71bf-488e-8a5a-9f6bed00c8fc` (*Temple & Track Concept Mock Artist*): Generated `mock_01_temple_imperial_turtle_track_1792072751474.jpg`, `mock_02_four_difficulty_tracks_blueprint_1792072773073.jpg`, and `mock_05_pbr_textures_and_rig_sheet_1792073056928.jpg`.
  - `3cf77b55-0d2a-4613-98ab-cb089fc8f8d6` (*White Marble Coupled Tile Mock Artist*): Generated `mock_03_white_marble_obsidian_coupled_tiles_1792072926732.jpg` and photorealistic `mock_04_photoreal_cc_kungfu_panda_tiles_v2_1792073270073.jpg` using GIC reference photos of Ale & Sebi.
  - `b05db318-15ba-431f-bea1-b17a972ffa4f` (*Kung Fu & Panda Tile Mock Artist*): Generated `mock_04_kungfu_panda_ghigna_pupurabbu_tiles_1792072760802.jpg`.
- **Character Consistency Audit Catch**:
  - Auditing `mock_04` revealed that omitting reference photos or mixing cartoon prompts caused style drift (Pixar look + shaved Shaolin head on Sebi in `D1`, `SCORE: 6.2/10 'nun me somijjia'`), whereas passing the GIC reference photos restored photorealistic likeness (`v2`).

---

### 4. `[2026-10-15T16:10:17+02:00]` — Crucial Architectural Pivot: Decoupled Pure 2D Oval Portrait $\rightarrow$ Generic 3D Marble Tile
- **User Prompt (`ricc`)**:
  > *"PS I dont think that asking nano banana to put ale/seby in a mahjong is a good idea, I'd just create an image in a circle or rtectangle or maybe a nice OVAL , and then render the 2d in there. Maybe do a bassorilieevo, but start with 2d rendering on generic tile."*
- **Agentic Loop & Validation (`16:11:50` – `16:19:04`)**:
  - Instructed subagent `3cf77b55-0d2a-4613-98ab-cb089fc8f8d6` to generate a **pure 2D full-bleed photograph** (`portrait_cantonese_rice_pure2d_1792073558345.jpg`) with zero mahjong tile framing.
  - **Result**: Facial likeness jumped to **99% (`9.9/10 "me somijja"`)**!
  - Built `scripts/demo_oval_generic_tile.py` in Headless Blender 5.0.1 (`bpy`) + PIL to mask the pure 2D portrait into a **Gold-Rimmed OVAL Cameo Medallion** (+ optional tangent-space normal map for **Bassorilievo relief**) and rendered `mock_06_generic_tile_with_2d_oval_and_bassorilievo.png` on a single Generic 3D White Marble + Black Obsidian Finiture tile.

---

### 5. `[2026-10-15T16:30:06+02:00]` & `[16:45:45+02:00]` — Plan Approval (`LGTM`), Inline Refinements & Article Logging Mandate
- **User Inline Comments on `FAMILY_MAHJONG_3D_MASTER_PLAN.md` + `LGTM`**:
  1. `"1/ LGTM"` & `"2. correct"` & `"Easy -> LGTM"` — Approved Temple table/pavement toggle, Generic 3D White Marble + Obsidian Finiture tile with 2D Oval Medallion + Bassorilievo slider, and 4 difficulty tracks.
  2. `"yes dontt copy from my chess game the king and queen we're just mum and dad"` — Enforced that Kate & Riccardo are strictly **Mamma Kate & Papà Riccardo (Mum & Dad)**, never King/Queen.
  3. `"i hope you use the ORIGINAL mahjong alphabvet/card art"` — Enforced authentic Traditional Chinese Mahjong card art (`一萬..九萬`, `一筒..九筒`, `一索..九索` with 1-Bamboo Sparrow, `東 南 西 北`, `中 發 白`, `春 夏 秋 冬`, `梅 蘭 菊 竹`).
  4. `"all previews are NOT visible"` — Noted that `.md` artifact carousels showed "Preview unavailable" in the client viewer; resolved by serving all images & interactive 3D GLBs directly in `progress.html` and the main web app + standard PNG links.
- **User Prompt (`16:45:45+02:00`)**:
  > *"in everything you do keep a docs/LOG.md which tracks my requests, tyhe timestamps, the agentic loops i ask and you do, ... for a future article. Add to a GEMINI.md in the folder where u work!"*
- **Subagent Wave 2 (`16:36:52` – `16:45:04`)**:
  - `3cf77b55-0d2a-4613-98ab-cb089fc8f8d6` generated pure 2D full-bleed portraits `pure2d_a1_tang_silk_1792075071280.jpg` (Tang Silk, `9.9/10` CC) and `pure2d_b1_sightseeing_1792075122386.jpg` (Great Wall Sightseeing, `9.9/10` CC) before the image cluster reported `500 memory-protection-90`.
  - Built `scripts/build_all_tile_textures.py` to generate all 2K PBR base maps, all 34 Original Mahjong suit/honour textures, and all 16 Coupled Family Oval Medallion textures + Bassorilievo normal maps.

### 6. `[2026-10-15T17:19:22+02:00]` — Repository Registration, GitHub Link & Full Playable Release
- **User Prompt**:
  > *"i still dont see anytthing"*
  > *"where's the code and GH repo?!?"*
  > *"add it to palladius repos-ricc"*
- **Actions Executed**:
  1. **Registered in `repos-ricc`**: Added `gh.repo "family-mahjong-3d", desc: "added on day 2026-10-15 on computer derek. Carlesso Family 3D Mahjong Solitaire 🀄 (Three.js + Blender 5.0.1 PWA)", size: :medium, symlinks: ["carmahjong3d"]` directly into `/usr/local/google/home/ricc/git/gic/bin/repos-ricc`.
  2. **Created GitHub Remote Repository**: Created `https://github.com/palladius/family-mahjong-3d` via `gh repo create palladius/family-mahjong-3d --public`.
  3. **Local Git Workspace Established**: Initialized `/usr/local/google/home/ricc/git/family-mahjong-3d` with symlink `/usr/local/google/home/ricc/git/carmahjong3d -> family-mahjong-3d` and configured remote `git@github.com:palladius/family-mahjong-3d.git`.
  4. **Headless Blender 5.0.1 Asset, Rigging & Cycles Pipeline Completed**:
     - Exported `tile_generic_white_marble_obsidian.glb` (1.4 MB) with 4-bone hierarchy (`Root_Bone` → `Tile_Body_Bone` → `Face_Overlay_Bone` + `Alphabet_Glyph_Bone`) and 4 baked animation actions (`Idle`, `Select`, `Pair`, `Disappear`).
     - Exported `tile_coupled_showcase.glb` (7.4 MB) and `temple_environment.glb` (268 KB).
     - Automated BMesh Topology Audit verified 0 non-manifold edges, 0 degenerate faces, and complete UV unwraps (`allManifoldPass=True`).
     - Rendered 4 offline Blender Cycles master ground-truth path-traced images (`cycles_cam1_hero.png`, `cycles_cam2_topdown.png`, `cycles_cam3_low_pavement.png`, `cycles_cam4_tile_macro.png`).
  5. **Playable Three.js WebGL Solitaire Application**:
     - 4 multi-difficulty tracks (Lotus Courtyard 36, Jade Pagoda 72, Twin Dragon Bridge 108, Imperial Turtle 144) with 100% Reverse-Peel Solvable layout generator.
     - Switchable surface: Low Carved Rosewood & Jade Table ↔ Sacred Stone Flagstone Pavement.
     - Interactive Look-Dev Studio with sliders for lighting, materials, and Bassorilievo normal relief + "Copy Settings as JSON" exporter.
     - Frame-by-Frame Rig Inspector with timeline scrubber (0..60).
     - Progress gallery (`public/progress.html`) with auto-rotating 3D GLB viewers.

