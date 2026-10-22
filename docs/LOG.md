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

---

## 📅 Session Timeline & Agentic Loops (2026-10-16 — Cross-Machine Handoff `derek` $\rightarrow$ macOS)

### 7. `[2026-10-16T11:05:54+02:00]` – `[11:35:58+02:00]` — Cross-Machine `git pull`, `tmp/GOAL.md` Handoff & Diptyque Split-Pair Mahjong Rule
- **User Prompts (`ricc`)**:
  > *"guarda codice qui, c'e' il Master Plan?"*
  > *"(iniziato progetto su altro computer)"*
  > *"/plan Esegui il master plan, fammi le necessarie domande e quando hai finito dammi un /goal da darti per finire il lavoro tuto da solo! Si ok fare npm install e just dev, perche no! E tienimi aggiornato sui tuoi asset graifci cosi mentre lavori posso tenerli osservati e criticarli. Considerami il revisore artistico."*
  > *"fai git pull"* / *"hai un GOAL.md ?"*
  > *"Allora, c'è un problema fondamentale. Intanto non puoi usare la mia foto originale di Cape Town, devi crearle tu. Non voglio che usi Ale e Sebi insieme, ma voglio che crei un'immagine di loro due insieme e poi spezzi e prendi solo Ale e solo Sebi, e quelli sono i due pezzi di mahjong che devono essere messi insieme. Un po' come quando hai le cose floreali, hai estate, autunno, inverno e primavera e ciascuna di esse può essere presente indipendentemente, mi spiego? Questa è l'idea. Con cardinalità 2 o con cardinalità 4. Questo è come io capisco il mahjong: tutti i pezzi sono da prendere a coppie deterministiche, tranne alcuni che hanno delle immagini diverse e tu puoi scegliere quale prendere. Ecco, io volevo un Ale e un Sebi da prendere insieme."*
  > *"Una volta che hai capito, genera queste cose con Ale, Ale con ghigna, Sebi col pupurabbu, oppure Ale e Sebi separati, oppure papà, mamma, Ale e Sebi come quattro pezzi. Sarebbero bellissimi quattro pezzi da scegliere come vuoi. Una volta puoi prendere, non so, puoi sia prendere mamma e papà oppure puoi prendere mamma e Ale, e poi gli altri due pezzi da prendere sono Sebi e papà. Insomma, usa la famiglia in maniera intelligente con questi pezzi."*
  > *"Come ti dicevo ieri, assicurati di mantenere un artefatto antigravity che cresce con le immagini, i video, le animazioni, i GLB e tutte le cose che crei, in modo che io, come direttore coreografico, possa entrare nel merito mentre tu lavori indisturbato per 8 ore di fila. Questa è l'idea."*
- **Agentic Discovery & Handoff Sync (`11:06:03` – `11:42:30`)**:
  - Executed `git pull origin main`, pulling commits `c86782b` ([`docs/MASTER_PLAN.md`](MASTER_PLAN.md)) and `78d9365` ([`tmp/GOAL.md`](../tmp/GOAL.md)) pushed from `derek`.
  - Installed npm dependencies (`npm install` + `esbuild` macOS binary) and started Vite dev server on `http://localhost:5173/` (`log/vite-dev.log`).
  - **Fundamental Creative & Game-Design Correction (Diptyque Split-Pair & Family Quartet Mahjong Rule)**:
    1. **NEVER use raw original reference photos directly on tiles** (such as the Cape Town selfie in `F1` or the indoor split-screens in `F2/H1/H2`). Reference photos in GIC (`alessandro`, `sebastian`, `kate-best`, `riccardo`) are strictly **input references** for Nano Banana Character Consistency generation.
    2. **Cardinality 2 — Diptyque Split-Pairs (`X1 = Solo Ale` ↔ `X2 = Solo Sebi`, or `Ale+Ghigna` ↔ `Sebi+Pupurabbu`)**:
       - Generate **ONE shared 2D scene of the two characters together** (e.g. Ale on the left, Sebi on the right in Tang Silk, Great Wall, Cantonese Rice, Shaolin Kung Fu, Chengdu Pandas) and **split/crop that shared scene into TWO separate solo Mahjong tiles**:
         - Tile `X1` = **Solo Ale** (left half of the shared scene)
         - Tile `X2` = **Solo Sebi** (right half of the shared scene)
       - Matching `X1` with `X2` in Mahjong Solitaire reunites the two halves of the scene!
    3. **Cardinality 4 — Family & Companion Quartets (`Papà + Mamma + Ale + Sebi` as 4 Seasons `春 夏 秋 冬`, and `Ale + Ghigna + Sebi + Pupurabbu` as 4 Flowers `梅 蘭 菊 竹`)**:
       - Just like Traditional Mahjong Seasons/Flowers, the 4 tiles of the Family Quartet share the same `matchGroup` (`quartet_family_seasons`).
       - The player can freely pair **ANY two** of the four tiles (e.g., **Mamma Kate + Papà Riccardo** and then **Ale + Sebi**, OR **Mamma Kate + Ale** leaving **Sebi + Papà Riccardo**!).
    4. **Living Antigravity Choreographic Director Artifact (`artistic_director_gallery.md`)**:
       - Maintain a continuously growing Antigravity artifact in `/Users/ricc/.gemini/antigravity/brain/9efaaa30-d5fa-49dc-b7c4-7292c03768b3/artistic_director_gallery.md` embedding every generated 2D portrait, Diptyque split-pair, Quartet tile, 3D GLB, animation strip, and Cycles/WebGL QA comparison as work progresses autonomously.

### 8. `[2026-10-16T11:42:35+02:00]` – `[12:35:00+02:00]` — Autonomous `/goal` Execution: Nano Banana Pro (`gemini-3-pro-image-preview`), Diptyque Split-Pairs, Cardinality-4 Quartets & 10-Round 3-Critic QA Loop
- **User Prompt (`/goal`)**:
  > *"/goal You are continuing the Carlesso Family 3D Mahjong Solitaire project (https://github.com/palladius/family-mahjong-3d) on macOS. Execute the approved Master Plan & Milestone 4: 1. Never use raw reference photos directly on tiles... 2. Upgrade `bamboo_1.png`... 3. Fix the 3D `Alphabet_Glyph_Mesh` corner occlusion... 4. Continuously update the living Antigravity artifact `artistic_director_gallery.md` AND `public/progress.html`... 5. Run the 10-round iterative QA loop with 3 critic perspectives... 6. Verify `just test` and `npm run build` pass, update `VERSION` and `CHANGELOG.md`, and finally run `git rm tmp/GOAL.md` and commit & push!"*
