import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

// Canonical Tile Scale Contract
const TILE_W = 0.96;
const TILE_H = 1.28;
const TILE_D = 0.56;

// Audio Synthesizer (Web Audio API - Zero external assets needed)
class SoundFX {
  constructor() {
    this.ctx = null;
  }
  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.ctx = new AudioCtx();
    }
  }
  playClick() {
    this.init();
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(420, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(140, this.ctx.currentTime + 0.08);
    gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.08);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.08);
  }
  playMatch() {
    this.init();
    if (!this.ctx) return;
    const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
    notes.forEach((freq, i) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = "triangle";
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime + i * 0.06);
      gain.gain.setValueAtTime(0.25, this.ctx.currentTime + i * 0.06);
      gain.gain.exponentialRampToValueAtTime(0.005, this.ctx.currentTime + i * 0.06 + 0.35);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(this.ctx.currentTime + i * 0.06);
      osc.stop(this.ctx.currentTime + i * 0.06 + 0.35);
    });
  }
  playError() {
    this.init();
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = "sawtooth";
    osc.frequency.setValueAtTime(180, this.ctx.currentTime);
    osc.frequency.setValueAtTime(140, this.ctx.currentTime + 0.08);
    gain.gain.setValueAtTime(0.18, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.16);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.16);
  }
}

const sfx = new SoundFX();

// Solitaire Track Layout Definitions in 3D Slot Grid (col, row, layer)
const TRACK_LAYOUTS = {
  easy: {
    name: "Easy • Lotus Courtyard",
    tileCount: 36,
    generateSlots() {
      const slots = [];
      // Layer 0: 6x4 outer pond (24 tiles)
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 6; c++) {
          slots.push({ c: c - 2.5, r: r - 1.5, l: 0 });
        }
      }
      // Layer 1: 4x2 middle petals (8 tiles)
      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 4; c++) {
          slots.push({ c: c - 1.5, r: r - 0.5, l: 1 });
        }
      }
      // Layer 2: 2x2 central lotus blossom (4 tiles)
      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 2; c++) {
          slots.push({ c: c - 0.5, r: r - 0.5, l: 2 });
        }
      }
      return slots;
    },
  },
  medium: {
    name: "Medium • Jade Pagoda",
    tileCount: 72,
    generateSlots() {
      const slots = [];
      // Layer 0: 8x5 base (40 tiles)
      for (let r = 0; r < 5; r++) {
        for (let c = 0; c < 8; c++) {
          slots.push({ c: c - 3.5, r: r - 2.0, l: 0 });
        }
      }
      // Layer 1: 6x3 second tier (18 tiles)
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 6; c++) {
          slots.push({ c: c - 2.5, r: r - 1.0, l: 1 });
        }
      }
      // Layer 2: 4x2 third tier (8 tiles)
      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 4; c++) {
          slots.push({ c: c - 1.5, r: r - 0.5, l: 2 });
        }
      }
      // Layer 3: 2x2 spire pinnacle (4 tiles)
      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 2; c++) {
          slots.push({ c: c - 0.5, r: r - 0.5, l: 3 });
        }
      }
      // Wings: 2 side tiles
      slots.push({ c: -4.5, r: 0.0, l: 0 });
      slots.push({ c: 4.5, r: 0.0, l: 0 });
      return slots;
    },
  },
  hard: {
    name: "Hard • Twin Dragon Bridge",
    tileCount: 108,
    generateSlots() {
      const slots = [];
      // Two symmetrical 5-tier bridge arches (left & right) + central pavilion
      for (let side of [-1, 1]) {
        // Base: 5x4 on each side
        for (let r = 0; r < 4; r++) {
          for (let c = 0; c < 5; c++) {
            slots.push({ c: side * (c + 1.2), r: r - 1.5, l: 0 });
          }
        }
        // Tier 1: 4x3
        for (let r = 0; r < 3; r++) {
          for (let c = 0; c < 4; c++) {
            slots.push({ c: side * (c + 1.4), r: r - 1.0, l: 1 });
          }
        }
        // Tier 2: 3x2
        for (let r = 0; r < 2; r++) {
          for (let c = 0; c < 3; c++) {
            slots.push({ c: side * (c + 1.6), r: r - 0.5, l: 2 });
          }
        }
        // Arch summit: 2 tiles
        slots.push({ c: side * 2.2, r: -0.5, l: 3 });
        slots.push({ c: side * 2.2, r: 0.5, l: 3 });
      }
      // Central Keystone Bridge Pavilion (8 tiles)
      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 2; c++) {
          slots.push({ c: c - 0.5, r: r - 0.5, l: 0 });
          slots.push({ c: c - 0.5, r: r - 0.5, l: 1 });
        }
      }
      return slots;
    },
  },
  master: {
    name: "Master • Imperial Turtle",
    tileCount: 144,
    generateSlots() {
      const slots = [];
      // Classic 5-layer 144-tile Imperial Turtle formation
      // Layer 0: 12x8 main shell (86 tiles with rounded turtle shape)
      for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 12; c++) {
          const corner = (r === 0 || r === 7) && (c < 2 || c > 9);
          if (!corner) slots.push({ c: c - 5.5, r: r - 3.5, l: 0 });
        }
      }
      // Flank tiles: Left & Right turtle flippers (4 tiles)
      slots.push({ c: -6.6, r: -0.5, l: 0 });
      slots.push({ c: -6.6, r: 0.5, l: 0 });
      slots.push({ c: 6.6, r: -0.5, l: 0 });
      slots.push({ c: 6.6, r: 0.5, l: 0 });

      // Layer 1: 8x6 turtle heart (36 tiles)
      for (let r = 0; r < 6; r++) {
        for (let c = 0; c < 6; c++) {
          slots.push({ c: c - 2.5, r: r - 2.5, l: 1 });
        }
      }

      // Layer 2: 4x4 inner shell (16 tiles)
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
          slots.push({ c: c - 1.5, r: r - 1.5, l: 2 });
        }
      }

      // Layer 3: 2x2 carapace crest (4 tiles)
      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 2; c++) {
          slots.push({ c: c - 0.5, r: r - 0.5, l: 3 });
        }
      }

      // Layer 4: 1 pinnacle turtle crown jewel (cut or padded to exactly 144)
      while (slots.length > 144) slots.pop();
      while (slots.length < 144) {
        slots.push({ c: 0, r: 0, l: 4 });
      }
      return slots;
    },
  },
};

class MahjongSolitaireApp {
  constructor() {
    this.container = document.getElementById("canvas-container");
    this.manifest = null;
    this.tiles = [];
    this.selectedTile = null;
    this.score = 0;
    this.combo = 1;
    this.movesHistory = [];
    this.isDemoRunning = false;
    this.isPairPauseActive = false;
    this.activeSurface = "table"; // "table" or "pavement"
    const urlParams = new URLSearchParams(window.location.search);
    this.oniricaMode = urlParams.get("onirica") === "1";
    this.activeCameraPreset = urlParams.get("2d") === "1" ? "2d" : "hero";

    // Look-Dev Settings with Defaults matching Blender Cycles Master Renders
    this.settings = {
      sunIntensity: 3.8,
      sunElevation: 46,
      sunAzimuth: 32,
      lanternGlow: 2.4,
      ambient: 0.75,
      exposure: 1.10,
      marbleRoughness: 0.14,
      marbleClearcoat: 0.35,
      obsidianMetallic: 0.22,
      bassorilievo: 1.15,
      normalScale: 1.0,
      fov: 38,
      camDistance: 11.5,
      autoRotate: false,
      shadows: true,
    };

    this.tweens = [];
    this.initThree();
    this.initLights();
    this.loadManifestAndAssets();
    this.bindUI();
    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  initThree() {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x120f14);

    this.camera = new THREE.PerspectiveCamera(this.settings.fov, window.innerWidth / window.innerHeight, 0.1, 100);

    this.renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = this.settings.exposure;
    this.renderer.shadowMap.enabled = this.settings.shadows;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.container.appendChild(this.renderer.domElement);

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.maxPolarAngle = Math.PI / 2 - 0.04;
    this.controls.minDistance = 3.0;
    this.controls.maxDistance = 28.0;

    this.setCameraPreset(this.activeCameraPreset);

    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();

    window.addEventListener("resize", () => {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });

    this.renderer.domElement.addEventListener("pointerdown", (e) => this.onPointerDown(e));
  }

  initLights() {
    this.ambientLight = new THREE.AmbientLight(0xfff1dc, this.settings.ambient);
    this.scene.add(this.ambientLight);

    this.sunLight = new THREE.DirectionalLight(0xffeed4, this.settings.sunIntensity);
    this.sunLight.castShadow = true;
    this.sunLight.shadow.mapSize.width = 2048;
    this.sunLight.shadow.mapSize.height = 2048;
    this.sunLight.shadow.camera.near = 1.0;
    this.sunLight.shadow.camera.far = 40.0;
    const d = 12;
    this.sunLight.shadow.camera.left = -d;
    this.sunLight.shadow.camera.right = d;
    this.sunLight.shadow.camera.top = d;
    this.sunLight.shadow.camera.bottom = -d;
    this.sunLight.shadow.bias = -0.0004;
    this.scene.add(this.sunLight);

    // Warm Silk Lantern Glows around Courtyard
    this.lanternLights = [];
    const lanternCoords = [
      [-7.5, -5.5, 4.2],
      [7.5, -5.5, 4.2],
      [-7.5, 5.5, 4.2],
      [7.5, 5.5, 4.2],
    ];
    lanternCoords.forEach(([lx, ly, lz]) => {
      const pLight = new THREE.PointLight(0xff8833, this.settings.lanternGlow, 18, 1.2);
      pLight.position.set(lx, lz, ly); // Three.js Y-up
      this.scene.add(pLight);
      this.lanternLights.push(pLight);
    });

    this.updateSunPosition();
  }

