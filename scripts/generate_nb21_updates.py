#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai",
#     "python-dotenv",
#     "pillow",
# ]
# ///
"""
Generate updated portraits for Papà Riccardo (S1) and Mamma Kate 2016 (S2) using NB21
(gemini-3.1-flash-image-preview) + strict solo character consistency crops, plus
the 3 comedic Chinese Imperial Bamboo & Gold Filigree suit emblems for Ale & Sebi:
  - bamboo_2_hotwheels_emblem.png (Hot Wheels Chinese Bamboo & Gold Racer)
  - bamboo_3_shiryu_dragon_emblem.png (Sirio il Dragone / Saint Seiya + Towering Chinese Dragon in Bamboo & Gold)
  - bamboo_4_gems_rubies_emblem.png (Ale's Imperial Rubies, Diamonds & Gems in Bamboo & Gold)
"""

import base64
import os
import subprocess
import time
from pathlib import Path
from PIL import Image, ImageOps
from google import genai
from google.genai import types

ROOT = Path(__file__).resolve().parent.parent
PORTRAITS_DIR = ROOT / "public" / "portraits"
PORTRAITS_DIR.mkdir(parents=True, exist_ok=True)

GIC_CHARS = Path.home() / "git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters"


def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key.strip()
    env_file = Path.home() / "git/media-arneis/.env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    out = subprocess.check_output(
        ["zsh", "-ic", "echo $GEMINI_API_KEY"], text=True
    ).strip()
    for line in reversed(out.splitlines()):
        if line.strip().startswith("AIza"):
            return line.strip()
    raise RuntimeError("Could not find GEMINI_API_KEY")


def prepare_clean_kate2016_crops() -> list[Path]:
    """Create tight solo face/head-and-shoulders crops of Kate from kate2016."""
    tmp_dir = ROOT / "public/portraits/refs_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    crops = []

    # 1. Right half face & shoulders (Kate 2016 only) from crop_kate2016 KR-o-0476.jpg
    p1 = GIC_CHARS / "kate2016/cleaned/crop_kate2016  KR-o-0476.jpg"
    if p1.exists():
        im = Image.open(p1).convert("RGB")
        w, h = im.size
        c1 = im.crop((int(w * 0.44), int(h * 0.06), int(w * 0.88), int(h * 0.52)))
        out1 = tmp_dir / "kate2016_face_1.jpg"
        c1.save(out1, quality=95)
        crops.append(out1)

    # 2. Tight head-and-shoulders crop from crop_kate2016 IMG_5542.jpg
    p2 = GIC_CHARS / "kate2016/cleaned/crop_kate2016  IMG_5542.jpg"
    if p2.exists():
        im = Image.open(p2).convert("RGB")
        w, h = im.size
        c2 = im.crop((int(w * 0.05), int(h * 0.05), int(w * 0.72), int(h * 0.56)))
        out2 = tmp_dir / "kate2016_face_2.jpg"
        c2.save(out2, quality=95)
        crops.append(out2)

    # 3. Tight head-and-shoulders crop from crop_kate2016 KR-e-0136.jpg
    p3 = GIC_CHARS / "kate2016/cleaned/crop_kate2016  KR-e-0136.jpg"
    if p3.exists():
        im = Image.open(p3).convert("RGB")
        w, h = im.size
        c3 = im.crop((int(w * 0.25), int(h * 0.06), int(w * 0.88), int(h * 0.42)))
        out3 = tmp_dir / "kate2016_face_3.jpg"
        c3.save(out3, quality=95)
        crops.append(out3)

    # 4. Tight head-and-shoulders crop from crop_IMG_20141004_145136.jpg (purple dress)
    p4 = GIC_CHARS / "kate2016/cleaned/crop_IMG_20141004_145136.jpg"
    if p4.exists():
        im = Image.open(p4).convert("RGB")
        w, h = im.size
        c4 = im.crop((int(w * 0.12), int(h * 0.06), int(w * 0.92), int(h * 0.46)))
        out4 = tmp_dir / "kate2016_face_4.jpg"
        c4.save(out4, quality=95)
        crops.append(out4)

    return crops


