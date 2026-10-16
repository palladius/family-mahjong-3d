#!/usr/bin/env python3
"""
Remastered 2K PBR & 50-Tile Mahjong Deck Texture Generator (macOS & Linux portable).
Generates:
1. 2K Baked/Procedural PBR Base Maps (2048x2048) for White Imperial Marble, Volcanic Black Obsidian + Gold Kintsugi Finiture,
   Carved Ming Rosewood Table, Celadon Jade Mat, and Sacred Chinese Temple Flagstone Pavement.
2. All 34 Original Traditional Mahjong Tile Faces (Characters 1-9 萬, Circles 1-9 筒, Bamboos 1-9 索 with ornate 1-Bamboo Imperial Sparrow/Peacock,
   Winds 東南西北, Dragons 中發白) with authentic Original Mahjong calligraphy & corner glyphs.
3. All 16 Non-Identical Family & Magical Companion Tile Faces:
   - Quartet 1 (Cardinality 4, `matchGroup: "quartet_family_seasons"`):
     `S1` Solo Papà Riccardo, `S2` Solo Mamma Kate, `S3` Solo Ale, `S4` Solo Sebi (any 2 of the 4 match!)
   - Quartet 2 (Cardinality 4, `matchGroup: "quartet_magic_flowers"`):
     `M1` Ale & Ghigna 🐹, `M2` Sebi & Pupurabbu 👾, `M3` Solo Ghigna 🐹, `M4` Solo Pupurabbu 👾 (any 2 of the 4 match!)
   - 4 Diptyque Split-Pairs (Cardinality 2, `Solo Ale <-> Solo Sebi` split from one shared scene):
     * `E1 <-> E2` Great Wall Explorers (`Solo Ale` <-> `Solo Sebi`)
     * `F1 <-> F2` Cantonese Fried Rice (`Solo Ale` <-> `Solo Sebi`)
     * `G1 <-> G2` Shaolin Kung Fu Dragon & Tiger (`Solo Ale` <-> `Solo Sebi`)
     * `H1 <-> H2` Chengdu Giant Pandas (`Solo Ale` <-> `Solo Sebi`)
"""
import json
import math
import shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

PROJECT_DIR = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = Path("/Users/ricc/.gemini/antigravity/brain/9efaaa30-d5fa-49dc-b7c4-7292c03768b3")
PBR_DIR = PROJECT_DIR / "public" / "textures" / "pbr"
TILES_DIR = PROJECT_DIR / "public" / "textures" / "tiles"
NORMALS_DIR = PROJECT_DIR / "public" / "textures" / "tiles_normal"
PORTRAITS_DIR = PROJECT_DIR / "public" / "portraits"

