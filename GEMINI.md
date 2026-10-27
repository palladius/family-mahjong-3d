# 🀄 Carlesso Family Mahjong 3D — Agent Instructions (`GEMINI.md`)

## 1. Mandatory Article Telemetry & Engineering Log (`docs/LOG.md`) 📝
- **ALWAYS update [`docs/LOG.md`](docs/LOG.md)** on every user request, milestone, subagent dispatch, and Critic QA round!
- `docs/LOG.md` serves as the primary chronological dataset and narrative log for **RiccardinoCM26 🦖's upcoming technical article** on multi-agent 3D game creation with Headless Blender (`bpy`), Nano Banana Character Consistency, and Three.js.
- Every entry in `docs/LOG.md` MUST record:
  1. **Exact ISO-8601 Timestamp** (`YYYY-MM-DDTHH:MM:SS+02:00`)
  2. **Verbatim User Request / Feedback** (or Subagent / Critic Event)
  3. **Agentic Loop / Subagent Orchestration Details** (conversation IDs, tools used, rate-limit/sandbox adaptations, Character Consistency scores)
  4. **Concrete Artifacts & Code Produced**

## 2. Core Architectural & Creative Guardrails 🏛️🎨
1. **Decoupled 2D Oval Medallion $\rightarrow$ Generic 3D Tile Pipeline**:
   - NEVER ask Nano Banana to draw a 3D Mahjong tile around characters (which shrinks faces and degrades likeness).
   - Instead, generate **pure 2D portraits** using GIC reference photos (`~/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/`), validate with the **Character Consistency skill** (`characterconsistency-family-images`), mask into a **Gold-Rimmed OVAL Cameo Medallion**, and map onto ONE canonical **Generic 3D White Imperial Marble + Black Obsidian/Gold Kintsugi Finiture Tile** (`tile_generic_white_marble_obsidian.glb`).
   - Support both **Pure Flat 2D (`bassorilievo = 0.0`, default)** and **Sculpted Bassorilievo Cameo Relief (`0.0 .. 1.5`)** via normal maps and an on-screen Control Panel slider.
2. **Family Cast Naming Rule**:
   - **Alessandro (Ale)** & **Sebastian (Sebi / Seby)**: 8+ Coupled Asian-theme non-identical pairs (`A1↔A2` .. `G1↔G2`).
   - **Mamma Kate & Papà Riccardo**: Strictly **Mum and Dad (`Mamma Kate & Papà Riccardo`)** — NEVER copy "King" and "Queen" from the chess game!
   - **Magical Companions**: **Ghigna 🐹** (nerdy calico guinea pig with glasses) & **Pupurabbu / Pupurannu 👾** (giant friendly purple monster).
3. **Original Mahjong Alphabet & Card Art**:
   - Use authentic **Traditional Chinese Mahjong calligraphy and motifs**:
     - Suits: **Characters (`一萬..九萬`)**, **Circles/Dots (`一筒..九筒`)**, **Bamboos (`一索..九索` with the iconic 1-Bamboo Sparrow/Peacock)**.
     - Honours: **Four Winds (`東 南 西 北`)**, **Three Dragons (`中 發 白`)**, and **Seasons/Flowers (`春 夏 秋 冬 梅 蘭 菊 竹`)** paired with corner glyphs (`A1/A2..H1/H2`, `1..9`, `E/S/W/N`).
4. **3D Board Navigation & `OrbitControls` Ergonomics (`/learn` Rule)**:
   - In 3D board games like Mahjong Solitaire where Left/Right orientation matters for game rules, bind `OrbitControls` **Left-Click / 1-Finger drag** to horizontal `XZ` plane translation (`THREE.MOUSE.PAN` with `screenSpacePanning = false` and a `6px` click-vs-drag guard so dragging never clicks tiles) and reserve 3D rotation for **Right-Click, `Shift+Drag`, or 2-Finger Twist**.
5. **Deliverables & Hygiene**:
   - Maintain [`public/progress.html`](public/progress.html) with milestone camera screenshots and **auto-rotating 3D GLB previews**.
   - Provide the on-screen Studio Control Panel with **"Copy Settings as JSON"** (`?debug=1` querystring support).
   - Run `just test` and update `VERSION` and `CHANGELOG.md` after every milestone.