- **Agentic Execution & Subagent / Script Orchestration Details**:
  1. **Character Consistency Generation via Nano Banana Pro (`scripts/generate_nano_banana_portraits.py`)**:
     - Discovered that the image-generator tool subagent returned `HTTP 503 SERVICE_UNAVAILABLE` on the default preview endpoint, so we built [`scripts/generate_nano_banana_portraits.py`](../scripts/generate_nano_banana_portraits.py) using the `google-genai` SDK (`gemini-3-pro-image-preview`) conditioned directly on the GIC reference photos in `~/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/` (`riccardo`, `kate-best`, `alessandro`, `sebastian`, `ghigna`, `pupurabbu`).
     - Generated **11 pure 2D master portraits and shared Diptyque scenes** in `public/portraits/` (0 raw reference photos on any tile!):
       - `diptyque_S1_S2_papa_mamma.png` (`9.9/10` CC): Shared Imperial Bridge scene of **Papà Riccardo** (Left) & **Mamma Kate** (Right, *acqua e sapone*, royal purple & emerald silk).
       - `diptyque_S3_S4_ale_sebi_tang.png` (`9.9/10` CC): Shared Tang Dynasty silk scene of **Ale** (Left) & **Sebi** (Right).
       - `quartet_M1_ale_ghigna.png` (`9.8/10` CC): **Ale & Ghigna 🐹** (tricolour calico guinea pig with round black glasses & red bow tie).
       - `quartet_M2_sebi_pupurabbu.png` (`9.8/10` CC): **Sebi & Pupurabbu 👾** (giant friendly fluffy purple monster with rainbow propeller beanie).
       - `quartet_M3_solo_ghigna.png` (`10.0/10` CC): **Solo Ghigna 🐹** in Mandarin scholar vest with jade abacus.
       - `quartet_M4_solo_pupurabbu.png` (`10.0/10` CC): **Solo Pupurabbu 👾** holding a glowing crimson silk lantern.
       - `diptyque_A_great_wall.png` (`9.9/10` CC): Shared Great Wall scene sliced into `E1` (Solo Ale) ↔ `E2` (Solo Sebi).
       - `diptyque_B_cantonese_rice.png` (`9.9/10` CC): Shared Cantonese Fried Rice banquet scene sliced into `F1` (Solo Ale) ↔ `F2` (Solo Sebi).
       - `diptyque_C_shaolin_kungfu.png` (`9.9/10` CC): Shared Shaolin Kung Fu scene sliced into `G1` (Solo Ale Dragon) ↔ `G2` (Solo Sebi Tiger).
       - `diptyque_D_chengdu_pandas.png` (`9.9/10` CC): Shared Chengdu Giant Pandas scene sliced into `H1` (Solo Ale) ↔ `H2` (Solo Sebi).
       - `bamboo_1_sparrow_emblem.png` (`10.0/10` CC): Ornate carved Imperial Jade, Crimson & Gold Sparrow (`鳥`) emblem for `bamboo_1.png`.
  2. **50-Tile Gold-Rimmed Oval Cameo & Normal Map Pipeline (`scripts/build_all_tile_textures.py`)**:
     - Added custom aspect-ratio-matched crop boxes (`crop_box = (x0, y0, x1, y1)`) for every Diptyque half and Quartet portrait so every character's head, hair, and hat (including Pupurabbu's propeller cap and Sebi's hair) are framed with generous headroom inside the Gold-Rimmed Oval Cameo.
     - Rebuilt all 50 tile diffuse textures (`public/textures/tiles/*.png`), 50 Sobel Bassorilievo normal maps (`public/textures/tiles_normal/*_normal.png`), 2K PBR marble/obsidian/jade/stone maps (`public/textures/pbr/*.png`), and `public/textures/manifest.json` (`tileCount: 50`, `suitsCount: 34`, `coupledCount: 16`, `quartetCount: 8`, `diptyquePairCount: 8`).
  3. **Headless Blender 5.0.1 Asset & Cycles Rebuild (`scripts/blender/build_all_assets.py`)**:
     - Repositioned `Alphabet_Glyph_Mesh` and `Alphabet_Glyph_Bone` from top-left `(-0.36, 0.36)` to a sleek top-center golden crown inlay bar `(0.0, TILE_H * 0.422)` so top-left (`S1..S4`, `M1..M4`, `E1..H2`, `1..9`) and top-right (`春 夏 秋 冬`, `梅 蘭 菊 竹`) corner glyphs are 100% unobstructed.
     - Updated portable `PROJECT_DIR = Path(__file__).resolve().parents[2]` and placed Quartet 1 (`S1..S4`) and Quartet 2 (`M1..M4`) on the front row of the Cycles pyramid.
     - Re-exported `tile_generic_white_marble_obsidian.glb` (`3.0 MB`), `tile_coupled_showcase.glb` (`9.7 MB`), `temple_environment.glb` (`940 KB`), `topology_audit.json` (`allManifoldPass: true`, `0` non-manifold edges, `0` degenerate faces), and all 4 offline Cycles master renders (`cycles_cam1_hero.png .. cycles_cam4_tile_macro.png`).
  4. **Three.js WebGL Engine, Solvable Board Generator & Look-Dev Studio (`src/main.js`, `index.html`)**:
     - Implemented Cardinality-4 Quartet dealing (`S1..S4` and `M1..M4` all dealt onto the board; any 2 of the 4 match via `t1.matchGroup === t2.matchGroup`).
     - Implemented `assignSolvableDeckToSlots(slots, deckPairs)` using reverse-peel simulation so every dealt board is guaranteed solvable.
     - Shared tile geometries and materials via `initSharedTileResources()` (`60 FPS` steady), added `kintsugiMesh` golden waist seam and top-center `badgeMesh`, added `#sel-thumb` live 2D tile preview in the Selection Card, and wired all Studio Look-Dev sliders and Rig Inspector scrubber controls.
  5. **10-Round 3-Critic Iterative QA Loop Completed**:
     - Documented all 10 QA rounds across Critic 1 (Topology & Manifold), Critic 2 (60 FPS WebGL Performance & Solvable Gameplay), and Critic 3 (Cycles vs. WebGL Visual & Character Consistency Fidelity) in [`public/progress.html`](../public/progress.html) and `artistic_director_gallery.md`.
---

## [2026-10-16T13:23:00+02:00] Milestone 5 — Artistic Director Review (`v1.2.0`): NB21 `S1/S2` Remasters (`kate2016` & Solo Riccardo), Comedic Chinese Bamboo & 24k Gold Suit Tiles (`bamboo_2..4`), Modalità Onirica A/B Toggle ("Less is More"), & Balanced Family Pyramid

### 1. Verbatim User Feedback & Inline Artifact Comments
> **User Request**: `alcuni commenti - ottimo lavoro. quando hai un gioco giocabili in localhost fai partire il browser - no pressure, continua con la parte creativa!`
>
> **Inline Comment 1 (`artistic_director_gallery.md`, `S1..S4`)**: `i bimbi sono perfetti purtroppo papa' e mamma no. Usa un modello NB21 e character consistency per noi 2, e per kate usa le foto 2016, e' brutta e vecchia. io non somiglio. Rifai papa e mamma il resto perfetto!`
> **Inline Comment 2 (`artistic_director_gallery.md`, `M1..M4`)**: `bellissimi tutti e 4. WOW`
> **Inline Comment 3 (`artistic_director_gallery.md`, `E1..H2`)**: `bellissimi tutti e 4`
> **Inline Comment 4 (`artistic_director_gallery.md`, `bamboo_1.png`)**: `MArvelloud! I was wondering if we can add, in chiave comica. qualcosa che ad Ale e a Seby piacciono, ma versione stilizzata cinese: - una macchinina hot wheels, ma in chiave/stile cinese :) - un drago tipo cavalieri dello zodiaco, tipo Sirio il dragon, con il drago cinese davanti o che torreggia dietro. - Gemme, diamanti, rubini che piacciono ad ale tutto pero' in questo stile bambu con finiture oro... che non c'entra niente, quindi fa ridere.`
> **Inline Comment 5 (`artistic_director_gallery.md`, `cycles_cam2_topdown.png`)**: `la cardinalita della famiglia carlesso sembra un p[o' troppo altina qui! :) inoltre le foto ovali sembrano forse un po' troppo "solide" e appesantiscono il gioco. Facciamo un A/B testing. prova le foto di bimbi e altor, invece di metterle in ovale, di metterle come in una trasparenza con molto piu' bianco (sfondo - less is more) e farle trasparire quasi in acquerello , non proprio acquerello, ma in una sfumatura che non vedi bene se c'e' o non c'e'. TIENI la versione attuale ma metti TOGGLE per passare in modalita' "onirica" .`

### 2. Agentic Execution & Root-Cause Resolution
1. **Why `S1` (Papà Riccardo) previously had glasses & why `kate2016` fixed `S2` (`scripts/generate_nb21_updates.py`)**:
   - Root cause for `S1`: `riccardo2016/KR-e-0018.jpg` includes a second man on the left wearing black-rimmed glasses helping Riccardo adjust his collar. Cropping strictly to Riccardo's solo face + combining 5 clean solo portraits (`riccardo/ricc-google-switzerland.png`, `papino 2026-07-20.png`, `20240504_155052.jpg`, `PXL_20250406_151658760.PORTRAIT.jpg`) with **NB21 (`gemini-3.1-flash-image-preview`)** produced `public/portraits/quartet_S1_papa_riccardo.png` with **zero glasses** and **10.0/10** Italian facial likeness.
   - Root cause for `S2`: Switching exclusively to solo face crops from `~/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/kate2016/cleaned/` (`KR-o-0476.jpg`, `IMG_5542.jpg`, `KR-e-0136.jpg`, `IMG_20141004_145136.jpg`) with **NB21 (`gemini-3.1-flash-image-preview`)** produced `public/portraits/quartet_S2_mamma_kate2016.png` — young 33-year-old radiant 2016 Kate with *acqua e sapone* fresh glowing skin, dimpled smile, ash-blonde waves, and royal purple & emerald silk (`10.0/10` CC).
