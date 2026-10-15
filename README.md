# 🀄 Carlesso Family 3D Mahjong Solitaire

> **AAA-Quality 3D Solitary Mahjong Web App & Studio Look-Dev Suite** built with **Headless Blender 5.0.1 (`bpy`)**, **Three.js (`r170`)**, and **Vite 6**.

[![Version](https://img.shields.io/badge/version-1.0.0-gold.svg)](VERSION)
[![Blender](https://img.shields.io/badge/Blender-5.0.1%20Cycles-orange.svg)](https://blender.org)
[![Three.js](https://img.shields.io/badge/Three.js-r170-black.svg)](https://threejs.org)
[![Vite](https://img.shields.io/badge/Vite-6.0-purple.svg)](https://vitejs.dev)

---

## 🏛️ Overview

**Carlesso Family 3D Mahjong Solitaire** is a playable 3D solitary game set inside a traditional Chinese temple courtyard featuring:
- **Creamy Imperial White Marble & Volcanic Obsidian Tiles**: Manifold 3D geometry with Gold Kintsugi bevel finiture and raised metallic 3D corner alphabet overlays.
- **Decoupled 2D Oval Medallion Cameo Architecture**: Pure 2D family portraits (Ale & Sebi, Mamma Kate & Papà Riccardo, Ghigna & Pupurabbu) framed in gold-rimmed ovals on canonical generic 3D tiles, paired with normal-mapped **Bassorilievo Relief** (`0.0 = Flat 2D` $\rightarrow$ `1.5 = Sculpted Relief`).
- **34 Original Authentic Mahjong Suits & Honours**: Characters (`一萬..九萬`), Circles (`一筒..九筒`), Bamboos (`一索..九索` with iconic sparrow/peacock), Winds (`東 南 西 北`), and Dragons (`中 發 白`).
- **16 Coupled Non-Identical Family Tiles (8 Pairs)**:
  - `A1↔A2` (`春`): Ale & Sebi in Tang Silk Clothing
  - `B1↔B2` (`夏`): Ale & Sebi Great Wall Sightseeing Explorers
  - `C1↔C2` (`秋`): Ale & Sebi enjoying Cantonese Fried Rice at Dim Sum
  - `D1↔D2` (`冬`): Ale & Sebi in Shaolin Kung Fu Dragon & Tiger Stances
  - `E1↔E2` (`梅`): Ale & Sebi at Chengdu Panda Sanctuary
  - `F1↔F2` (`蘭`): Ale & Sebi Dragon Peak Mountain Explorers
  - `G1↔G2` (`菊`): Ghigna 🐹 & Pupurabbu 👾 Magical Companions
  - `H1↔H2` (`竹`): Mamma Kate & Papà Riccardo (Mum & Dad)
- **4 Multi-Difficulty Tracks (100% Reverse-Peel Solvable)**:
  1. **Easy**: *Lotus Courtyard* (36 tiles / 18 pairs, 3 layers)
  2. **Medium**: *Jade Pagoda* (72 tiles / 36 pairs, 4 layers)
  3. **Hard**: *Twin Dragon Bridge* (108 tiles / 54 pairs, 5 layers)
  4. **Master**: *Imperial Turtle* (144 tiles / 72 pairs, 5 layers)
- **Switchable Surface**: Toggle between the **Low Carved Rosewood & Celadon Jade Table** and placing tiles directly on the **Sacred Temple Stone Flagstone Pavement**!
- **Interactive Look-Dev Studio & JSON Exporter**: Real-time sliders for Lighting, Materials, Bassorilievo Strength, and FOV, plus a "Copy Settings as JSON" button.
- **Frame-by-Frame Rig Inspector**: Timeline scrubber for the 4-bone Armature (`Idle`, `Select`, `Pair`, `Disappear`).
- **Progress Gallery (`/progress.html`)**: Auto-rotating 3D GLB viewers and 4-camera offline Blender Cycles master ground-truth renders.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
just setup # or npm install

# 2. Launch development server
just dev   # or npx vite --host

# 3. Build production bundle
just build

# 4. Run verification tests
just test
```

---

## 📂 Repository Structure

```
├── index.html                   # Playable Web App & Studio UI
├── src/
│   ├── main.js                  # Three.js Solitaire Engine & Look-Dev Controller
│   └── style.css                # Lacquer & Gold Glassmorphic Styling
├── public/
│   ├── progress.html            # Auto-rotating 3D GLB Gallery & Cycles Master Renders
│   ├── models/                  # Manifold GLB models exported by Blender 5.0.1
│   │   ├── tile_generic_white_marble_obsidian.glb
│   │   ├── tile_coupled_showcase.glb
│   │   ├── temple_environment.glb
│   │   └── topology_audit.json
│   ├── textures/
│   │   ├── manifest.json        # 50-tile deck metadata & coupling rules
│   │   ├── pbr/                 # 2K PBR Maps (Marble, Obsidian, Jade, Rosewood, Pavement)
│   │   ├── tiles/               # 50 crisp 2D face textures
│   │   └── tiles_normal/        # 50 Bassorilievo tangent-space normal maps
│   └── renders/cycles/          # Offline Blender Cycles Master Ground Truth
├── scripts/
│   ├── build_all_tile_textures.py # 2K PBR & 50-tile procedural texture generator
│   └── blender/
│       └── build_all_assets.py  # Headless Blender 5.0.1 asset, rig & Cycles pipeline
├── docs/LOG.md                  # Comprehensive agentic log & timeline
├── justfile                     # Task runner
├── package.json
└── VERSION                      # 1.0.0
```

---

## 🎨 Creative Direction & Technical Notes

- **Decoupled 2D Oval Medallion Architecture**: Rather than generating unstable 3D tiles from text prompts, Nano Banana was directed to generate pure 2D photographs. These were audited with Riccardo's Character Consistency criteria (9.9/10 score), masked into gold-rimmed oval cameo medallions with tangent-space normal maps, and mapped onto a canonical 3D manifold tile mesh.
- **Topology Audit**: Verified 0 non-manifold edges, 0 degenerate faces, and full UV mapping.
- **Cycles Ground Truth**: Rendered with path-traced lighting from 4 canonical angles (`hero`, `topdown`, `low_pavement`, `macro`) to establish ground truth for WebGL look-dev.

---

## 📜 License & Credits

Created with ❤️ by **RiccardinoCM26 🦖** and **Jetski**.
All rights reserved • Carlesso Family 2026.
