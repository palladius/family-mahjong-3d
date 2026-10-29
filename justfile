# Carlesso Family Mahjong 3D - Cross-Platform Justfile (macOS & Linux)
export UV_INDEX_URL := "https://pypi.org/simple"

# List all available tasks
list:
    @just -l

# Install npm and Python dependencies
setup:
    npm install
    node node_modules/esbuild/install.js || true

# Run full verification suite (3D topology, 3D line-of-sight visibility, solvability & deadlock solver, chessboard self-occlusion & XZ pan/rotate integration)
test:
    node scripts/verify_build.mjs
    node scripts/test_3d_visibility.mjs
    node scripts/test_solvability_solver.mjs
    node scripts/test_board_integration.mjs

# Build production bundle and run Pre-Deploy Broken-Push Gate against dist/
test-dist:
    npm run build
    node scripts/verify_build.mjs
    node scripts/test_3d_visibility.mjs
    node scripts/test_solvability_solver.mjs
    node scripts/test_board_integration.mjs --check-dist

# Manual fallback deploy: build, run Pre-Deploy Broken-Push Gate, push ./dist to origin/gh-pages
deploy:
    bash scripts/deploy_ghp_manual.sh

# Run post-deploy live verification against GitHub Pages (https://palladius.github.io/family-mahjong-3d/)
test-post-deploy:
    node scripts/test_board_integration.mjs --post-deploy

# Start the local Vite development server
dev:
    npm run dev

# Build production bundle
build:
    npm run build

# Regenerate 50 tile textures, Diptyque Split-Pairs, Quartets, and Bassorilievo normal maps
textures-build:
    uv run python scripts/build_all_tile_textures.py

# Regenerate 3D GLB assets and Cycles renders via headless Blender (bpy)
blender-build:
    uv run python scripts/blender/build_all_assets.py

# Regenerate Raspberry Pi 400 (Sguisatazzo V3D 4.2) lightweight GLBs (*_rpi.glb) and 256px textures
rpi-assets:
    uv run --with pillow python scripts/build_rpi_assets.py

# Clean temporary build caches
clean:
    rm -rf dist/ node_modules/