2. **3 New Comedic Chinese Imperial Bamboo, Jade & 24k Gold Suit Tiles (`bamboo_2..4`)**:
   - Generated via NB21 (`gemini-3.1-flash-image-preview`) and baked into both Classic Oval (`public/textures/tiles/`) and Onirica (`public/textures/tiles_onirica/`) suites:
     - `bamboo_2.png` (`2索`): **Chinese Bamboo & Gold Hot Wheels Muscle Supercar** (`public/portraits/bamboo_2_hotwheels_emblem.png`)
     - `bamboo_3.png` (`3索`): **Sirio il Dragone (Saint Seiya Dragon Shiryu) & Towering Chinese Shenlong** (`public/portraits/bamboo_3_shiryu_dragon_emblem.png`)
     - `bamboo_4.png` (`4索`): **Ale's Imperial Rubies, Diamonds & Emeralds in Bamboo & Gold Filigree** (`public/portraits/bamboo_4_gems_rubies_emblem.png`)
3. **A/B Toggle: `Classica Ovale` vs. `🌙 Modalità Onirica (Less is More)` (`scripts/build_all_tile_textures.py`, `src/main.js`, `index.html`)**:
   - Built all 50 Onirica textures (`public/textures/tiles_onirica/*.png`) on pure untouched Imperial White Marble (`#FCF9F2`) with 75%+ white breathing room and an organic cloud-feathered pastel/watercolor wash (`max_opacity=0.50` at the center fading smoothly to `0.0` with zero solid oval frame).
   - Wired `#btn-onirica-toggle` (`toggleOniricaMode()` in `src/main.js`, plus `?onirica=1` URL parameter) to hot-swap all 88/144 tiles on the live board between Classic Oval Cameo and Modalità Onirica.
4. **Lower Family Tile Cardinality (`~18%`) & Localhost Browser Launch**:
   - Capped coupled family pairs in `generateDeckPairs` (`src/main.js`) and `render_cycles_ground_truth_suite` (`scripts/blender/build_all_assets.py`) to `~18%` of the pyramid while prioritizing `bamboo_1..4` in the standard suit rotation.
   - Re-ran `uv run python scripts/blender/build_all_assets.py` (`allManifoldPass=True`) and launched `http://localhost:5173/` in the user's browser.
---

## [2026-10-16T13:47:00+02:00] Milestone 6 — UX & 3D Geometry Polish (`v1.3.0`): Coplanar XZ Table Fix, Automated 3D Line-of-Sight Unit Tests (`4,320` Raycasts), Yellow-Purple Selection Border + `550ms` Pair Pause, Visual SVG Icon Dock (`2D` Mode), & Rotating 3D Tile Inspector + `"Did you know?"` Lore

### 1. Verbatim User Feedback
> **User Request 1**: `Tipo, alcuni commenti: il gioco è bellissimo. Alcuni commenti: 1. Quando seleziona la prima cosa, deve esserci un bordino giallo-viola che seleziona il primo, e quando seleziona il secondo, un altro bordino giallo-viola e aspetti quel mezzo secondo per dare la visibilità del fatto che questa è una coppia prima poi di prenderli via. Questo vale per la demo e vale anche se gioco io. Numero uno. 2. C'è un problema 3D assurdo, non si riesce a vedere niente, lo schermo è tagliato a metà da uno schermo verticale che fa schifo. Questo va testato, nel senso, devi aggiungere uno unit test di qualche tipo che verifichi che da qualunque punto di vista io possa vedere sempre tutta la scacchiera, qualunque cosa succede. Cioè, se c'è una barriera, i miei occhi devono essere davanti a quella barriera, sennò game over. E poi ci deve essere anche un bottone per il 2D. Se vomito per troppo 3D, devo poter premere un bottone e andare in modalità più o meno 3D, cioè 2D vista dall'alto, va bene 3D, ma comunque vista dall'alto. Ok?`
> **User Request 2**: `e crea icone carine per i bottoni in basso affinche siano piu "visive" , meno parole piu' immagini/simboli per capire. tipo "2D" e un immagine stilizzata.`
> **User Request 3**: `credo il piano del gioco sia ortogonale al piano INTESO del gioco :) E magari un effetto wow - quando clicco su un TILE, metti in alto un GLB rotante del tile e in basso la sua descrizione "Did you know? <> symbolizes the number 4 in blah bah blah"`
> **User Request 4**: `bellissimo! Ma il piano di gioco ha ancora quell'ostacolo orribile`

### 2. Root-Cause Diagnosis & Engineering Resolution
1. **Why the Table & Floor Were Orthogonal to the Mahjong Board (`src/main.js` line 379)**:
   - Blender's glTF 2.0 exporter (`bpy.ops.export_scene.gltf`) **automatically converts** Blender's `+Z Up` into glTF/Three.js `+Y Up` (`XZ` horizontal plane).
   - `src/main.js` previously had `this.templeEnv.rotation.x = -Math.PI / 2;`, which rotated the already-horizontal `XZ` table and stone floor by `-90°` into the vertical `XY` plane — literally slicing the horizontal `XZ` Mahjong board in half with an orthogonal vertical wall!
   - Removing `this.templeEnv.rotation.x = -Math.PI / 2`, fixing `toggleSurface()` to animate `.position.y` instead of `.position.z`, moving the 4 temple pillars outward to `(±14.5, ±10.5)`, and adding `updateEnvironmentVisibility()` made the table, floor, and 144 tiles 100% coplanar in the horizontal `XZ` plane.
2. **Automated 3D Line-of-Sight, Coplanar Plane & Frustum Unit Test (`scripts/test_3d_visibility.mjs`)**:
   - Added `scripts/test_3d_visibility.mjs` (wired into `just test`) which parses `public/models/temple_environment.glb`, constructs the 3D scene and all 144 Master Imperial Turtle tiles in Node.js via `three`, and verifies:
     - `Temple_Stone_Pavement` and `Low_Rosewood_Jade_Table` are horizontal in the `XZ` plane (`Y <= -0.05m`) below all 144 tiles (`Y >= 0.28m`).
     - Across all 6 camera presets (`2d`, `hero`, `topdown`, `pavement`, `macro`, `orbit`) + 24 full-circle orbit viewpoints (`4,320` camera-to-tile raycasts), **0 rays** are occluded by any environment mesh.
     - In `2d` (`Y=24.5, FOV=26°`), `topdown` (`Y=15.6, FOV=40°`), and `hero` (`Y=8.8, Z=11.6, FOV=38°`), **144/144 tiles (`100%`)** project inside the camera viewport.
3. **Yellow-Purple Selection Border (`bordino giallo-viola`) + `550ms` Pair Visibility Pause (`src/main.js`)**:
   - Added a 3D hollow double-frame mesh (`selOuterPurple` `#a832ff` + `selInnerYellow` `#ffe600`) on top of every tile (`selectionBorder`), plus matching yellow-purple styling on `#selection-card`.
   - When the 1st tile is selected, its yellow-purple border lights up; when the 2nd matching tile is selected, the 2nd tile's yellow-purple border ALSO lights up, both tiles are shown side-by-side in `#selection-card`, and the game pauses for **`550ms` (`mezzo secondo`)** (in both manual play and Demo Auto-Play) before animating the pair away.
4. **Dedicated `2D` Anti-Motion-Sickness Mode + Visual SVG Icon Camera Dock (`index.html`, `src/style.css`)**:
   - Redesigned `#camera-bar` with custom stylized SVG icons and short visual labels: **`2D`** (flat overhead view with 3D rotation locked), **`3D`**, **`Zen`**, **`Basso`**, **`Macro`**, and **`360°`**, plus a top-bar **`📐 Passa a 2D / 2D Alto`** button (`?2d=1`).
5. **WOW Effect: Top Rotating 3D Tile GLB Inspector (`#wow-3d-popup`) + Bottom `"💡 Did you know?"` Cultural & Family Lore (`#sel-did-you-know`)**:
   - Clicking any tile (or matching a pair) opens `#wow-3d-popup` in the top-left corner with a live 60 FPS WebGL canvas (`#wow-3d-canvas`) spinning the 3D Mahjong tile(s) (showing the Imperial White Marble, Black Obsidian back, Gold Kintsugi seam, and portrait/suit face), while the bottom `#selection-card` displays `"💡 Did you know? ..."` lore for all 50 tiles.

---

## 2026-10-16T15:03:58+02:00 — Milestone 7 (`v1.4.0`): GitHub Pages Live Deployment + 3D "Incandescent Pen" Carved Intaglio (`buco bassorilievo`) + Enlarged `2/4` Circles & `+10%` Chinese Calligraphy

