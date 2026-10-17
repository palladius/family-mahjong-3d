#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai",
#     "pillow",
#     "numpy",
# ]
# ///
"""
Generates:
1. Bespoke ornate 2D relief emblems for the Three Dragons (especially Red Dragon `dragon_red` / 紅中)
   on pure ivory-white marble (#FAF6EE) with sinuous S-curves, engraved dragon scales, auspicious
   cloud curls, and sweeping brush-calligraphy `中` so 3D intaglio carving has rich organic curves.
2. White-background (#FFFFFF) keyframe animation sequence for the "Cloud Puff -> Fire-Breathing Dragon
   Biribip Power-Up" video effect when matching Ale, Sebi, or Dragon tiles.
"""

import os
import sys
import time
from io import BytesIO
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

ROOT = Path(__file__).resolve().parent.parent
PORTRAITS_DIR = ROOT / "public" / "portraits"
FX_DIR = ROOT / "public" / "fx"
PORTRAITS_DIR.mkdir(parents=True, exist_ok=True)
FX_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NB21 = "gemini-3.1-flash-image-preview"


def get_api_key() -> str:
    for var in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if os.environ.get(var):
            return os.environ[var]
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith(("GEMINI_API_KEY=", "GOOGLE_API_KEY=")):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("No GEMINI_API_KEY found in environment or .env")


def generate_image(client: genai.Client, prompt: str, out_path: Path, aspect_ratio: str = "3:4"):
    print(f"🎨 Generating {out_path.name} with {MODEL_NB21}...")
    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model=MODEL_NB21,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                    image_config=types.ImageConfig(aspect_ratio=aspect_ratio),
                ),
            )
            for part in resp.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    im = Image.open(BytesIO(part.inline_data.data)).convert("RGB")
                    im.save(out_path, "PNG")
                    print(f"✅ Saved {out_path} ({im.size})")
                    return True
        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed for {out_path.name}: {e}")
            time.sleep(2)
    return False


def main():
    client = genai.Client(api_key=get_api_key())

    tasks = [
        # 1. Bespoke Red Dragon (紅中) Ornate Curved Relief Emblem on Pure Ivory-White Marble
        (
            PORTRAITS_DIR / "dragon_red_ornate_emblem.png",
            "3:4",
            (
                "A flat-front 2D graphic emblem on a SOLID PURE UNIFORM IVORY-WHITE (#FAF6EE) background "
                "(do NOT draw a 3D Mahjong tile box or perspective edges — ONLY the centered 2D artwork on pure white). "
                "Subject: An extraordinarily ornate, curvy Imperial Chinese Red Dragon ('紅中') relief carving design. "
                "In the center is the traditional Chinese character '中' written in sweeping, curvy master brush calligraphy "
                "(NO rigid straight geometric lines — organic curved brush strokes with calligraphic hooks and dragon-scale engravings inside the red strokes). "
                "Coiling gracefully around and weaving through the '中' character in a dynamic S-curve is a majestic crimson-red and 24k burnished-gold "
                "Chinese Shenlong dragon with intricate curved scales, flowing mane, antlers, whiskers, claws, and swirling auspicious cloud curls (祥雲) and flames. "
                "Deep crimson cinnabar lacquer (#B81414), burnished 24k gold (#D8A632), and dark umber carved contour lines on a pure uniform #FAF6EE white background. "
                "High contrast, crisp engraved linework, zero text other than the central calligraphic '中'."
            ),
        ),
        # 2. Bespoke Green Dragon (發財) Ornate Curved Relief Emblem on Pure Ivory-White Marble
        (
            PORTRAITS_DIR / "dragon_green_ornate_emblem.png",
            "3:4",
            (
                "A flat-front 2D graphic emblem on a SOLID PURE UNIFORM IVORY-WHITE (#FAF6EE) background "
                "(do NOT draw a 3D Mahjong tile box or perspective edges — ONLY the centered 2D artwork on pure white). "
                "Subject: An extraordinarily ornate, curvy Imperial Chinese Green Jade Dragon ('發') relief carving design. "
                "In the center is the traditional Chinese character '發' written in sweeping, curvy master brush calligraphy "
                "with imperial emerald-jade (#107A3C) and 24k gold (#D8A632) engraved filigree. "
                "Coiling gracefully around the '發' character in an S-curve is a sinuous emerald-jade and gold Chinese dragon "
                "with finely carved scales, whiskers, and swirling auspicious cloud scrolls on a pure uniform #FAF6EE white background. "
                "High contrast, crisp engraved linework, zero text other than the central calligraphic '發'."
            ),
        ),
        # 3. White-Background Power-Up Keyframe 1: Magical Cloud Puff Explosion (#FFFFFF background)
        (
            FX_DIR / "powerup_frame1_cloud_puff_white.png",
            "1:1",
            (
                "Isolated 2D VFX game sprite on a 100% SOLID PURE FLAT WHITE (#FFFFFF) background with wide pure white margins all around. "
                "Subject: A vibrant, stylized Chinese Imperial magical cloud puff explosion ('POOF!' / '祥雲') bursting outward from the center — "
                "swirling golden-amber, crimson, and celestial cyan-jade smoke curls, golden star sparks, and dynamic comic/arcade cloud rings. "
                "The outer background MUST be 100% pure uniform #FFFFFF white with no vignette, no floor, no shadow on the background, "
                "so the white background can be cleanly keyed out for transparency."
            ),
        ),
        # 4. White-Background Power-Up Keyframe 2: Dragon Emerging from Cloud Puff & Breathing Fire (#FFFFFF background)
        (
            FX_DIR / "powerup_frame2_dragon_emerge_white.png",
            "1:1",
            (
                "Isolated 2D VFX game sprite on a 100% SOLID PURE FLAT WHITE (#FFFFFF) background with pure white margins all around. "
                "Subject: A spectacular, joyful, dynamic Chinese Crimson & 24k Gold Dragon (Shenlong) bursting out of a swirling golden-crimson magical cloud puff "
                "and breathing a dramatic stream of golden-orange and crimson dragon fire! "
                "Vibrant arcade power-up energy, glowing golden scales, expressive eyes, swirling cloud curls at its base, and fiery sparks. "
                "CRITICAL: The entire surrounding background MUST be 100% pure uniform flat white (#FFFFFF) with zero background scenery, zero border, and zero vignette, "
                "designed specifically for white-background alpha keying over a 3D game."
            ),
        ),
        # 5. White-Background Power-Up Keyframe 3: Full Roaring Fire-Breathing Dragon Power-Up Climax (#FFFFFF background)
        (
            FX_DIR / "powerup_frame3_dragon_fire_white.png",
            "1:1",
            (
                "Isolated 2D VFX game sprite on a 100% SOLID PURE FLAT WHITE (#FFFFFF) background with pure white margins all around. "
                "Subject: Climax frame of an arcade power-up: a magnificent coiled Crimson, Gold, and Jade Chinese Dragon (Shenlong) "
                "roaring joyfully and breathing a huge swirling vortex of golden-crimson dragon flames and lightning sparks out of a magical cloud puff. "
                "CRITICAL: The entire surrounding background MUST be 100% pure uniform flat white (#FFFFFF) with zero background scenery and zero vignette."
            ),
        ),
    ]

    for out_path, ratio, prompt in tasks:
        generate_image(client, prompt, out_path, aspect_ratio=ratio)


if __name__ == "__main__":
    main()
