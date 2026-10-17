import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, "public/textures/manifest.json"), "utf8"));

function areTilesMatching(t1, t2) {
  if (t1.coupled && t2.coupled) {
    return t1.matchGroup === t2.matchGroup;
  }
  return t1.id === t2.id;
}

const TRACK_LAYOUTS = {
  easy: {
    name: "Easy • Lotus Courtyard",
    tileCount: 36,
    generateSlots() {
      const slots = [];
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 6; c++) slots.push({ c: c - 2.5, r: r - 1.5, l: 0 });
      }
      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 4; c++) slots.push({ c: c - 1.5, r: r - 0.5, l: 1 });
      }
      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 2; c++) slots.push({ c: c - 0.5, r: r - 0.5, l: 2 });
      }
      return slots;
    },
  },
  medium: {
    name: "Medium • Jade Pagoda",
    tileCount: 72,
    generateSlots() {
      const slots = [];
      for (let r = 0; r < 5; r++) {
        for (let c = 0; c < 8; c++) slots.push({ c: c - 3.5, r: r - 2.0, l: 0 });
      }
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 6; c++) slots.push({ c: c - 2.5, r: r - 1.0, l: 1 });
      }
      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 4; c++) slots.push({ c: c - 1.5, r: r - 0.5, l: 2 });
      }
      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 2; c++) slots.push({ c: c - 0.5, r: r - 0.5, l: 3 });
      }
      slots.push({ c: -4.5, r: 0.0, l: 0 });
      slots.push({ c: 4.5, r: 0.0, l: 0 });
      return slots;
    },
  },
  master: {
    name: "Master • Imperial Turtle",
    tileCount: 144,
    generateSlots() {
      const slots = [];
      for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 12; c++) {
          const corner = (r === 0 || r === 7) && (c < 2 || c > 9);
          if (!corner) slots.push({ c: c - 5.5, r: r - 3.5, l: 0 });
        }
      }
      slots.push({ c: -6.6, r: -0.5, l: 0 });
      slots.push({ c: -6.6, r: 0.5, l: 0 });
      slots.push({ c: 6.6, r: -0.5, l: 0 });
      slots.push({ c: 6.6, r: 0.5, l: 0 });
      for (let r = 0; r < 6; r++) {
        for (let c = 0; c < 6; c++) slots.push({ c: c - 2.5, r: r - 2.5, l: 1 });
      }
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) slots.push({ c: c - 1.5, r: r - 1.5, l: 2 });
      }
      for (let r = 0; r < 2; r++) {
        for (let c = 0; c < 2; c++) slots.push({ c: c - 0.5, r: r - 0.5, l: 3 });
      }
      while (slots.length > 144) slots.pop();
      while (slots.length < 144) slots.push({ c: 0, r: 0, l: 4 });
      return slots;
    },
  },
};

function generateDeckPairs(numPairs) {
  const allDeckTiles = manifest.tiles;
  const coupled = allDeckTiles.filter((t) => t.coupled);
  const standard = allDeckTiles.filter((t) => !t.coupled);
  const priorityIds = new Set(["dots_2", "dots_4", "char_8", "bamboo_1", "bamboo_2", "bamboo_3", "bamboo_4", "dragon_red", "dragon_green", "dragon_white"]);
  const prioritySuits = standard.filter((t) => priorityIds.has(t.id));
  const otherSuits = standard.filter((t) => !priorityIds.has(t.id));
  const orderedStandard = [...prioritySuits, ...otherSuits];

  const deckPairs = [];
  let pairCount = 0;
  const maxCoupledPairs = Math.max(3, Math.min(8, Math.round(numPairs * 0.18)));

  const coupledThemes = {};
  coupled.forEach((t) => {
    coupledThemes[t.matchGroup] = coupledThemes[t.matchGroup] || [];
    coupledThemes[t.matchGroup].push(t);
  });

  Object.values(coupledThemes).forEach((groupList) => {
    if (pairCount >= maxCoupledPairs) return;
    const list = [...groupList];
    for (let k = 0; k + 1 < list.length && pairCount < maxCoupledPairs && pairCount < numPairs; k += 2) {
      deckPairs.push([list[k], list[k + 1]]);
      pairCount++;
    }
  });

  let stdIdx = 0;
  while (pairCount < numPairs) {
    const st = orderedStandard[stdIdx % orderedStandard.length];
    deckPairs.push([st, st]);
    pairCount++;
    stdIdx++;
  }
  return deckPairs;
}