### 1. Verbatim User Request
> "molto bello!
> 1. push su GHP subito!
> 2. non mi convincono molto le immagine proprioe . C'e' troppo spazio bianco, correi che i 2/4 pallino fossero un opo' piu grandi, e anche i simboli cinesi un pelino (5-10% di piu). E sono molto 2d -> mi piaceerebbe provassi a fare un carvingi 3d molto figo, magaeri testandolo su 1-2 pezzi e poi a crescere, come se una penna incandescente avesse scavato il tile un pochttino, che si vede il buco bassorilievo ruotando. se no il 3d e' inutile!"

### 2. Agentic Loop & Engineering Execution
1. **Immediate GitHub Pages Deployment (`https://palladius.github.io/family-mahjong-3d/`)**:
   - Created `vite.config.js` (`base: "./"`), converted root-relative URLs to `./` across `index.html`, `src/main.js`, and `public/progress.html`, added `.github/workflows/deploy-ghp.yml`, and published `dist/` to the `gh-pages` branch.
2. **Enlarged Suit Motifs (`2/4` Pallini `+51–56%` & `+10%` Chinese Calligraphy)**:
   - Updated `scripts/build_all_tile_textures.py` so `dots_2` (`二筒`) radius grew from `95px` to `148px` (`+56%`) and `dots_4` (`四筒`) radius grew from `82px` to `124px` (`+51%`) with 12-petal carved coin rosettes, enlarged `dots_1..9` & `bamboo_5..9`, and increased Chinese calligraphy (`char_1..9`, `wind_*`, `dragon_*`) by `+10%` (`276px/298px` and `462px`).
3. **True 3D "Incandescent Pen" Carved Intaglio (`buco bassorilievo scavato`)**:
   - Built `apply_incandescent_pen_carving()` in `scripts/build_all_tile_textures.py` outputting 50 smooth chamfered 8-bit 3D vertex displacement maps (`public/textures/tiles_depth/{id}_depth.png`), high-slope normal maps (`strength=18.0`), and pyro-carved diffuse maps with scorched-umber inner groove wall shadows and molten-gold raised rims.
   - Upgraded `src/main.js` (`initSharedTileResources` & `createTileMesh`) with a subdivided `72×96` `PlaneGeometry` face mesh (`displacementMap` + `displacementScale` + `normalScale`), recessed cavity body, and outer marble collar so rotating any tile in `#wow-3d-popup` or tilting the 3D board camera reveals a physical 3D excavated cavity.
   - Created `scripts/blender/build_carved_intaglio_showcase.py` in Headless Blender 5.0.1 to export `public/models/tile_carved_intaglio_showcase.glb` (`120×160` displaced BMesh for `dots_2`, `dots_4`, `char_8`) and render the oblique raking-light Cycles ground truth `public/renders/cycles/cycles_cam5_carved_intaglio.png`.

---

## 2026-10-16T15:35:22+02:00 — Milestone 7b (`v1.4.1`): Visual Tile Matching Guide Modal (`Tasto H`) + Live `"🔗 VA CON:"` Partner Thumbnail Strip

### 1. Verbatim User Request
> "perfetto, metti anche istruzioni che spieghino quale tile va con quale tile, che mi confondo sempre con tasto "H""

### 2. Agentic Loop & Engineering Execution
1. **Visual Tile Matching Cheat-Sheet Modal (`#help-modal`, Key `H`)**:
   - Added `#help-modal` in `index.html`, styled in `src/style.css`, and wired in `src/main.js` (`toggleHelpModal`) to open/close when pressing **`H`** (or **`?`**) on the keyboard or clicking **`📖 Guida (H)`** in the top HUD or bottom dock.
   - Visually illustrates all 4 matching rules with actual tile thumbnails:
     1. **Quartetto Famiglia Carlesso (`S1..S4`)**: *Qualsiasi 2 su 4 fanno coppia* (`Papà Riccardo`, `Mamma Kate`, `Ale`, `Sebi`).
     2. **Quartetto Compagni Magici (`M1..M4`)**: *Qualsiasi 2 su 4 fanno coppia* (`Ale+Ghigna`, `Sebi+Pupurabbu`, `Solo Ghigna`, `Solo Pupurabbu`).
     3. **4 Dittici Divisi a Metà (`E1↔E2` Muraglia, `F1↔F2` Riso, `G1↔G2` Shaolin, `H1↔H2` Panda)**: *Metà Sinistra Ale (`X1`) ↔ Metà Destra Sebi (`X2`)*.
     4. **34 Semi Classici & Bambù Comici (`1索..4索` Pavone/Hot Wheels/Sirio/Gemme, `1..9`, Venti, Draghi)**: *Coppie Identiche*.
2. **Live `"🔗 VA CON:"` Partner Preview Strip (`#sel-partners-box`)**:
   - Whenever any tile is clicked on the board, `showSelectionCard()` in `src/main.js` immediately populates `#sel-partners-list` with the exact thumbnail image(s) and code(s) of the partner tile(s) that match with the selected tile.
3. **Unit Test & GitHub Pages Update**:
   - Added automated verification for `#help-modal`, `#btn-help-toggle`, `#sel-partners-box`, and `key === "h"` in `scripts/test_3d_visibility.mjs`, verified `just test`, and pushed `v1.4.1` to `main` and `gh-pages`.

---

## 2026-10-16T15:36:02+02:00 — Choreographic Director Feedback on Camera 5 (`cycles_cam5_carved_intaglio.png`)

### 1. Verbatim User Feedback
> "OMG fantastico 🔥 Camera 5: 3D Incandescent-Pen Carved Intaglio Macro (2筒, 4筒, 8萬) !!!"

### 2. Telemetry Note
- Validated that the dual-frequency 3D Incandescent-Pen Carving pipeline (`apply_incandescent_pen_carving` in `scripts/build_all_tile_textures.py` + `120×160` displaced BMesh in `scripts/blender/build_carved_intaglio_showcase.py` + `72×96` displaced `PlaneGeometry` in `src/main.js`) achieved the exact physical carved-groove look requested by RiccardinoCM26 🦖.

---

## 2026-10-16T16:13:55+02:00 — Milestone 8 (`v1.5.0`): Adversarial Net of 3 Critic Subagents for `S1 春 • Solo Papà Riccardo` Top 3 + Minimal Non-Intrusive Selection UI ($\pm 30^\circ$ Face-Forward 3D Inspector)

### 1. Verbatim User Requests
> 1. "purtroppo la S1 春 • Solo Papà Riccardo NON MI SOMGILIA! Rifalla 5-10 volte e usa una adversarial net of agents che scelga la migliore! Dammi la top 3 e committa la top 3 grazie."
> 2. "l'hover occupa TUTTO lo spazio, rende il gioco ingiocabile, e' un po' pacchiano. Nella rotazione a sx togli il viola e ruota con faccia visibile se possibile, magari piu meno 30 gradi? Cerca la partte scritta di renderla piu' piccola e minimale, fuori dalla vista, voglio continuare a vedere la scacchiera e pianificare la prox mossa!"

### 2. Root-Cause Analysis & 8-Candidate Portrait Generation (`scripts/generate_s1_riccardo_candidates.py`)
- **Why the previous `quartet_S1_papa_riccardo.png` failed likeness**: The earlier prompt in `scripts/generate_remastered_portraits.py` asked for `"looking around age 36-38 with short dark brown/black hair"` and passed full landscape selfies where Riccardo's face was small in the frame.
- **Fix**: Extracted 5 tight high-res facial crops (`public/portraits/candidates_s1/refs_crops/ricc_crop_1_papino.jpg` through `ricc_crop_5_lake.jpg`) from Riccardo's real GIC photos (`papino 2026-07-20.png`, `ricc-google-switzerland.png`, `riccardosouthafrica.png`, `ricc-za-wine-tasting.png`, `ricc-za-lake.png`) and generated 8 candidate portraits (`public/portraits/candidates_s1/s1_cand_01.png` .. `s1_cand_08.png`) using `gemini-3.1-flash-image-preview` and `gemini-3-pro-image-preview`, anchored on Riccardo's exact craniofacial features (receding hairline with wispy silver-grey crown hair, expressive forehead creases, deep-set warm brown eyes, closed-lip warm knowing smile, short silver-grey/salt-and-pepper stubble).

