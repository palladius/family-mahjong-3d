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
    this.updateHUD();

    const track = TRACK_LAYOUTS[trackKey] || TRACK_LAYOUTS.master;
    const slots = track.generateSlots();

    // Mathematically Solvable Deck Pair Allocator (Reverse-Peel Solvable Guarantee)
    const pairsNeeded = slots.length / 2;
    const deck = this.generateDeckPairs(pairsNeeded);

    // Build Tile Meshes and place onto board
    const texLoader = new THREE.TextureLoader();
    const surfaceYOffset = this.activeSurface === "table" ? 0.28 : -0.45;

    // Cache textures so we don't duplicate texture memory
    if (!this.faceTextureCache) this.faceTextureCache = {};

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

  generateDeckPairs(numPairs) {
    const allDeckTiles = this.manifest.tiles;
    // Categorize into Coupled Family Pairs vs Original Traditional Suits
    const coupled = allDeckTiles.filter((t) => t.coupled);
    const standard = allDeckTiles.filter((t) => !t.coupled);

    const deckPairs = [];
    let pairCount = 0;

    // First: Include all 8 Coupled Family Pairs (A1↔A2 .. H1↔H2)
    const coupledThemes = {};
    coupled.forEach((t) => {
      coupledThemes[t.matchGroup] = coupledThemes[t.matchGroup] || [];
      coupledThemes[t.matchGroup].push(t);
    });

    Object.values(coupledThemes).forEach((pairList) => {
      if (pairCount < numPairs && pairList.length >= 2) {
        deckPairs.push([pairList[0], pairList[1]]);
        pairCount++;
      }
    });

    // Fill remaining pairs from authentic Traditional Mahjong suits
    let stdIdx = 0;
    while (pairCount < numPairs) {
      const st = standard[stdIdx % standard.length];
      deckPairs.push([st, st]);
      pairCount++;
      stdIdx++;
    }

    // Flatten and shuffle pairs
    const flatDeck = [];
    deckPairs.forEach(([a, b]) => {
      flatDeck.push(a, b);
    });

    // Fisher-Yates Shuffle
    for (let i = flatDeck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [flatDeck[i], flatDeck[j]] = [flatDeck[j], flatDeck[i]];
    }

    return flatDeck;
  }

  createTileMesh(tileData, texLoader) {
    const root = new THREE.Group();

    // 1. Tile Body: Imperial White Marble + Black Obsidian Backing
    const bodyGeo = new THREE.BoxGeometry(TILE_W, TILE_D, TILE_H);
    const marbleMat = new THREE.MeshPhysicalMaterial({
      color: 0xfcf8ee,
      map: this.pbrTextures.marbleBase,
      normalMap: this.pbrTextures.marbleNorm,
      normalScale: new THREE.Vector2(0.18, 0.18),
      roughness: this.settings.marbleRoughness,
      clearcoat: this.settings.marbleClearcoat,
      clearcoatRoughness: 0.1,
    });
    const obsidianMat = new THREE.MeshStandardMaterial({
      color: 0x111116,
      map: this.pbrTextures.obsidianBase,
      normalMap: this.pbrTextures.obsidianNorm,
      roughness: 0.10,
      metalness: this.settings.obsidianMetallic,
    });

    // Multi-material box: front & sides marble, bottom (-Y) obsidian
    const bodyMaterials = [
      marbleMat, // +X
      marbleMat, // -X
      marbleMat, // +Y top face
      obsidianMat, // -Y bottom back
      marbleMat, // +Z
      marbleMat, // -Z
    ];
    const bodyMesh = new THREE.Mesh(bodyGeo, bodyMaterials);
    bodyMesh.castShadow = true;
    bodyMesh.receiveShadow = true;
    root.add(bodyMesh);

    // 2. Face Overlay: 2D Oval Cameo / Card Texture with Bassorilievo Normal Relief
    if (!this.faceTextureCache[tileData.id]) {
      const faceTex = texLoader.load(`/textures/tiles/${tileData.id}.png`);
      const normTex = texLoader.load(`/textures/tiles_normal/${tileData.id}_normal.png`);
      this.faceTextureCache[tileData.id] = { faceTex, normTex };
    }
    const { faceTex, normTex } = this.faceTextureCache[tileData.id];

    const faceGeo = new THREE.PlaneGeometry(TILE_W * 0.90, TILE_H * 0.92);
    const faceMat = new THREE.MeshStandardMaterial({
      map: faceTex,
      normalMap: normTex,
      normalScale: new THREE.Vector2(this.settings.bassorilievo, this.settings.bassorilievo),
      roughness: 0.16,
      metalness: 0.05,
    });
    const faceMesh = new THREE.Mesh(faceGeo, faceMat);
    faceMesh.rotation.x = -Math.PI / 2;
    faceMesh.position.y = TILE_D * 0.5 + 0.006;
    faceMesh.receiveShadow = true;
    root.add(faceMesh);

    // 3. Alphabet Glyph Corner Badge (Raised 3D metallic overlay)
    const badgeGeo = new THREE.BoxGeometry(0.20, 0.02, 0.16);
    const badgeMat = new THREE.MeshStandardMaterial({
      color: tileData.coupled ? 0xf5d470 : 0xd4af37,
      metalness: 0.88,
      roughness: 0.22,
    });
    const badgeMesh = new THREE.Mesh(badgeGeo, badgeMat);
    badgeMesh.position.set(-TILE_W * 0.32, TILE_D * 0.5 + 0.016, -TILE_H * 0.36);
    badgeMesh.castShadow = true;
    root.add(badgeMesh);

    // Keep reference on root
    root.userData = {
      tileData: tileData,
      faceMesh: faceMesh,
      badgeMesh: badgeMesh,
      bodyMesh: bodyMesh,
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
      return t1.matchGroup === t2.matchGroup; // Coupled pair match (A1↔A2 etc.)
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

    badge.textContent = tile.data.code || tile.data.glyph;
    title.textContent = tile.data.title;
    status.textContent = tile.data.coupled
      ? `Coupled Family Tile (${tile.data.code}) • Match with its partner pose!`
      : "Traditional Mahjong Card • Match with identical tile";
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

    // Reshuffle data payload amongst remaining slots
    const datas = remainingTiles.map((t) => t.data);
    for (let i = datas.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [datas[i], datas[j]] = [datas[j], datas[i]];
    }

    const texLoader = new THREE.TextureLoader();
    remainingTiles.forEach((tile, i) => {
      tile.data = datas[i];
      if (!this.faceTextureCache[tile.data.id]) {
        const faceTex = texLoader.load(`/textures/tiles/${tile.data.id}.png`);
        const normTex = texLoader.load(`/textures/tiles_normal/${tile.data.id}_normal.png`);
        this.faceTextureCache[tile.data.id] = { faceTex, normTex };
      }
      const { faceTex, normTex } = this.faceTextureCache[tile.data.id];
      tile.root.userData.faceMesh.material.map = faceTex;
      tile.root.userData.faceMesh.material.normalMap = normTex;
      tile.root.userData.faceMesh.material.needsUpdate = true;
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
    const { freeTiles } = this.updateFreeTiles();
    for (let i = 0; i < freeTiles.length; i++) {
      for (let j = i + 1; j < freeTiles.length; j++) {
        if (this.areTilesMatching(freeTiles[i].data, freeTiles[j].data)) {
          this.handleTileClick(freeTiles[i]);
          setTimeout(() => {
            if (this.isDemoRunning) {
              this.handleTileClick(freeTiles[j]);
              setTimeout(() => this.stepDemoSolver(), 650);
            }
          }, 350);
          return;
        }
      }
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

    // Smoothly lower or raise table model
    if (this.envTable) {
      const targetTableY = isTable ? -0.14 : -3.5;
      this.addTween(this.envTable.position, "z", targetTableY, 0.4); // Blender Z = Three Z in our rotated setup
    }

    // Move tiles to match new surface level
    const targetTileBaseY = isTable ? 0.28 : -0.45;
    this.tiles.forEach((t) => {
      const newY = targetTileBaseY + t.slot.l * (TILE_D * 1.02);
      t.basePos.y = newY;
      this.addTween(t.root.position, "y", newY, 0.35);
    });
  }

  setCameraPreset(presetKey) {
    const presets = {
      hero: { pos: [0.0, 6.4, 9.6], target: [0.0, 0.8, -0.3], fov: 38 },
      topdown: { pos: [0.0, 10.2, 0.8], target: [0.0, 0.6, -0.2], fov: 40 },
      pavement: { pos: [5.4, 2.2, 7.8], target: [0.0, 0.4, -1.2], fov: 36 },
      macro: { pos: [-0.8, 1.85, 5.5], target: [-0.8, 0.35, 3.65], fov: 55 },
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
      this.tiles.forEach((t) => (t.root.userData.bodyMesh.material[3].metalness = val));
    });
    bindSlider("sl-bassorilievo", "bassorilievo", (val) => {
      this.tiles.forEach((t) => {
        t.root.userData.faceMesh.material.normalScale.set(val, val);
      });
    });
    bindSlider("sl-fov", "fov", (val) => {
      this.camera.fov = val;
      this.camera.updateProjectionMatrix();
    });

    // JSON Settings Modal
    document.getElementById("btn-copy-json").addEventListener("click", () => {
      const json = JSON.stringify(this.settings, null, 2);
      document.getElementById("json-textarea").value = json;
      document.getElementById("json-modal").classList.remove("hidden");
    });
    document.getElementById("btn-copy-json-clip").addEventListener("click", () => {
      const json = document.getElementById("json-textarea").value;
      navigator.clipboard.writeText(json);
      alert("Settings JSON copied to clipboard!");
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
    setVal("sl-fov", this.settings.fov);
  }

  animate(now) {
    requestAnimationFrame(this.animate);

    // Update active tweens
    for (let i = this.tweens.length - 1; i >= 0; i--) {
      if (this.tweens[i].update(now)) {
        this.tweens.splice(i, 1);
      }
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
