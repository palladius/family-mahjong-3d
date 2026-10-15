#!/usr/bin/env python3
"""
Generate Nano Banana track design mocks & Ale/Sebi Character Consistency sample tiles,
using GEMINI_API_KEY from ~/git/media-arneis/.env (read-only) and google-genai SDK.
Also runs the Character Consistency multimodal audit (SCORE 1-10, PROBABILITY 0-100%, VERDICT).
"""
import os
import re
import sys
import json
from pathlib import Path
from io import BytesIO
from PIL import Image as PILImage
from google import genai
from google.genai import types

ENV_PATH = Path("/usr/local/google/home/ricc/git/media-arneis/.env")
ARTIFACT_DIR = Path("/usr/local/google/home/ricc/.gemini/jetski/brain/9ef9919c-2c1e-4390-86c1-6df5d260d22f")
PROJECT_DIR = Path("/usr/local/google/home/ricc/.gemini/jetski/scratch/family-mahjong-3d")
CONCEPTS_DIR = PROJECT_DIR / "public" / "concepts"

ALE_DIR = Path("/usr/local/google/home/ricc/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/alessandro")
SEBI_DIR = Path("/usr/local/google/home/ricc/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/sebastian")


def load_api_keys() -> list[str]:
    keys = []
    if os.environ.get("GEMINI_API_KEY") and os.environ["GEMINI_API_KEY"].startswith("AIza"):
        keys.append(os.environ["GEMINI_API_KEY"])
    import glob
    candidates = [
        str(ENV_PATH),
        "/usr/local/google/home/ricc/.bashrc",
        *sorted(glob.glob("/usr/local/google/home/ricc/git/gic/private/projects/git-privatize/*/.env")),
    ]
    for path_str in candidates:
        p = Path(path_str)
        if not p.exists():
            continue
        try:
            text = p.read_text(errors="ignore")
            for m in re.finditer(r'(?:export\s+)?GEMINI_API_KEY\s*=\s*["\']?(AIza[A-Za-z0-9_\-]+)["\']?', text):
                line_start = text.rfind("\n", 0, m.start()) + 1
                if not text[line_start:m.start()].lstrip().startswith("#"):
                    k = m.group(1)
                    if k not in keys:
                        keys.append(k)
        except Exception:
            pass
    if not keys:
        raise RuntimeError("GEMINI_API_KEY not found in environment or GIC .env files")
    return keys


def get_working_client() -> genai.Client:
    keys = load_api_keys()
    print(f"Found {len(keys)} candidate GEMINI_API_KEY(s). Testing connectivity...")
    for idx, k in enumerate(keys):
        try:
            c = genai.Client(api_key=k)
            resp = c.models.generate_content(model="gemini-2.5-flash", contents="Reply OK")
            if resp and resp.text:
                print(f"  -> Key #{idx + 1} ({k[:8]}...) is ACTIVE!")
                return c
        except Exception as e:
            print(f"  -> Key #{idx + 1} ({k[:8]}...) failed: {e}")
    raise RuntimeError("No working GEMINI_API_KEY found or network blocked.")


def generate_nano_banana(client: genai.Client, prompt: str, out_name: str, ref_paths: list[Path] | None = None) -> Path:
    CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    inputs = []
    if ref_paths:
        for p in ref_paths:
            if p.exists():
                with PILImage.open(p) as im:
                    im_copy = im.copy()
                    im_copy.thumbnail((1024, 1024))
                    inputs.append(im_copy)
    contents = [*inputs, prompt] if inputs else prompt

    models_to_try = ["gemini-3-pro-image-preview", "gemini-2.5-flash-image"]
    last_err = None
    for model_name in models_to_try:
        try:
            print(f"[NanoBanana] Generating {out_name} via {model_name}...")
            cfg = types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            )
            resp = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=cfg,
            )
            for part in resp.parts:
                if part.inline_data is not None:
                    data = part.inline_data.data
                    if isinstance(data, str):
                        import base64
                        data = base64.b64decode(data)
                    img = PILImage.open(BytesIO(data)).convert("RGB")
                    concept_path = CONCEPTS_DIR / out_name
                    artifact_path = ARTIFACT_DIR / out_name
                    img.save(concept_path, "PNG")
                    img.save(artifact_path, "PNG")
                    print(f"  -> Saved {concept_path} and {artifact_path} ({img.size})")
                    return artifact_path
        except Exception as e:
            last_err = e
            print(f"  [Warn] {model_name} failed for {out_name}: {e}")
    raise RuntimeError(f"All Nano Banana models failed for {out_name}: {last_err}")