### 3. Adversarial Net of 3 Critic Subagents & Consensus Top 3 (`scripts/finalize_s1_top3.py`)
- Spawned 3 independent Critic Subagents in parallel (`invoke_subagent`):
  1. **Judge 1 — Forensic Craniofacial Likeness Critic** (`conversation://04bdab1d-a60f-4062-b961-1c14ba10d816`): Ranked `#1: s1_cand_03 (9.70)`, `#2: s1_cand_07 (9.50)`, `#3: s1_cand_01 (9.35)` (and scored `s1_cand_04: 9.08`, `s1_cand_08: 8.85`).
  2. **Judge 2 — Adversarial Impostor Detector ("Red Team Disqualifier")** (`conversation://ce6181b9-00b9-47ab-b911-e281f52c733a`): Ranked `#1: s1_cand_04 (9.70)`, `#2: s1_cand_08 (9.50)`, `#3: s1_cand_01 (9.30)`.
  3. **Judge 3 — Mahjong Cameo & Artistic Critic** (`conversation://00f23166-2cff-4b05-9c29-b3434d96e95d`): Ranked `#1: s1_cand_06 (9.67)`, `#2: s1_cand_08 (8.53)`, `#3: s1_cand_01 (8.23)` (and `s1_cand_04: 8.13`).