def call_nb21(client: genai.Client, prompt: str, ref_paths: list[Path], out_path: Path, aspect_ratio: str = "3:4"):
    models_to_try = ["gemini-3.1-flash-image-preview", "gemini-3.1-flash-image-preview", "gemini-3-pro-image-preview"]
    safety_settings = [
        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
        types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
    ]

    for attempt, model_id in enumerate(models_to_try, start=1):
        contents = []
        for p in ref_paths:
            if p.exists():
                data = p.read_bytes()
                mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
                contents.append(types.Part.from_bytes(data=data, mime_type=mime))

        if ref_paths:
            full_prompt = (
                f"Using the provided reference images of the same person, generate a new image matching this description: {prompt}. "
                "It is CRITICAL that the generated person has the EXACT same facial features, hair, eyes, dimpled smile, and build as the reference person. "
                "The style MUST be PHOTOREALISTIC and highly detailed. Output ONLY the image."
            )
        else:
            full_prompt = prompt

        contents.append(full_prompt)

        print(f"🎨 [Attempt {attempt}: {model_id}] Generating {out_path.name} (refs={len(ref_paths)})...")
        try:
            resp = client.models.generate_content(
                model=model_id,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    safety_settings=safety_settings,
                    image_config=types.ImageConfig(aspect_ratio=aspect_ratio),
                ),
            )
            if resp and resp.parts:
                for part in resp.parts:
                    if part.inline_data:
                        raw = part.inline_data.data
                        if isinstance(raw, str):
                            raw = base64.b64decode(raw)
                        out_path.write_bytes(raw)
                        print(f"✅ Saved {out_path} ({len(raw) // 1024} KB)")
                        return
            else:
                reason = resp.candidates[0].finish_reason if (resp and resp.candidates) else "unknown"
                print(f"⚠️ Attempt {attempt} returned no parts (reason={reason}), retrying...")
        except Exception as e:
            print(f"⚠️ Attempt {attempt} error: {e}")
        time.sleep(2)

    raise RuntimeError(f"Failed to generate {out_path.name}")


