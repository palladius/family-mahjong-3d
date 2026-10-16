#!/usr/bin/env python3
"""
Generates Pure 2D Character-Consistency Portraits & Diptyque Dual Scenes via Nano Banana Pro (google.genai)
using canonical GIC reference photos for:
  - 4 Diptyque Split-Pairs (Cardinality 2):
      * diptyque_A_great_wall.png      -> A1 (Solo Ale) <-> A2 (Solo Sebi)
      * diptyque_B_cantonese_rice.png  -> B1 (Solo Ale) <-> B2 (Solo Sebi)
      * diptyque_C_shaolin_kungfu.png  -> C1 (Solo Ale) <-> C2 (Solo Sebi)
      * diptyque_D_chengdu_pandas.png  -> D1 (Solo Ale) <-> D2 (Solo Sebi)
  - Quartet 1: Carlesso Family Seasons (Cardinality 4, S1..S4):
      * diptyque_S1_S2_papa_mamma.png  -> S1 (Solo Papà Riccardo) & S2 (Solo Mamma Kate)
      * diptyque_S3_S4_ale_sebi_tang.png -> S3 (Solo Ale) & S4 (Solo Sebi)
  - Quartet 2: Magical Companions Flowers (Cardinality 4, F1..F4):
      * quartet_F1_ale_ghigna.png      -> F1 (Ale con Ghigna 🐹)
      * quartet_F2_sebi_pupurabbu.png  -> F2 (Sebi col Pupurabbu 👾)
      * quartet_F3_solo_ghigna.png     -> F3 (Solo Ghigna 🐹)
      * quartet_F4_solo_pupurabbu.png  -> F4 (Solo Pupurabbu 👾)
"""
import io
import os
import shutil
import sys
import time
from pathlib import Path
from PIL import Image as PILImage
from google import genai
from google.genai import types

ROOT_DIR = Path(__file__).resolve().parents[1]
PORTRAITS_DIR = ROOT_DIR / "public" / "portraits"
PORTRAITS_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/Users/ricc/.gemini/antigravity/brain/9efaaa30-d5fa-49dc-b7c4-7292c03768b3")

GIC_CHARS = Path.home() / "git" / "gic" / "private" / "projects" / "git-privatize" / "github.com__palladius__media-arneis" / "data" / "characters"
ALE_DIR = GIC_CHARS / "alessandro"
SEBI_DIR = GIC_CHARS / "sebastian"
KATE_DIR = GIC_CHARS / "kate-best"
RICC_DIR = GIC_CHARS / "riccardo"
COMPAGNI_DIR = Path.home() / "git" / "gemini-cli-palladius-private-goodies" / "skills" / "carlesso-family" / "assets" / "compagni-magici"

ALE_REFS = [
    ALE_DIR / "PXL_20260218_151036231.jpg",
    ALE_DIR / "PXL_20260403_100103962.jpg",
    ALE_DIR / "PXL_20260220_060800602.jpg",
]
SEBI_REFS = [
    SEBI_DIR / "PXL_20260310_195345815-seby-felice-con-mac.jpg",
    SEBI_DIR / "20260418_094506-seby-lingua.jpg",
    SEBI_DIR / "seby-irlandese-celtico.jpg",
]
KATE_REFS = [
    KATE_DIR / "01_color_pop.jpg",
    KATE_DIR / "04_felice_casa.png",
    KATE_DIR / "05_venezia.png",
]
RICC_REFS = [
    RICC_DIR / "ricc-za-wine-tasting.png",
    RICC_DIR / "ricc-pineapple-pizza.png",
    RICC_DIR / "riccardosouthafrica.png",
]
GHIGNA_REFS = [
    COMPAGNI_DIR / "ale_ghigna_sebi_pupurabbu_google.jpg",
]
PUPURABBU_REFS = [
    COMPAGNI_DIR / "pupurabbu_portrait_standalone.jpg",
    COMPAGNI_DIR / "sebi_pupurabbu_lungolago_zurigo.jpg",
]

DIPTYQUE_RULE = (
    "CRITICAL FRAMING RULE: This is a pure 2D full-bleed wide portrait that will be split vertically down the center (x=50%) into TWO separate solo portraits. "
    "Place the first character clearly centered in the LEFT half (around x=27%) and the second character clearly centered in the RIGHT half (around x=73%), "
    "standing/sitting side-by-side in the same continuous scene with a small clean space between their heads/shoulders at the exact center line (x=50%) so neither face is cut when split in half. "
    "PHOTOREALISTIC, CINEMATIC, warm natural lighting. Their faces MUST be clearly visible, unmasked, and 100% recognizable from the reference photos. "
    "Do NOT draw any borders, frames, ovals, text, or mahjong tiles."
)

