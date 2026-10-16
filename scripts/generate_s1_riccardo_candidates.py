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
Generates 8 candidate portraits (s1_cand_01.png .. s1_cand_08.png) of Papà Riccardo (S1 春)
using tight solo face crops from GIC reference photos and Nano Banana (gemini-3.1-flash-image-preview /
gemini-3-pro-image-preview) for evaluation by the Adversarial Net of 3 Critic Subagents.
"""

import base64
import os
import subprocess
import time
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

ROOT = Path(__file__).resolve().parent.parent
CAND_DIR = ROOT / "public" / "portraits" / "candidates_s1"
CAND_DIR.mkdir(parents=True, exist_ok=True)
REFS_TMP = CAND_DIR / "refs_crops"
REFS_TMP.mkdir(parents=True, exist_ok=True)

GIC_RICC = Path.home() / "git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/riccardo"


def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key.strip()
    env_file = Path.home() / "git/media-arneis/.env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    out = subprocess.check_output(["zsh", "-ic", "echo $GEMINI_API_KEY"], text=True).strip()
    for line in reversed(out.splitlines()):
        if line.strip().startswith("AIza"):
            return line.strip()
    raise RuntimeError("Could not find GEMINI_API_KEY")


def prepare_tight_riccardo_crops() -> dict[str, Path]:
    """
    Create tight head-and-shoulders crops from Riccardo's reference photos so the model
    receives maximum facial resolution instead of distant landscape backgrounds.
    """
    crops = {}

    # 1. papino 2026-07-20.png (already close-up face, slight crop to center head)
    p1 = GIC_RICC / "papino 2026-07-20.png"
    if p1.exists():
        im = Image.open(p1).convert("RGB")
        w, h = im.size
        c = im.crop((int(w * 0.02), int(h * 0.0), int(w * 0.98), int(h * 0.96)))
        out = REFS_TMP / "ricc_crop_1_papino.jpg"
        c.save(out, quality=95)
        crops["papino"] = out

    # 2. ricc-google-switzerland.png (head & shoulders crop)
    p2 = GIC_RICC / "ricc-google-switzerland.png"
    if p2.exists():
        im = Image.open(p2).convert("RGB")
        w, h = im.size
        c = im.crop((int(w * 0.14), int(h * 0.04), int(w * 0.86), int(h * 0.72)))
        out = REFS_TMP / "ricc_crop_2_switzerland.jpg"
        c.save(out, quality=95)
        crops["switzerland"] = out

    # 3. riccardosouthafrica.png (tight crop on Riccardo's head & polo collar in center)
    p3 = GIC_RICC / "riccardosouthafrica.png"
    if p3.exists():
        im = Image.open(p3).convert("RGB")
        w, h = im.size
        c = im.crop((int(w * 0.34), int(h * 0.31), int(w * 0.62), int(h * 0.75)))
        out = REFS_TMP / "ricc_crop_3_southafrica.jpg"
        c.save(out, quality=95)
        crops["southafrica"] = out

    # 4. ricc-za-wine-tasting.png (tight crop on Riccardo's face on the left)
    p4 = GIC_RICC / "ricc-za-wine-tasting.png"
    if p4.exists():
        im = Image.open(p4).convert("RGB")
        w, h = im.size
        c = im.crop((int(w * 0.16), int(h * 0.27), int(w * 0.41), int(h * 0.66)))
        out = REFS_TMP / "ricc_crop_4_wine.jpg"
        c.save(out, quality=95)
        crops["wine"] = out

    # 5. ricc-za-lake.png (tight crop on Riccardo's face at bottom center-left)
    p5 = GIC_RICC / "ricc-za-lake.png"
    if p5.exists():
        im = Image.open(p5).convert("RGB")
        w, h = im.size
        c = im.crop((int(w * 0.28), int(h * 0.48), int(w * 0.58), int(h * 0.96)))
        out = REFS_TMP / "ricc_crop_5_lake.jpg"
        c.save(out, quality=95)
        crops["lake"] = out

    return crops


IDENTITY_ANCHOR = (
    "CRITICAL FACIAL LIKENESS: The man in the generated portrait MUST be 100% recognizable as THIS EXACT Italian man (Riccardo) from the provided reference photos. "
    "Preserve his exact craniofacial geometry and real features: "
    "(1) high forehead with receding hairline and short, fine silver-grey / salt-and-pepper hair with a light wispy tuft at the top crown (NEVER give him thick dark hair!); "
    "(2) warm deep-set dark brown eyes with slightly hooded eyelids, friendly crow's feet, expressive horizontal forehead creases, and salt-and-pepper eyebrows; "
    "(3) his exact straight-to-softly-rounded nose bridge and tip; "
    "(4) his signature warm, gentle CLOSED-LIP SMILE (lips together with upturned corners, friendly knowing expression — do NOT give him a fake wide open-mouth toothy grin); "
    "(5) short silver-grey and salt-and-pepper stubble beard along his jaw and chin with a neat salt-and-pepper moustache; "
    "(6) broad, warm mid-40s Italian face, NO glasses. "
    "Pure 2D photorealistic head-and-shoulders portrait centered for a vertical portrait frame. Do NOT draw any mahjong tile, border, frame, or text."
)

CANDIDATE_SPECS = [
    (
        "s1_cand_01.png",
        ["switzerland", "papino", "southafrica", "wine"],
        "gemini-3.1-flash-image-preview",
        f"{IDENTITY_ANCHOR} "
        "He is wearing an elegant imperial navy-blue and gold brocade silk Tang Dynasty Mandarin-collar jacket over a crisp white linen shirt. "
        "Setting: Warm golden-hour light in a serene Imperial Chinese lotus courtyard with soft-focus glowing red silk lanterns and a carved white marble bridge behind him.",
    ),
    (
        "s1_cand_02.png",
        ["papino", "switzerland", "lake", "southafrica"],
        "gemini-3.1-flash-image-preview",
        f"{IDENTITY_ANCHOR} "
        "He is wearing a royal burgundy-crimson and 24k gold embroidered silk Chinese Mandarin jacket, holding a delicate crystal glass of Italian red wine in one hand low near his chest. "
        "Setting: An ancient Chinese temple terrace overlooking misty green mountains at sunset with warm glowing silk lanterns.",
    ),
    (
        "s1_cand_03.png",
        ["switzerland", "southafrica", "wine", "lake"],
        "gemini-3.1-flash-image-preview",
        f"{IDENTITY_ANCHOR} "
        "Close-up head-and-shoulders portrait matching the exact head angle and warm closed-lip smile of the first two reference photos. "
        "He wears a dark emerald-jade and gold dragon-embroidered Chinese silk tunic. "
        "Setting: Sunlit Classical Suzhou garden with bamboo groves and warm golden afternoon bokeh.",
    ),
    (
        "s1_cand_04.png",
        ["papino", "switzerland", "wine"],
        "gemini-3-pro-image-preview",
        f"{IDENTITY_ANCHOR} "
        "Ultra-detailed close-up portrait capturing his exact face shape, receding silver-grey hair tuft, deep brown eyes, and short white-and-grey stubble beard. "
        "He wears a tailored midnight-blue silk Mandarin collar blazer with a subtle golden dragon lapel pin. "
        "Setting: Imperial Chinese pavilion at dusk with warm amber lantern glow.",
    ),
    (
        "s1_cand_05.png",
        ["southafrica", "lake", "switzerland", "papino"],
        "gemini-3.1-flash-image-preview",
        f"{IDENTITY_ANCHOR} "
        "Outdoor daylight head-and-shoulders portrait with natural sunlight on his face, matching his exact facial proportions in the vineyard and lake reference photos. "
        "He wears an imperial gold-and-navy silk Chinese Tang jacket. "
        "Setting: Scenic stone watchtower of the Great Wall of China with lush green hills under a bright warm sky.",
    ),
    (
        "s1_cand_06.png",
        ["switzerland", "papino", "wine", "lake", "southafrica"],
        "gemini-3.1-flash-image-preview",
        f"{IDENTITY_ANCHOR} "
        "Warm, jovial portrait of this exact man with his unmistakable closed-lip smile, high forehead with wispy grey hair, and silver-grey stubble. "
        "He wears a rich plum-purple and gold silk Chinese scholar's robe to harmonize with Mamma Kate's royal purple dress. "
        "Setting: Carved white marble bridge over a lotus pond with glowing red lanterns.",
    ),
    (
        "s1_cand_07.png",
        ["papino", "switzerland", "southafrica"],
        "gemini-3-pro-image-preview",
        f"{IDENTITY_ANCHOR} "
        "Studio-grade natural-light portrait in a Chinese Imperial courtyard, preserving every detail of his real eyes, nose, receding silver-grey hair, and short grey stubble. "
        "He wears a dark charcoal-black and gold-trimmed silk Mandarin jacket.",
    ),
    (
        "s1_cand_08.png",
        ["wine", "switzerland", "papino", "lake"],
        "gemini-3.1-flash-image-preview",
        f"{IDENTITY_ANCHOR} "
        "Slightly relaxed three-quarter head angle matching the wine-tasting reference photo, with his warm knowing closed-lip smile and silver-grey stubble. "
        "He wears a tailored imperial navy and crimson-red silk Chinese Tang jacket in a sunlit temple garden with bamboo and red lanterns.",
    ),
]


def generate_candidate(client: genai.Client, filename: str, ref_keys: list[str], preferred_model: str, prompt: str, crops: dict[str, Path]):
    out_path = CAND_DIR / filename
    models = [preferred_model, "gemini-3.1-flash-image-preview", "gemini-3-pro-image-preview"]
    safety_settings = [
        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
        types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
    ]

    for attempt, model_id in enumerate(models, start=1):
        contents = []
        for k in ref_keys:
            p = crops[k]
            contents.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/jpeg"))
        contents.append(prompt)

        print(f"🎨 [{filename}] Attempt {attempt} with {model_id} (refs={ref_keys})...")
        try:
            resp = client.models.generate_content(
                model=model_id,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    safety_settings=safety_settings,
                    image_config=types.ImageConfig(aspect_ratio="3:4"),
                ),
            )
            if resp and resp.parts:
                for part in resp.parts:
                    if part.inline_data:
                        raw = part.inline_data.data
                        if isinstance(raw, str):
                            raw = base64.b64decode(raw)
                        out_path.write_bytes(raw)
                        print(f"✅ Saved {out_path.name} ({len(raw) // 1024} KB)")
                        return
        except Exception as e:
            print(f"⚠️ [{filename}] Attempt {attempt} error: {e}")
        time.sleep(1.5)

    raise RuntimeError(f"Failed to generate {filename}")


def main():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    crops = prepare_tight_riccardo_crops()
    print(f"✂️ Prepared {len(crops)} tight facial reference crops of Riccardo: {list(crops.keys())}")

    for filename, ref_keys, preferred_model, prompt in CANDIDATE_SPECS:
        generate_candidate(client, filename, ref_keys, preferred_model, prompt, crops)


if __name__ == "__main__":
    main()
