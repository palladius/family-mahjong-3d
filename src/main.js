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
    this.activeSurface = "table"; // "table" or "pavement"
    this.oniricaMode = new URLSearchParams(window.location.search).get("onirica") === "1";

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
      bassorilievo: 0.32,
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
    this.setCameraPreset("hero");

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
    const res = await fetch("/textures/manifest.json");
    this.manifest = await res.json();

    // Preload PBR Textures
    this.pbrTextures = {
      marbleBase: texLoader.load("/textures/pbr/marble_basecolor_2k.png"),
      marbleNorm: texLoader.load("/textures/pbr/marble_normal_2k.png"),
      obsidianBase: texLoader.load("/textures/pbr/obsidian_basecolor_2k.png"),
      obsidianNorm: texLoader.load("/textures/pbr/obsidian_normal_2k.png"),
      rosewoodBase: texLoader.load("/textures/pbr/rosewood_basecolor_2k.png"),
      jadeBase: texLoader.load("/textures/pbr/jade_basecolor_2k.png"),
      pavementBase: texLoader.load("/textures/pbr/pavement_basecolor_2k.png"),
      pavementNorm: texLoader.load("/textures/pbr/pavement_normal_2k.png"),
    };
    Object.values(this.pbrTextures).forEach((t) => {
      t.wrapS = THREE.RepeatWrapping;
      t.wrapT = THREE.RepeatWrapping;
    });

    // 2. Load 3D Temple Environment GLB
    loader.load("/models/temple_environment.glb", (gltf) => {
      this.templeEnv = gltf.scene;
      // Convert Z-up Blender export to Y-up Three.js
      this.templeEnv.rotation.x = -Math.PI / 2;
      this.templeEnv.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true;
          child.receiveShadow = true;
        }
      });
      this.scene.add(this.templeEnv);
      this.cacheEnvironmentObjects();
    });

    // 3. Load Canonical Tile GLB
    loader.load("/models/tile_generic_white_marble_obsidian.glb", (gltf) => {
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
  }

  setupBoard(trackKey = "master") {
    // Clear old tiles
    this.tiles.forEach((t) => this.scene.remove(t.root));
    this.tiles = [];
    this.selectedTile = null;
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

  initSharedTileResources() {
    if (this.sharedGeo) return;
    this.sharedGeo = {
      body: new THREE.BoxGeometry(TILE_W, TILE_D, TILE_H),
      kintsugi: new THREE.BoxGeometry(TILE_W * 1.004, TILE_D * 0.06, TILE_H * 1.004),
      face: new THREE.PlaneGeometry(TILE_W * 0.90, TILE_H * 0.92),
      // Top-center golden crown inlay bar (never occludes top-left or top-right corner glyphs!)
      badge: new THREE.BoxGeometry(0.24, 0.016, 0.032),
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
    };
  }

  generateDeckPairs(numPairs) {
    const allDeckTiles = this.manifest.tiles;
    // Categorize into Coupled Family Quartets/Pairs vs Original Traditional Suits
    const coupled = allDeckTiles.filter((t) => t.coupled);
    const standard = allDeckTiles.filter((t) => !t.coupled);

    // Prioritize our 4 signature Bamboo & Gold emblems (1=Sparrow, 2=Hot Wheels, 3=Sirio il Dragone, 4=Ale's Gems & Rubies)
    const priorityIds = new Set(["bamboo_1", "bamboo_2", "bamboo_3", "bamboo_4", "dragon_red", "dragon_green", "dragon_white"]);
    const prioritySuits = standard.filter((t) => priorityIds.has(t.id));
    const otherSuits = standard.filter((t) => !priorityIds.has(t.id));
    const orderedStandard = [...prioritySuits, ...otherSuits];

    const deckPairs = [];
    let pairCount = 0;

    // Proportional Family Cardinality (~18% of board pairs, capped at 8 pairs on 144-tile Master board)
    // so the board feels light, authentic, and never overloaded with oval portraits!
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

    // Fill remaining pairs from authentic Traditional Mahjong suits (starting with Bamboo 1..4 & Dragons!)
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
        // Pick two random currently-free slots (preferring higher layers first to keep pyramid peeling natural)
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

    // 1. Tile Body: Imperial White Marble + Black Obsidian Backing
    const marbleMat = new THREE.MeshPhysicalMaterial({
      color: 0xfcf8ee,
      map: this.pbrTextures.marbleBase,
      normalMap: this.pbrTextures.marbleNorm,
      normalScale: new THREE.Vector2(0.18 * this.settings.normalScale, 0.18 * this.settings.normalScale),
      roughness: this.settings.marbleRoughness,
      clearcoat: this.settings.marbleClearcoat,
      clearcoatRoughness: 0.1,
    });

    // Multi-material box: front & sides marble, bottom (-Y) shared obsidian
    const bodyMaterials = [
      marbleMat, // +X
      marbleMat, // -X
      marbleMat, // +Y top face
      this.sharedMat.obsidian, // -Y bottom back
      marbleMat, // +Z
      marbleMat, // -Z
    ];
    const bodyMesh = new THREE.Mesh(this.sharedGeo.body, bodyMaterials);
    bodyMesh.castShadow = true;
    bodyMesh.receiveShadow = true;
    root.add(bodyMesh);

    // 1b. Gold Kintsugi Waist Seam (between White Marble upper body and Black Obsidian base)
    const kintsugiMesh = new THREE.Mesh(this.sharedGeo.kintsugi, this.sharedMat.kintsugiGold);
    kintsugiMesh.position.y = -TILE_D * 0.12;
    root.add(kintsugiMesh);

    // 2. Face Overlay: 2D Oval Cameo (Classic) OR Dreamlike Whisper-Fade on White Marble (Modalità Onirica)
    if (!this.faceTextureCache[tileData.id]) {
      const faceTex = texLoader.load(`/textures/tiles/${tileData.id}.png`);
      faceTex.colorSpace = THREE.SRGBColorSpace;
      const oniricaTex = texLoader.load(`/textures/tiles_onirica/${tileData.id}.png`);
      oniricaTex.colorSpace = THREE.SRGBColorSpace;
      const normTex = texLoader.load(`/textures/tiles_normal/${tileData.id}_normal.png`);
      this.faceTextureCache[tileData.id] = { faceTex, oniricaTex, normTex };
    }
    const { faceTex, oniricaTex, normTex } = this.faceTextureCache[tileData.id];

    const activeMap = this.oniricaMode ? oniricaTex : faceTex;
    const activeRelief = this.oniricaMode ? 0.08 : this.settings.bassorilievo;

    const faceMat = new THREE.MeshStandardMaterial({
      map: activeMap,
      normalMap: normTex,
      normalScale: new THREE.Vector2(activeRelief, activeRelief),
      roughness: this.oniricaMode ? 0.11 : 0.16,
      metalness: 0.05,
    });
    const faceMesh = new THREE.Mesh(this.sharedGeo.face, faceMat);
    faceMesh.rotation.x = -Math.PI / 2;
    faceMesh.position.y = TILE_D * 0.5 + 0.006;
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

    // Keep reference on root
    root.userData = {
      tileData: tileData,
      faceMesh: faceMesh,
      badgeMesh: badgeMesh,
      bodyMesh: bodyMesh,
      kintsugiMesh: kintsugiMesh,
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
      if (!t.removed) {
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
    if (this.isDemoRunning) return;
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
    if (!this.isTileFree(tile)) {
      sfx.playError();
      this.wiggleTile(tile);
      return;
    }

    sfx.playClick();

    if (!this.selectedTile) {
      // First tile selection
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
      // Second tile clicked -> attempt match!
      const first = this.selectedTile;
      if (this.areTilesMatching(first.data, tile.data)) {
        // MATCH SUCCESS!
        sfx.playMatch();
        this.hideSelectionCard();
        this.selectedTile = null;
        first.selected = false;
        tile.selected = false;

        this.score += 100 * this.combo;
        this.combo++;
        this.movesHistory.push([first, tile]);

        this.animatePairMatch(first, tile);
      } else {
        // Mismatch: drop first, select second
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
    const targetY = tile.basePos.y + (liftUp ? 0.35 : 0.0);
    const targetTilt = liftUp ? 0.18 : 0.0;
    this.addTween(tile.root.position, "y", targetY, 0.16);
    this.addTween(tile.root.rotation, "x", targetTilt, 0.16);
    tile.root.userData.bodyMesh.material[0].emissive = new THREE.Color(liftUp ? 0x443311 : 0x000000);
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
          const dt = (now - t0) / 450;
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
    }, 480);
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

  showSelectionCard(tile) {
    const card = document.getElementById("selection-card");
    const badge = document.getElementById("sel-badge");
    const title = document.getElementById("sel-title");
    const status = document.getElementById("sel-status");
    const thumb = document.getElementById("sel-thumb");

    if (thumb) {
      const folder = this.oniricaMode ? "tiles_onirica" : "tiles";
      thumb.src = `/textures/${folder}/${tile.data.id}.png`;
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
    card.classList.remove("hidden");
  }

  hideSelectionCard() {
    document.getElementById("selection-card").classList.add("hidden");
  }

  updateHUD() {
    const remaining = this.tiles.filter((t) => !t.removed).length;
    document.getElementById("stat-remaining").textContent = remaining;
    document.getElementById("stat-score").textContent = this.score;
    document.getElementById("stat-combo").textContent = `x${this.combo}`;
  }

  undoLastMove() {
    if (this.movesHistory.length === 0) return;
    const [tileA, tileB] = this.movesHistory.pop();
    [tileA, tileB].forEach((t) => {
      t.removed = false;
      t.root.visible = true;
      t.root.scale.set(1, 1, 1);
      t.root.position.copy(t.basePos);
      t.root.rotation.set(0, 0, 0);
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
        const faceTex = texLoader.load(`/textures/tiles/${tile.data.id}.png`);
        faceTex.colorSpace = THREE.SRGBColorSpace;
        const oniricaTex = texLoader.load(`/textures/tiles_onirica/${tile.data.id}.png`);
        oniricaTex.colorSpace = THREE.SRGBColorSpace;
        const normTex = texLoader.load(`/textures/tiles_normal/${tile.data.id}_normal.png`);
        this.faceTextureCache[tile.data.id] = { faceTex, oniricaTex, normTex };
      }
      const { faceTex, oniricaTex, normTex } = this.faceTextureCache[tile.data.id];
      tile.root.userData.faceMesh.material.map = this.oniricaMode ? oniricaTex : faceTex;
      tile.root.userData.faceMesh.material.normalMap = normTex;
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
      this.handleTileClick(tA);
      setTimeout(() => {
        if (this.isDemoRunning) {
          this.handleTileClick(tB);
          setTimeout(() => this.stepDemoSolver(), 620);
        }
      }, 320);
      return;
    }
    // If no moves, auto-shuffle
    this.solvableShuffle();
    setTimeout(() => this.stepDemoSolver(), 650);
  }

  toggleSurface(forceSurface = null) {
    this.activeSurface = forceSurface || (this.activeSurface === "table" ? "pavement" : "table");
    const nameEl = document.getElementById("surface-name");
    const isTable = this.activeSurface === "table";
    nameEl.textContent = isTable ? "Rosewood Table" : "Stone Pavement";

    // Smoothly lower or raise table model and legs
    if (this.envTable) {
      const targetTableZ = isTable ? -0.14 : -3.5;
      this.addTween(this.envTable.position, "z", targetTableZ, 0.4);
    }
    if (this.envLegs) {
      const targetLegZ = isTable ? -0.36 : -3.7;
      this.envLegs.forEach((leg) => this.addTween(leg.position, "z", targetLegZ, 0.4));
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

    const activeRelief = this.oniricaMode ? 0.08 : this.settings.bassorilievo;
    this.tiles.forEach((t) => {
      const cached = this.faceTextureCache[t.data.id];
      if (!cached) return;
      const mat = t.root.userData.faceMesh.material;
      mat.map = this.oniricaMode ? cached.oniricaTex : cached.faceTex;
      mat.normalScale.set(activeRelief, activeRelief);
      mat.roughness = this.oniricaMode ? 0.11 : 0.16;
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

  setCameraPreset(presetKey) {
    const presets = {
      hero: { pos: [0.0, 6.4, 9.6], target: [0.0, 0.8, -0.3], fov: 38 },
      topdown: { pos: [0.0, 10.2, 0.8], target: [0.0, 0.6, -0.2], fov: 40 },
      pavement: { pos: [5.4, 2.2, 7.8], target: [0.0, 0.4, -1.2], fov: 36 },
      macro: { pos: [0.0, 1.95, 5.8], target: [0.0, 0.35, 3.65], fov: 48 },
      orbit: { pos: [0.0, 7.0, 11.0], target: [0.0, 0.5, 0.0], fov: 42 },
    };

    const cfg = presets[presetKey] || presets.hero;
    this.addTween(this.camera.position, "x", cfg.pos[0], 0.4);
    this.addTween(this.camera.position, "y", cfg.pos[1], 0.4);
    this.addTween(this.camera.position, "z", cfg.pos[2], 0.4);

    if (this.controls) {
      this.controls.target.set(cfg.target[0], cfg.target[1], cfg.target[2]);
    }

    this.settings.fov = cfg.fov;
    this.camera.fov = cfg.fov;
    this.camera.updateProjectionMatrix();

    document.querySelectorAll(".cam-btn").forEach((b) => {
      b.classList.toggle("active", b.dataset.cam === presetKey);
    });
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
      this.tiles.forEach((t) => {
        t.root.userData.faceMesh.material.normalScale.set(val, val);
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
          bassorilievo: 0.32,
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
    this.tiles.forEach((t) => {
      t.root.userData.bodyMesh.material[0].roughness = this.settings.marbleRoughness;
      t.root.userData.bodyMesh.material[0].clearcoat = this.settings.marbleClearcoat;
      t.root.userData.faceMesh.material.normalScale.set(this.settings.bassorilievo, this.settings.bassorilievo);
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
      this.controls.autoRotate = this.settings.autoRotate;
      this.controls.update();
    }

    this.renderer.render(this.scene, this.camera);
  }
}

// Bootstrapping
window.addEventListener("DOMContentLoaded", () => {
  window.app = new MahjongSolitaireApp();
});
