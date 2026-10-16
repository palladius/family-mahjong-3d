# Carlesso Family Mahjong 3D - Cross-Platform Justfile (macOS & Linux)
export UV_INDEX_URL := "https://pypi.org/simple"

# List all available tasks
list:
    @just -l

# Install npm and Python dependencies
setup:
    npm install
    node node_modules/esbuild/install.js || true

# Run verification tests (3D topology, textures, build, QA rounds)
test:
    node scripts/verify_build.mjs

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

# Clean temporary build caches
clean:
    rm -rf dist/
