# Carlesso Family Mahjong 3D - Justfile
export PATH := "/usr/local/google/home/ricc/.nvm/versions/node/v24.0.0/bin:/usr/local/google/home/ricc/.local/bin:" + env_var('PATH')
export UV_INDEX_URL := "https://pypi.org/simple"

# List all available tasks
list:
    @just -l

# Run verification tests (3D topology, textures, build, QA rounds)
test:
    node scripts/verify_build.mjs

# Start the local Vite development server
dev:
    npm run dev

# Build production bundle
build:
    npm run build

# Regenerate 3D GLB assets and Cycles renders via headless Blender (bpy)
blender-build:
    uv run python scripts/blender/build_all_assets.py

# Clean temporary build caches
clean:
    rm -rf dist/

# Synchronize scratch workspace into canonical git repo in ~/git/family-mahjong-3d
sync-git:
    rsync -av --exclude='.venv' --exclude='node_modules' --exclude='.git' --exclude='dist' ./ /usr/local/google/home/ricc/git/family-mahjong-3d/

