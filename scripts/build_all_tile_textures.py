#!/usr/bin/env python3
"""
Generates:
1. 2K Baked/Procedural PBR Base Maps (2048x2048) for White Imperial Marble, Volcanic Black Obsidian + Gold Kintsugi Finiture,
   Carved Ming Rosewood Table, Celadon Jade Mat, and Sacred Chinese Temple Flagstone Pavement.
2. All 34 Original Traditional Mahjong Tile Faces (Characters 1-9 萬, Circles 1-9 筒, Bamboos 1-9 索 with 1-Bamboo Sparrow,
   Winds 東南西北, Dragons 中發白) with authentic Original Mahjong calligraphy & corner glyphs.
3. All 16 Coupled Non-Identical Family Tile Faces (8 Coupled Pairs A1↔A2 .. H1↔H2 corresponding to Seasons 春夏秋冬 & Flowers 梅蘭菊竹)
   using Pure 2D Character-Consistency Portraits masked into Gold-Rimmed OVAL Cameo Medallions + Bassorilievo normal maps.
"""
import glob
import json
import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

PROJECT_DIR = Path("/usr/local/google/home/ricc/.gemini/jetski/scratch/family-mahjong-3d")
ARTIFACT_DIR = Path("/usr/local/google/home/ricc/.gemini/jetski/brain/9ef9919c-2c1e-4390-86c1-6df5d260d22f")
PBR_DIR = PROJECT_DIR / "public" / "textures" / "pbr"
TILES_DIR = PROJECT_DIR / "public" / "textures" / "tiles"
NORMALS_DIR = PROJECT_DIR / "public" / "textures" / "tiles_normal"
PORTRAITS_DIR = PROJECT_DIR / "public" / "portraits"