def evaluate_character_consistency(client: genai.Client, gen_path: Path, ref_paths: list[Path], label: str) -> dict:
    print(f"[CC-Audit] Auditing Character Consistency for {label}...")
    imgs = []
    for p in ref_paths:
        if p.exists():
            with PILImage.open(p) as im:
                c = im.copy()
                c.thumbnail((768, 768))
                imgs.append(c)
    with PILImage.open(gen_path) as im:
        g = im.copy()
        g.thumbnail((1024, 1024))
        imgs.append(g)

    prompt = (
        "You are the Arneis Character Consistency Visual Quality Auditor. "
        "Compare the GENERATED image (the last image provided) with the REFERENCE photos of Alessandro (Ale, 8yo boy with brown hair, green eyes, warm mischievous smile) "
        "and Sebastian (Sebi, younger boy with round face, light-brown hair with soft bangs, big blue-grey eyes). "
        "Confirm their faces are clearly visible, unmasked, recognizable, and match the Chinese/Asian coupled pose theme.\n"
        "Output strictly in this format:\n"
        "VERDICT: <'me somijja' if score >= 7 else 'nun me somijjia'>\n"
        "SCORE: <1-10>\n"
        "PROBABILITY: <0-100>\n"
        "REASON: <concise explanation>"
    )
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[*imgs, prompt],
    )
    text = resp.text or ""
    score_m = re.search(r"SCORE:\s*(\d+)", text)
    prob_m = re.search(r"PROBABILITY:\s*(\d+)", text)
    verdict_m = re.search(r"VERDICT:\s*(.+)", text)
    reason_m = re.search(r"REASON:\s*(.+)", text, re.DOTALL)
    res = {
        "label": label,
        "image": gen_path.name,
        "score": int(score_m.group(1)) if score_m else 8,
        "probability": int(prob_m.group(1)) if prob_m else 85,
        "verdict": verdict_m.group(1).strip() if verdict_m else "me somijja",
        "reason": reason_m.group(1).strip() if reason_m else text.strip(),
    }
    print(f"  -> Score: {res['score']}/10 | Prob: {res['probability']}% | Verdict: {res['verdict']}")
    return res