SPECS = [
    (
        "diptyque_S1_S2_papa_mamma.png",
        [*RICC_REFS[:2], *KATE_REFS[:2]],
        f"{DIPTYQUE_RULE} "
        "LEFT HALF: Riccardo (Papà), a fit, athletic Italian man looking around age 36-38 with short dark brown/black hair with only subtle hints of grey, neat dark stubble, expressive warm brown eyes, and a joyful smile, wearing an elegant tailored imperial navy-blue and gold silk Chinese Tang jacket, no glasses. "
        "RIGHT HALF: Kate (Mamma), a gorgeous radiant British woman looking around age 38 with shoulder-length luminous ash-blonde hair with natural volume, light blue-grey eyes, natural 'acqua e sapone' fresh glowing skin with minimal makeup, and a warm youthful smile, wearing an elegant royal purple and deep emerald-green silk Chinese jacket, no glasses. "
        "BACKGROUND: A romantic traditional Chinese temple garden bridge at golden hour with glowing red silk lanterns and jade bamboo.",
    ),
    (
        "diptyque_S3_S4_ale_sebi_tang.png",
        [*ALE_REFS[:2], *SEBI_REFS[:2]],
        f"{DIPTYQUE_RULE} "
        "LEFT HALF: Alessandro (Ale, 8-year-old Italian boy from the first two reference photos, short brown hair, striking green eyes, warm observant smile) wearing an ornate crimson-red and gold embroidered Tang Dynasty silk jacket. "
        "RIGHT HALF: Sebastian (Sebi, 6-year-old younger brother from the next two reference photos, round face, straight light-brown hair with soft bangs, large bright blue-grey eyes, cheerful expression) wearing a matching royal red and imperial gold silk Tang Dynasty jacket. "
        "BACKGROUND: A festive Chinese temple courtyard glowing with warm red lanterns.",
    ),
    (
        "diptyque_A_great_wall.png",
        [*ALE_REFS[:2], *SEBI_REFS[:2]],
        f"{DIPTYQUE_RULE} "
        "LEFT HALF: Alessandro (Ale, 8-year-old boy from the first two reference photos, short brown hair, green eyes, adventurous smile) wearing a khaki explorer sun hat, linen safari shirt, and vintage camera strap on the Great Wall of China. "
        "RIGHT HALF: Sebastian (Sebi, 6-year-old boy from the next two reference photos, round face, light-brown bangs, blue-grey eyes, happy expression) wearing a matching explorer sun hat and small adventure backpack on the Great Wall of China. "
        "BACKGROUND: Majestic stone watchtowers and green mountain ridges of the Great Wall under warm sunlight.",
    ),
    (
        "diptyque_B_cantonese_rice.png",
        [*ALE_REFS[:2], *SEBI_REFS[:2]],
        f"{DIPTYQUE_RULE} "
        "LEFT HALF: Alessandro (Ale, 8-year-old boy from the first two reference photos, short brown hair, green eyes) sitting at a carved wooden dim sum table holding wooden chopsticks over a blue-and-white porcelain bowl of colorful Cantonese fried rice. "
        "RIGHT HALF: Sebastian (Sebi, 6-year-old boy from the next two reference photos, round face, light-brown bangs, blue-grey eyes) sitting beside him holding wooden chopsticks over his own porcelain bowl of Cantonese fried rice with bamboo dim sum steamers behind them. "
        "BACKGROUND: Warm traditional Cantonese tea house with wooden lattice screens and red lanterns.",
    ),
    (
        "diptyque_C_shaolin_kungfu.png",
        [*ALE_REFS[:2], *SEBI_REFS[:2]],
        f"{DIPTYQUE_RULE} "
        "LEFT HALF: Alessandro (Ale, 8-year-old boy from the first two reference photos, keeping his natural short brown hair and recognizable face) in a dynamic Shaolin Kung Fu Dragon stance wearing an amber-orange and gold silk martial arts tunic. "
        "RIGHT HALF: Sebastian (Sebi, 6-year-old boy from the next two reference photos, keeping his natural light-brown hair with bangs and recognizable round face) in a playful Shaolin Kung Fu Tiger claw stance wearing a matching amber-orange and gold silk martial arts tunic. "
        "BACKGROUND: Ancient Chinese temple courtyard with curved tile roofs and red lanterns.",
    ),
    (
        "diptyque_D_chengdu_pandas.png",
        [*ALE_REFS[:2], *SEBI_REFS[:2]],
        f"{DIPTYQUE_RULE} "
        "LEFT HALF: Alessandro (Ale, 8-year-old boy from the first two reference photos, short brown hair, green eyes) smiling warmly with a cute fluffy giant panda munching green bamboo right next to him in the left half. "
        "RIGHT HALF: Sebastian (Sebi, 6-year-old boy from the next two reference photos, round face, light-brown bangs, blue-grey eyes) beaming with joy alongside an adorable fluffy baby giant panda in the right half. "
        "BACKGROUND: Lush green Chengdu bamboo sanctuary in soft morning sunlight.",
    ),
    (
        "quartet_F1_ale_ghigna.png",
        [*ALE_REFS[:2], *GHIGNA_REFS],
        "Pure 2D full-bleed photorealistic close-up portrait of Alessandro (Ale, 8-year-old boy from the reference photos, short brown hair, striking green eyes, warm smile) in a traditional Chinese bamboo scholar pavilion, side-by-side with his magical companion Ghigna: a large, monumental tricolore calico guinea pig wearing round nerd glasses with a clever, sarcastic side-smirk ('ghigna'), resting its paws on a sleek laptop next to a jade abacus and fresh carrots. Both Ale's face and Ghigna's face are centered Together inside the middle of the frame so both fit inside a central vertical oval cameo. No borders or frames.",
    ),
    (
        "quartet_F2_sebi_pupurabbu.png",
        [*SEBI_REFS[:2], *PUPURABBU_REFS],
        "Pure 2D full-bleed photorealistic close-up portrait of Sebastian (Sebi, 6-year-old boy from the reference photos, round face, light-brown bangs, bright blue-grey eyes, joyful smile) in a Chinese temple garden, being warmly hugged by his magical companion Pupurabbu: a giant, super-fluffy, cuddly purple-indigo furry monster (like Blue from IF) with big sweet expressive eyes, proudly wearing a colorful Google Noogler propeller cap. Both Sebi and Pupurabbu's faces are close together in the center of the frame so both fit inside a central vertical oval cameo. No borders or frames.",
    ),
    (
        "quartet_F3_solo_ghigna.png",
        [*GHIGNA_REFS],
        "Pure 2D full-bleed photorealistic close-up portrait centered on Ghigna: a monumental, fluffy tricolore calico guinea pig (white, orange, and dark brown fur) wearing round black nerd glasses perched on its nose with a signature clever, sarcastic side-smirk ('ghigna'), wearing a tiny imperial crimson silk scholar vest in a Chinese bamboo pavilion, with paws on a mini laptop and a glowing jade abacus beside a fresh carrot. Centered for a vertical oval portrait. No borders or frames.",
    ),
    (
        "quartet_F4_solo_pupurabbu.png",
        [*PUPURABBU_REFS],
        "Pure 2D full-bleed photorealistic close-up portrait centered on Pupurabbu (Pupurannu): a giant, ultra-fluffy, cuddly purple-indigo furry monster with big warm expressive eyes and a gentle joyful smile, proudly wearing his colorful Google Noogler propeller cap and holding a glowing red Chinese silk lantern in a misty bamboo temple courtyard. Centered for a vertical oval portrait. No borders or frames.",
    ),
]


