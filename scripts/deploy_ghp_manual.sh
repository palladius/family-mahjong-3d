#!/usr/bin/env bash
# Carlesso Family Mahjong 3D - Manual GitHub Pages Deploy Script (with Broken-Push Test Gate)
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VERSION_STR="$(cat VERSION 2>/dev/null | tr -d '[:space:]' || echo 'latest')"
SHORT_SHA="$(git rev-parse --short HEAD)"

echo "🔨 [1/4] Building production Vite bundle (dist/)..."
npm run build

echo "🧪 [2/4] Running Pre-Deploy Broken-Push Test Gate..."
node scripts/verify_build.mjs
node scripts/test_3d_visibility.mjs
node scripts/test_solvability_solver.mjs
node scripts/test_board_integration.mjs --check-dist

echo "🚀 [3/4] Publishing ./dist to origin/gh-pages (v${VERSION_STR} @ ${SHORT_SHA})..."
REMOTE_URL="$(git config --get remote.origin.url)"
TMP_GHP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/mahjong-ghp-XXXXXX")"
trap 'rm -rf "$TMP_GHP_DIR"' EXIT

cp -R dist/. "$TMP_GHP_DIR/"
touch "$TMP_GHP_DIR/.nojekyll"

(
  cd "$TMP_GHP_DIR"
  git init -q
  git checkout -q -B gh-pages
  git add -A
  git commit -q -m "Deploy v${VERSION_STR} (${SHORT_SHA}) to GitHub Pages [manual verified]"
  git push -f "$REMOTE_URL" gh-pages:gh-pages
)

echo "✅ [4/4] Pushed to origin/gh-pages! Run 'just test-post-deploy' to verify live CDN propagation."