def main():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    papa_out = PORTRAITS_DIR / "quartet_S1_papa_riccardo.png"
    mamma_out = PORTRAITS_DIR / "quartet_S2_mamma_kate2016.png"

    kate_refs = prepare_clean_kate2016_crops()

    # Generate Mamma Kate 2016 (S2) using NB21 and her 2016 solo face crops
    call_nb21(
        client,
        prompt=(
            "Close-up waist-up outdoor portrait of this radiant 34-year-old British woman (Kate) with luminous golden ash-blonde hair, "
            "bright blue-grey eyes, natural fresh 'acqua e sapone' glowing skin, and her distinctive warm dimpled smile. "
            "She is wearing an elegant royal purple and deep emerald-green silk wrap dress with delicate gold embroidery (no veil, no glasses). "
            "She stands by a carved white marble bridge in an Imperial Chinese lotus garden at golden sunset with warm red silk lanterns in the background, centered head-and-shoulders framing"
        ),
        ref_paths=kate_refs,
        out_path=mamma_out,
        aspect_ratio="3:4",
    )

    # Combine S1 and S2 into the updated diptyque_S1_S2_papa_mamma.png
    im_s1 = Image.open(papa_out).convert("RGB")
    im_s2 = Image.open(mamma_out).convert("RGB")
    h = max(im_s1.height, im_s2.height)
    im_s1_fit = ImageOps.fit(im_s1, (int(h * 0.75), h), method=Image.Resampling.LANCZOS)
    im_s2_fit = ImageOps.fit(im_s2, (int(h * 0.75), h), method=Image.Resampling.LANCZOS)
    diptyque_pm = Image.new("RGB", (im_s1_fit.width + im_s2_fit.width, h))
    diptyque_pm.paste(im_s1_fit, (0, 0))
    diptyque_pm.paste(im_s2_fit, (im_s1_fit.width, 0))
    diptyque_pm.save(PORTRAITS_DIR / "diptyque_S1_S2_papa_mamma.png")
    print("✅ Updated combined diptyque_S1_S2_papa_mamma.png")

    # 3. Comedic Chinese Bamboo & Gold Suit Tile 1: Hot Wheels Racer (bamboo_2_hotwheels_emblem.png)
    hw_out = PORTRAITS_DIR / "bamboo_2_hotwheels_emblem.png"
    if not hw_out.exists():
        call_nb21(
            client,
            prompt=(
                "Pure 2D vertical Mahjong tile centerpiece illustration on a uniform warm ivory-cream background (#FBF6EC), NO 3D tile border, NO text: "
                "A hilarious, ultra-detailed Hot Wheels style flame-racer muscle supercar with oversized deep-dish racing wheels, a giant rear wing spoiler, and roaring exhaust flames, "
                "entirely sculpted and crafted out of green Chinese bamboo stalks, carved celadon imperial jade, cinnabar red lacquer flames, and gleaming 24k gold filigree inlay! "
                "The car has a carved golden Chinese dragon hood ornament and two crossed green bamboo stalks behind it. "
                "Masterpiece traditional Chinese imperial jade-and-bamboo relief carving style with rich 24k gold leaf highlights, centered in the frame."
            ),
            ref_paths=[],
            out_path=hw_out,
            aspect_ratio="3:4",
        )

    # 4. Comedic Chinese Bamboo & Gold Suit Tile 2: Sirio il Dragone / Saint Seiya Dragon Shiryu (bamboo_3_shiryu_dragon_emblem.png)
    shiryu_out = PORTRAITS_DIR / "bamboo_3_shiryu_dragon_emblem.png"
    if not shiryu_out.exists():
        call_nb21(
            client,
            prompt=(
                "Pure 2D vertical Mahjong tile centerpiece illustration on a uniform warm ivory-cream background (#FBF6EC), NO 3D tile border, NO text: "
                "An epic, comedic homage to 'Sirio il Dragone' (Dragon Shiryu from Knights of the Zodiac / Saint Seiya) rendered entirely as an ornate Chinese Imperial Bamboo, Celadon Jade, and 24k Gold Filigree relief sculpture! "
                "In the foreground, a heroic emerald-jade armored warrior with long flowing jet-black hair and an iconic round emerald Dragon Shield on his left arm unleashes a rising dragon punch, "
                "while a colossal, majestic emerald-jade and 24k-gold Chinese Dragon with glowing golden whiskers coils around him and towers dramatically behind him framed by three carved green bamboo stalks. "
                "Warm ivory-cream background (#FBF6EC) all around the edges, museum-grade jade, bamboo, and 24k gold leaf relief."
            ),
            ref_paths=[],
            out_path=shiryu_out,
            aspect_ratio="3:4",
        )

    # 5. Comedic Chinese Bamboo & Gold Suit Tile 3: Ale's Gems, Diamonds & Rubies in Bamboo & Gold (bamboo_4_gems_rubies_emblem.png)
    gems_out = PORTRAITS_DIR / "bamboo_4_gems_rubies_emblem.png"
    if not gems_out.exists():
        call_nb21(
            client,
            prompt=(
                "Pure 2D vertical Mahjong tile centerpiece illustration on a uniform warm ivory-cream background (#FBF6EC), NO 3D tile border, NO text: "
                "A dazzling, luxurious treasure composition of giant faceted crimson rubies, sparkling brilliant-cut white diamonds, and glowing emerald crystals, "
                "all mounted inside an ornate Chinese Imperial Bamboo and 24k Gold Filigree pagoda-style treasure cradle formed by four carved green bamboo stalks tied with 24k gold ribbons and golden dragon claws holding the largest ruby and diamond! "
                "Hilarious contrast between video-game style glittering gems/diamonds/rubies and ancient Chinese bamboo-and-gold imperial craftsmanship, on a clean warm ivory-cream background (#FBF6EC)."
            ),
            ref_paths=[],
            out_path=gems_out,
            aspect_ratio="3:4",
        )


if __name__ == "__main__":
    main()
