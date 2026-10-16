#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pillow",
#     "numpy",
# ]
# ///
"""
Finalizes the Adversarial Net Consensus Top 3 portraits for S1 春 • Solo Papà Riccardo:
  - Top 1: s1_cand_01.png -> public/portraits/quartet_S1_papa_riccardo_top1.png (and canonical quartet_S1_papa_riccardo.png)
  - Top 2: s1_cand_04.png -> public/portraits/quartet_S1_papa_riccardo_top2.png
  - Top 3: s1_cand_08.png -> public/portraits/quartet_S1_papa_riccardo_top3.png
Also builds the rendered Mahjong tiles (coupled_A1_top1..3.png and onirica_coupled_A1_top1..3.png)
and updates coupled_A1.png, onirica_coupled_A1.png, coupled_A1_depth.png, coupled_A1_normal.png,
and diptyque_S1_S2_papa_mamma.png.
"""

import shutil
from pathlib import Path
from PIL import Image, ImageOps
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_all_tile_textures as builder

CAND_DIR = ROOT / "public" / "portraits" / "candidates_s1"
PORTRAITS_DIR = ROOT / "public" / "portraits"
TILES_DIR = ROOT / "public" / "textures" / "tiles"
ONIRICA_DIR = ROOT / "public" / "textures" / "tiles_onirica"
ARTIFACT_DIR = Path("/Users/ricc/.gemini/antigravity/brain/9efaaa30-d5fa-49dc-b7c4-7292c03768b3")

TOP3 = [
    ("top1", "s1_cand_01.png", "Top 1 (Unanimous Consensus 8.96/10 • Navy & Gold Brocade on Marble Bridge)"),
    ("top2", "s1_cand_04.png", "Top 2 (Red-Team #1 9.70/10 • Midnight-Blue Silk & Gold Dragon Pin)"),
    ("top3", "s1_cand_08.png", "Top 3 (Dynamic 3/4 Angle 8.96/10 • Navy & Crimson Dragon Collar)"),
]


def main():
    for rank_tag, cand_file, desc in TOP3:
        src = CAND_DIR / cand_file
        dst_portrait = PORTRAITS_DIR / f"quartet_S1_papa_riccardo_{rank_tag}.png"
        shutil.copy2(src, dst_portrait)
        print(f"✅ Saved portrait {dst_portrait.name} ({desc})")

        # Temporarily set as quartet_S1_papa_riccardo.png and build coupled_A1 tile
        shutil.copy2(src, PORTRAITS_DIR / "quartet_S1_papa_riccardo.png")
        builder.generate_coupled_family_oval_tiles()

        tile_out = TILES_DIR / f"coupled_A1_{rank_tag}.png"
        onirica_out = ONIRICA_DIR / f"onirica_coupled_A1_{rank_tag}.png"
        shutil.copy2(TILES_DIR / "coupled_A1.png", tile_out)
        shutil.copy2(ONIRICA_DIR / "coupled_A1.png", onirica_out)
        print(f"✅ Rendered Mahjong tiles: {tile_out.name}, {onirica_out.name}")

        if ARTIFACT_DIR.exists():
            shutil.copy2(dst_portrait, ARTIFACT_DIR / dst_portrait.name)
            shutil.copy2(tile_out, ARTIFACT_DIR / tile_out.name)
            shutil.copy2(onirica_out, ARTIFACT_DIR / onirica_out.name)

    # Set Top 1 (s1_cand_01.png) as canonical quartet_S1_papa_riccardo.png and rebuild canonical S1 maps
    shutil.copy2(CAND_DIR / "s1_cand_01.png", PORTRAITS_DIR / "quartet_S1_papa_riccardo.png")
    builder.generate_coupled_family_oval_tiles()

    # Update diptyque_S1_S2_papa_mamma.png with new canonical S1 + S2
    im_s1 = Image.open(PORTRAITS_DIR / "quartet_S1_papa_riccardo.png").convert("RGB")
    im_s2 = Image.open(PORTRAITS_DIR / "quartet_S2_mamma_kate2016.png").convert("RGB")
    h = max(im_s1.height, im_s2.height)
    im_s1_fit = ImageOps.fit(im_s1, (int(h * 0.75), h), method=Image.Resampling.LANCZOS)
    im_s2_fit = ImageOps.fit(im_s2, (int(h * 0.75), h), method=Image.Resampling.LANCZOS)
    diptyque_pm = Image.new("RGB", (im_s1_fit.width + im_s2_fit.width, h))
    diptyque_pm.paste(im_s1_fit, (0, 0))
    diptyque_pm.paste(im_s2_fit, (im_s1_fit.width, 0))
    diptyque_pm.save(PORTRAITS_DIR / "diptyque_S1_S2_papa_mamma.png")

    if ARTIFACT_DIR.exists():
        shutil.copy2(PORTRAITS_DIR / "quartet_S1_papa_riccardo.png", ARTIFACT_DIR / "quartet_S1_papa_riccardo.png")
        shutil.copy2(PORTRAITS_DIR / "diptyque_S1_S2_papa_mamma.png", ARTIFACT_DIR / "diptyque_S1_S2_papa_mamma.png")
        shutil.copy2(TILES_DIR / "coupled_A1.png", ARTIFACT_DIR / "coupled_A1.png")
        shutil.copy2(ONIRICA_DIR / "coupled_A1.png", ARTIFACT_DIR / "onirica_coupled_A1.png")

    print("🎉 Finalized Top 3 portraits and canonical S1 tile textures!")


if __name__ == "__main__":
    main()