  updateSunPosition() {
    const phi = THREE.MathUtils.degToRad(90 - this.settings.sunElevation);
    const theta = THREE.MathUtils.degToRad(this.settings.sunAzimuth);
    const dist = 18.0;
    this.sunLight.position.set(
      dist * Math.sin(phi) * Math.cos(theta),
      dist * Math.cos(phi),
      dist * Math.sin(phi) * Math.sin(theta)
    );
    this.sunLight.intensity = this.settings.sunIntensity;
    this.ambientLight.intensity = this.settings.ambient;
    this.lanternLights.forEach((l) => (l.intensity = this.settings.lanternGlow));
    this.renderer.toneMappingExposure = this.settings.exposure;
  }

  async loadManifestAndAssets() {
    const loader = new GLTFLoader();
    const texLoader = new THREE.TextureLoader();

    // 1. Load Manifest
    const res = await fetch("./textures/manifest.json");
    this.manifest = await res.json();

    // Preload PBR Textures
    this.pbrTextures = {
      marbleBase: texLoader.load("./textures/pbr/marble_basecolor_2k.png"),
      marbleNorm: texLoader.load("./textures/pbr/marble_normal_2k.png"),
      obsidianBase: texLoader.load("./textures/pbr/obsidian_basecolor_2k.png"),
      obsidianNorm: texLoader.load("./textures/pbr/obsidian_normal_2k.png"),
      rosewoodBase: texLoader.load("./textures/pbr/rosewood_basecolor_2k.png"),
      jadeBase: texLoader.load("./textures/pbr/jade_basecolor_2k.png"),
      pavementBase: texLoader.load("./textures/pbr/pavement_basecolor_2k.png"),
      pavementNorm: texLoader.load("./textures/pbr/pavement_normal_2k.png"),
    };
    Object.values(this.pbrTextures).forEach((t) => {
      t.wrapS = THREE.RepeatWrapping;
      t.wrapT = THREE.RepeatWrapping;
    });

    // 2. Load 3D Temple Environment GLB (Blender glTF exporter ALREADY outputs +Y Up!)
    loader.load("./models/temple_environment.glb", (gltf) => {
      this.templeEnv = gltf.scene;
      // IMPORTANT: Do NOT rotate templeEnv by -PI/2 around X! glTF is already +Y Up; rotating it turned the horizontal table & floor into a vertical wall cutting the board in half!
      this.templeEnv.rotation.set(0, 0, 0);
      this.templeEnv.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true;
          child.receiveShadow = true;
        }
      });
      this.scene.add(this.templeEnv);
      this.cacheEnvironmentObjects();
      this.updateEnvironmentVisibility();
    });

    // 3. Load Canonical Tile GLB
    loader.load("./models/tile_generic_white_marble_obsidian.glb", (gltf) => {
      this.canonicalTileScene = gltf.scene;
      this.canonicalTileAnimations = gltf.animations;
      this.setupBoard("master");
    });
  }

  cacheEnvironmentObjects() {
    if (!this.templeEnv) return;
    this.envTable = this.templeEnv.getObjectByName("Low_Rosewood_Jade_Table");
    this.envLegs = [];
    for (let i = 1; i <= 4; i++) {
      const leg = this.templeEnv.getObjectByName(`Rosewood_Table_Leg_${i}`);
      if (leg) this.envLegs.push(leg);
    }
    this.envOverheadObstacles = [];
    this.templeEnv.traverse((child) => {
      if (
        child.isMesh &&
        (child.name.startsWith("Temple_Crimson_Pillar") || child.name.startsWith("Temple_Silk_Lantern"))
      ) {
        this.envOverheadObstacles.push(child);
      }
    });
  }

  updateEnvironmentVisibility() {
    if (!this.envOverheadObstacles || !this.camera) return;
    const isTopView = this.activeCameraPreset === "2d" || this.activeCameraPreset === "topdown";
    const camPos = this.camera.position;
    const camDistToCenter = Math.hypot(camPos.x, camPos.z);

    this.envOverheadObstacles.forEach((mesh) => {
      if (isTopView) {
        mesh.visible = false;
        return;
      }
      // If a pillar/lantern is on the camera side of the board and could cross the camera frustum, hide it so it NEVER blocks the board
      const box = new THREE.Box3().setFromObject(mesh);
      const center = new THREE.Vector3();
      box.getCenter(center);
      const dotSide = center.x * camPos.x + center.z * camPos.z;
      const objDist = Math.hypot(center.x, center.z);
      mesh.visible = !(dotSide > 0 && camDistToCenter > objDist - 3.5);
    });
  }

  setupBoard(trackKey = "master") {
    // Clear old tiles
    this.tiles.forEach((t) => this.scene.remove(t.root));
    this.tiles = [];
    this.selectedTile = null;
    this.isPairPauseActive = false;
    this.movesHistory = [];
    this.combo = 1;
    this.hideSelectionCard();
    this.updateHUD();

    const track = TRACK_LAYOUTS[trackKey] || TRACK_LAYOUTS.master;
    const slots = track.generateSlots();

    // Mathematically Solvable Deck Pair Allocator (Reverse-Peel Solvable Guarantee)
    const pairsNeeded = Math.floor(slots.length / 2);
    const deckPairs = this.generateDeckPairs(pairsNeeded);
    const deck = this.assignSolvableDeckToSlots(slots, deckPairs);

    // Build Tile Meshes and place onto board
    const texLoader = new THREE.TextureLoader();
    const surfaceYOffset = this.activeSurface === "table" ? 0.28 : -0.45;

    if (!this.faceTextureCache) this.faceTextureCache = {};
    this.initSharedTileResources();

    slots.forEach((slot, idx) => {
      const tileData = deck[idx];
      const tileInstance = this.createTileMesh(tileData, texLoader);

      // Three.js Coordinate mapping: X = slot.c * width, Y = layer * depth + base, Z = slot.r * height
      const x = slot.c * (TILE_W * 1.03);
      const y = surfaceYOffset + slot.l * (TILE_D * 1.02);
      const z = slot.r * (TILE_H * 1.03);

      tileInstance.position.set(x, y, z);
      this.scene.add(tileInstance);

      this.tiles.push({
        id: `tile_${idx}`,
        data: tileData,
        slot: slot,
        root: tileInstance,
        basePos: new THREE.Vector3(x, y, z),
        baseRot: new THREE.Euler(0, 0, 0),
        removed: false,
        selected: false,
      });
    });

    this.updateFreeTiles();
    this.updateHUD();
  }

  makeHollowRectShape(outerW, outerH, innerW, innerH) {
    const shape = new THREE.Shape();
    shape.moveTo(-outerW / 2, -outerH / 2);
    shape.lineTo(outerW / 2, -outerH / 2);
    shape.lineTo(outerW / 2, outerH / 2);
    shape.lineTo(-outerW / 2, outerH / 2);
    shape.closePath();

    const hole = new THREE.Path();
    hole.moveTo(-innerW / 2, -innerH / 2);
    hole.lineTo(innerW / 2, -innerH / 2);
    hole.lineTo(innerW / 2, innerH / 2);
    hole.lineTo(-innerW / 2, innerH / 2);
    hole.closePath();
    shape.holes.push(hole);
    return shape;
  }

  makeHollowRectGeometry(outerW, outerH, innerW, innerH) {
    return new THREE.ShapeGeometry(this.makeHollowRectShape(outerW, outerH, innerW, innerH));
  }

  initSharedTileResources() {
    if (this.sharedGeo) return;
    const collarShape = this.makeHollowRectShape(TILE_W, TILE_H, TILE_W * 0.90, TILE_H * 0.91);
    const collarGeo = new THREE.ExtrudeGeometry(collarShape, { depth: 0.080, bevelEnabled: false });
    collarGeo.rotateX(-Math.PI / 2);

    this.sharedGeo = {
      // Lowered inner cavity floor (-0.076) so downward-displaced 3D carved grooves ('il buco bassorilievo') are NEVER clipped!
      body: new THREE.BoxGeometry(TILE_W, TILE_D - 0.076, TILE_H),
      topCollar: collarGeo,
      kintsugi: new THREE.BoxGeometry(TILE_W * 1.004, TILE_D * 0.06, TILE_H * 1.004),
      // 72x96 high-density subdivided face mesh so displacementMap physically carves 3D grooves & pits into the tile!
      face: new THREE.PlaneGeometry(TILE_W * 0.94, TILE_H * 0.95, 72, 96),
      // Top-center golden crown inlay bar (never occludes top-left or top-right corner glyphs!)
      badge: new THREE.BoxGeometry(0.24, 0.016, 0.032),
      // Yellow-Purple Selection Double Border ("bordino giallo-viola")
      selOuterPurple: this.makeHollowRectGeometry(TILE_W * 1.12, TILE_H * 1.10, TILE_W * 1.01, TILE_H * 1.00),
      selInnerYellow: this.makeHollowRectGeometry(TILE_W * 1.01, TILE_H * 1.00, TILE_W * 0.90, TILE_H * 0.91),
    };
    this.sharedMat = {
      obsidian: new THREE.MeshStandardMaterial({
        color: 0x111116,
        map: this.pbrTextures.obsidianBase,
        normalMap: this.pbrTextures.obsidianNorm,
        normalScale: new THREE.Vector2(0.22 * this.settings.normalScale, 0.22 * this.settings.normalScale),
        roughness: 0.10,
        metalness: this.settings.obsidianMetallic,
      }),
      kintsugiGold: new THREE.MeshStandardMaterial({
        color: 0xf0c850,
        metalness: 0.92,
        roughness: 0.18,
      }),
      badgeCoupled: new THREE.MeshStandardMaterial({
        color: 0xf5d470,
        metalness: 0.90,
        roughness: 0.20,
      }),
      badgeStandard: new THREE.MeshStandardMaterial({
        color: 0xd4af37,
        metalness: 0.88,
        roughness: 0.22,
      }),
      selPurple: new THREE.MeshBasicMaterial({
        color: 0xa832ff,
        side: THREE.DoubleSide,
      }),
      selYellow: new THREE.MeshBasicMaterial({
        color: 0xffe600,
        side: THREE.DoubleSide,
      }),
    };
  }

  generateDeckPairs(numPairs) {
    const allDeckTiles = this.manifest.tiles;
    // Categorize into Coupled Family Quartets/Pairs vs Original Traditional Suits
    const coupled = allDeckTiles.filter((t) => t.coupled);
    const standard = allDeckTiles.filter((t) => !t.coupled);

    // Prioritize our 4 signature Bamboo & Gold emblems + Enlarged 2/4 Dots + Carved Dragons & Characters!
    const priorityIds = new Set([
      "dots_2",
      "dots_4",
      "char_8",
      "bamboo_1",
      "bamboo_2",
      "bamboo_3",
      "bamboo_4",
      "dragon_red",
      "dragon_green",
      "dragon_white",
    ]);
    const prioritySuits = standard.filter((t) => priorityIds.has(t.id));
    const otherSuits = standard.filter((t) => !priorityIds.has(t.id));
    const orderedStandard = [...prioritySuits, ...otherSuits];

    const deckPairs = [];
    let pairCount = 0;

    // Proportional Family Cardinality (~18% of board pairs, capped at 8 pairs on 144-tile Master board)
    const maxCoupledPairs = Math.max(3, Math.min(8, Math.round(numPairs * 0.18)));

    const coupledThemes = {};
    coupled.forEach((t) => {
      coupledThemes[t.matchGroup] = coupledThemes[t.matchGroup] || [];
      coupledThemes[t.matchGroup].push(t);
    });

    Object.values(coupledThemes).forEach((groupList) => {
      if (pairCount >= maxCoupledPairs) return;
      const list = [...groupList];
      if (list.length > 2) {
        for (let i = list.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [list[i], list[j]] = [list[j], list[i]];
        }
      }
      for (let k = 0; k + 1 < list.length && pairCount < maxCoupledPairs && pairCount < numPairs; k += 2) {
        deckPairs.push([list[k], list[k + 1]]);
        pairCount++;
      }
    });

    // Fill remaining pairs from authentic Traditional Mahjong suits
    let stdIdx = 0;
    while (pairCount < numPairs) {
      const st = orderedStandard[stdIdx % orderedStandard.length];
      deckPairs.push([st, st]);
      pairCount++;
      stdIdx++;
    }

    // Shuffle the order of pairs
    for (let i = deckPairs.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [deckPairs[i], deckPairs[j]] = [deckPairs[j], deckPairs[i]];
    }

    return deckPairs;
  }

  assignSolvableDeckToSlots(slots, deckPairs) {
    // True Reverse-Peel Solvable Generator:
    // Simulates peeling pairs of free slots until the board is empty, assigning a matching pair to each peeled slot pair.
    const n = slots.length;
    const assigned = new Array(n).fill(null);
    const remainingIndices = new Set(slots.map((_, idx) => idx));

    const isSlotFreeSim = (idx) => {
      const s = slots[idx];
      for (const otherIdx of remainingIndices) {
        if (otherIdx === idx) continue;
        const o = slots[otherIdx];
        if (o.l === s.l + 1 && Math.abs(o.c - s.c) < 0.95 && Math.abs(o.r - s.r) < 0.95) {
          return false;
        }
      }
      let leftBlocked = false;
      let rightBlocked = false;
      for (const otherIdx of remainingIndices) {
        if (otherIdx === idx) continue;
        const o = slots[otherIdx];
        if (o.l === s.l && Math.abs(o.r - s.r) < 0.8) {
          const dc = o.c - s.c;
          if (dc > 0.8 && dc < 1.3) rightBlocked = true;
          if (dc < -0.8 && dc > -1.3) leftBlocked = true;
        }
      }
      return !leftBlocked || !rightBlocked;
    };

    let pairIdx = 0;
    while (remainingIndices.size >= 2 && pairIdx < deckPairs.length) {
      const freeList = [];
      for (const idx of remainingIndices) {
        if (isSlotFreeSim(idx)) freeList.push(idx);
      }
      let idxA, idxB;
      if (freeList.length >= 2) {
        freeList.sort((a, b) => slots[b].l - slots[a].l + (Math.random() - 0.5) * 0.8);
        idxA = freeList[0];
        idxB = freeList[1];
      } else {
        const remArr = Array.from(remainingIndices);
        idxA = remArr[0];
        idxB = remArr[1];
      }
      const [tileA, tileB] = deckPairs[pairIdx++];
      assigned[idxA] = tileA;
      assigned[idxB] = tileB;
      remainingIndices.delete(idxA);
      remainingIndices.delete(idxB);
    }

    return assigned;
  }

  createTileMesh(tileData, texLoader) {
    const root = new THREE.Group();

    // 1. Tile Body: Imperial White Marble + Black Obsidian Backing (recessed top cavity for 3D carved grooves)
    const marbleMat = new THREE.MeshPhysicalMaterial({
      color: 0xfcf8ee,
      map: this.pbrTextures.marbleBase,
      normalMap: this.pbrTextures.marbleNorm,
      normalScale: new THREE.Vector2(0.18 * this.settings.normalScale, 0.18 * this.settings.normalScale),
      roughness: this.settings.marbleRoughness,
      clearcoat: this.settings.marbleClearcoat,
      clearcoatRoughness: 0.1,
    });

    const bodyMaterials = [
      marbleMat, // +X
      marbleMat, // -X
      marbleMat, // +Y inner cavity floor
      this.sharedMat.obsidian, // -Y bottom back
      marbleMat, // +Z
      marbleMat, // -Z
    ];
    const bodyMesh = new THREE.Mesh(this.sharedGeo.body, bodyMaterials);
    bodyMesh.position.y = -0.038;
    bodyMesh.castShadow = true;
    bodyMesh.receiveShadow = true;
    root.add(bodyMesh);

    // 1a. Outer Marble Top Collar Frame (flush with +TILE_D * 0.5 around the 3D carved face window)
    const collarMesh = new THREE.Mesh(this.sharedGeo.topCollar, marbleMat);
    collarMesh.position.y = TILE_D * 0.5 - 0.080;
    collarMesh.castShadow = true;
    collarMesh.receiveShadow = true;
    root.add(collarMesh);

    // 1b. Gold Kintsugi Waist Seam (between White Marble upper body and Black Obsidian base)
    const kintsugiMesh = new THREE.Mesh(this.sharedGeo.kintsugi, this.sharedMat.kintsugiGold);
    kintsugiMesh.position.y = -TILE_D * 0.12;
    root.add(kintsugiMesh);

    // 2. 3D Incandescent-Pen Carved Face Overlay (72x96 subdivided mesh with real vertex displacement + high-slope normal map!)
    if (!this.faceTextureCache[tileData.id]) {
      const faceTex = texLoader.load(`./textures/tiles/${tileData.id}.png`);
      faceTex.colorSpace = THREE.SRGBColorSpace;
      const oniricaTex = texLoader.load(`./textures/tiles_onirica/${tileData.id}.png`);
      oniricaTex.colorSpace = THREE.SRGBColorSpace;
      const normTex = texLoader.load(`./textures/tiles_normal/${tileData.id}_normal.png`);
      const depthTex = texLoader.load(`./textures/tiles_depth/${tileData.id}_depth.png`);
      this.faceTextureCache[tileData.id] = { faceTex, oniricaTex, normTex, depthTex };
    }
    const { faceTex, oniricaTex, normTex, depthTex } = this.faceTextureCache[tileData.id];

    const activeMap = this.oniricaMode ? oniricaTex : faceTex;
    const activeRelief = this.oniricaMode ? 0.12 : this.settings.bassorilievo;
    const dispScale = 0.076 * activeRelief;

    const faceMat = new THREE.MeshStandardMaterial({
      map: activeMap,
      normalMap: normTex,
      normalScale: new THREE.Vector2(1.45 * activeRelief, 1.45 * activeRelief),
      displacementMap: depthTex,
      displacementScale: dispScale,
      displacementBias: -0.88 * dispScale,
      roughness: this.oniricaMode ? 0.11 : 0.17,
      metalness: 0.08,
    });
    const faceMesh = new THREE.Mesh(this.sharedGeo.face, faceMat);
    faceMesh.rotation.x = -Math.PI / 2;
    faceMesh.position.y = TILE_D * 0.5 + 0.002;
    faceMesh.castShadow = true;
    faceMesh.receiveShadow = true;
    root.add(faceMesh);

    // 3. Alphabet_Glyph_Mesh (Top-Center Golden Crown Inlay Bar — never occludes top-left or top-right corner glyphs!)
    const badgeMesh = new THREE.Mesh(
      this.sharedGeo.badge,
      tileData.coupled ? this.sharedMat.badgeCoupled : this.sharedMat.badgeStandard
    );
    badgeMesh.position.set(0.0, TILE_D * 0.5 + 0.014, -TILE_H * 0.422);
    badgeMesh.castShadow = true;
    root.add(badgeMesh);

    // 4. Yellow-Purple Selection Double Border ("bordino giallo-viola" when tile 1 or tile 2 is selected!)
    const selectionBorder = new THREE.Group();
    const outerPurpleMesh = new THREE.Mesh(this.sharedGeo.selOuterPurple, this.sharedMat.selPurple);
    const innerYellowMesh = new THREE.Mesh(this.sharedGeo.selInnerYellow, this.sharedMat.selYellow);
    outerPurpleMesh.rotation.x = -Math.PI / 2;
    innerYellowMesh.rotation.x = -Math.PI / 2;
    innerYellowMesh.position.y = 0.002;
    selectionBorder.add(outerPurpleMesh);
    selectionBorder.add(innerYellowMesh);
    selectionBorder.position.y = TILE_D * 0.5 + 0.012;
    selectionBorder.visible = false;
    root.add(selectionBorder);

    // Keep reference on root
    root.userData = {
      tileData: tileData,
      faceMesh: faceMesh,
      badgeMesh: badgeMesh,
      bodyMesh: bodyMesh,
      collarMesh: collarMesh,
      kintsugiMesh: kintsugiMesh,
      selectionBorder: selectionBorder,
    };

    return root;
  }

  isTileFree(tile) {
    if (tile.removed) return false;
    const { c, r, l } = tile.slot;

    // 1. Is any tile resting on top of it in layer l + 1?
    for (let other of this.tiles) {
      if (other.removed || other === tile) continue;
      if (other.slot.l === l + 1) {
        if (Math.abs(other.slot.c - c) < 0.95 && Math.abs(other.slot.r - r) < 0.95) {
          return false; // Covered by tile above
        }
      }
    }

    // 2. Is either left OR right long side unblocked in the same layer l?
    let leftBlocked = false;
    let rightBlocked = false;

    for (let other of this.tiles) {
      if (other.removed || other === tile) continue;
      if (other.slot.l === l && Math.abs(other.slot.r - r) < 0.8) {
        const dc = other.slot.c - c;
        if (dc > 0.8 && dc < 1.3) rightBlocked = true;
        if (dc < -0.8 && dc > -1.3) leftBlocked = true;
      }
    }

    return !leftBlocked || !rightBlocked;
  }

  updateFreeTiles() {
    let freeCount = 0;
    const freeTiles = [];

    this.tiles.forEach((t) => {
      const free = this.isTileFree(t);
      t.isFree = free;
      if (free) {
        freeCount++;
        freeTiles.push(t);
      }
      // Subtle visual state
      if (!t.removed && !t.selected) {
        t.root.userData.bodyMesh.material[0].color.setHex(free ? 0xfcf8ee : 0xe2ded4);
      }
    });

    // Count matching free pairs
    let matchablePairs = 0;
    for (let i = 0; i < freeTiles.length; i++) {
      for (let j = i + 1; j < freeTiles.length; j++) {
        if (this.areTilesMatching(freeTiles[i].data, freeTiles[j].data)) {
          matchablePairs++;
        }
      }
    }

    document.getElementById("stat-free-pairs").textContent = matchablePairs;
    return { freeTiles, matchablePairs };
  }

  areTilesMatching(t1, t2) {
    if (t1.coupled && t2.coupled) {
      // Supports both Cardinality 4 Quartets (any 2 in quartet_family_seasons / quartet_magic_flowers match!)
      // and Cardinality 2 Diptyque Split-Pairs (pair_E_great_wall .. pair_H_chengdu_pandas)!
      return t1.matchGroup === t2.matchGroup;
    }
    return t1.id === t2.id; // Exact traditional suit match
  }

  onPointerDown(e) {
    if (this.isDemoRunning || this.isPairPauseActive) return;
    this.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    this.mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

    this.raycaster.setFromCamera(this.mouse, this.camera);
    const intersects = this.raycaster.intersectObjects(this.tiles.map((t) => t.root), true);

    if (intersects.length > 0) {
      let hitRoot = intersects[0].object;
      while (hitRoot.parent && !hitRoot.userData.tileData) {
        hitRoot = hitRoot.parent;
      }

      const hitTile = this.tiles.find((t) => t.root === hitRoot);
      if (hitTile && !hitTile.removed) {
        this.handleTileClick(hitTile);
      }
    }
  }

  handleTileClick(tile) {
    if (this.isPairPauseActive) return;
    if (!this.isTileFree(tile)) {
      sfx.playError();
      this.wiggleTile(tile);
      return;
    }

    sfx.playClick();

    if (!this.selectedTile) {
      // 1st Tile Selected -> Show Yellow-Purple Border ("bordino giallo-viola") on 1st tile!
      this.selectedTile = tile;
      tile.selected = true;
      this.liftTile(tile, true);
      this.showSelectionCard(tile);
    } else if (this.selectedTile === tile) {
      // Deselect clicked tile
      this.liftTile(tile, false);
      tile.selected = false;
      this.selectedTile = null;
      this.hideSelectionCard();
    } else {
      // 2nd Tile Clicked -> Attempt Match!
      const first = this.selectedTile;
      if (this.areTilesMatching(first.data, tile.data)) {
        // MATCH SUCCESS!
        // Show 2nd Yellow-Purple Border ("altro bordino giallo-viola") on 2nd tile too & wait 550ms ("mezzo secondo") before removing!
        sfx.playMatch();
        this.selectedTile = null;
        tile.selected = true;
        this.liftTile(tile, true);
        this.showPairMatchCard(first, tile);
        this.isPairPauseActive = true;

        this.score += 100 * this.combo;
        this.combo++;
        this.movesHistory.push([first, tile]);
        this.updateHUD();

        setTimeout(() => {
          first.selected = false;
          tile.selected = false;
          if (first.root.userData.selectionBorder) first.root.userData.selectionBorder.visible = false;
          if (tile.root.userData.selectionBorder) tile.root.userData.selectionBorder.visible = false;
          this.hideSelectionCard();
          this.isPairPauseActive = false;
          this.animatePairMatch(first, tile);
        }, 550);
      } else {
        // Mismatch: drop first, select second with Yellow-Purple border
        sfx.playError();
        this.liftTile(first, false);
        first.selected = false;
        this.combo = 1;

        this.selectedTile = tile;
        tile.selected = true;
        this.liftTile(tile, true);
        this.showSelectionCard(tile);
      }
    }

    this.updateHUD();
  }

  liftTile(tile, liftUp) {
    const is2D = this.activeCameraPreset === "2d";
    const targetY = tile.basePos.y + (liftUp ? 0.35 : 0.0);
    const targetTilt = liftUp && !is2D ? 0.16 : 0.0;
    this.addTween(tile.root.position, "y", targetY, 0.15);
    this.addTween(tile.root.rotation, "x", targetTilt, 0.15);
    tile.root.userData.bodyMesh.material[0].emissive = new THREE.Color(liftUp ? 0x3b155e : 0x000000);
    if (tile.root.userData.selectionBorder) {
      tile.root.userData.selectionBorder.visible = Boolean(liftUp);
    }
  }

  wiggleTile(tile) {
    const origX = tile.basePos.x;
    const t0 = performance.now();
    this.tweens.push({
      update(now) {
        const dt = (now - t0) / 180;
        if (dt < 1.0) {
          tile.root.position.x = origX + Math.sin(dt * Math.PI * 4) * 0.08;
          return false;
        }
        tile.root.position.x = origX;
        return true;
      },
    });
  }

  animatePairMatch(tileA, tileB) {
    tileA.removed = true;
    tileB.removed = true;

    // Celebratory pair arc spin & implosive disappear
    [tileA, tileB].forEach((t) => {
      const origPos = t.root.position.clone();
      const t0 = performance.now();
      this.tweens.push({
        update(now) {
          const dt = (now - t0) / 420;
          if (dt < 1.0) {
            t.root.position.y = origPos.y + Math.sin(dt * Math.PI) * 0.85;
            t.root.rotation.y = dt * Math.PI * 2;
            const s = Math.max(0.01, 1.0 - Math.pow(dt, 3));
            t.root.scale.set(s, s, s);
            return false;
          }
          t.root.visible = false;
          return true;
        },
      });
    });

    setTimeout(() => {
      const { matchablePairs } = this.updateFreeTiles();
      this.updateHUD();
      this.checkGameEnd(matchablePairs);
    }, 450);
  }

  checkGameEnd(matchablePairs) {
    const remaining = this.tiles.filter((t) => !t.removed).length;
    if (remaining === 0) {
      document.getElementById("vic-score").textContent = this.score;
      document.getElementById("vic-moves").textContent = this.movesHistory.length;
      document.getElementById("vic-combo").textContent = `x${this.combo}`;
      document.getElementById("victory-modal").classList.remove("hidden");
    } else if (matchablePairs === 0) {
      // Auto-offer shuffle when no moves remain
      const toast = document.getElementById("sel-status");
      if (toast) toast.textContent = "No matchable pairs remain — click Shuffle to continue solvably!";
    }
  }

  getDidYouKnowLore(d) {
    const loreMap = {
      bamboo_1: "1索 (Yī Suǒ) is the only suit tile that depicts a bird — the Imperial Sparrow (麻雀, Máquè), after which Mahjong ('Clattering Sparrows') is named!",
      bamboo_2: "2索 (Èr Suǒ) fuses Sebi & Ale's passion for Hot Wheels flame supercars with carved green bamboo stalks, celadon jade, and 24k gold filigree!",
      bamboo_3: "3索 (Sān Suǒ) honors Sirio il Dragone (Dragon Shiryu from Saint Seiya), forging his indestructible emerald Dragon Shield in Imperial Jade & 24k gold!",
      bamboo_4: "4索 (Sì Suǒ) symbolizes the Four Cardinal Virtues, reimagined here with Ale's favorite faceted crimson rubies, diamonds, and emeralds in golden dragon claws!",
      dragon_red: "中 (Hóng Zhōng, Red Center) symbolizes passing the Imperial Mandarin examination and hitting the bullseye of fortune!",
      dragon_green: "發 (Fā Cái, Green Prosperity) comes from 'Gong Xi Fa Cai' — wishing overflowing wealth, growth, and springtime jade vitality!",
      dragon_white: "白 (Bái Bǎn, White Jade Tablet) represents pure, uncarved flawlessness and limitless beginnings in Taoist philosophy.",
      wind_E: "東 (Dōng, East Wind) is the seat of the prevailing dealer in traditional Chinese Mahjong and heralds the rising dawn.",
      wind_S: "南 (Nán, South Wind) symbolizes summer warmth, vermilion fire, and the imperial throne's southward gaze.",
      wind_W: "西 (Xī, West Wind) represents autumn harvest, golden metal, and the serene sunset over mountain temples.",
      wind_N: "北 (Běi, North Wind) embodies winter stillness, deep tortoise water wisdom, and starry polar skies.",
      coupled_A1: "S1 春 (Spring) features Papà Riccardo (NB21) — as a Cardinality-4 Season tile, he matches with ANY of Mamma Kate (S2), Ale (S3), or Sebi (S4)!",
      coupled_A2: "S2 夏 (Summer) features Mamma Kate 2016 (NB21, acqua e sapone) — as a Cardinality-4 Season tile, she pairs with ANY Carlesso family member!",
      coupled_B1: "S3 秋 (Autumn) features Solo Alessandro in Tang crimson & gold silk — matches with Papà, Mamma, or Sebi in the Family Quartet!",
      coupled_B2: "S4 冬 (Winter) features Solo Sebastian in Tang crimson & gold silk — matches with Papà, Mamma, or Ale in the Family Quartet!",
      coupled_C1: "M1 梅 (Plum Blossom) pairs Ale with nerdy calico guinea pig Ghigna 🐹 — matches ANY of the 4 Magical Companion tiles (M1..M4)!",
      coupled_C2: "M2 蘭 (Orchid) pairs Sebi with friendly purple monster Pupurabbu 👾 — matches ANY of the 4 Magical Companion tiles (M1..M4)!",
      coupled_D1: "M3 菊 (Chrysanthemum) showcases Mandarin Scholar Ghigna 🐹 with his jade abacus — matches ANY Magical Companion tile!",
      coupled_D2: "M4 竹 (Bamboo Flower) showcases Solo Pupurabbu 👾 holding a glowing silk lantern — matches ANY Magical Companion tile!",
    };
    if (loreMap[d.id]) return loreMap[d.id];
    if (d.coupled) {
      return `Diptyque Split-Pair (${d.code}): generated as ONE shared 2D scene of Ale & Sebi together and sliced in half so Solo Ale (Left) reunites with Solo Sebi (Right)!`;
    }
    const numMatch = d.id.match(/_(\d+)$/);
    const n = numMatch ? parseInt(numMatch[1], 10) : 1;
    const numLore = {
      1: "the number 1 (一, Yī) symbolizes primordial unity, the origin of all things (Tao), and auspicious new beginnings.",
      2: "the number 2 (二, Èr) embodies the Chinese proverb 'Hǎoshì Chéng Shuāng' (好事成雙) — good things always come in pairs!",
      3: "the number 3 (三, Sān) sounds like 'Shēng' (生, life/growth) and represents the Triad of Heaven, Earth, and Humanity.",
      4: "the number 4 (四, Sì) mirrors the Four Directions, Four Seasons, and Four Treasures of the Scholar's Studio (brush, ink, paper, inkstone).",
      5: "the number 5 (五, Wǔ) symbolizes the Five Elements (Wu Xing: Wood, Fire, Earth, Metal, Water) and the Five Imperial Blessings.",
      6: "the number 6 (六, Liù) sounds like 'Liú' (流, smooth flow) — 'Liùliù Dàshùn' wishes that everything in life flows effortlessly!",
      7: "the number 7 (七, Qī) represents togetherness and the cosmic harmony of Yin, Yang, and the Five Elements.",
      8: "the number 8 (八, Bā) is the luckiest number in Chinese culture because it rhymes with 'Fā' (發, boundless prosperity)!",
      9: "the number 9 (九, Jiǔ) sounds identical to 'Jiǔ' (久, eternity/longevity) and was reserved for the Emperor's Nine Dragons!",
    };
    if (d.suit === "characters") {
      return `In the Characters suit (萬子, Wànzi), ${d.glyph} represents ${n * 10000} strung copper coins — and in Chinese tradition, ${numLore[n]}`;
    }
    if (d.suit === "dots") {
      return `In the Circles suit (筒子, Tǒngzi), ${d.glyph} depicts copper coins with a square center (round heaven, square earth) — where ${numLore[n]}`;
    }
    return `In the Bamboos suit (索子, Suǒzi), ${d.glyph} represents strings of 100 copper coins — where ${numLore[n]}`;
  }

  initWow3DPreview() {
    if (this.wowRenderer) return;
    const canvas = document.getElementById("wow-3d-canvas");
    if (!canvas) return;
    this.wowScene = new THREE.Scene();
    this.wowCamera = new THREE.PerspectiveCamera(34, 1, 0.1, 20);
    this.wowCamera.position.set(0, 1.65, 2.75);
    this.wowCamera.lookAt(0, 0, 0);

    this.wowRenderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    this.wowRenderer.setSize(210, 210);
    this.wowRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.wowRenderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.wowRenderer.toneMappingExposure = 1.18;

    const amb = new THREE.AmbientLight(0xfff4e0, 1.15);
    const dir1 = new THREE.DirectionalLight(0xffe6aa, 3.6);
    dir1.position.set(3.5, 4.5, 3.2);
    const dir2 = new THREE.PointLight(0xa832ff, 2.2, 10);
    dir2.position.set(-3, -2, 3);
    // Raking incandescent amber light across the face to accentuate the 3D carved groove cavity ('il buco bassorilievo')
    this.wowRakeLight = new THREE.PointLight(0xffb84d, 3.8, 12);
    this.wowRakeLight.position.set(2.4, 0.8, 2.2);
    this.wowScene.add(amb, dir1, dir2, this.wowRakeLight);

    this.wowGroup = new THREE.Group();
    this.wowScene.add(this.wowGroup);
  }

  updateWow3DPreview(tileA, tileB = null) {
    this.initWow3DPreview();
    const popup = document.getElementById("wow-3d-popup");
    if (!popup || !this.wowGroup) return;

    while (this.wowGroup.children.length > 0) {
      this.wowGroup.remove(this.wowGroup.children[0]);
    }

    const texLoader = new THREE.TextureLoader();
    const cloneA = this.createTileMesh(tileA.data, texLoader);
    cloneA.rotation.x = Math.PI * 0.34;
    if (tileB) {
      const cloneB = this.createTileMesh(tileB.data, texLoader);
      cloneB.rotation.x = Math.PI * 0.34;
      cloneA.position.set(-0.62, 0, 0);
      cloneB.position.set(0.62, 0, 0);
      if (cloneA.userData.selectionBorder) cloneA.userData.selectionBorder.visible = true;
      if (cloneB.userData.selectionBorder) cloneB.userData.selectionBorder.visible = true;
      this.wowGroup.add(cloneA, cloneB);
      this.wowCamera.position.set(0, 1.85, 3.55);
    } else {
      cloneA.position.set(0, 0, 0);
      if (cloneA.userData.selectionBorder) cloneA.userData.selectionBorder.visible = true;
      this.wowGroup.add(cloneA);
      this.wowCamera.position.set(0, 1.55, 2.55);
    }
    this.wowCamera.lookAt(0, 0, 0);

    const badgeEl = document.getElementById("wow-3d-badge");
    const subEl = document.getElementById("wow-3d-subtitle");
    if (badgeEl) badgeEl.textContent = tileB ? "✨ PAIR" : tileA.data.code || tileA.data.glyph;
    if (subEl) subEl.textContent = tileB ? `${tileA.data.code || tileA.data.glyph} ⚡ ${tileB.data.code || tileB.data.glyph}` : tileA.data.title;

    popup.classList.remove("hidden");
  }

  showSelectionCard(tile) {
    const card = document.getElementById("selection-card");
    const badge = document.getElementById("sel-badge");
    const title = document.getElementById("sel-title");
    const status = document.getElementById("sel-status");
    const dyk = document.getElementById("sel-did-you-know");
    const thumb = document.getElementById("sel-thumb");
    const thumb2 = document.getElementById("sel-thumb-2");
    const plusEl = document.getElementById("sel-pair-plus");

    card.classList.remove("pair-matched");
    if (thumb2) thumb2.classList.add("hidden");
    if (plusEl) plusEl.classList.add("hidden");

    if (thumb) {
      const folder = this.oniricaMode ? "tiles_onirica" : "tiles";
      thumb.src = `./textures/${folder}/${tile.data.id}.png`;
    }
    badge.textContent = tile.data.code || tile.data.glyph;
    title.textContent = tile.data.title;
    if (tile.data.coupled) {
      if (tile.data.cardinality === 4) {
        const groupDesc =
          tile.data.matchGroup === "quartet_family_seasons"
            ? "Carlesso Family Quartet (S1 Papà, S2 Mamma, S3 Ale, S4 Sebi)"
            : "Magical Companions Quartet (M1 Ale+Ghigna, M2 Sebi+Pupurabbu, M3 Ghigna, M4 Pupurabbu)";
        status.textContent = `Cardinality 4 • ${groupDesc} — Match ANY 2 of the 4!`;
      } else {
        status.textContent = `Cardinality 2 Diptyque Split-Pair (${tile.data.code}) • Match Solo Ale (Left) ↔ Solo Sebi (Right)!`;
      }
    } else {
      status.textContent = "Traditional Mahjong Card • Match with identical suit tile";
    }
    if (dyk) {
      dyk.innerHTML = `💡 <strong>Did you know?</strong> ${this.getDidYouKnowLore(tile.data)}`;
    }
    card.classList.remove("hidden");
    this.updateWow3DPreview(tile, null);
  }

  showPairMatchCard(tileA, tileB) {
    const card = document.getElementById("selection-card");
    const badge = document.getElementById("sel-badge");
    const title = document.getElementById("sel-title");
    const status = document.getElementById("sel-status");
    const dyk = document.getElementById("sel-did-you-know");
    const thumb = document.getElementById("sel-thumb");
    const thumb2 = document.getElementById("sel-thumb-2");
    const plusEl = document.getElementById("sel-pair-plus");

    const folder = this.oniricaMode ? "tiles_onirica" : "tiles";
    if (thumb) thumb.src = `./textures/${folder}/${tileA.data.id}.png`;
    if (thumb2) {
      thumb2.src = `./textures/${folder}/${tileB.data.id}.png`;
      thumb2.classList.remove("hidden");
    }
    if (plusEl) plusEl.classList.remove("hidden");

    card.classList.add("pair-matched");
    badge.textContent = "✨ COPPIA!";
    title.textContent = `${tileA.data.title} ⚡ ${tileB.data.title}`;
    status.textContent = "Entrambe le tessere selezionate (Giallo-Viola) • Rimozione tra 0.5s...";
    if (dyk) {
      dyk.innerHTML = `💡 <strong>Did you know?</strong> ${this.getDidYouKnowLore(tileB.data)}`;
    }
    card.classList.remove("hidden");
    this.updateWow3DPreview(tileA, tileB);
  }

  hideSelectionCard() {
    const card = document.getElementById("selection-card");
    if (card) {
      card.classList.add("hidden");
      card.classList.remove("pair-matched");
    }
    const popup = document.getElementById("wow-3d-popup");
    if (popup) popup.classList.add("hidden");
  }

  updateHUD() {
    const remaining = this.tiles.filter((t) => !t.removed).length;
    document.getElementById("stat-remaining").textContent = remaining;
    document.getElementById("stat-score").textContent = this.score;
    document.getElementById("stat-combo").textContent = `x${this.combo}`;
  }

  undoLastMove() {
    if (this.movesHistory.length === 0 || this.isPairPauseActive) return;
    const [tileA, tileB] = this.movesHistory.pop();
    [tileA, tileB].forEach((t) => {
      t.removed = false;
      t.selected = false;
      t.root.visible = true;
      t.root.scale.set(1, 1, 1);
      t.root.position.copy(t.basePos);
      t.root.rotation.set(0, 0, 0);
      if (t.root.userData.selectionBorder) t.root.userData.selectionBorder.visible = false;
    });
    this.score = Math.max(0, this.score - 100);
    this.combo = 1;
    this.updateFreeTiles();
    this.updateHUD();
    sfx.playClick();
  }

  provideHint() {
    const { freeTiles } = this.updateFreeTiles();
    for (let i = 0; i < freeTiles.length; i++) {
      for (let j = i + 1; j < freeTiles.length; j++) {
        if (this.areTilesMatching(freeTiles[i].data, freeTiles[j].data)) {
          sfx.playMatch();
          this.pulseTile(freeTiles[i]);
          this.pulseTile(freeTiles[j]);
          return;
        }
      }
    }
    sfx.playError();
  }

  pulseTile(tile) {
    const origY = tile.basePos.y;
    const t0 = performance.now();
    this.tweens.push({
      update(now) {
        const dt = (now - t0) / 400;
        if (dt < 1.0) {
          tile.root.position.y = origY + Math.sin(dt * Math.PI) * 0.4;
          tile.root.userData.bodyMesh.material[0].emissive = new THREE.Color(0x228833);
          return false;
        }
        tile.root.position.y = origY;
        tile.root.userData.bodyMesh.material[0].emissive = new THREE.Color(0x000000);
        return true;
      },
    });
  }

  solvableShuffle() {
    const remainingTiles = this.tiles.filter((t) => !t.removed);
    if (remainingTiles.length === 0) return;

    // Group remaining tile data into valid matching pairs and re-assign via Reverse-Peel
    const pool = remainingTiles.map((t) => t.data);
    const used = new Array(pool.length).fill(false);
    const pairs = [];
    for (let i = 0; i < pool.length; i++) {
      if (used[i]) continue;
      for (let j = i + 1; j < pool.length; j++) {
        if (!used[j] && this.areTilesMatching(pool[i], pool[j])) {
          used[i] = true;
          used[j] = true;
          pairs.push([pool[i], pool[j]]);
          break;
        }
      }
    }
    const remSlots = remainingTiles.map((t) => t.slot);
    const datas =
      pairs.length * 2 === remainingTiles.length
        ? this.assignSolvableDeckToSlots(remSlots, pairs)
        : pool.sort(() => Math.random() - 0.5);

    const texLoader = new THREE.TextureLoader();
    remainingTiles.forEach((tile, i) => {
      tile.data = datas[i] || pool[i];
      if (!this.faceTextureCache[tile.data.id]) {
        const faceTex = texLoader.load(`./textures/tiles/${tile.data.id}.png`);
        faceTex.colorSpace = THREE.SRGBColorSpace;
        const oniricaTex = texLoader.load(`./textures/tiles_onirica/${tile.data.id}.png`);
        oniricaTex.colorSpace = THREE.SRGBColorSpace;
        const normTex = texLoader.load(`./textures/tiles_normal/${tile.data.id}_normal.png`);
        const depthTex = texLoader.load(`./textures/tiles_depth/${tile.data.id}_depth.png`);
        this.faceTextureCache[tile.data.id] = { faceTex, oniricaTex, normTex, depthTex };
      }
      const { faceTex, oniricaTex, normTex, depthTex } = this.faceTextureCache[tile.data.id];
      tile.root.userData.faceMesh.material.map = this.oniricaMode ? oniricaTex : faceTex;
      tile.root.userData.faceMesh.material.normalMap = normTex;
      tile.root.userData.faceMesh.material.displacementMap = depthTex;
      tile.root.userData.faceMesh.material.needsUpdate = true;
      tile.root.userData.badgeMesh.material = tile.data.coupled
        ? this.sharedMat.badgeCoupled
        : this.sharedMat.badgeStandard;
      tile.root.userData.tileData = tile.data;
      this.pulseTile(tile);
    });

    sfx.playMatch();
    this.updateFreeTiles();
    this.updateHUD();
  }

  toggleDemoSolver() {
    this.isDemoRunning = !this.isDemoRunning;
    const btn = document.getElementById("btn-demo");
    btn.textContent = this.isDemoRunning ? "⏹ Stop Demo" : "▶ Demo Auto-Play";
    if (this.isDemoRunning) this.stepDemoSolver();
  }

  stepDemoSolver() {
    if (!this.isDemoRunning) return;
    if (this.isPairPauseActive) {
      setTimeout(() => this.stepDemoSolver(), 250);
      return;
    }
    const remaining = this.tiles.filter((t) => !t.removed).length;
    if (remaining === 0) {
      this.isDemoRunning = false;
      const btn = document.getElementById("btn-demo");
      if (btn) btn.textContent = "▶ Demo Auto-Play";
      return;
    }
    const { freeTiles } = this.updateFreeTiles();
    // Prefer matching Coupled Family Quartet / Diptyque tiles first during Demo Auto-Play!
    const pairs = [];
    for (let i = 0; i < freeTiles.length; i++) {
      for (let j = i + 1; j < freeTiles.length; j++) {
        if (this.areTilesMatching(freeTiles[i].data, freeTiles[j].data)) {
          pairs.push([freeTiles[i], freeTiles[j]]);
        }
      }
    }
    if (pairs.length > 0) {
      pairs.sort((a, b) => (b[0].data.coupled ? 1 : 0) - (a[0].data.coupled ? 1 : 0));
      const [tA, tB] = pairs[0];
      // Step 1: Select 1st tile -> shows 1st Yellow-Purple border ("bordino giallo-viola")
      this.handleTileClick(tA);
      setTimeout(() => {
        if (this.isDemoRunning) {
          // Step 2: Select 2nd tile -> shows 2nd Yellow-Purple border & waits 550ms ("mezzo secondo") before flying away!
          this.handleTileClick(tB);
          setTimeout(() => this.stepDemoSolver(), 1150);
        }
      }, 450);
      return;
    }
    // If no moves, auto-shuffle
    this.solvableShuffle();
    setTimeout(() => this.stepDemoSolver(), 750);
  }

  toggleSurface(forceSurface = null) {
    this.activeSurface = forceSurface || (this.activeSurface === "table" ? "pavement" : "table");
    const nameEl = document.getElementById("surface-name");
    const isTable = this.activeSurface === "table";
    nameEl.textContent = isTable ? "Rosewood Table" : "Stone Pavement";

    // Smoothly lower or raise table model and legs along the Three.js vertical Y axis!
    if (this.envTable) {
      const targetTableY = isTable ? 0.0 : -3.5;
      this.addTween(this.envTable.position, "y", targetTableY, 0.4);
    }
    if (this.envLegs) {
      const targetLegY = isTable ? 0.0 : -3.5;
      this.envLegs.forEach((leg) => this.addTween(leg.position, "y", targetLegY, 0.4));
    }

    // Move tiles to match new surface level
    const targetTileBaseY = isTable ? 0.28 : -0.45;
    this.tiles.forEach((t) => {
      const newY = targetTileBaseY + t.slot.l * (TILE_D * 1.02);
      t.basePos.y = newY;
      this.addTween(t.root.position, "y", newY, 0.35);
    });
  }

  toggleOniricaMode(forceMode = null) {
    this.oniricaMode = forceMode !== null ? forceMode : !this.oniricaMode;
    const nameEl = document.getElementById("onirica-name");
    const btnEl = document.getElementById("btn-onirica-toggle");
    if (nameEl) {
      nameEl.textContent = this.oniricaMode ? "Onirica (Less is More)" : "Classica Ovale";
    }
    if (btnEl) {
      btnEl.classList.toggle("active", this.oniricaMode);
    }

    const activeRelief = this.oniricaMode ? 0.12 : this.settings.bassorilievo;
    const dispScale = 0.076 * activeRelief;
    this.tiles.forEach((t) => {
      const cached = this.faceTextureCache[t.data.id];
      if (!cached) return;
      const mat = t.root.userData.faceMesh.material;
      mat.map = this.oniricaMode ? cached.oniricaTex : cached.faceTex;
      mat.normalScale.set(1.45 * activeRelief, 1.45 * activeRelief);
      mat.displacementScale = dispScale;
      mat.displacementBias = -0.88 * dispScale;
      mat.roughness = this.oniricaMode ? 0.11 : 0.17;
      mat.needsUpdate = true;
      if (t.data.coupled && !t.removed) {
        this.pulseTile(t);
      }
    });

    if (this.selectedTile) {
      this.showSelectionCard(this.selectedTile);
    }
    sfx.playClick();
  }

  toggle2DMode() {
    const nextPreset = this.activeCameraPreset === "2d" ? "hero" : "2d";
    this.setCameraPreset(nextPreset);
    sfx.playClick();
  }

  setCameraPreset(presetKey) {
    const presets = {
      // 2D Anti-Motion-Sickness Flat Overhead View (telephoto FOV 26° from Y=24.5 so all 144 tiles + HUD margins fit 100% inside the screen!)
      "2d": { pos: [0.0, 24.5, 0.001], target: [0.0, 0.2, 0.0], fov: 26 },
      hero: { pos: [0.0, 8.8, 11.6], target: [0.0, 0.3, 0.0], fov: 38 },
      topdown: { pos: [0.0, 15.6, 1.6], target: [0.0, 0.3, 0.0], fov: 40 },
      pavement: { pos: [5.4, 2.6, 8.4], target: [0.0, 0.4, -0.5], fov: 36 },
      macro: { pos: [0.0, 2.1, 6.2], target: [0.0, 0.35, 3.2], fov: 44 },
      orbit: { pos: [0.0, 8.6, 12.0], target: [0.0, 0.4, 0.0], fov: 40 },
    };

    this.activeCameraPreset = presets[presetKey] ? presetKey : "hero";
    const cfg = presets[this.activeCameraPreset];
    this.addTween(this.camera.position, "x", cfg.pos[0], 0.38);
    this.addTween(this.camera.position, "y", cfg.pos[1], 0.38);
    this.addTween(this.camera.position, "z", cfg.pos[2], 0.38);

    if (this.controls) {
      this.controls.target.set(cfg.target[0], cfg.target[1], cfg.target[2]);
      // Lock 3D rotation in 2D mode so the user never experiences 3D motion sickness!
      this.controls.enableRotate = this.activeCameraPreset !== "2d";
    }

    this.settings.fov = cfg.fov;
    this.camera.fov = cfg.fov;
    this.camera.updateProjectionMatrix();

    document.querySelectorAll(".cam-btn").forEach((b) => {
      b.classList.toggle("active", b.dataset.cam === this.activeCameraPreset);
    });

    const btn2d = document.getElementById("btn-2d-toggle");
    const name2d = document.getElementById("view-mode-name");
    if (btn2d) btn2d.classList.toggle("active", this.activeCameraPreset === "2d");
    if (name2d) name2d.textContent = this.activeCameraPreset === "2d" ? "2D Alto (Attivo)" : "Passa a 2D";

    this.updateEnvironmentVisibility();
  }

  applyRigPoseAtFrame(animName, frame) {
    // Applies procedural pose matching the 4 Blender NLA actions (Idle, Select, Pair, Disappear) onto the active/front tile
    const targetTile = this.selectedTile || this.tiles.find((t) => !t.removed && t.isFree) || this.tiles[0];
    if (!targetTile) return;
    const u = Math.max(0, Math.min(1, frame / 60));
    const root = targetTile.root;
    const base = targetTile.basePos;

    root.position.copy(base);
    root.rotation.set(0, 0, 0);
    root.scale.set(1, 1, 1);

    if (animName === "Idle") {
      const s = Math.sin(u * Math.PI);
      root.position.y = base.y + s * 0.04;
      root.rotation.x = s * 0.02;
    } else if (animName === "Select") {
      const s = Math.sin(u * Math.PI);
      root.position.y = base.y + s * 0.35;
      root.rotation.x = s * 0.21;
    } else if (animName === "Pair") {
      const s = Math.sin(u * Math.PI);
      root.position.y = base.y + s * 0.65;
      root.rotation.y = u * Math.PI * 2;
      root.rotation.x = s * 0.30;
    } else if (animName === "Disappear") {
      root.position.y = base.y + Math.sin(u * Math.PI * 0.8) * 0.9;
      root.rotation.y = u * Math.PI * 3;
      const sc = Math.max(0.05, 1.0 - Math.pow(u, 2.2));
      root.scale.set(sc, sc, sc);
    }
  }

  addTween(obj, prop, targetVal, durationSec = 0.2) {
    const startVal = obj[prop];
    const t0 = performance.now();
    const durMs = durationSec * 1000;
    this.tweens.push({
      update(now) {
        const dt = (now - t0) / durMs;
        if (dt < 1.0) {
          obj[prop] = startVal + (targetVal - startVal) * (1 - Math.pow(1 - dt, 2));
          return false;
        }
        obj[prop] = targetVal;
        return true;
      },
    });
  }

  bindUI() {
    // Track picker
    document.getElementById("track-select").addEventListener("change", (e) => {
      this.setupBoard(e.target.value);
    });

    // Action buttons
    document.getElementById("btn-hint").addEventListener("click", () => this.provideHint());
    document.getElementById("btn-undo").addEventListener("click", () => this.undoLastMove());
    document.getElementById("btn-shuffle").addEventListener("click", () => this.solvableShuffle());
    document.getElementById("btn-restart").addEventListener("click", () => {
      this.setupBoard(document.getElementById("track-select").value);
    });
    document.getElementById("btn-demo").addEventListener("click", () => this.toggleDemoSolver());
    document.getElementById("btn-surface-toggle").addEventListener("click", () => this.toggleSurface());
    const btn2d = document.getElementById("btn-2d-toggle");
    if (btn2d) {
      btn2d.addEventListener("click", () => this.toggle2DMode());
    }
    const btnOnirica = document.getElementById("btn-onirica-toggle");
    if (btnOnirica) {
      btnOnirica.addEventListener("click", () => this.toggleOniricaMode());
      if (this.oniricaMode) {
        btnOnirica.classList.add("active");
        const nameEl = document.getElementById("onirica-name");
        if (nameEl) nameEl.textContent = "Onirica (Less is More)";
      }
    }

    // Camera buttons
    document.querySelectorAll(".cam-btn").forEach((btn) => {
      btn.addEventListener("click", () => this.setCameraPreset(btn.dataset.cam));
    });

    // Panel toggles
    const studioPanel = document.getElementById("studio-panel");
    const rigPanel = document.getElementById("rig-inspector");

    document.getElementById("btn-studio-toggle").addEventListener("click", () => {
      studioPanel.classList.toggle("hidden");
    });
    document.getElementById("btn-close-studio").addEventListener("click", () => {
      studioPanel.classList.add("hidden");
    });

    document.getElementById("btn-rig-toggle").addEventListener("click", () => {
      rigPanel.classList.toggle("hidden");
    });
    document.getElementById("btn-close-rig").addEventListener("click", () => {
      rigPanel.classList.add("hidden");
    });

    // Sliders Look-Dev Binding
    const bindSlider = (id, settingKey, cb) => {
      const el = document.getElementById(id);
      const valEl = document.getElementById(id.replace("sl-", "val-"));
      if (!el) return;
      el.addEventListener("input", (e) => {
        const val = parseFloat(e.target.value);
        this.settings[settingKey] = val;
        if (valEl) valEl.textContent = val.toFixed(2);
        if (cb) cb(val);
      });
    };

    bindSlider("sl-sun-intensity", "sunIntensity", () => this.updateSunPosition());
    bindSlider("sl-sun-elevation", "sunElevation", () => this.updateSunPosition());
    bindSlider("sl-sun-azimuth", "sunAzimuth", () => this.updateSunPosition());
    bindSlider("sl-lantern-glow", "lanternGlow", () => this.updateSunPosition());
    bindSlider("sl-ambient", "ambient", () => this.updateSunPosition());
    bindSlider("sl-exposure", "exposure", () => this.updateSunPosition());

    bindSlider("sl-marble-roughness", "marbleRoughness", (val) => {
      this.tiles.forEach((t) => (t.root.userData.bodyMesh.material[0].roughness = val));
    });
    bindSlider("sl-marble-clearcoat", "marbleClearcoat", (val) => {
      this.tiles.forEach((t) => (t.root.userData.bodyMesh.material[0].clearcoat = val));
    });
    bindSlider("sl-obsidian-metallic", "obsidianMetallic", (val) => {
      if (this.sharedMat) this.sharedMat.obsidian.metalness = val;
    });
    bindSlider("sl-bassorilievo", "bassorilievo", (val) => {
      const dispScale = 0.076 * val;
      this.tiles.forEach((t) => {
        const mat = t.root.userData.faceMesh.material;
        mat.normalScale.set(1.45 * val, 1.45 * val);
        mat.displacementScale = dispScale;
        mat.displacementBias = -0.88 * dispScale;
      });
    });
    bindSlider("sl-normal-scale", "normalScale", (val) => {
      this.tiles.forEach((t) => {
        t.root.userData.bodyMesh.material[0].normalScale.set(0.18 * val, 0.18 * val);
      });
      if (this.sharedMat) {
        this.sharedMat.obsidian.normalScale.set(0.22 * val, 0.22 * val);
      }
    });
    bindSlider("sl-fov", "fov", (val) => {
      this.camera.fov = val;
      this.camera.updateProjectionMatrix();
    });
    bindSlider("sl-cam-distance", "camDistance", (val) => {
      if (!this.controls) return;
      const dir = this.camera.position.clone().sub(this.controls.target).normalize();
      this.camera.position.copy(this.controls.target).addScaledVector(dir, val);
    });

    // Checkboxes & Reset
    const chkAutoRotate = document.getElementById("chk-auto-rotate");
    if (chkAutoRotate) {
      chkAutoRotate.addEventListener("change", (e) => {
        this.settings.autoRotate = e.target.checked;
      });
    }
    const chkShadows = document.getElementById("chk-shadows");
    if (chkShadows) {
      chkShadows.addEventListener("change", (e) => {
        this.settings.shadows = e.target.checked;
        this.renderer.shadowMap.enabled = e.target.checked;
        this.sunLight.castShadow = e.target.checked;
      });
    }
    const btnResetSettings = document.getElementById("btn-reset-settings");
    if (btnResetSettings) {
      btnResetSettings.addEventListener("click", () => {
        Object.assign(this.settings, {
          sunIntensity: 3.8,
          sunElevation: 46,
          sunAzimuth: 32,
          lanternGlow: 2.4,
          ambient: 0.75,
          exposure: 1.10,
          marbleRoughness: 0.14,
          marbleClearcoat: 0.35,
          obsidianMetallic: 0.22,
          bassorilievo: 1.15,
          normalScale: 1.0,
          fov: 38,
          camDistance: 11.5,
          autoRotate: false,
          shadows: true,
        });
        this.updateSunPosition();
        this.syncSliderUI();
      });
    }

    // Rig Inspector Timeline Scrubber & Play/Pause
    this.activeRigAnim = "Idle";
    this.rigPlaying = false;
    this.rigFrame = 0;
    const rigScrubber = document.getElementById("rig-scrubber");
    const rigFrameDisplay = document.getElementById("rig-frame-display");

    document.querySelectorAll(".anim-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".anim-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        this.activeRigAnim = btn.dataset.anim;
        this.applyRigPoseAtFrame(this.activeRigAnim, this.rigFrame);
      });
    });
    if (rigScrubber) {
      rigScrubber.addEventListener("input", (e) => {
        this.rigFrame = parseInt(e.target.value, 10);
        if (rigFrameDisplay) rigFrameDisplay.textContent = `Frame ${this.rigFrame} / 60`;
        this.applyRigPoseAtFrame(this.activeRigAnim, this.rigFrame);
      });
    }
    const btnRigPlay = document.getElementById("btn-rig-play");
    const btnRigPause = document.getElementById("btn-rig-pause");
    const btnRigReset = document.getElementById("btn-rig-reset");
    if (btnRigPlay) btnRigPlay.addEventListener("click", () => (this.rigPlaying = true));
    if (btnRigPause) btnRigPause.addEventListener("click", () => (this.rigPlaying = false));
    if (btnRigReset) {
      btnRigReset.addEventListener("click", () => {
        this.rigPlaying = false;
        this.rigFrame = 0;
        if (rigScrubber) rigScrubber.value = 0;
        if (rigFrameDisplay) rigFrameDisplay.textContent = "Frame 0 / 60";
        this.applyRigPoseAtFrame(this.activeRigAnim, 0);
      });
    }

    // JSON Settings Modal
    const openJsonModal = () => {
      const json = JSON.stringify(this.settings, null, 2);
      document.getElementById("json-textarea").value = json;
      document.getElementById("json-modal").classList.remove("hidden");
    };
    document.getElementById("btn-copy-json").addEventListener("click", openJsonModal);
    const btnPasteJson = document.getElementById("btn-paste-json");
    if (btnPasteJson) btnPasteJson.addEventListener("click", openJsonModal);

    document.getElementById("btn-copy-json-clip").addEventListener("click", () => {
      const json = document.getElementById("json-textarea").value;
      navigator.clipboard.writeText(json);
    });
    document.getElementById("btn-apply-json").addEventListener("click", () => {
      try {
        const parsed = JSON.parse(document.getElementById("json-textarea").value);
        Object.assign(this.settings, parsed);
        this.updateSunPosition();
        this.syncSliderUI();
        document.getElementById("json-modal").classList.add("hidden");
      } catch (err) {
        alert("Invalid JSON: " + err.message);
      }
    });
    document.getElementById("btn-close-json").addEventListener("click", () => {
      document.getElementById("json-modal").classList.add("hidden");
    });
    document.getElementById("btn-play-again").addEventListener("click", () => {
      document.getElementById("victory-modal").classList.add("hidden");
      this.setupBoard("master");
    });
    document.getElementById("btn-close-vic").addEventListener("click", () => {
      document.getElementById("victory-modal").classList.add("hidden");
    });

    // Check URL query parameters for ?debug=1
    const params = new URLSearchParams(window.location.search);
    if (params.get("debug") === "1") {
      studioPanel.classList.remove("hidden");
    }
  }

  syncSliderUI() {
    const setVal = (id, val) => {
      const el = document.getElementById(id);
      const valEl = document.getElementById(id.replace("sl-", "val-"));
      if (el) el.value = val;
      if (valEl) valEl.textContent = Number(val).toFixed(2);
    };
    setVal("sl-sun-intensity", this.settings.sunIntensity);
    setVal("sl-sun-elevation", this.settings.sunElevation);
    setVal("sl-sun-azimuth", this.settings.sunAzimuth);
    setVal("sl-lantern-glow", this.settings.lanternGlow);
    setVal("sl-ambient", this.settings.ambient);
    setVal("sl-exposure", this.settings.exposure);
    setVal("sl-marble-roughness", this.settings.marbleRoughness);
    setVal("sl-marble-clearcoat", this.settings.marbleClearcoat);
    setVal("sl-obsidian-metallic", this.settings.obsidianMetallic);
    setVal("sl-bassorilievo", this.settings.bassorilievo);
    setVal("sl-normal-scale", this.settings.normalScale);
    setVal("sl-fov", this.settings.fov);
    setVal("sl-cam-distance", this.settings.camDistance);
    const dispScale = 0.076 * this.settings.bassorilievo;
    this.tiles.forEach((t) => {
      t.root.userData.bodyMesh.material[0].roughness = this.settings.marbleRoughness;
      t.root.userData.bodyMesh.material[0].clearcoat = this.settings.marbleClearcoat;
      const mat = t.root.userData.faceMesh.material;
      mat.normalScale.set(1.45 * this.settings.bassorilievo, 1.45 * this.settings.bassorilievo);
      mat.displacementScale = dispScale;
      mat.displacementBias = -0.88 * dispScale;
    });
  }

  animate(now) {
    requestAnimationFrame(this.animate);

    // Update active tweens
    for (let i = this.tweens.length - 1; i >= 0; i--) {
      if (this.tweens[i].update(now)) {
        this.tweens.splice(i, 1);
      }
    }

    // Advance Rig Inspector timeline if playing
    if (this.rigPlaying) {
      this.rigFrame = (this.rigFrame + 0.5) % 61;
      const intFrame = Math.floor(this.rigFrame);
      const rigScrubber = document.getElementById("rig-scrubber");
      const rigFrameDisplay = document.getElementById("rig-frame-display");
      if (rigScrubber) rigScrubber.value = intFrame;
      if (rigFrameDisplay) rigFrameDisplay.textContent = `Frame ${intFrame} / 60`;
      this.applyRigPoseAtFrame(this.activeRigAnim, intFrame);
    }

    if (this.controls) {
      this.controls.autoRotate = this.settings.autoRotate && this.activeCameraPreset !== "2d";
      this.controls.update();
    }

    this.updateEnvironmentVisibility();
    this.renderer.render(this.scene, this.camera);

    // Render Top Rotating 3D Tile GLB Showcase (#wow-3d-popup) when visible:
    // Gently rock X tilt while rotating Y so raking light sweeps across the 3D carved groove cavity ('il buco bassorilievo')!
    const wowPopup = document.getElementById("wow-3d-popup");
    if (this.wowRenderer && this.wowGroup && wowPopup && !wowPopup.classList.contains("hidden")) {
      this.wowGroup.rotation.y = now * 0.0020;
      this.wowGroup.rotation.x = Math.sin(now * 0.0028) * 0.22;
      this.wowRenderer.render(this.wowScene, this.wowCamera);
    }
  }
}

// Bootstrapping
window.addEventListener("DOMContentLoaded", () => {
  window.app = new MahjongSolitaireApp();
});