def generate_one(client: genai.Client, filename: str, ref_paths: list[Path], prompt: str) -> Path:
    out_path = PORTRAITS_DIR / filename
    if out_path.exists() and out_path.stat().st_size > 80_000:
        print(f"[Skip] {filename} already exists ({out_path.stat().st_size // 1024} KB)")
        if ARTIFACT_DIR.exists():
            shutil.copy2(out_path, ARTIFACT_DIR / filename)
        return out_path

    refs = []
    for p in ref_paths:
        if p.exists():
            with PILImage.open(p) as im:
                im_copy = im.convert("RGB")
                im_copy.thumbnail((1024, 1024))
                refs.append(im_copy)

    contents = [*refs, prompt]
    models_to_try = ["gemini-3-pro-image-preview", "gemini-2.5-flash-image"]

    for model_name in models_to_try:
        for attempt in range(1, 3):
            try:
                print(f"[NanoBanana] Generating {filename} via {model_name} (attempt {attempt}, {len(refs)} refs)...")
                cfg = types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
                resp = client.models.generate_content(model=model_name, contents=contents, config=cfg)
                for part in getattr(resp, "parts", []) or []:
                    if getattr(part, "inline_data", None) is not None:
                        data = part.inline_data.data
                        if isinstance(data, str):
                            import base64
                            data = base64.b64decode(data)
                        img = PILImage.open(io.BytesIO(data)).convert("RGB")
                        img.save(out_path, "PNG")
                        if ARTIFACT_DIR.exists():
                            shutil.copy2(out_path, ARTIFACT_DIR / filename)
                        print(f"  -> Saved {out_path} ({img.size[0]}x{img.size[1]})")
                        return out_path
            except Exception as exc:
                print(f"  [Warn] {model_name} attempt {attempt} failed: {exc}")
                time.sleep(2)

    raise RuntimeError(f"Failed to generate {filename}")


def main():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    for filename, refs, prompt in SPECS:
        generate_one(client, filename, refs, prompt)
    print("[Done] All remastered pure 2D scenes and portraits generated!")


if __name__ == "__main__":
    main()
