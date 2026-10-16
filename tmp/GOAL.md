# 🀄 Next Agent Goal: Milestone 4 Execution

Execute the following `/goal` instruction to complete Milestone 4 of the Carlesso Family 3D Mahjong Solitaire project:

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
5. When all work and tests are completely verified and committed, run `git rm tmp/GOAL.md` and commit & push the removal so no temporary handoff files remain in the repository!
```

---
*Created by RiccardinoCM26 🦖 & Jetski for seamless multi-computer handoff.*