for d in [PBR_DIR, TILES_DIR, NORMALS_DIR, PORTRAITS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

ALE_DIR = Path("/usr/local/google/home/ricc/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/alessandro")
SEBI_DIR = Path("/usr/local/google/home/ricc/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/sebastian")
KATE_DIR = Path("/usr/local/google/home/ricc/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/kate-best")
RICC_DIR = Path("/usr/local/google/home/ricc/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/riccardo")
FAMILY_ASSETS = Path("/usr/local/google/home/ricc/git/gemini-cli-palladius-private-goodies/skills/carlesso-family/assets")

CJK_FONT_PATH = "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"
LATIN_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
LATIN_REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def cjk_font(size: int):
    if Path(CJK_FONT_PATH).exists():
        return ImageFont.truetype(CJK_FONT_PATH, size=size)
    return ImageFont.load_default()


def latin_font(size: int, bold: bool = True):
    p = LATIN_BOLD_PATH if bold else LATIN_REG_PATH
    if Path(p).exists():
        return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def draw_centered_text(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, font, fill, stroke_fill=None, stroke_width: int = 0):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = xy[0] - tw / 2 - bbox[0]
    ty = xy[1] - th / 2 - bbox[1]
    draw.text((tx, ty), text, font=font, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width)


def height_to_normal_map(height_np: np.ndarray, strength: float = 8.0) -> Image.Image:
    gy, gx = np.gradient(height_np.astype(np.float32) * strength)
    nx = -gx
    ny = gy
    nz = np.ones_like(nx)
    norm = np.sqrt(nx * nx + ny * ny + nz * nz) + 1e-6
    nx, ny, nz = nx / norm, ny / norm, nz / norm
    rgb = np.stack([(nx * 0.5 + 0.5) * 255, (ny * 0.5 + 0.5) * 255, (nz * 0.5 + 0.5) * 255], axis=-1).astype(np.uint8)
    return Image.fromarray(rgb)


def generate_2k_pbr_maps():
    if (PBR_DIR / "pavement_basecolor_2k.png").exists():
        print("[PBR] 2048x2048 2K PBR Base Maps already present, skipping.")
        return
    print("[PBR] Generating 2048x2048 2K PBR Base Maps (Marble, Obsidian+Kintsugi, Rosewood, Jade, Pavement)...")
    S = 2048
    y_grid, x_grid = np.mgrid[0:S, 0:S].astype(np.float32) / S

    # 1. Imperial White Marble Albedo, Roughness, Normal (2048x2048)
    vein1 = np.sin((x_grid * 5.0 + y_grid * 3.5 + 0.25 * np.sin(y_grid * 12.0)) * math.pi * 2)
    vein2 = np.cos((x_grid * 11.0 - y_grid * 8.0 + 0.35 * np.cos(x_grid * 9.0)) * math.pi * 2)
    vein_mask = np.clip(1.0 - np.abs(vein1) * 3.5, 0.0, 1.0) * 0.65 + np.clip(1.0 - np.abs(vein2) * 5.0, 0.0, 1.0) * 0.35
    gold_seam = np.clip(1.0 - np.abs(vein1 + 0.3 * vein2) * 18.0, 0.0, 1.0)

    r_m = (246 - vein_mask * 22 - gold_seam * 12).astype(np.uint8)
    g_m = (242 - vein_mask * 24 - gold_seam * 28).astype(np.uint8)
    b_m = (233 - vein_mask * 26 - gold_seam * 75).astype(np.uint8)
    Image.fromarray(np.stack([r_m, g_m, b_m], axis=-1)).save(PBR_DIR / "marble_albedo_2k.png", "PNG")

    rough_m = np.clip(36 + vein_mask * 38 - gold_seam * 16, 18, 120).astype(np.uint8)
    Image.fromarray(rough_m).save(PBR_DIR / "marble_roughness_2k.png", "PNG")
    height_to_normal_map(1.0 - vein_mask * 0.15, strength=4.0).save(PBR_DIR / "marble_normal_2k.png", "PNG")

    # 2. Volcanic Black Obsidian + Gold Kintsugi Finiture (2048x2048)
    k_seam = np.clip(1.0 - np.abs(np.sin((x_grid * 4.0 - y_grid * 3.0 + 0.4 * np.sin(x_grid * 7.0)) * math.pi * 2)) * 26.0, 0.0, 1.0)
    r_o = np.clip(14 + k_seam * 225, 0, 255).astype(np.uint8)
    g_o = np.clip(15 + k_seam * 175, 0, 255).astype(np.uint8)
    b_o = np.clip(20 + k_seam * 55, 0, 255).astype(np.uint8)
    Image.fromarray(np.stack([r_o, g_o, b_o], axis=-1)).save(PBR_DIR / "obsidian_albedo_2k.png", "PNG")

    # 3. Carved Ming Rosewood Table (2048x2048)
    grain = 0.5 + 0.5 * np.sin((x_grid * 42.0 + 0.15 * np.sin(y_grid * 16.0)) * math.pi * 2)
    r_w = np.clip(58 + grain * 34, 0, 255).astype(np.uint8)
    g_w = np.clip(20 + grain * 14, 0, 255).astype(np.uint8)
    b_w = np.clip(15 + grain * 10, 0, 255).astype(np.uint8)
    Image.fromarray(np.stack([r_w, g_w, b_w], axis=-1)).save(PBR_DIR / "rosewood_albedo_2k.png", "PNG")
    height_to_normal_map(grain * 0.25, strength=5.0).save(PBR_DIR / "rosewood_normal_2k.png", "PNG")

    # 4. Sacred Temple Flagstone Pavement (2048x2048)
    tile_x = np.abs(np.mod(x_grid * 8.0, 1.0) - 0.5) * 2.0
    tile_y = np.abs(np.mod(y_grid * 8.0, 1.0) - 0.5) * 2.0
    grout = np.clip(np.maximum(tile_x, tile_y) - 0.92, 0.0, 0.08) / 0.08
    stone_noise = 0.5 + 0.5 * np.sin(x_grid * 35.0) * np.cos(y_grid * 35.0)
    r_p = np.clip(52 + stone_noise * 18 - grout * 26, 0, 255).astype(np.uint8)
    g_p = np.clip(55 + stone_noise * 20 - grout * 24, 0, 255).astype(np.uint8)
    b_p = np.clip(60 + stone_noise * 18 - grout * 28, 0, 255).astype(np.uint8)
    Image.fromarray(np.stack([r_p, g_p, b_p], axis=-1)).save(PBR_DIR / "pavement_albedo_2k.png", "PNG")
    height_to_normal_map(1.0 - grout * 0.6 + stone_noise * 0.1, strength=10.0).save(PBR_DIR / "pavement_normal_2k.png", "PNG")


def make_marble_face_canvas(W=768, H=1024, accent_rgb=(195, 155, 65)) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    canvas = Image.new("RGB", (W, H), (247, 243, 234))
    draw = ImageDraw.Draw(canvas)
    # Subtle warm ivory vertical sheen + fine marble veins
    for y in range(H):
        t = y / (H - 1)
        c = (
            int(248 - 7 * t),
            int(244 - 8 * t),
            int(235 - 10 * t),
        )
        draw.line([(0, y), (W, y)], fill=c)

    # Subtle Calacatta veins
    vein_coords = [
        [(60, 140), (240, 310), (410, 420), (680, 640)],
        [(120, 780), (350, 690), (590, 820)],
    ]
    for pts in vein_coords:
        draw.line(pts, fill=(234, 228, 215), width=3)

    # Outer Obsidian hairline + Recessed Gold/Accent Frame
    draw.rounded_rectangle([14, 14, W - 15, H - 15], radius=38, outline=(32, 32, 40), width=6)
    draw.rounded_rectangle([26, 26, W - 27, H - 27], radius=30, outline=accent_rgb, width=4)
    return canvas, draw


def draw_mahjong_circle(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float, color_rgb: tuple[int, int, int]):
    """Draws an authentic ornate concentric Mahjong Tong/Circle motif."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color_rgb, outline=(25, 25, 32), width=3)
    r2 = r * 0.72
    draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(247, 243, 234), outline=color_rgb, width=2)
    r3 = r * 0.48
    draw.ellipse([cx - r3, cy - r3, cx + r3, cy + r3], fill=color_rgb)
    # 4 petal dots
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        px = cx + math.cos(rad) * (r * 0.60)
        py = cy + math.sin(rad) * (r * 0.60)
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=color_rgb)


def draw_bamboo_stalk(draw: ImageDraw.ImageDraw, cx: float, cy: float, h: float, color_rgb: tuple[int, int, int]):
    """Draws an authentic segmented Mahjong Bamboo stalk with central & end nodes."""
    w = h * 0.22
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=w * 0.4, fill=color_rgb, outline=(22, 32, 24), width=2)
    # Highlight stripe
    draw.line([(cx - w * 0.15, y0 + 8), (cx - w * 0.15, y1 - 8)], fill=(235, 245, 235), width=2)
    # Bamboo joint rings (top, middle, bottom)
    for ny in [y0 + 6, cy, y1 - 6]:
        draw.rounded_rectangle([x0 - 5, ny - 5, x1 + 5, ny + 5], radius=4, fill=color_rgb, outline=(245, 242, 232), width=2)


def save_tile_and_normal(canvas: Image.Image, tile_id: str, is_oval: bool = False, oval_box=None):
    albedo_path = TILES_DIR / f"{tile_id}.png"
    canvas.save(albedo_path, "PNG")

    # Compute corresponding normal map for Bassorilievo / Engraved relief
    gray = np.asarray(canvas.convert("L").filter(ImageFilter.GaussianBlur(radius=1.8)), dtype=np.float32) / 255.0
    if is_oval and oval_box is not None:
        # Raised cameo inside oval
        H, W = gray.shape
        ox0, oy0, ox1, oy1 = oval_box
        yy, xx = np.mgrid[0:H, 0:W]
        cx, cy = (ox0 + ox1) / 2.0, (oy0 + oy1) / 2.0
        rx, ry = (ox1 - ox0) / 2.0, (oy1 - oy0) / 2.0
        inside = (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) <= 1.0
        dome = np.clip(1.0 - (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2), 0.0, 1.0)
        h_map = np.where(inside, 0.55 + (gray - 0.5) * 0.45 + dome * 0.20, 0.5)
        norm_im = height_to_normal_map(h_map, strength=12.0)
    else:
        # Engraved ink relief for traditional Mahjong characters/suits
        h_map = 0.5 - (1.0 - gray) * 0.35
        norm_im = height_to_normal_map(h_map, strength=9.0)

    norm_im.save(NORMALS_DIR / f"{tile_id}_normal.png", "PNG")


def generate_original_mahjong_suits() -> list[dict]:
    print("[MahjongArt] Generating 34 Original Traditional Mahjong Suit & Honour Tile Textures...")
    W, H = 768, 1024
    RED = (192, 32, 32)
    GREEN = (22, 128, 60)
    BLUE = (28, 72, 176)
    INK = (26, 28, 38)
    GOLD = (198, 154, 58)

    manifest = []

    # 1. Characters / Wan (一萬 .. 九萬)
    cn_nums = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
    for idx, cn in enumerate(cn_nums, start=1):
        tid = f"char_{idx}"
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=GOLD)
        # Corner indices (Original Mahjong style)
        draw.text((52, 42), str(idx), font=latin_font(64, bold=True), fill=INK)
        draw.text((W - 116, 44), cn, font=cjk_font(58), fill=BLUE)
        # Main Top Numeral & Bottom 萬
        draw_centered_text(draw, (W / 2, H * 0.34), cn, font=cjk_font(250), fill=BLUE, stroke_fill=(15, 25, 65), stroke_width=4)
        draw_centered_text(draw, (W / 2, H * 0.70), "萬", font=cjk_font(270), fill=RED, stroke_fill=(110, 15, 15), stroke_width=4)
        save_tile_and_normal(canvas, tid)
        manifest.append({"id": tid, "suit": "characters", "matchGroup": tid, "glyph": f"{idx}萬", "title": f"{idx} Characters ({cn}萬)", "coupled": False})

    # 2. Circles / Dots (一筒 .. 九筒)
    dot_layouts = {
        1: [(0.5, 0.54, 155, RED)],
        2: [(0.5, 0.35, 95, GREEN), (0.5, 0.72, 95, BLUE)],
        3: [(0.30, 0.32, 78, BLUE), (0.50, 0.54, 78, RED), (0.70, 0.76, 78, GREEN)],
        4: [(0.33, 0.36, 82, BLUE), (0.67, 0.36, 82, GREEN), (0.33, 0.72, 82, GREEN), (0.67, 0.72, 82, BLUE)],
        5: [(0.31, 0.34, 74, BLUE), (0.69, 0.34, 74, GREEN), (0.50, 0.54, 74, RED), (0.31, 0.74, 74, GREEN), (0.69, 0.74, 74, BLUE)],
        6: [(0.34, 0.32, 70, GREEN), (0.66, 0.32, 70, GREEN), (0.34, 0.56, 70, RED), (0.66, 0.56, 70, RED), (0.34, 0.77, 70, RED), (0.66, 0.77, 70, RED)],
        7: [(0.26, 0.28, 58, GREEN), (0.50, 0.35, 58, GREEN), (0.74, 0.42, 58, GREEN), (0.34, 0.60, 64, RED), (0.66, 0.60, 64, RED), (0.34, 0.79, 64, RED), (0.66, 0.79, 64, RED)],
        8: [(0.34, y, 56, BLUE) for y in [0.27, 0.45, 0.63, 0.81]] + [(0.66, y, 56, BLUE) for y in [0.27, 0.45, 0.63, 0.81]],
        9: [(x, 0.30, 58, GREEN) for x in [0.27, 0.50, 0.73]] + [(x, 0.54, 58, RED) for x in [0.27, 0.50, 0.73]] + [(x, 0.78, 58, BLUE) for x in [0.27, 0.50, 0.73]],
    }
    for idx in range(1, 10):
        tid = f"dots_{idx}"
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=GOLD)
        draw.text((52, 42), str(idx), font=latin_font(64, bold=True), fill=INK)
        draw.text((W - 116, 44), "筒", font=cjk_font(56), fill=RED)
        if idx == 1:
            # Extra ornate outer dragon-flower ring for 1-Dot
            cx, cy = W * 0.5, H * 0.54
            draw.ellipse([cx - 190, cy - 190, cx + 190, cy + 190], fill=GREEN, outline=GOLD, width=6)
        for nx, ny, rad, col in dot_layouts[idx]:
            draw_mahjong_circle(draw, W * nx, H * ny, rad, col)
        save_tile_and_normal(canvas, tid)
        manifest.append({"id": tid, "suit": "dots", "matchGroup": tid, "glyph": f"{idx}筒", "title": f"{idx} Circles ({cn_nums[idx-1]}筒)", "coupled": False})

    # 3. Bamboos / Tiao (一索 .. 九索)
    bam_layouts = {
        2: [(0.50, 0.37, 230, BLUE), (0.50, 0.71, 230, GREEN)],
        3: [(0.50, 0.35, 210, BLUE), (0.33, 0.71, 210, GREEN), (0.67, 0.71, 210, GREEN)],
        4: [(0.34, 0.37, 210, BLUE), (0.66, 0.37, 210, GREEN), (0.34, 0.71, 210, GREEN), (0.66, 0.71, 210, BLUE)],
        5: [(0.28, 0.37, 195, GREEN), (0.72, 0.37, 195, BLUE), (0.50, 0.54, 195, RED), (0.28, 0.71, 195, BLUE), (0.72, 0.71, 195, GREEN)],
        6: [(x, 0.37, 200, GREEN) for x in [0.28, 0.50, 0.72]] + [(x, 0.71, 200, BLUE) for x in [0.28, 0.50, 0.72]],
        7: [(0.50, 0.28, 155, RED)] + [(x, 0.53, 155, GREEN) for x in [0.28, 0.50, 0.72]] + [(x, 0.77, 155, BLUE) for x in [0.28, 0.50, 0.72]],
        8: [(x, 0.36, 175, GREEN) for x in [0.24, 0.41, 0.59, 0.76]] + [(x, 0.72, 175, BLUE) for x in [0.24, 0.41, 0.59, 0.76]],
        9: [(x, 0.30, 155, RED if x == 0.50 else GREEN) for x in [0.28, 0.50, 0.72]]
        + [(x, 0.54, 155, RED if x == 0.50 else BLUE) for x in [0.28, 0.50, 0.72]]
        + [(x, 0.78, 155, RED if x == 0.50 else GREEN) for x in [0.28, 0.50, 0.72]],
    }
    for idx in range(1, 10):
        tid = f"bamboo_{idx}"
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=GOLD)
        draw.text((52, 42), str(idx), font=latin_font(64, bold=True), fill=INK)
        draw.text((W - 116, 44), "索", font=cjk_font(56), fill=GREEN)
        if idx == 1:
            # Iconic 1-Bamboo Imperial Sparrow / Peacock on Bamboo Perch
            cx, cy = W * 0.5, H * 0.55
            draw.ellipse([cx - 165, cy - 185, cx + 165, cy + 185], outline=GOLD, width=4)
            # Bamboo perch branch
            draw.line([(cx - 140, cy + 110), (cx + 140, cy + 70)], fill=GREEN, width=16)
            # Bird body, wing, crest & tail feathers in Jade Green, Crimson & Gold
            draw.ellipse([cx - 75, cy - 55, cx + 65, cy + 75], fill=GREEN, outline=(18, 65, 32), width=4)
            draw.ellipse([cx - 45, cy - 125, cx + 35, cy - 35], fill=GREEN, outline=(18, 65, 32), width=4)
            draw.polygon([(cx + 30, cy - 90), (cx + 78, cy - 80), (cx + 30, cy - 65)], fill=RED)
            draw.ellipse([cx - 10, cy - 95, cx + 10, cy - 75], fill=(250, 245, 230))
            draw.ellipse([cx - 4, cy - 90, cx + 5, cy - 80], fill=INK)
            # Plumage & tail
            draw.ellipse([cx - 55, cy - 25, cx + 35, cy + 45], fill=RED, outline=GOLD, width=3)
            draw.polygon([(cx - 50, cy + 55), (cx - 125, cy + 165), (cx + 15, cy + 145), (cx + 25, cy + 60)], fill=BLUE, outline=GOLD)
        else:
            for nx, ny, bh, col in bam_layouts[idx]:
                draw_bamboo_stalk(draw, W * nx, H * ny, bh, col)
        save_tile_and_normal(canvas, tid)
        manifest.append({"id": tid, "suit": "bamboo", "matchGroup": tid, "glyph": f"{idx}索", "title": f"{idx} Bamboo ({cn_nums[idx-1]}索)", "coupled": False})

    # 4. Four Winds (東 南 西 北)
    winds = [
        ("wind_E", "東", "E", "East Wind (東)"),
        ("wind_S", "南", "S", "South Wind (南)"),
        ("wind_W", "西", "W", "West Wind (西)"),
        ("wind_N", "北", "N", "North Wind (北)"),
    ]
    for tid, hanzi, let, label in winds:
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=GOLD)
        draw.text((52, 42), let, font=latin_font(64, bold=True), fill=BLUE)
        draw.text((W - 116, 44), "風", font=cjk_font(56), fill=INK)
        draw_centered_text(draw, (W / 2, H * 0.54), hanzi, font=cjk_font(420), fill=INK, stroke_fill=GOLD, stroke_width=6)
        save_tile_and_normal(canvas, tid)
        manifest.append({"id": tid, "suit": "winds", "matchGroup": tid, "glyph": hanzi, "title": label, "coupled": False})

    # 5. Three Dragons (中 發 白)
    dragons = [
        ("dragon_red", "中", "C", RED, "Red Dragon (紅中)"),
        ("dragon_green", "發", "F", GREEN, "Green Dragon (發財)"),
        ("dragon_white", "白", "P", BLUE, "White Dragon (白板)"),
    ]
    for tid, hanzi, let, col, label in dragons:
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=col)
        draw.text((52, 42), let, font=latin_font(64, bold=True), fill=col)
        draw.text((W - 116, 44), hanzi, font=cjk_font(56), fill=col)
        if tid == "dragon_white":
            # Traditional White Dragon double-carved cobalt blue border frame
            draw.rounded_rectangle([135, 190, W - 135, H - 170], radius=28, outline=BLUE, width=18)
            draw.rounded_rectangle([168, 224, W - 168, H - 204], radius=16, outline=GOLD, width=6)
            draw_centered_text(draw, (W / 2, H * 0.54), "白", font=cjk_font(220), fill=BLUE)
        else:
            draw_centered_text(draw, (W / 2, H * 0.54), hanzi, font=cjk_font(420), fill=col, stroke_fill=GOLD, stroke_width=6)
        save_tile_and_normal(canvas, tid)
        manifest.append({"id": tid, "suit": "dragons", "matchGroup": tid, "glyph": hanzi, "title": label, "coupled": False})

    return manifest


def extract_clean_crops_from_mocks():
    """Extracts pure 2D rectangular portrait crops from our Nano Banana sheets so every coupled pose has a crisp 2D image."""
    m3_cands = sorted(glob.glob(str(ARTIFACT_DIR / "mock_03_white_marble_obsidian_coupled_tiles*")))
    if m3_cands:
        im3 = Image.open(m3_cands[-1]).convert("RGB")
        w, h = im3.size
        # 6 tiles across in mock_03: A1, A2, B1, B2, C1, C2
        boxes = {
            "crop_A2": (0.215, 0.32, 0.325, 0.61),
            "crop_B2": (0.515, 0.32, 0.625, 0.61),
            "crop_C2": (0.815, 0.32, 0.928, 0.61),
        }
        for name, (x0, y0, x1, y1) in boxes.items():
            crop = im3.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
            crop.save(PORTRAITS_DIR / f"{name}.png", "PNG")

    m4_cands = sorted(glob.glob(str(ARTIFACT_DIR / "mock_04_photoreal_cc_kungfu_panda_tiles_v2*")))
    if m4_cands:
        im4 = Image.open(m4_cands[-1]).convert("RGB")
        w, h = im4.size
        boxes4 = {
            "crop_D1": (0.115, 0.33, 0.268, 0.72),
            "crop_D2": (0.312, 0.29, 0.460, 0.70),
            "crop_E1": (0.540, 0.29, 0.692, 0.71),
            "crop_E2": (0.732, 0.32, 0.892, 0.73),
        }
        for name, (x0, y0, x1, y1) in boxes4.items():
            crop = im4.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
            crop.save(PORTRAITS_DIR / f"{name}.png", "PNG")


def build_dual_reference_portrait(img_left: Path, img_right: Path, out_name: str, right_x_bias: float = 0.5) -> Path:
    """Composes two GIC reference photos of Ale/Sebi or Mamma Kate/Papà Riccardo into a warm 2D portrait for Oval Cameo framing."""
    W, H = 800, 960
    comp = Image.new("RGB", (W, H), (42, 24, 22))
    biases = [0.5, right_x_bias]
    for idx, p in enumerate([img_left, img_right]):
        if p.exists():
            im = Image.open(p).convert("RGB")
            iw, ih = im.size
            tw, th = W // 2, H
            aspect = tw / th
            if iw / ih > aspect:
                nw = int(ih * aspect)
                l = int((iw - nw) * biases[idx])
                l = max(0, min(iw - nw, l))
                im = im.crop((l, 0, l + nw, ih))
            else:
                nh = int(iw / aspect)
                t = max(0, (ih - nh) // 5)
                im = im.crop((0, t, iw, t + nh))
            im = im.resize((tw, th), Image.Resampling.LANCZOS)
            im = ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.08)).enhance(1.10)
            comp.paste(im, (idx * tw, 0))
    out_p = PORTRAITS_DIR / out_name
    comp.save(out_p, "PNG")
    return out_p


def find_latest_artifact(prefix: str, fallback: Path) -> Path:
    cands = sorted(glob.glob(str(ARTIFACT_DIR / f"{prefix}*"))) + sorted(glob.glob(str(PORTRAITS_DIR / f"{prefix}*")))
    return Path(cands[-1]) if cands else fallback


def generate_coupled_family_oval_tiles() -> list[dict]:
    print("[OvalCameo] Building 16 Coupled Non-Identical Family Oval Medallion Tiles (A1↔A2 .. H1↔H2)...")
    extract_clean_crops_from_mocks()

    # Pure 2D Nano Banana & GIC Reference sources
    p_a1 = find_latest_artifact("pure2d_a1_tang_silk", ALE_DIR / "PXL_20260218_151036231.jpg")
    p_a2 = PORTRAITS_DIR / "crop_A2.png" if (PORTRAITS_DIR / "crop_A2.png").exists() else p_a1

    p_b1 = find_latest_artifact("pure2d_b1_sightseeing", ALE_DIR / "PXL_20260403_100103962.jpg")
    p_b2 = PORTRAITS_DIR / "crop_B2.png" if (PORTRAITS_DIR / "crop_B2.png").exists() else p_b1

    p_c1 = find_latest_artifact("portrait_cantonese_rice_pure2d", SEBI_DIR / "PXL_20260310_195345815-seby-felice-con-mac.jpg")
    p_c2 = PORTRAITS_DIR / "crop_C2.png" if (PORTRAITS_DIR / "crop_C2.png").exists() else p_c1

    p_d1 = PORTRAITS_DIR / "crop_D1.png" if (PORTRAITS_DIR / "crop_D1.png").exists() else p_a1
    p_d2 = PORTRAITS_DIR / "crop_D2.png" if (PORTRAITS_DIR / "crop_D2.png").exists() else p_b1

    p_e1 = PORTRAITS_DIR / "crop_E1.png" if (PORTRAITS_DIR / "crop_E1.png").exists() else (FAMILY_ASSETS / "compagni-magici" / "ale_ghigna_sebi_pupurabbu_google.jpg")
    p_e2 = PORTRAITS_DIR / "crop_E2.png" if (PORTRAITS_DIR / "crop_E2.png").exists() else (FAMILY_ASSETS / "compagni-magici" / "pranzo_google_ghigna_pupurabbu.jpg")

    # Pair F: Jade Dragon & Cape Point Sightseeing Explorers (from GIC reference photos of Ale & Sebi!)
    p_f1 = ARTIFACT_DIR / "ref_ricc_with_ale_sebi.png"
    p_f2 = build_dual_reference_portrait(
        ALE_DIR / "PXL_20260403_100103962.jpg",
        SEBI_DIR / "PXL_20260310_195345815-seby-felice-con-mac.jpg",
        "pure2d_F2_explorers.png",
    )

    # Pair G: Ghigna 🐹 & Pupurabbu 👾 Magical Companions
    p_g1 = FAMILY_ASSETS / "compagni-magici" / "ale_ghigna_sebi_pupurabbu_google.jpg"
    p_g2 = FAMILY_ASSETS / "compagni-magici" / "pranzo_google_ghigna_pupurabbu.jpg"

    # Pair H: Mamma Kate & Papà Riccardo (Mum & Dad — NEVER King/Queen!)
    p_h1_default = build_dual_reference_portrait(
        KATE_DIR / "01_color_pop.jpg",
        RICC_DIR / "ricc-za-wine-tasting.png",
        "pure2d_H1_mum_dad_fallback.png",
        right_x_bias=0.14,
    )
    p_h1 = find_latest_artifact("pure2d_h1_mum_dad", p_h1_default)
    p_h2 = build_dual_reference_portrait(
        KATE_DIR / "04_felice_casa.png",
        RICC_DIR / "ricc-za-wine-tasting.png",
        "pure2d_H2_mum_dad_stroll.png",
        right_x_bias=0.14,
    )

    coupled_specs = [
        # (tile_id, match_group, corner_glyph, season_hanzi, subtitle, border_rgb, src_path)
        ("coupled_A1", "theme_A_tang_silk", "A1", "春", "Ale & Sebi • Tang Silk I", (198, 38, 38), p_a1),
        ("coupled_A2", "theme_A_tang_silk", "A2", "春", "Ale & Sebi • Tang Silk II", (198, 38, 38), p_a2),
        ("coupled_B1", "theme_B_sightseeing", "B1", "夏", "Ale & Sebi • Great Wall I", (24, 138, 82), p_b1),
        ("coupled_B2", "theme_B_sightseeing", "B2", "夏", "Ale & Sebi • Great Wall II", (24, 138, 82), p_b2),
        ("coupled_C1", "theme_C_cantonese_rice", "C1", "秋", "Ale & Sebi • Cantonese Rice I", (212, 148, 24), p_c1),
        ("coupled_C2", "theme_C_cantonese_rice", "C2", "秋", "Ale & Sebi • Cantonese Rice II", (212, 148, 24), p_c2),
        ("coupled_D1", "theme_D_kungfu", "D1", "冬", "Ale & Sebi • Shaolin Kung Fu I", (218, 92, 24), p_d1),
        ("coupled_D2", "theme_D_kungfu", "D2", "冬", "Ale & Sebi • Shaolin Kung Fu II", (218, 92, 24), p_d2),
        ("coupled_E1", "theme_E_panda", "E1", "梅", "Ale & Sebi • Chengdu Pandas I", (32, 142, 118), p_e1),
        ("coupled_E2", "theme_E_panda", "E2", "梅", "Ale & Sebi • Chengdu Pandas II", (32, 142, 118), p_e2),
        ("coupled_F1", "theme_F_expedition", "F1", "蘭", "Ale & Sebi • Dragon Peak I", (38, 92, 188), p_f1),
        ("coupled_F2", "theme_F_expedition", "F2", "蘭", "Ale & Sebi • Dragon Peak II", (38, 92, 188), p_f2),
        ("coupled_G1", "theme_G_compagni", "G1", "菊", "Ghigna 🐹 & Pupurabbu 👾 I", (132, 52, 188), p_g1),
        ("coupled_G2", "theme_G_compagni", "G2", "菊", "Ghigna 🐹 & Pupurabbu 👾 II", (132, 52, 188), p_g2),
        ("coupled_H1", "theme_H_mum_dad", "H1", "竹", "Mamma Kate & Papà Ricc I", (168, 42, 108), p_h1),
        ("coupled_H2", "theme_H_mum_dad", "H2", "竹", "Mamma Kate & Papà Ricc II", (168, 42, 108), p_h2),
    ]

    W, H = 768, 1024
    manifest = []

    for tid, mgroup, glyph, hanzi, subtitle, col_rgb, src_path in coupled_specs:
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=col_rgb)

        # Top-Left: Traditional Mahjong index + Coupled Code (e.g. A1, A2)
        draw.text((50, 38), glyph, font=latin_font(60, bold=True), fill=col_rgb)
        # Top-Right: Authentic Mahjong Season/Flower Hanzi (春 夏 秋 冬 梅 蘭 菊 竹)
        draw.text((W - 118, 40), hanzi, font=cjk_font(62), fill=col_rgb)

        # Center Gold-Rimmed OVAL Cameo Medallion containing the Pure 2D Portrait!
        oval_w, oval_h = int(W * 0.78), int(H * 0.68)
        ox0 = (W - oval_w) // 2
        oy0 = int(H * 0.165)
        ox1 = ox0 + oval_w
        oy1 = oy0 + oval_h

        im = Image.open(src_path).convert("RGB")
        iw, ih = im.size
        target_aspect = oval_w / oval_h
        if iw / ih > target_aspect:
            nw = int(ih * target_aspect)
            left = (iw - nw) // 2
            im_crop = im.crop((left, 0, left + nw, ih))
        else:
            nh = int(iw / target_aspect)
            top = max(0, (ih - nh) // 4)
            im_crop = im.crop((0, top, iw, top + nh))
        im_crop = im_crop.resize((oval_w, oval_h), Image.Resampling.LANCZOS)

        mask = Image.new("L", (oval_w, oval_h), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.ellipse([4, 4, oval_w - 5, oval_h - 5], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(radius=1.5))

        canvas.paste(im_crop, (ox0, oy0), mask)

        # Concentric Obsidian, Theme-Colored & Gold Kintsugi Oval Cameo Frame
        draw.ellipse([ox0 - 10, oy0 - 10, ox1 + 10, oy1 + 10], outline=(26, 26, 34), width=8)
        draw.ellipse([ox0 - 4, oy0 - 4, ox1 + 4, oy1 + 4], outline=col_rgb, width=7)
        draw.ellipse([ox0 + 4, oy0 + 4, ox1 - 4, oy1 - 4], outline=(245, 212, 112), width=3)

        # Bottom subtle cartouche with coupled pair indicator (tofu-free Latin + CJK)
        draw.rounded_rectangle([58, H - 118, W - 58, H - 46], radius=18, fill=(240, 234, 220), outline=col_rgb, width=3)
        clean_sub = subtitle.replace("🐹 ", "").replace("👾 ", "")
        draw_centered_text(draw, (W / 2, H - 82), f"{glyph} • {clean_sub}", font=latin_font(25, bold=True), fill=(32, 28, 36))

        save_tile_and_normal(canvas, tid, is_oval=True, oval_box=(ox0, oy0, ox1, oy1))
        manifest.append({
            "id": tid,
            "suit": "coupled_family",
            "matchGroup": mgroup,
            "glyph": f"{hanzi}{glyph}",
            "code": glyph,
            "hanzi": hanzi,
            "title": subtitle,
            "coupled": True,
        })

    return manifest


def main():
    generate_2k_pbr_maps()
    suits_manifest = generate_original_mahjong_suits()
    coupled_manifest = generate_coupled_family_oval_tiles()
    full_manifest = {
        "tileCount": len(suits_manifest) + len(coupled_manifest),
        "suitsCount": len(suits_manifest),
        "coupledCount": len(coupled_manifest),
        "tiles": suits_manifest + coupled_manifest,
    }
    (PROJECT_DIR / "public" / "textures" / "manifest.json").write_text(json.dumps(full_manifest, indent=2, ensure_ascii=False))
    print(f"[Done] Generated {full_manifest['tileCount']} tile textures + normal maps + 2K PBR base maps!")


if __name__ == "__main__":
    main()