- **Consensus Top 3 Committed to Repository**:
  - **🥇 TOP 1 (`s1_cand_01.png` — Ensemble `8.96/10`, Unanimous Top-3 across ALL 3 judges)**:
    - Portrait: `public/portraits/quartet_S1_papa_riccardo_top1.png` (and active `quartet_S1_papa_riccardo.png`)
    - Mahjong Tiles: `public/textures/tiles/coupled_A1_top1.png` (and active `coupled_A1.png`), `public/textures/tiles_onirica/coupled_A1_top1.png`
  - **🥈 TOP 2 (`s1_cand_04.png` — Ensemble `8.97/10`, Judge 2 Red-Team #1 Winner `9.70/10`)**:
    - Portrait: `public/portraits/quartet_S1_papa_riccardo_top2.png`
    - Mahjong Tiles: `public/textures/tiles/coupled_A1_top2.png`, `public/textures/tiles_onirica/coupled_A1_top2.png`
  - **🥉 TOP 3 (`s1_cand_08.png` — Ensemble `8.96/10`, Ranked #2 by both Judge 2 & Judge 3)**:
    - Portrait: `public/portraits/quartet_S1_papa_riccardo_top3.png`
    - Mahjong Tiles: `public/textures/tiles/coupled_A1_top3.png`, `public/textures/tiles_onirica/coupled_A1_top3.png`

### 4. Minimal Non-Intrusive Selection UI & $\pm 30^\circ$ Face-Forward 3D Inspector (`index.html`, `src/main.js`, `src/style.css`)
- **Top-Left `#wow-3d-popup` (`top: 74px; left: 12px; width: 128px;`)**:
  - Removed all purple styling (`selectionBorder.visible = false` on the preview clone, removed the `0xa832ff` purple point light, removed the purple CSS border/glow).
  - Oriented the preview tile upright facing the camera (`rotation.x = Math.PI * 0.45`) and replaced 360° spinning with a smooth **$\pm 30^\circ$ (`Math.sin(now * 0.0022) * (Math.PI / 6)`)** face-forward oscillation so the carved 3D bassorilievo face never turns its back to the player.
- **Top-Right Minimal `#selection-card` (`top: 74px; right: 12px; max-width: 395px; padding: 5px 10px;`)**:
  - Relocated out of the bottom-center of the board into the top-right empty margin with compact `9.5px–11px` typography and subtle gold/dark glass styling so **0% of the Mahjong board is obstructed**.

---

## 📅 Session Timeline & Agentic Loops (2026-10-17 — `pupurabbux` Ubuntu Host)

## 2026-10-17T08:14:24+02:00 — Milestone 9 (`v1.6.0`): Solvability & Early Deadlock Engine + Dedicated Game Over Modal + Real Mahjong Dimensions & GHP Readme Link

### 1. Verbatim User Requests
> 1. *"ho trovato un bug - se il gioco NON e' solubile deve FINIRE con GAME OVER! E se il gioco non e' solubile anche da prima (nel senso se NON esiste un path di risoluzione) deve dare game over anticipato. qui siamo bloccati e non lo dice, e la HINT dice 'non ho hint'"* (with screenshot: Remaining 18, Matchable 0, Score 27800, Combo x7).
> 2. *"(e quanf hai un attimo linka il GHP in cima al README)"*
> 3. *"e i piezzi sono TROPPO GROSSI! Usa la dimensione REALE deipezzi di mahgonng, con il rapporto base altezza spessore REALE!"* (with screenshot: chunky thick block tiles).

### 2. Root Cause Analysis
1. **Deadlock Game Over Bug**: In `checkGameEnd(matchablePairs)`, when `matchablePairs === 0`, the code only set `toast.textContent` on `#sel-status`, which was hidden when `#selection-card` was closed. No Game Over screen existed in the DOM, so players remained frozen on the board with `Matchable: 0`. Calling `provideHint()` simply played `sfx.playError()`.
2. **Early Unsolvability**: Players making legal moves could branch into dead-end states where no sequence of remaining moves could clear the board, leading to wasted time before reaching deadlock.
3. **Chunky Tile Dimensions**: Virtual tiles were defined as `0.96 × 1.28 × 0.56`, making them 56cm thick blocks resembling giant monolithic cliff walls when viewed in 3D perspective.

### 3. Agentic Loop & Engineering Execution
1. **Solvability & Deadlock Engine (`MahjongSolvabilityEngine` in `src/main.js`)**:
   - Built a deterministic DFS solver with spatial coverage graphs (`coverList`, `leftBlockList`, `rightBlockList`), bitmask state representation (`BigInt` / uint32 base-36 transposition hashing), and heuristic move ordering (prioritizing high layers & coupled family tiles).
   - Validated across all 4 layouts in `scripts/test_solvability_solver.mjs`:
     - *Easy Lotus (36 tiles)*: Solved in `0.27ms` (19 nodes).
     - *Medium Jade Pagoda (72 tiles)*: Solved in `0.81ms` (37 nodes).
     - *Master Imperial Turtle (144 tiles)*: Solved in `3.24ms` (73 nodes).
     - *Deadlocked state (18 tiles)*: Detected unsolvable in `0.06ms`!
2. **Dedicated Game Over Modal (`#gameover-modal`, `.gameover-card` in `index.html`, `src/style.css`, `src/main.js`)**:
   - Styled with dark obsidian & crimson lacquer aesthetic (`border-color: rgba(255, 95, 88, 0.7)`, drop-shadow glow).
   - Displays Remaining Tiles, Final Score, Total Moves, and Max Combo.
   - Provides 3 direct actions:
     - 🔄 **"Rimescola Risolvibile (Solvable Shuffle)"**: Re-arranges remaining tiles into a 100% mathematically solvable configuration, preserving score!
     - 🔁 **"Ricomincia Livello"**: Restarts the track layout.
     - 👁️ **"Rivedi Scacchiera"**: Closes modal to inspect remaining board state.
   - Automatically detects both **Immediate Deadlock** (`matchablePairs === 0`) and **Early Unsolvable States** (`res.solvable === false && res.exhaustedSearch`).
3. **Smart Winning-Path Hint (`provideHint` in `src/main.js`)**:
   - Upgraded Hint to consult `solvabilityEngine.findSolution()`: pulses the exact pair on the *winning resolution path*, preventing players from walking into dead-end traps.
   - If no winning path exists, alerts player via audio/toast and immediately opens the Game Over modal.
4. **Authentic Real-World Mahjong Dimensions & Proportions (`src/main.js`, `scripts/test_3d_visibility.mjs`)**:
   - Replaced chunky blocks with standard Mahjong tile ratio (**Base 22mm : Height 30mm : Thickness 13mm**, ratio `0.739 : 1.000 : 0.413`):
     - `TILE_W = 0.68`, `TILE_H = 0.92`, `TILE_D = 0.38`.
   - Scaled extruded top collar, kintsugi waist seam, subdivided face intaglio displacement (`dispScale = 0.052 * relief`), crown badge, and selection borders.
   - Calibrated camera presets (`2d`, `hero`, `topdown`, `pavement`, `macro`, `orbit`) verifying **100% frustum coverage (144/144 tiles)** and **0 environment occlusion** across all 30 viewpoints.
5. **GitHub Pages Link in README (`README.md`)**:
   - Placed direct playable link [**https://palladius.github.io/family-mahjong-3d/**](https://palladius.github.io/family-mahjong-3d/) and GitHub Pages badge at the very top of `README.md`.
6. **Verification & Delivery**:
   - `just test`: Passed all 3D topology, manifold, line-of-sight, frustum, and unit tests.
   - `just build`: Vite 6 bundle built in 1.96s with 0 errors.
   - Bumped `VERSION` to `1.6.0` and updated `CHANGELOG.md`.

---

## 2026-10-17T10:26:20+02:00 — Milestone 10 (`v1.6.1`): Choreographic Director Final Selection for `S1 春 • Solo Papà Riccardo` (`top3` Wins, `top1` Kept in Subordine, `top2` Removed)

### 1. Verbatim User Request
> "questo no quartet_S1_papa_riccardo_top2 .
> La 3 vince 🥉 TOP 3 Portrait (quartet_S1_papa_riccardo_top3.png)
> e la 1 tienila, in subordine."

### 2. Engineering Execution
1. **Promoted `quartet_S1_papa_riccardo_top3.png` (`s1_cand_08.png`) as Active Winner**:
   - Updated `scripts/finalize_s1_top3.py` so `public/portraits/quartet_S1_papa_riccardo_top3.png` is copied to `public/portraits/quartet_S1_papa_riccardo.png` and rebuilt `public/textures/tiles/coupled_A1.png`, `public/textures/tiles_onirica/coupled_A1.png`, `public/textures/tiles_depth/coupled_A1_depth.png`, `public/textures/tiles_normal/coupled_A1_normal.png`, and `public/portraits/diptyque_S1_S2_papa_mamma.png`.
2. **Kept `top1` in Reserve (*in subordine*) & Removed `top2`**:
   - Retained `public/portraits/quartet_S1_papa_riccardo_top1.png`, `public/textures/tiles/coupled_A1_top1.png`, and `public/textures/tiles_onirica/onirica_coupled_A1_top1.png` in the repository.
   - Deleted rejected `quartet_S1_papa_riccardo_top2.png`, `coupled_A1_top2.png`, and `onirica_coupled_A1_top2.png` and added byte-equality and absence assertions in `scripts/verify_build.mjs`.

---

## 2026-10-17T11:04:00+02:00 — Milestone 11 (`v1.7.0`): Ornate 3D Carved Red Dragon (`紅中`), Ma Shan Zheng Brush Calligraphy, Transparent "Puff $\rightarrow$ Frame 2 Dragon Emerge Biribip Power-Up" (GitHub Issue #1), & Vetrina Showcase

### 1. Verbatim User Requests
> "I pezzi circolari 1-2-3-4 cerchi fatti in 3D sono bellissimi, ma i testi cinesi invece sono molto meccanici, come hai fatto una riga verticale e una riga ortogonale. Per esempio, il drago rosso fa veramente schifo in 3D, quindi ti chiederei di farlo con tutte le sue belle curve e incisioni, dedicatici bene al drago. Un'ultima cosa: quando prendi pezzi di Ale, Sebi o del drago, mi piacerebbe che si creasse un effetto video, come che dal nulla, da un puff, una nuvola, venisse fuori una specie di video con come un power-up, un biribip, con un drago che soffia, un drago che sbuca dal nulla. La cosa difficile è che dovresti fare una specie di video con su base bianca e poi togliere la base bianca, perché poi deve essere magari va bene anche 2D, però deve essere come dire, in trasparenza rispetto al retro 3D. Prova a fare una cosa del genere. Se è troppo difficile, crea un paio di sottoagenti in antagonismo che lo fanno tra di loro. Fammi vedere cosa viene fuori, magari crea una GitHub issue per questo."
> "il frame2 emerge white e' il mio preferito come effetto"
> "Allora, fai una git pull perché mi sa che dall'altro computer ho pushato qualche cosa. Assicurati di avere nel README un link al GitHub Pages, quindi io clicco sul repo e clicco su GitHub Pages subito. Aggiungi questo bellissimo sito a vetrina, così quando vado su vetrina ce l'ho nella vetrina. Inventati una screenshot fighissima per far vedere questo gioco."

### 2. Adversarial Subagent Duel & GitHub Issue #1
- Opened **GitHub Issue #1** (`https://github.com/palladius/family-mahjong-3d/issues/1`).
- Spawned 2 antagonistic subagents:
  - **Subagent A (`Dragon & VFX Power-Up Architect`)**: `conversation://1995b359-305e-4ea8-9892-14713fcd562d`
  - **Subagent B (`Adversarial VFX & 3D Dragon Critic`)**: `conversation://8d189132-26b8-457b-af2b-b820ab124842`
- **Root-Cause & Mathematical Resolution**:
  1. **3D Chinese Calligraphy & Ornate Red Dragon (`紅中`)**:
     - Replaced `STHeiti Medium.ttc` (geometric sans-serif) with **`MaShanZheng-Regular.ttf`** (`public/fonts/MaShanZheng-Regular.ttf`) + `Songti.ttc (index=1)` for Traditional-only glyphs (`萬`, `東`, `風`, `發`, `蘭`).
     - Generated ornate coiled dragon emblems (`public/portraits/dragon_red_ornate_emblem.png`, `dragon_green_ornate_emblem.png`, `dragon_white_ornate_emblem.png`) and upgraded `apply_incandescent_pen_carving()` in `scripts/build_all_tile_textures.py` with a **Multi-Scale V-Groove + Medial-Axis Spine** heightfield (`0.42*v_fine + 0.36*v_med + 0.22*v_deep + 0.30*spine + 0.24*detail_relief`).
     - Re-rendered `public/models/tile_carved_intaglio_showcase.glb` and `public/renders/cycles/cycles_cam5_carved_intaglio.png` with `dots_4` (`4筒`), **`dragon_red` (`紅中`)**, and `char_8` (`八萬`).
  2. **White-Background (`#FFFFFF`) $\rightarrow$ Zero-Halo Transparent 2D-over-3D Power-Up (`powerup_frame2_dragon_emerge`)**:
     - Generated white-background keyframes (`powerup_frame1_cloud_puff_white.png`, **`powerup_frame2_dragon_emerge_white.png`**, `powerup_frame3_dragon_fire_white.png`) and `dragon_powerup_white.mp4`.
     - Solved the classic white-halo & eye-hole failure modes via **Border-Seeded Flood-Fill (`d_max = 1 - min(R,G,B) < 0.34`) + Exact White Un-Premultiplication ($\mathbf{C}_{\text{clean}} = \frac{\mathbf{C} - (1-\alpha)}{\alpha}$) + Fiery Edge Despill** (`scripts/build_powerup_video_fx.py`, `src/main.js`).
     - Wired `triggerDragonPowerUpEffect()` and `sfx.playDragonBiribipPowerUp()` in `src/main.js` when matching any Ale, Sebi, or Dragon pair (plus `🐉 Biribip FX (D)` button).
  3. **Git Pull, GitHub Pages Link, & Vetrina Integration**:
     - Pulled & rebased `v1.6.0` from `pupurabbux`, added GitHub Pages link & repo homepage URL, created composite showcase screenshot for `/Users/ricc/git/vetrina/assets/screenshots/family-mahjong-3d.jpg`, and added `family-mahjong-3d` to `/Users/ricc/git/vetrina/data/games.yaml`.



---

## 2026-10-19T17:58:00+02:00 — Milestone 12 (`v1.7.1`): Septober Action Item — Fullscreen Mobile UI, Clean Floating HUD & Default 2D View with 3D Orbit Toggle (GitHub Issue #2 / PR #3)

### 1. Verbatim User Request & Septober Issue #2
> "guarda GHI, penso ci sia un AI da speotber"
> **GitHub Issue #2** (`feat(mobile): Fullscreen mobile UI, clean HUD and default 2D top-down view` — filed by Ermete Bottazzi 🚛 on behalf of Riccardo Carlesso and Andrea Patrignani):
> - *"Togli tutta la roba sopra e sotto, facciamolo diventare uno schermo intero su cellulare, sarebbe più figo."*
> - *"Default 2D poi puoi ruotarlo."*

### 2. Engineering Execution & PR #3 Merge
1. **Merged & Polished `origin/fix/issue-2` (PR #3) into `main` (`v1.7.1`)**:
   - **Clean Fullscreen Mobile Viewport**: Added `@media (max-width: 768px), (pointer: coarse) and (max-width: 1024px)` in `src/style.css` locking `html, body, #canvas-container` to `100vw` $\times$ `100dvh` (`touch-action: none; overscroll-behavior: none`), hiding desktop look-dev controls (`#studio-panel`, `#rig-inspector`, `.brand-sub`, `.link-btn`, `#btn-surface-toggle`, `#btn-onirica-toggle`, `#btn-demo`, `#btn-dragon-fx`, `#btn-undo`), and keeping only floating HUD chips + a floating bottom pill dock (`#camera-bar`).
   - **One-Tap Fullscreen Button (`#btn-fullscreen`)**: Added `⛶ Full` in `index.html` and wired `toggleFullscreen()` (`requestFullscreen` / `webkitRequestFullscreen`) in `src/main.js`.
   - **Default 2D Top-Down View on Mobile + Seamless 3D Rotation Toggle**: Added `isMobileViewport()` detection (`window.matchMedia("(max-width: 768px), (pointer: coarse) and (max-width: 1024px)")`) so mobile sessions start in `2d` flat top-down view by default while allowing one-tap toggle to `hero` / `orbit` 3D rotation via `#btn-2d-toggle` and `#camera-bar`.
   - **Portrait-Aware FOV Scaling, Forgiving Touch Hitboxes, & Haptic Feedback**: Added dynamic FOV scaling when `aspect < 1.0`, 5-point forgiving touch raycast probes (`probeOffsets`), and `navigator.vibrate` haptic feedback on tile selection, pair match, and mismatch.


---

## 2026-10-19T18:22:00+02:00 — Milestone 13 (`v1.8.0`): Ultra-Clean Single-Row Mobile HUD, 60 FPS Lightweight 3D Engine (6,900x Fewer Triangles), Ornate "Tarchiato" Dragon Hover/Selection Morphing, & Exclusive Carlesso Family Power-Up Video

### 1. Verbatim User Request
> "cmq il gioco e' INGIOCABILE su mobile. va cambiato.
> 1. tastini idioti sopra la scacchiera lo rendono in giocabile,d obbiamo progettarla meglio
> 2. 3d SUER PESANTE
>
> poi i draghi in animazione sono troppi, il video c'e' sempre. Fallo che c'e' SOLO per i draghi rosso e verde, e gia che ci siamo i draghi rosso e verde sono FIGHISSIMI cosi ma non in linea con il gioco, quindi propongo:
> - metti i draghi rossi e verdi con solo il simbolo cinese
> - quando selezioni il drago verde o rosso (NON DRAGONE!) allora l'hover lo rende automaticamente tarchiato come e' adesso, bellissimo! E quando li accoppi viene fuori il video del drago.
> - per tutti gli altri pezzi il video SOCMPARE.
> - per i pezzi della famiglia carlesso creiamo un video in stile simile per la famiglia carlesso (decidi tu ma con quella trasparenza, che viene dal nulla come l'altro video, guarda come e' stato fatto )"

### 2. Engineering Execution & Subagent Orchestration
- **Subagent Dispatched (`Carlesso Family VFX Keyframe Generator`)**: `conversation://06e48c85-3df9-49c6-80f9-acb4989cae64`
  - Generated 2 square 1024×1024 pure solid white (`#FFFFFF`) keyframes for the Carlesso Family Power-Up:
    - `public/fx/family_powerup_frame2_crest_white.png` (Pupurabbu, Ghigna with nerd glasses, and Chengdu baby panda emerging from a golden-jade circular cloud crest with cherry blossoms & lotus petals)
    - `public/fx/family_powerup_frame3_celebrate_white.png` (Festive climax burst of golden silk ribbons, red-gold Chinese lanterns, and stars)
- **Zero-Halo Transparent RGBA + MP4 Pipeline (`scripts/build_powerup_video_fx.py`)**:
  - Processed both family keyframes through our **Border-Seeded Flood-Fill (`d_max = 1 - min(R,G,B) < 0.34`) + Exact White Un-Premultiplication ($\mathbf{C}_{\text{clean}} = \frac{\mathbf{C} - (1-\alpha)}{\alpha}$)** pipeline with inner radial protection (`r < 0.25*W`) so Ghigna's white fur and the baby panda's white fur remain 100% opaque while the outer `#FFFFFF` background keys to `alpha = 0`:
    - `public/fx/family_powerup_frame2_crest_rgba.png`
    - `public/fx/family_powerup_frame3_celebrate_rgba.png`
    - `public/fx/family_powerup_white.mp4` (779 KB, 36 frames @ 24fps)
- **Clean Calligraphic Board Dragons + Automatic "Tarchiato" Ornate Dragon on Hover/Selection (`scripts/build_all_tile_textures.py`, `src/main.js`)**:
  - Rebuilt `public/textures/tiles/dragon_red.png` (`中`) and `public/textures/tiles/dragon_green.png` (`發`) with **ONLY the traditional Chinese brush calligraphy character**, matching the clean board style of all other suits.
  - Exported the ornate coiled 3D carved dragons to `public/textures/tiles/dragon_red_ornate.png` and `public/textures/tiles/dragon_green_ornate.png` (plus `_normal.png`, `_depth.png`, `tiles_onirica/`).
  - Implemented `isMorphingDragonTile(tileData)` (strictly `dragon_red` and `dragon_green` — never `bamboo_3` *"Sirio il Dragone"* and never `dragon_white`) and `setDragonOrnateState(tile, ornateActive)` in `src/main.js`: hovering (`onPointerMove`) or selecting (`liftTile`) `dragon_red` or `dragon_green` swaps its 3D face texture and normal/displacement maps to `dragon_red_ornate` / `dragon_green_ornate` and scales the tile to a chunky "tarchiato" `[1.06, 1.14, 1.04]` relief!
- **Strictly Separated Power-Up Videos (`src/main.js`)**:
  - `isRedOrGreenDragonPair(a, b)` $\rightarrow$ triggers `triggerDragonPowerUpEffect(tileA, tileB)` **ONLY** for `dragon_red` (`中`) or `dragon_green` (`發`).
  - `isCarlessoFamilyPair(a, b)` $\rightarrow$ triggers `triggerFamilyPowerUpEffect(tileA, tileB)` **ONLY** for Carlesso Family tiles (`coupled === true`: `S1..S4`, `M1..M4`, `E1..H2`).
  - All other tiles (`dots_*`, `bamboo_*`, `char_*`, `wind_*`, `dragon_white`) trigger **NO video** (`"per tutti gli altri pezzi il video SCOMPARE"`).
- **Ultra-Clean Single-Row Mobile HUD & 60 FPS Lightweight 3D Overhaul (`src/style.css`, `index.html`, `src/main.js`)**:
  - **Mobile HUD**: Collapsed `#game-hud` to a single 38px horizontal bar (`flex-wrap: nowrap`), hid `#camera-bar`, `#wow-3d-popup`, and `.btn-label` text on mobile, keeping only 5 compact 30×30px icon buttons (`📖`, `💡`, `🔀`, `📐`, `⛶`) and turning `#selection-card` into a 36px bottom micro-pill.
  - **3D Performance**: Reduced tile face geometry from `72x96` (1,990,656 triangles across 144 tiles) to `1x1` on mobile (288 triangles total — **6,900x reduction**) and `24x32` on desktop; shared 4 body material sets across all 144 tiles; cached `child.userData.cachedCenter` to eliminate per-frame `THREE.Box3().setFromObject()` allocations; and disabled shadow maps, 4 dynamic lantern `PointLight`s, and the secondary `wowRenderer` on mobile.

---

## 2026-10-19T18:36:00+02:00 — Milestone 14 (`v1.8.1`): "Less is More" Clean Tiles (Zero Octagonal Circles), Half-Thickness 8-Bevel White/Ivory Parallelepiped (`TILE_D = 0.19`), & Toggleable `Debug Simboli` (OFF by Default)

### 1. Verbatim User Request
> "ah e togli quegli ORRIBILI cerchi ottagonali che hai messo, TOGLILI, LESS IS MORE. voglio i pezxzi piu' "vuoti" troppo pieni.
>
> E gia avevo chiesto tempo fa i pezzi dovrebbero avere spessore dimezzat e non avere quella cosa rossa in mezzo, un banalissimo parallelepipedo bianco/avorio con 8 bordi smussati, niente piu. ok il bordo esterno. La C/S2/S3 mettiamola togglabile, che se metti "sdebug simboli" li abilita se no li disablita secondo me a dflt dovrebbero essere disabilitati questi 2 in alto"

### 2. Engineering Execution & Artifacts
- **Removed Octagonal Circles & Visual Clutter (`scripts/build_all_tile_textures.py`)**:
  - Removed `draw_imperial_cloud_flourishes` (which drew an octagonal 8-bead circle around `char_1..9`, `wind_E/S/W/N`, and `dragon_red/green/white`).
  - Removed diagonal marble vein lines, inner red borders, and bottom text cartouches on `coupled_*` tiles, keeping only a subtle outer border (`ok il bordo esterno`) on pure warm ivory (`#FAF6EE`).
- **Top-Left & Top-Right Symbols Toggleable via `🏷️ Debug Simboli` — `OFF` by Default (`scripts/build_all_tile_textures.py`, `public/textures/manifest.json`, `src/main.js`, `index.html`)**:
  - Regenerated all 50 tile textures (`public/textures/tiles/*.png`, `public/textures/tiles_onirica/*.png`) without baked-in top-left (`C`, `S1..S4`, `1..9`) and top-right (`中`, `春`) corner symbols.
  - Exported `cornerLeft`, `cornerRight`, and `cornerColor` in `public/textures/manifest.json`.
  - Added `debugCornerMesh` + `getDebugCornerMaterial()` + `toggleDebugSymbols()` in `src/main.js`, defaulting to **`this.debugSymbols = false`** (`OFF`), toggleable anytime via `#btn-debug-symbols` (`🏷️ Debug Simboli: OFF`), `#chk-debug-symbols` in the Studio Panel, key **`S`**, or `?symbols=1`.
- **Half-Thickness White/Ivory 8-Bevel Parallelepiped (`TILE_D = 0.19`, `src/main.js`)**:
  - Halved `TILE_D` from `0.38` to **`0.19`**.
  - Replaced the multi-part tile body (`kintsugiMesh` middle band + `collarMesh` + `badgeMesh` + obsidian back) with a single uniform white/ivory beveled parallelepiped (`makeBeveledParallelepipedGeometry(TILE_W, TILE_D, TILE_H, 0.042, 0.015)`).

---

## 2026-10-21T08:24:00+02:00 — Milestone 15 (`v1.8.2`): Fix `faceMesh` Buried Under `bodyMesh` Self-Occlusion Bug, Smooth 3D Rotation Drag-vs-Click Guard, & Pre/Post-Deploy Board Integration Test (`scripts/test_board_integration.mjs`)

### 1. Verbatim User Request & Screenshot (`media_1792563128539_3f33301b.png`)
> "mahjong is broken! Lets add an integration test which post deploy, or before deploy checks the initial chessboard and checks it looks all good! and tries to rotate and ensures its rotateable , look how awful"

### 2. Root-Cause Diagnosis & Engineering Fix
- **Root Cause 1 (`faceMesh` Buried Underneath `bodyMesh` Top Cap)**:
  - In `v1.8.1`, `bodyMesh` became a solid beveled parallelepiped (`makeBeveledParallelepipedGeometry(TILE_W, TILE_D, TILE_H)`) whose flat top surface sits at `y = +TILE_D * 0.5 = +0.0950`.
  - Meanwhile, `faceMesh` (`y = +0.0965`) had `displacementScale = 0.032 * 1.15 = 0.0368` and `displacementBias = -0.88 * dispScale = -0.0324`. For every pixel with `depth < 0.88` (98.5% of every tile face, including the marble background at `depth = 0.855` and all carved artwork at `depth = 0.15..0.75`), vertex displacement pushed `faceMesh` **downward** to `y = +0.064..+0.094 < +0.0950` — burying the artwork underneath the opaque beige top cap of `bodyMesh`!
  - **Fix**: Removed negative `displacementBias` from `faceMesh` (`createTileMesh`, `toggleOniricaMode`, `sl-bassorilievo`, `syncSliderUI`) and placed `faceMesh` strictly at `y = TILE_D * 0.5 + 0.003` (`+0.0980`) with `polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2`, using the 1024×1024 `normalMap` (`normTex`) for crisp 3D relief lighting.
- **Root Cause 2 (3D Rotation & Pointer Drag-vs-Click Conflict)**:
  - Previously, `onPointerDown` fired immediately on `pointerdown` (selecting or error-buzzing tiles the moment the user pressed down on the board to drag-rotate), and `this.controls.enableRotate` was disabled in `"2d"` mode.
  - **Fix**: Enabled `this.controls.enableRotate = true` across all presets, cancelled camera preset tweens on `OrbitControls` `"start"`, and added a 6px pointer movement guard between `pointerdown` and `pointerup` so dragging rotates the 3D board cleanly while stationary clicks (`< 6px`) select tiles.
- **Automated Pre-Deploy & Post-Deploy Integration Test (`scripts/test_board_integration.mjs`)**:
  - Wired into `just test` (pre-deploy) and `just test-post-deploy` (`--post-deploy`):
    - Casts 1,296 vertical rays and 1,296 Hero-3D camera rays across all 144 tiles on the initial chessboard to prove `100%` hit `faceMesh` before `bodyMesh`.
    - Decodes PNG IDAT scanlines of tile textures to verify strong RGB luminance contrast (`lumRange = 188..253.8`).
    - Simulates pointer drag events on `OrbitControls` to verify the 3D board rotates (`11.5°` azimuth rotation on drag) without triggering tile clicks.

---

## 2026-10-21T11:46:00+02:00 — Milestone 16 (`v1.8.3`): Left-Click / 1-Finger Drag Bound to Horizontal Board Translation (`PAN`) to Preserve Left/Right Mahjong Alignment

### 1. Verbatim User Request
> "daomanda: ma e' normale che se clicco e muovo mouse cliccato (pinned) triggeri una rotazione? raramente voglio ruotare il mahjong, piu probabilmente voglio TRASLARLO - qui e' importnte tenere i bordi sempre a sx/dx per le regole del gioco. possiam cambiare quella funzionalita?"

### 2. Engineering Execution & Verification
- **Configured `OrbitControls` for Horizontal Table-Plane Translation (`PAN`) on Left-Click / 1-Finger Drag (`src/main.js`)**:
  - `this.controls.screenSpacePanning = false;` (translates strictly parallel to the horizontal `XZ` table plane).
  - `this.controls.mouseButtons = { LEFT: THREE.MOUSE.PAN, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: THREE.MOUSE.ROTATE };`
  - `this.controls.touches = { ONE: THREE.TOUCH.PAN, TWO: THREE.TOUCH.DOLLY_ROTATE };`
  - Left-click drag (and 1-finger touch drag) now translates the board horizontally with `0.00°` azimuth rotation so Left/Right tile edges always remain strictly Left/Right for Mahjong rules, while Right-click drag (or `Shift/Ctrl/Cmd + Left-click drag`, or 2-finger gesture) rotates the 3D view when desired.
- **Updated Integration Test Suite (`scripts/test_board_integration.mjs`)**:
  - Verifies that `button: 0` (Left-Click drag) translates `controls.target` (`> 1.1m`) with `0.00°` azimuth drift, and `button: 2` (Right-Click drag) rotates the 3D camera (`11.5°`).

---

## 2026-10-22T14:35:00+02:00 — Milestone 17 (`v1.8.4`): White Dragon (`dragon_white` / `白`) Redesigned in White-Silver Pearl & 24k Gold (No Box, No Blue) + Ornate "Tarchiato" Hover/Selection Morphing

### 1. Verbatim User Request & Feedback
> "che diavolo e sto pezzo, e perche e blu?!?"
> "il click funziona BENISSIMO grazie"
> Selected Option: "(Recommended) Togli il rettangolo e fai il carattere 白 in Bianco-Argento/Perla bordato d'Oro (e mostra il Drago Bianco tarchiato in hover come gli altri 2 draghi)"

### 2. Engineering Execution & Artifacts
- **Redesigned `dragon_white.png` (`scripts/build_all_tile_textures.py`)**:
  - Removed the rectangular frame and blue fill from `dragon_white`.
  - Rendered the brush calligraphy character **`白`** in luminous **White-Silver Pearl (`(238, 241, 247)`)** bordered by **24k Imperial Gold (`(214, 168, 48)`)** and **Antique Bronze (`(86, 62, 18)`)** with 3D V-groove carving.
- **Built `dragon_white_ornate.png` in White-Silver Platinum & 24k Gold & Wired Hover/Select Morphing (`scripts/build_all_tile_textures.py`, `src/main.js`)**:
  - Recolored the cobalt-blue lines of `dragon_white_ornate_emblem.png` into warm **Silver-Platinum & 24k Gold** around the White-Silver Pearl `白`, exporting `public/textures/tiles/dragon_white_ornate.png`, `tiles_onirica/dragon_white_ornate.png`, `tiles_normal/dragon_white_ornate_normal.png`, and `tiles_depth/dragon_white_ornate_depth.png`.
  - Updated `isMorphingDragonTile(tileData)` in `src/main.js` so all 3 real Mahjong Dragons (`dragon_red`, `dragon_green`, and `dragon_white` — never `bamboo_3` *"Sirio il Dragone"*) morph into their chunky "tarchiato" ornate dragon on hover and selection!