// Check slot freedom given active mask
function isSlotFreeWithMask(idx, slots, mask) {
  const s = slots[idx];
  for (let i = 0; i < slots.length; i++) {
    if (!mask[i] || i === idx) continue;
    const o = slots[i];
    if (o.l === s.l + 1 && Math.abs(o.c - s.c) < 0.95 && Math.abs(o.r - s.r) < 0.95) {
      return false;
    }
  }
  let leftBlocked = false;
  let rightBlocked = false;
  for (let i = 0; i < slots.length; i++) {
    if (!mask[i] || i === idx) continue;
    const o = slots[i];
    if (o.l === s.l && Math.abs(o.r - s.r) < 0.8) {
      const dc = o.c - s.c;
      if (dc > 0.8 && dc < 1.3) rightBlocked = true;
      if (dc < -0.8 && dc > -1.3) leftBlocked = true;
    }
  }
  return !leftBlocked || !rightBlocked;
}

// Pure Reverse-Peel Solvable Assigner
function assignSolvableDeckToSlots(slots, deckPairs) {
  const n = slots.length;
  const assigned = new Array(n).fill(null);
  const remainingIndices = new Set(slots.map((_, idx) => idx));

  const isSlotFreeSim = (idx) => {
    const s = slots[idx];
    for (const otherIdx of remainingIndices) {
      if (otherIdx === idx) continue;
      const o = slots[otherIdx];
      if (o.l === s.l + 1 && Math.abs(o.c - s.c) < 0.95 && Math.abs(o.r - s.r) < 0.95) return false;
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

// Fast Mahjong Solitaire Solver & Solvability Checker
class MahjongSolver {
  constructor(slots, tiles) {
    this.slots = slots;
    this.tiles = tiles; // Array of tile objects with data
    this.n = slots.length;
    // Precompute adjacency / obstruction graphs for ultra-fast lookup!
    this.coverList = new Array(this.n);
    this.leftBlockList = new Array(this.n);
    this.rightBlockList = new Array(this.n);

    for (let i = 0; i < this.n; i++) {
      this.coverList[i] = [];
      this.leftBlockList[i] = [];
      this.rightBlockList[i] = [];
      const s = slots[i];
      for (let j = 0; j < this.n; j++) {
        if (i === j) continue;
        const o = slots[j];
        if (o.l === s.l + 1 && Math.abs(o.c - s.c) < 0.95 && Math.abs(o.r - s.r) < 0.95) {
          this.coverList[i].push(j);
        }
        if (o.l === s.l && Math.abs(o.r - s.r) < 0.8) {
          const dc = o.c - s.c;
          if (dc > 0.8 && dc < 1.3) this.rightBlockList[i].push(j);
          if (dc < -0.8 && dc > -1.3) this.leftBlockList[i].push(j);
        }
      }
    }
  }

  isFree(idx, mask) {
    // 1. Is any covering tile active?
    const covers = this.coverList[idx];
    for (let k = 0; k < covers.length; k++) {
      if (mask[covers[k]]) return false;
    }
    // 2. Is left blocked AND right blocked?
    let leftBlocked = false;
    const lefts = this.leftBlockList[idx];
    for (let k = 0; k < lefts.length; k++) {
      if (mask[lefts[k]]) { leftBlocked = true; break; }
    }
    let rightBlocked = false;
    const rights = this.rightBlockList[idx];
    for (let k = 0; k < rights.length; k++) {
      if (mask[rights[k]]) { rightBlocked = true; break; }
    }
    return !leftBlocked || !rightBlocked;
  }

  getFreeTiles(mask) {
    const res = [];
    for (let i = 0; i < this.n; i++) {
      if (mask[i] && this.isFree(i, mask)) res.push(i);
    }
    return res;
  }

  getMatchablePairs(freeIndices) {
    const pairs = [];
    for (let i = 0; i < freeIndices.length; i++) {
      const idxA = freeIndices[i];
      const dataA = this.tiles[idxA];
      for (let j = i + 1; j < freeIndices.length; j++) {
        const idxB = freeIndices[j];
        const dataB = this.tiles[idxB];
        if (areTilesMatching(dataA, dataB)) {
          pairs.push([idxA, idxB]);
        }
      }
    }
    return pairs;
  }

  encodeState(mask) {
    // 144 bits can be stored as 5 uint32 numbers
    let s = "";
    let cur = 0;
    let b = 0;
    for (let i = 0; i < this.n; i++) {
      if (mask[i]) cur |= (1 << b);
      b++;
      if (b === 30) {
        s += cur.toString(36) + ".";
        cur = 0;
        b = 0;
      }
    }
    if (b > 0) s += cur.toString(36);
    return s;
  }

  findSolution(currentMask, maxNodes = 20000) {
    const mask = new Uint8Array(currentMask);
    let remaining = 0;
    for (let i = 0; i < this.n; i++) if (mask[i]) remaining++;

    const visitedDeadends = new Set();
    const solutionPath = [];
    let nodeCount = 0;

    const dfs = (remCount) => {
      nodeCount++;
      if (remCount === 0) return true;
      if (nodeCount > maxNodes) return false;

      const stateKey = this.encodeState(mask);
      if (visitedDeadends.has(stateKey)) return false;

      const free = this.getFreeTiles(mask);
      const pairs = this.getMatchablePairs(free);

      if (pairs.length === 0) {
        visitedDeadends.add(stateKey);
        return false;
      }

      // Move ordering: heuristic prefers pairs that expose more tiles or higher layers
      pairs.sort((a, b) => {
        const layerA = this.slots[a[0]].l + this.slots[a[1]].l;
        const layerB = this.slots[b[0]].l + this.slots[b[1]].l;
        return layerB - layerA;
      });

      for (let p = 0; p < pairs.length; p++) {
        const [a, b] = pairs[p];
        mask[a] = 0;
        mask[b] = 0;
        solutionPath.push([a, b]);

        if (dfs(remCount - 2)) return true;

        solutionPath.pop();
        mask[a] = 1;
        mask[b] = 1;
      }

      visitedDeadends.add(stateKey);
      return false;
    };

    const t0 = performance.now();
    const solved = dfs(remaining);
    const ms = performance.now() - t0;

    return {
      solvable: solved,
      path: solved ? solutionPath : null,
      visitedStates: visitedDeadends.size,
      nodeCount,
      timeMs: ms,
      exhaustedSearch: nodeCount <= maxNodes,
    };
  }
}

// Test on Easy Lotus (36 tiles)
const slots = TRACK_LAYOUTS.easy.generateSlots();
const deckPairs = generateDeckPairs(slots.length / 2);
const assignedDeck = assignSolvableDeckToSlots(slots, deckPairs);
const solver = new MahjongSolver(slots, assignedDeck);

const initialMask = new Uint8Array(slots.length).fill(1);
const res = solver.findSolution(initialMask);
console.log("Easy Lotus Solve Result:", {
  solvable: res.solvable,
  movesFound: res.path?.length,
  timeMs: res.timeMs.toFixed(2),
  nodeCount: res.nodeCount,
  visitedStates: res.visitedStates
});

// Test deadlocked state (simulate removing until stuck, like user's 18 tiles)
const halfMask = new Uint8Array(slots.length).fill(0);
// Pick 18 tiles that have NO matchable free pairs
for (let i = 0; i < 18; i++) halfMask[i] = 1;
const deadCheck = solver.findSolution(halfMask);
console.log("Deadlock check result:", {
  solvable: deadCheck.solvable,
  movesFound: deadCheck.path?.length,
  timeMs: deadCheck.timeMs.toFixed(2),
  exhausted: deadCheck.exhaustedSearch
});

for (const trackKey of ["easy", "medium", "master"]) {
  const trk = TRACK_LAYOUTS[trackKey];
  const s = trk.generateSlots();
  const dp = generateDeckPairs(s.length / 2);
  const deck = assignSolvableDeckToSlots(s, dp);
  const slv = new MahjongSolver(s, deck);
  const m = new Uint8Array(s.length).fill(1);
  const r = slv.findSolution(m);
  console.log(`Track ${trackKey} (${s.length} tiles):`, {
    solvable: r.solvable,
    moves: r.path?.length,
    timeMs: r.timeMs.toFixed(2),
    nodes: r.nodeCount
  });
}