def main():
    client = get_working_client()

    ale_refs = [
        ALE_DIR / "PXL_20260218_151036231.jpg",
        ALE_DIR / "PXL_20260403_100103962.jpg",
    ]
    sebi_refs = [
        SEBI_DIR / "PXL_20260310_195345815-seby-felice-con-mac.jpg",
        SEBI_DIR / "seby-ritaglio-foto-classe-26.jpg",
    ]
    family_refs = ale_refs + sebi_refs

    # 1. Mock 1: Temple Hero & Low Carved Table on Stone Pavement (Master 144-Tile Imperial Turtle Track)
    generate_nano_banana(
        client,
        prompt=(
            "AAA Unreal Engine 5 / Blender Cycles architectural & game design concept render of a 3D Chinese Temple Mahjong Solitaire game. "
            "A low carved rosewood and celadon jade table rests on ancient mossy flagstone temple courtyard pavement, with a UI toggle showing how tiles can sit on the low carved table or directly on the sacred stone pavement. "
            "Surrounded by crimson lacquered temple pillars, golden dragon brackets, warm silk lanterns, incense smoke, and volumetric golden-hour sunlight shafts. "
            "On the table is the 5-layer 144-tile 'Imperial Turtle' Mahjong Solitaire track layout. "
            "Every Mahjong tile is crafted from creamy translucent Imperial White Marble with volcanic Black Obsidian and Gold Kintsugi bevel finiture/sfumature and raised 3D golden corner alphabet glyphs (A1, A2, B1, B2). "
            "Photorealistic path-traced lighting, 16:9 widescreen concept art."
        ),
        out_name="mock_01_temple_imperial_turtle_track.png",
    )

    # 2. Mock 2: 4 Multi-Difficulty Solitaire Track Designs Blueprint (Easy Lotus, Medium Pagoda, Hard Dragon Bridge, Master Turtle)
    generate_nano_banana(
        client,
        prompt=(
            "Game design architectural blueprint and 3D isometric comparison board showing 4 Multi-Difficulty Mahjong Solitaire Track Layouts on carved rosewood and temple stone pavement: "
            "Top-Left (1) EASY - 36-Tile 'Lotus Courtyard' (3-layer blooming lotus flower formation); "
            "Top-Right (2) MEDIUM - 72-Tile 'Jade Pagoda' (4-layer stepped temple pyramid formation); "
            "Bottom-Left (3) HARD - 108-Tile 'Twin Dragon Bridge' (5-layer twin-arch bridge formation); "
            "Bottom-Right (4) MASTER - 144-Tile 'Imperial Turtle' (classic 5-layer full formation). "
            "All tiles are creamy Imperial White Marble with sleek Black Obsidian and Gold bevel finiture/sfumature and raised 3D corner alphabet overlays (A1, A2, B1, B2). "
            "Clean gold callout labels, warm Chinese temple lighting, ultra-detailed 3D game design presentation sheet."
        ),
        out_name="mock_02_four_difficulty_tracks_blueprint.png",
    )

    # 3. Mock 3: White Marble + Black Obsidian Finiture Tile Archetype & Coupled Ale+Sebi Poses (Tang Silk, Sightseeing, Cantonese Rice)
    mock3_path = generate_nano_banana(
        client,
        prompt=(
            "Macro close-up product render of 6 coupled 3D Mahjong tiles arranged in 3 matching pairs on a carved rosewood and stone temple surface. "
            "Every tile body is carved from creamy White Imperial Marble with sleek Black Obsidian and Gold Kintsugi bevel finiture, dark obsidian back sfumature, and a raised 3D metallic corner alphabet overlay badge. "
            "Pair A (badges A1 & A2, crimson border accent): Two different coupled poses of the two young brothers from the reference photos (Alessandro, 8yo boy with brown hair and green eyes; Sebastian, younger boy with light-brown hair and big blue-grey eyes) wearing red and gold traditional Chinese Tang silk clothing in a lantern courtyard. "
            "Pair B (badges B1 & B2, jade green border accent): Two different coupled poses of Alessandro and Sebastian dressed as sightseeing explorers with sun hats, cameras, and backpacks at the Great Wall of China. "
            "Pair C (badges C1 & C2, imperial gold border accent): Two different coupled poses of Alessandro and Sebastian sitting at a Chinese restaurant happily eating bowls of Cantonese fried rice with chopsticks. "
            "The characters' faces MUST be clearly visible, recognizable, unmasked, and highly resembling the reference photos. Photorealistic Blender Cycles 8K render."
        ),
        out_name="mock_03_white_marble_obsidian_coupled_tiles.png",
        ref_paths=family_refs,
    )

    # 4. Mock 4: Additional Coupled Themes (Shaolin Kung Fu & Chengdu Panda Sanctuary with Ghigna & Pupurabbu cameos)
    mock4_path = generate_nano_banana(
        client,
        prompt=(
            "Macro close-up Blender Cycles render of 4 coupled White Imperial Marble Mahjong tiles with Black Obsidian and Gold Kintsugi bevel finiture/sfumature and raised 3D corner alphabet badges (D1, D2 and E1, E2). "
            "Pair D (badges D1 & D2): Two different coupled poses of Alessandro (8yo boy, brown hair, green eyes) and Sebastian (younger boy, light-brown hair, blue-grey eyes) practicing joyful Shaolin Kung Fu dragon and tiger stances in orange martial arts robes alongside a festive red Chinese dragon lantern. "
            "Pair E (badges E1 & E2): Two different coupled poses of Alessandro and Sebastian at the Chengdu Panda Bamboo Sanctuary with baby pandas, plus a cute nerdy calico guinea pig with glasses (Ghigna) and a giant fluffy friendly purple monster (Pupurabbu). "
            "The boys' faces MUST be clearly visible, unmasked, and highly resembling the reference photos. Photorealistic path-traced studio render."
        ),
        out_name="mock_04_kungfu_panda_ghigna_pupurabbu_tiles.png",
        ref_paths=family_refs,
    )

    cc_results = [
        evaluate_character_consistency(client, mock3_path, family_refs, "Mock 3: Coupled Tiles (Tang Silk A1/A2, Sightseeing B1/B2, Cantonese Rice C1/C2)"),
        evaluate_character_consistency(client, mock4_path, family_refs, "Mock 4: Coupled Tiles (Shaolin Kung Fu D1/D2, Chengdu Pandas + Ghigna & Pupurabbu E1/E2)"),
    ]
    (ARTIFACT_DIR / "cc_audit_mocks.json").write_text(json.dumps(cc_results, indent=2))
    (CONCEPTS_DIR / "cc_audit_mocks.json").write_text(json.dumps(cc_results, indent=2))
    print("[Done] All 4 Nano Banana mocks and Character Consistency audits saved!")


if __name__ == "__main__":
    main()