for d in [PBR_DIR, TILES_DIR, NORMALS_DIR, PORTRAITS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

CJK_FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
]
LATIN_BOLD_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
LATIN_REG_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def cjk_font(size: int):
    for p in CJK_FONT_CANDIDATES:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def latin_font(size: int, bold: bool = True):
    cands = LATIN_BOLD_CANDIDATES if bold else LATIN_REG_CANDIDATES
    for p in cands:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                continue
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
    print("[PBR] Ensuring 2048x2048 2K PBR Base Maps (both *_albedo_2k.png and *_basecolor_2k.png aliases)...")
    S = 2048
    if not (PBR_DIR / "marble_albedo_2k.png").exists():
        y_grid, x_grid = np.mgrid[0:S, 0:S].astype(np.float32) / S
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

        k_seam = np.clip(1.0 - np.abs(np.sin((x_grid * 4.0 - y_grid * 3.0 + 0.4 * np.sin(x_grid * 7.0)) * math.pi * 2)) * 26.0, 0.0, 1.0)
        r_o = np.clip(14 + k_seam * 225, 0, 255).astype(np.uint8)
        g_o = np.clip(15 + k_seam * 175, 0, 255).astype(np.uint8)
        b_o = np.clip(20 + k_seam * 55, 0, 255).astype(np.uint8)
        Image.fromarray(np.stack([r_o, g_o, b_o], axis=-1)).save(PBR_DIR / "obsidian_albedo_2k.png", "PNG")

        grain = 0.5 + 0.5 * np.sin((x_grid * 42.0 + 0.15 * np.sin(y_grid * 16.0)) * math.pi * 2)
        r_w = np.clip(58 + grain * 34, 0, 255).astype(np.uint8)
        g_w = np.clip(20 + grain * 14, 0, 255).astype(np.uint8)
        b_w = np.clip(15 + grain * 10, 0, 255).astype(np.uint8)
        Image.fromarray(np.stack([r_w, g_w, b_w], axis=-1)).save(PBR_DIR / "rosewood_albedo_2k.png", "PNG")
        height_to_normal_map(grain * 0.25, strength=5.0).save(PBR_DIR / "rosewood_normal_2k.png", "PNG")

        tile_x = np.abs(np.mod(x_grid * 8.0, 1.0) - 0.5) * 2.0
        tile_y = np.abs(np.mod(y_grid * 8.0, 1.0) - 0.5) * 2.0
        grout = np.clip(np.maximum(tile_x, tile_y) - 0.92, 0.0, 0.08) / 0.08
        stone_noise = 0.5 + 0.5 * np.sin(x_grid * 35.0) * np.cos(y_grid * 35.0)
        r_p = np.clip(52 + stone_noise * 18 - grout * 26, 0, 255).astype(np.uint8)
        g_p = np.clip(55 + stone_noise * 20 - grout * 24, 0, 255).astype(np.uint8)
        b_p = np.clip(60 + stone_noise * 18 - grout * 28, 0, 255).astype(np.uint8)
        Image.fromarray(np.stack([r_p, g_p, b_p], axis=-1)).save(PBR_DIR / "pavement_albedo_2k.png", "PNG")
        height_to_normal_map(1.0 - grout * 0.6 + stone_noise * 0.1, strength=10.0).save(PBR_DIR / "pavement_normal_2k.png", "PNG")

    # Ensure basecolor aliases and jade/obsidian normal maps exist so zero 404s happen in Three.js or Blender
    aliases = [
        ("marble_albedo_2k.png", "marble_basecolor_2k.png"),
        ("obsidian_albedo_2k.png", "obsidian_basecolor_2k.png"),
        ("rosewood_albedo_2k.png", "rosewood_basecolor_2k.png"),
        ("pavement_albedo_2k.png", "pavement_basecolor_2k.png"),
        ("marble_normal_2k.png", "obsidian_normal_2k.png"),
    ]
    for src_name, dst_name in aliases:
        src_p = PBR_DIR / src_name
        dst_p = PBR_DIR / dst_name
        if src_p.exists() and not dst_p.exists():
            shutil.copy2(src_p, dst_p)

    jade_p = PBR_DIR / "jade_basecolor_2k.png"
    if not jade_p.exists():
        y_g, x_g = np.mgrid[0:512, 0:512].astype(np.float32) / 512.0
        j_swirl = 0.5 + 0.5 * np.sin((x_g * 6.0 + y_g * 4.0) * math.pi * 2)
        jr = (158 + j_swirl * 18).astype(np.uint8)
        jg = (198 + j_swirl * 22).astype(np.uint8)
        jb = (172 + j_swirl * 16).astype(np.uint8)
        Image.fromarray(np.stack([jr, jg, jb], axis=-1)).save(jade_p, "PNG")


def make_marble_face_canvas(W=768, H=1024, accent_rgb=(195, 155, 65)) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    canvas = Image.new("RGB", (W, H), (247, 243, 234))
    draw = ImageDraw.Draw(canvas)
    for y in range(H):
        t = y / (H - 1)
        c = (int(248 - 7 * t), int(244 - 8 * t), int(235 - 10 * t))
        draw.line([(0, y), (W, y)], fill=c)

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
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color_rgb, outline=(25, 25, 32), width=3)
    r2 = r * 0.72
    draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(247, 243, 234), outline=color_rgb, width=2)
    r3 = r * 0.48
    draw.ellipse([cx - r3, cy - r3, cx + r3, cy + r3], fill=color_rgb)
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        px = cx + math.cos(rad) * (r * 0.60)
        py = cy + math.sin(rad) * (r * 0.60)
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=color_rgb)


def draw_bamboo_stalk(draw: ImageDraw.ImageDraw, cx: float, cy: float, h: float, color_rgb: tuple[int, int, int]):
    w = h * 0.22
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=w * 0.4, fill=color_rgb, outline=(22, 32, 24), width=2)
    draw.line([(cx - w * 0.15, y0 + 8), (cx - w * 0.15, y1 - 8)], fill=(235, 245, 235), width=2)
    for ny in [y0 + 6, cy, y1 - 6]:
        draw.rounded_rectangle([x0 - 5, ny - 5, x1 + 5, ny + 5], radius=4, fill=color_rgb, outline=(245, 242, 232), width=2)


def save_tile_and_normal(canvas: Image.Image, tile_id: str, is_oval: bool = False, oval_box=None):
    albedo_path = TILES_DIR / f"{tile_id}.png"
    canvas.save(albedo_path, "PNG")

    gray = np.asarray(canvas.convert("L").filter(ImageFilter.GaussianBlur(radius=1.8)), dtype=np.float32) / 255.0
    if is_oval and oval_box is not None:
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
        h_map = 0.5 - (1.0 - gray) * 0.35
        norm_im = height_to_normal_map(h_map, strength=9.0)

    norm_im.save(NORMALS_DIR / f"{tile_id}_normal.png", "PNG")


ONIRICA_DIR = PROJECT_DIR / "public" / "textures" / "tiles_onirica"
ONIRICA_DIR.mkdir(parents=True, exist_ok=True)


def build_onirica_tile(
    W: int,
    H: int,
    src_crop: Image.Image,
    glyph_left: str,
    glyph_right: str,
    col_rgb: tuple[int, int, int],
    tile_id: str,
    max_opacity: float = 0.50,
):
    """
    Modalità Onirica ('Less is More'):
    - Pure luminous white marble canvas with wide white breathing room (no solid oval frame, no bottom box).
    - The portrait/emblem is softly infused into the white stone like an ethereal watercolor/memory wash
      ('una sfumatura che non vedi bene se c'e' o non c'e'').
    """
    canvas = Image.new("RGB", (W, H), (252, 249, 243))
    draw = ImageDraw.Draw(canvas)
    for y in range(H):
        t = y / (H - 1)
        c = (int(253 - 4 * t), int(250 - 5 * t), int(244 - 6 * t))
        draw.line([(0, y), (W, y)], fill=c)

    # Pure untouched Imperial White Marble (no diagonal vein line crossing the face)
    soft_gold = (226, 202, 145)
    draw.rounded_rectangle([24, 24, W - 25, H - 25], radius=32, outline=soft_gold, width=2)

    # Prepare ethereal watercolor-like stone wash of src_crop in a compact central region (lots of white space!)
    wash_w, wash_h = int(W * 0.62), int(H * 0.52)
    wx0 = (W - wash_w) // 2
    wy0 = int(H * 0.23)

    im_fit = ImageOps.fit(src_crop, (wash_w, wash_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.42))
    im_soft = im_fit.filter(ImageFilter.GaussianBlur(radius=0.9))
    arr = np.asarray(im_soft, dtype=np.float32) / 255.0
    luma = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]

    # Watercolor-pastel stone blend: preserve warm skin & character colors while lifting dark background shadows
    pastel = np.zeros_like(arr)
    tint = np.array([col_rgb[0] / 255.0, col_rgb[1] / 255.0, col_rgb[2] / 255.0], dtype=np.float32)
    for c_i in range(3):
        pastel[:, :, c_i] = arr[:, :, c_i] * 0.74 + (luma * 0.85 + tint[c_i] * 0.15) * 0.26
    # Gently lift deep shadows so it reads like a luminous watercolor wash on white marble
    pastel = 1.0 - (1.0 - pastel) * 0.76
    pastel_im = Image.fromarray(np.clip(pastel * 255.0, 0, 255).astype(np.uint8))

    # Build a tight, organic cloud-like radial fade mask focused on the face/center (75%+ pure white marble around it)
    yy, xx = np.mgrid[0:wash_h, 0:wash_w]
    nx = (xx - wash_w * 0.50) / (wash_w * 0.41)
    ny = (yy - wash_h * 0.45) / (wash_h * 0.42)
    dist2 = nx * nx + ny * ny
    cloud = (
        0.09 * np.sin(xx * 0.045 + yy * 0.03)
        + 0.07 * np.cos(xx * 0.03 - yy * 0.05)
        + 0.05 * np.sin((xx + yy) * 0.07)
    )
    radial = np.clip(1.0 - (dist2 + cloud), 0.0, 1.0) ** 2.05
    detail_weight = np.clip(1.0 - luma * 0.30, 0.65, 1.0)
    alpha = np.clip(radial * detail_weight * max_opacity * 255.0, 0, 255).astype(np.uint8)
    alpha_im = Image.fromarray(alpha, mode="L").filter(ImageFilter.GaussianBlur(radius=8.0))

    canvas.paste(pastel_im, (wx0, wy0), alpha_im)

    # Subtle, airy corner glyphs in muted ink/theme tint
    soft_col = (
        int(col_rgb[0] * 0.72 + 55),
        int(col_rgb[1] * 0.72 + 50),
        int(col_rgb[2] * 0.72 + 50),
    )
    draw.text((52, 40), glyph_left, font=latin_font(56, bold=True), fill=soft_col)
    draw.text((W - 114, 42), glyph_right, font=cjk_font(56), fill=soft_col)

    out_path = ONIRICA_DIR / f"{tile_id}.png"
    canvas.save(out_path, "PNG")
    if ARTIFACT_DIR.exists():
        shutil.copy2(out_path, ARTIFACT_DIR / f"onirica_{tile_id}.png")


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
        draw.text((52, 42), str(idx), font=latin_font(64, bold=True), fill=INK)
        draw.text((W - 116, 44), cn, font=cjk_font(58), fill=BLUE)
        draw_centered_text(draw, (W / 2, H * 0.34), cn, font=cjk_font(250), fill=BLUE, stroke_fill=(15, 25, 65), stroke_width=4)
        draw_centered_text(draw, (W / 2, H * 0.70), "萬", font=cjk_font(270), fill=RED, stroke_fill=(110, 15, 15), stroke_width=4)
        save_tile_and_normal(canvas, tid)
        shutil.copy2(TILES_DIR / f"{tid}.png", ONIRICA_DIR / f"{tid}.png")
        manifest.append({"id": tid, "suit": "characters", "matchGroup": tid, "cardinality": 2, "glyph": f"{idx}萬", "title": f"{idx} Characters ({cn}萬)", "coupled": False})

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
            cx, cy = W * 0.5, H * 0.54
            draw.ellipse([cx - 190, cy - 190, cx + 190, cy + 190], fill=GREEN, outline=GOLD, width=6)
        for nx, ny, rad, col in dot_layouts[idx]:
            draw_mahjong_circle(draw, W * nx, H * ny, rad, col)
        save_tile_and_normal(canvas, tid)
        shutil.copy2(TILES_DIR / f"{tid}.png", ONIRICA_DIR / f"{tid}.png")
        manifest.append({"id": tid, "suit": "dots", "matchGroup": tid, "cardinality": 2, "glyph": f"{idx}筒", "title": f"{idx} Circles ({cn_nums[idx-1]}筒)", "coupled": False})

    # 3. Bamboos / Tiao (一索 .. 九索) — with Special Comedic Carved Bamboo & Gold Emblems on 1..4!
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
    special_bamboos = {
        1: (PORTRAITS_DIR / "bamboo_1_sparrow_emblem.png", (0.235, 0.215, 0.785, 0.765), "1 Bamboo • Imperial Sparrow (一索)"),
        2: (PORTRAITS_DIR / "bamboo_2_hotwheels_emblem.png", (0.06, 0.12, 0.94, 0.88), "2 Bamboo • Hot Wheels Bamboo & Gold Racer (二索)"),
        3: (PORTRAITS_DIR / "bamboo_3_shiryu_dragon_emblem.png", (0.10, 0.08, 0.90, 0.93), "3 Bamboo • Sirio il Dragone Bamboo & Gold (三索)"),
        4: (PORTRAITS_DIR / "bamboo_4_gems_rubies_emblem.png", (0.08, 0.08, 0.92, 0.92), "4 Bamboo • Ale's Rubies, Diamonds & Bamboo Gold (四索)"),
    }
    for idx in range(1, 10):
        tid = f"bamboo_{idx}"
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=GOLD)
        draw.text((52, 42), str(idx), font=latin_font(64, bold=True), fill=INK)
        draw.text((W - 116, 44), "索", font=cjk_font(56), fill=GREEN)
        if idx in special_bamboos and special_bamboos[idx][0].exists():
            emb_path, cbox, custom_title = special_bamboos[idx]
            oval_w, oval_h = int(W * 0.76), int(H * 0.68)
            ox0, oy0 = (W - oval_w) // 2, int(H * 0.17)
            ox1, oy1 = ox0 + oval_w, oy0 + oval_h
            sp_im = Image.open(emb_path).convert("RGB")
            sw, sh = sp_im.size
            sp_crop = sp_im.crop((int(sw * cbox[0]), int(sh * cbox[1]), int(sw * cbox[2]), int(sh * cbox[3])))
            sp_resized = sp_crop.resize((oval_w, oval_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (oval_w, oval_h), 0)
            ImageDraw.Draw(mask).ellipse([4, 4, oval_w - 5, oval_h - 5], fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(radius=1.5))
            canvas.paste(sp_resized, (ox0, oy0), mask)
            draw.ellipse([ox0 - 6, oy0 - 6, ox1 + 6, oy1 + 6], outline=GREEN, width=5)
            draw.ellipse([ox0, oy0, ox1, oy1], outline=GOLD, width=4)
            save_tile_and_normal(canvas, tid, is_oval=True, oval_box=(ox0, oy0, ox1, oy1))
            build_onirica_tile(W, H, sp_crop, str(idx), "索", GREEN, tid, max_opacity=0.42)
            if ARTIFACT_DIR.exists():
                shutil.copy2(TILES_DIR / f"{tid}.png", ARTIFACT_DIR / f"{tid}.png")
            manifest.append({"id": tid, "suit": "bamboo", "matchGroup": tid, "cardinality": 2, "glyph": f"{idx}索", "title": custom_title, "coupled": False})
        else:
            for nx, ny, bh, col in bam_layouts.get(idx, bam_layouts[2]):
                draw_bamboo_stalk(draw, W * nx, H * ny, bh, col)
            save_tile_and_normal(canvas, tid)
            shutil.copy2(TILES_DIR / f"{tid}.png", ONIRICA_DIR / f"{tid}.png")
            manifest.append({"id": tid, "suit": "bamboo", "matchGroup": tid, "cardinality": 2, "glyph": f"{idx}索", "title": f"{idx} Bamboo ({cn_nums[idx-1]}索)", "coupled": False})

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
        shutil.copy2(TILES_DIR / f"{tid}.png", ONIRICA_DIR / f"{tid}.png")
        manifest.append({"id": tid, "suit": "winds", "matchGroup": tid, "cardinality": 2, "glyph": hanzi, "title": label, "coupled": False})

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
            draw.rounded_rectangle([135, 190, W - 135, H - 170], radius=28, outline=BLUE, width=18)
            draw.rounded_rectangle([168, 224, W - 168, H - 204], radius=16, outline=GOLD, width=6)
            draw_centered_text(draw, (W / 2, H * 0.54), "白", font=cjk_font(220), fill=BLUE)
        else:
            draw_centered_text(draw, (W / 2, H * 0.54), hanzi, font=cjk_font(420), fill=col, stroke_fill=GOLD, stroke_width=6)
        save_tile_and_normal(canvas, tid)
        shutil.copy2(TILES_DIR / f"{tid}.png", ONIRICA_DIR / f"{tid}.png")
        manifest.append({"id": tid, "suit": "dragons", "matchGroup": tid, "cardinality": 2, "glyph": hanzi, "title": label, "coupled": False})

    return manifest


def slice_diptyque_half(scene_path: Path, side: str | tuple[float, float, float, float]) -> Image.Image:
    """
    Slices a shared 2-subject Diptyque scene into either the LEFT solo portrait ('left'),
    the RIGHT solo portrait ('right'), or a custom normalized (x0, y0, x1, y1) box
    so each tile contains ONE well-centered character!
    """
    im = Image.open(scene_path).convert("RGB")
    w, h = im.size
    if isinstance(side, tuple) and len(side) == 4:
        x0, y0, x1, y1 = side
        return im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
    elif side == "left":
        return im.crop((0, 0, int(w * 0.50), h))
    elif side == "right":
        return im.crop((int(w * 0.50), 0, w, h))
    return im


def generate_coupled_family_oval_tiles() -> list[dict]:
    print("[OvalCameo] Building 16 Non-Identical Family Tiles (Classic Oval + Modalità Onirica A/B Set)...")

    specs = [
        # QUARTET 1: CARLESSO FAMILY SEASONS (Cardinality 4 — ANY 2 MATCH!)
        (
            "coupled_A1",
            "quartet_family_seasons",
            4,
            "S1",
            "春",
            "S1 • Solo Papà Riccardo (Family Quartet)",
            (188, 42, 92),
            PORTRAITS_DIR / "quartet_S1_papa_riccardo.png",
            (0.08, 0.05, 0.92, 0.88),
        ),
        (
            "coupled_A2",
            "quartet_family_seasons",
            4,
            "S2",
            "夏",
            "S2 • Solo Mamma Kate 2016 (Family Quartet)",
            (188, 42, 92),
            PORTRAITS_DIR / "quartet_S2_mamma_kate2016.png",
            (0.08, 0.06, 0.92, 0.89),
        ),
        (
            "coupled_B1",
            "quartet_family_seasons",
            4,
            "S3",
            "秋",
            "S3 • Solo Ale • Tang Silk (Family Quartet)",
            (188, 42, 92),
            PORTRAITS_DIR / "diptyque_S3_S4_ale_sebi_tang.png",
            (0.01, 0.25, 0.495, 0.65),
        ),
        (
            "coupled_B2",
            "quartet_family_seasons",
            4,
            "S4",
            "冬",
            "S4 • Solo Sebi • Tang Silk (Family Quartet)",
            (188, 42, 92),
            PORTRAITS_DIR / "diptyque_S3_S4_ale_sebi_tang.png",
            (0.505, 0.36, 0.99, 0.76),
        ),
        # QUARTET 2: KIDS & MAGICAL COMPANIONS FLOWERS (Cardinality 4 — ANY 2 MATCH!)
        (
            "coupled_C1",
            "quartet_magic_flowers",
            4,
            "M1",
            "梅",
            "M1 • Ale & Ghigna (Magic Quartet)",
            (132, 52, 188),
            PORTRAITS_DIR / "quartet_F1_ale_ghigna.png",
            "full",
        ),
        (
            "coupled_C2",
            "quartet_magic_flowers",
            4,
            "M2",
            "蘭",
            "M2 • Sebi & Pupurabbu (Magic Quartet)",
            (132, 52, 188),
            PORTRAITS_DIR / "quartet_F2_sebi_pupurabbu.png",
            (0.05, 0.05, 0.95, 0.95),
        ),
        (
            "coupled_D1",
            "quartet_magic_flowers",
            4,
            "M3",
            "菊",
            "M3 • Solo Ghigna Genius (Magic Quartet)",
            (132, 52, 188),
            PORTRAITS_DIR / "quartet_F3_solo_ghigna.png",
            "full",
        ),
        (
            "coupled_D2",
            "quartet_magic_flowers",
            4,
            "M4",
            "竹",
            "M4 • Solo Pupurabbu Lantern (Magic Quartet)",
            (132, 52, 188),
            PORTRAITS_DIR / "quartet_F4_solo_pupurabbu.png",
            "full",
        ),
        # DIPTYQUE PAIR E: GREAT WALL EXPLORERS (Cardinality 2 — Solo Ale <-> Solo Sebi)
        (
            "coupled_E1",
            "pair_E_great_wall",
            2,
            "E1",
            "夏",
            "E1 • Solo Ale • Great Wall (Left)",
            (24, 138, 82),
            PORTRAITS_DIR / "diptyque_A_great_wall.png",
            "left",
        ),
        (
            "coupled_E2",
            "pair_E_great_wall",
            2,
            "E2",
            "夏",
            "E2 • Solo Sebi • Great Wall (Right)",
            (24, 138, 82),
            PORTRAITS_DIR / "diptyque_A_great_wall.png",
            "right",
        ),
        # DIPTYQUE PAIR F: CANTONESE RICE & DIM SUM (Cardinality 2 — Solo Ale <-> Solo Sebi)
        (
            "coupled_F1",
            "pair_F_cantonese_rice",
            2,
            "F1",
            "秋",
            "F1 • Solo Ale • Cantonese Rice (Left)",
            (212, 148, 24),
            PORTRAITS_DIR / "diptyque_B_cantonese_rice.png",
            "left",
        ),
        (
            "coupled_F2",
            "pair_F_cantonese_rice",
            2,
            "F2",
            "秋",
            "F2 • Solo Sebi • Cantonese Rice (Right)",
            (212, 148, 24),
            PORTRAITS_DIR / "diptyque_B_cantonese_rice.png",
            "right",
        ),
        # DIPTYQUE PAIR G: SHAOLIN KUNG FU DRAGON & TIGER (Cardinality 2 — Solo Ale <-> Solo Sebi)
        (
            "coupled_G1",
            "pair_G_shaolin_kungfu",
            2,
            "G1",
            "冬",
            "G1 • Solo Ale • Shaolin Dragon (Left)",
            (218, 92, 24),
            PORTRAITS_DIR / "diptyque_C_shaolin_kungfu.png",
            (0.01, 0.30, 0.495, 0.77),
        ),
        (
            "coupled_G2",
            "pair_G_shaolin_kungfu",
            2,
            "G2",
            "冬",
            "G2 • Solo Sebi • Shaolin Tiger (Right)",
            (218, 92, 24),
            PORTRAITS_DIR / "diptyque_C_shaolin_kungfu.png",
            (0.505, 0.32, 0.99, 0.79),
        ),
        # DIPTYQUE PAIR H: CHENGDU GIANT PANDAS (Cardinality 2 — Solo Ale <-> Solo Sebi)
        (
            "coupled_H1",
            "pair_H_chengdu_pandas",
            2,
            "H1",
            "春",
            "H1 • Solo Ale • Chengdu Panda (Left)",
            (32, 142, 118),
            PORTRAITS_DIR / "diptyque_D_chengdu_pandas.png",
            "left",
        ),
        (
            "coupled_H2",
            "pair_H_chengdu_pandas",
            2,
            "H2",
            "春",
            "H2 • Solo Sebi • Chengdu Panda (Right)",
            (32, 142, 118),
            PORTRAITS_DIR / "diptyque_D_chengdu_pandas.png",
            "right",
        ),
    ]

    W, H = 768, 1024
    manifest = []

    for tid, mgroup, cardinality, glyph, hanzi, subtitle, col_rgb, src_path, slice_mode in specs:
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=col_rgb)

        # Top-Left: Coupled/Quartet Code (S1..S4, M1..M4, E1..H2)
        draw.text((50, 38), glyph, font=latin_font(60, bold=True), fill=col_rgb)
        # Top-Right: Authentic Mahjong Season/Flower Hanzi (春 夏 秋 冬 梅 蘭 菊 竹)
        draw.text((W - 118, 40), hanzi, font=cjk_font(62), fill=col_rgb)

        # Center Gold-Rimmed OVAL Cameo Medallion
        oval_w, oval_h = int(W * 0.78), int(H * 0.68)
        ox0 = (W - oval_w) // 2
        oy0 = int(H * 0.165)
        ox1 = ox0 + oval_w
        oy1 = oy0 + oval_h

        im = slice_diptyque_half(src_path, slice_mode)
        if isinstance(slice_mode, tuple):
            im_crop = ImageOps.fit(im, (oval_w, oval_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        else:
            iw, ih = im.size
            target_aspect = oval_w / oval_h
            if iw / ih > target_aspect:
                nw = int(ih * target_aspect)
                left = (iw - nw) // 2
                im_crop = im.crop((left, 0, left + nw, ih))
            else:
                nh = int(iw / target_aspect)
                top = max(0, (ih - nh) // 5)
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

        # Bottom cartouche with clear pair/quartet subtitle
        draw.rounded_rectangle([46, H - 118, W - 46, H - 46], radius=18, fill=(240, 234, 220), outline=col_rgb, width=3)
        draw_centered_text(draw, (W / 2, H - 82), subtitle, font=latin_font(23, bold=True), fill=(32, 28, 36))

        save_tile_and_normal(canvas, tid, is_oval=True, oval_box=(ox0, oy0, ox1, oy1))
        build_onirica_tile(W, H, im_crop, glyph, hanzi, col_rgb, tid, max_opacity=0.50)
        if ARTIFACT_DIR.exists():
            shutil.copy2(TILES_DIR / f"{tid}.png", ARTIFACT_DIR / f"{tid}.png")

        manifest.append({
            "id": tid,
            "suit": "coupled_family",
            "matchGroup": mgroup,
            "cardinality": cardinality,
            "glyph": f"{hanzi}{glyph}",
            "code": glyph,
            "hanzi": hanzi,
            "title": subtitle,
            "coupled": True,
            "sliceMode": "custom_crop" if isinstance(slice_mode, tuple) else slice_mode,
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
