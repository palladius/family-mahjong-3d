#!/usr/bin/env python3
"""
Remastered 2K PBR & 50-Tile Mahjong Deck Texture + 3D Incandescent-Pen Carving Generator (v1.4.0).
Generates:
1. 2K Baked/Procedural PBR Base Maps (2048x2048) for White Imperial Marble, Volcanic Black Obsidian + Gold Kintsugi Finiture,
   Carved Ming Rosewood Table, Celadon Jade Mat, and Sacred Chinese Temple Flagstone Pavement.
2. All 34 Original Traditional Mahjong Tile Faces with:
   - Enlarged 2-Circles (`dots_2`, r=148) & 4-Circles (`dots_4`, r=124) and fuller `dots_1..9` & `bamboo_5..9` layouts (minimal empty white space)
   - +10% Larger Traditional Chinese Calligraphy (`char_1..9`, `wind_*`, `dragon_*`)
   - True 3D "Incandescent Pen" Carved Intaglio (`buco bassorilievo scavato`):
     * `public/textures/tiles/{id}.png` (diffuse with scorched-gold raised burr rim, directional trench wall shadow, and warm incandescent bounce)
     * `public/textures/tiles_depth/{id}_depth.png` (displacement heightmap for Three.js 72x96 subdivided mesh & Blender DISPLACE modifier)
     * `public/textures/tiles_normal/{id}_normal.png` (high-slope tangent-space normal map from carved depth field)
3. All 16 Non-Identical Family & Magical Companion Tile Faces (Classic Carved Oval Cameo + Modalità Onirica A/B Set).
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
DEPTH_DIR = PROJECT_DIR / "public" / "textures" / "tiles_depth"
ONIRICA_DIR = PROJECT_DIR / "public" / "textures" / "tiles_onirica"
PORTRAITS_DIR = PROJECT_DIR / "public" / "portraits"

for d in [PBR_DIR, TILES_DIR, NORMALS_DIR, DEPTH_DIR, ONIRICA_DIR, PORTRAITS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

CJK_BRUSH_FONT = PROJECT_DIR / "public" / "fonts" / "MaShanZheng-Regular.ttf"
CJK_FONT_CANDIDATES = [
    str(CJK_BRUSH_FONT),
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",
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


TRAD_ONLY_HANZI = {"萬", "東", "風", "發", "蘭"}


def cjk_font(size: int, text: str = ""):
    needs_trad_songti = any(ch in TRAD_ONLY_HANZI for ch in text)
    if not needs_trad_songti and CJK_BRUSH_FONT.exists():
        try:
            return ImageFont.truetype(str(CJK_BRUSH_FONT), size=size)
        except Exception:
            pass
    for p in CJK_FONT_CANDIDATES:
        if p == str(CJK_BRUSH_FONT) and needs_trad_songti:
            continue
        if Path(p).exists():
            try:
                if p.endswith("Songti.ttc"):
                    return ImageFont.truetype(p, size=size, index=1)
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


def height_to_normal_map(height_np: np.ndarray, strength: float = 16.0) -> Image.Image:
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
        draw.line(pts, fill=(236, 230, 218), width=3)

    # Outer Obsidian hairline + Recessed Gold/Accent Frame
    draw.rounded_rectangle([14, 14, W - 15, H - 15], radius=38, outline=(32, 32, 40), width=6)
    draw.rounded_rectangle([26, 26, W - 27, H - 27], radius=30, outline=accent_rgb, width=5)
    return canvas, draw


def draw_mahjong_circle(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float, color_rgb: tuple[int, int, int]):
    """
    Draws an ornate, bold Imperial Mahjong Circle (Tongzi) medallion with rich concentric carved rings,
    12-petal lotus/coin spokes, and a bold gold-rimmed center so there is minimal empty white space!
    """
    GOLD_RIM = (212, 168, 62)
    DARK_RIM = (26, 22, 28)

    # Outer dark carved edge + main colored ring
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color_rgb, outline=DARK_RIM, width=max(4, int(r * 0.055)))
    r_gold = r * 0.88
    draw.ellipse([cx - r_gold, cy - r_gold, cx + r_gold, cy + r_gold], outline=GOLD_RIM, width=max(3, int(r * 0.04)))

    # Carved cream ring with 12 radial spokes/beads
    r2 = r * 0.72
    draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(244, 238, 225), outline=color_rgb, width=max(3, int(r * 0.045)))

    bead_r = max(5.0, r * 0.068)
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        px = cx + math.cos(rad) * (r * 0.60)
        py = cy + math.sin(rad) * (r * 0.60)
        draw.ellipse([px - bead_r, py - bead_r, px + bead_r, py + bead_r], fill=color_rgb, outline=GOLD_RIM, width=1)

    # Bold inner ring + central carved square-in-circle coin heart
    r3 = r * 0.46
    draw.ellipse([cx - r3, cy - r3, cx + r3, cy + r3], fill=color_rgb, outline=DARK_RIM, width=max(3, int(r * 0.04)))
    r4 = r * 0.22
    draw.ellipse([cx - r4, cy - r4, cx + r4, cy + r4], fill=GOLD_RIM, outline=DARK_RIM, width=2)


def draw_bamboo_stalk(draw: ImageDraw.ImageDraw, cx: float, cy: float, h: float, color_rgb: tuple[int, int, int]):
    w = h * 0.27  # Wider, bolder carved bamboo stalks to reduce empty white space
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=w * 0.42, fill=color_rgb, outline=(20, 28, 22), width=4)
    # Central carved groove inside the bamboo stalk
    draw.line([(cx - w * 0.14, y0 + 12), (cx - w * 0.14, y1 - 12)], fill=(232, 244, 232), width=4)
    draw.line([(cx + w * 0.14, y0 + 12), (cx + w * 0.14, y1 - 12)], fill=(18, 45, 25), width=3)
    for ny in [y0 + 8, cy, y1 - 8]:
        draw.rounded_rectangle([x0 - 7, ny - 7, x1 + 7, ny + 7], radius=5, fill=color_rgb, outline=(218, 178, 72), width=3)


def apply_incandescent_pen_carving(
    canvas: Image.Image,
    tile_id: str,
    is_oval: bool = False,
    oval_box=None,
):
    """
    3D 'Incandescent Pen' Carved Intaglio Engine ('come se una penna incandescente avesse scavato il tile
    un pochettino, che si vede il buco bassorilievo ruotando'):
    1. Detects all inked/carved motifs on the marble canvas (calligraphy strokes, circles, bamboo stalks, borders).
    2. Constructs a physical 3D Depth/Displacement Map (`_depth.png`) where:
       - Flat uncarved marble plateau = 0.88 (224/255)
       - Raised molten-gold singed rim right around the carved edge = 1.00 (255/255)
       - Steeply excavated V/U-shaped groove cavity ('il buco bassorilievo') = 0.00..0.18 (0..45/255)
       - For Oval Cameo tiles (`is_oval=True`), the outer oval groove & frame are deeply carved while the character inside rises in sculpted cameo bassorilievo!
    3. Shades `canvas` with directional 3D trench wall lighting:
       - Top-left inner trench wall cast in deep scorched-umber/charcoal shadow
       - Bottom-right inner trench wall catching warm incandescent amber-gold light
       - Subtle recessed ambient occlusion at the bottom of the carved groove
    4. Generates a sharp, high-slope tangent-space Normal Map (`_normal.png`, strength=18.0).
    """
    arr = np.asarray(canvas, dtype=np.float32)
    H, W, _ = arr.shape

    # Identify carved pigment regions vs. uncarved cream-white marble background (~(245, 240, 230))
    bg_ref = np.array([245.0, 241.0, 232.0], dtype=np.float32)
    color_dist = np.sqrt(np.sum((arr - bg_ref) ** 2, axis=-1))
    # Ignore the outermost 22px tile border so the outer edge of the tile stays flush
    yy, xx = np.mgrid[0:H, 0:W]
    inner_valid = (xx > 22) & (xx < W - 22) & (yy > 22) & (yy < H - 22)

    if not is_oval:
        # Suit, Calligraphic & Ornate Dragon Tiles:
        # Multi-Scale Distance-Transform V-Groove + Medial-Axis Spine Ridge (Zero flat bottom plateau!)
        carve_raw = np.clip((color_dist - 22.0) / 52.0, 0.0, 1.0) * inner_valid.astype(np.float32)
        carve_im = Image.fromarray((carve_raw * 255.0).astype(np.uint8), mode="L")

        # Inward distance field cascade via morphological erosion + Gaussian smoothing (V-chisel walls all the way to stroke center)
        erode_1 = np.asarray(carve_im.filter(ImageFilter.MinFilter(size=5)).filter(ImageFilter.GaussianBlur(radius=2.2)), dtype=np.float32) / 255.0
        erode_2 = np.asarray(carve_im.filter(ImageFilter.MinFilter(size=11)).filter(ImageFilter.GaussianBlur(radius=4.0)), dtype=np.float32) / 255.0
        erode_3 = np.asarray(carve_im.filter(ImageFilter.MinFilter(size=19)).filter(ImageFilter.GaussianBlur(radius=6.5)), dtype=np.float32) / 255.0

        # Medial-axis kintsugi spine ridge inside wide calligraphic strokes (splits wide strokes into two angled 3D facets)
        medial_spine = np.clip(erode_2 - erode_3 * 0.85, 0.0, 1.0) * erode_1

        groove_steep = np.asarray(carve_im.filter(ImageFilter.GaussianBlur(radius=2.6)), dtype=np.float32) / 255.0
        groove_wide = np.asarray(carve_im.filter(ImageFilter.GaussianBlur(radius=8.5)), dtype=np.float32) / 255.0
        dilated = np.asarray(carve_im.filter(ImageFilter.MaxFilter(size=9)).filter(ImageFilter.GaussianBlur(radius=2.8)), dtype=np.float32) / 255.0

        # Raised rim right outside the carved trench
        rim_ring = np.clip(dilated - carve_raw, 0.0, 1.0)
        # V-groove depth profile combining outer wall slope + deep inward V-trough + subtle raised medial-axis chisel spine
        v_trough = np.clip(0.32 * carve_raw + 0.28 * groove_steep + 0.22 * erode_1 + 0.18 * erode_2 + 0.12 * groove_wide, 0.0, 1.0)
        height_map = np.clip(0.88 + 0.10 * rim_ring - 0.86 * v_trough + 0.16 * medial_spine, 0.0, 1.0)

        # Smooth macro height map for 3D vertex displacement (_depth.png) preserving V-groove curvature on the 72x96 mesh
        disp_smooth = np.asarray(
            Image.fromarray(np.clip(height_map * 255.0, 0, 255).astype(np.uint8), mode="L").filter(ImageFilter.GaussianBlur(radius=3.8)),
            dtype=np.float32,
        ) / 255.0

        # Compute directional slope for incandescent-pen trench wall shading (light from top-left (-1, -1))
        gy, gx = np.gradient(height_map)
        slope_light = (gx * 0.72 + gy * 0.72) * 16.0

        shadow_mask = np.clip(-slope_light, 0.0, 1.0) * np.clip(dilated * 1.4, 0.0, 1.0)
        highlight_mask = np.clip(slope_light, 0.0, 1.0) * np.clip(dilated * 1.4, 0.0, 1.0)
        cavity_ao = np.clip(v_trough * 0.24, 0.0, 0.26)

        # Apply scorched-umber inner trench shadow + cavity AO + warm incandescent gold rim & medial-spine glow
        shaded = arr.copy()
        for c_i, umber_tint in enumerate([28.0, 16.0, 10.0]):
            shaded[:, :, c_i] = shaded[:, :, c_i] * (1.0 - cavity_ao)
            shaded[:, :, c_i] = shaded[:, :, c_i] * (1.0 - shadow_mask * 0.64) + umber_tint * (shadow_mask * 0.64)

        incandescent_gold = np.array([255.0, 214.0, 118.0], dtype=np.float32)
        glow_strength = np.clip(highlight_mask * 0.60 + rim_ring * 0.30 + medial_spine * 0.34, 0.0, 0.78)
        for c_i in range(3):
            shaded[:, :, c_i] = shaded[:, :, c_i] * (1.0 - glow_strength) + incandescent_gold[c_i] * glow_strength

        out_canvas = Image.fromarray(np.clip(shaded, 0, 255).astype(np.uint8))
    else:
        # Oval Cameo & Special Bamboo Emblem Tiles:
        ox0, oy0, ox1, oy1 = oval_box
        cx, cy = (ox0 + ox1) / 2.0, (oy0 + oy1) / 2.0
        rx, ry = (ox1 - ox0) / 2.0, (oy1 - oy0) / 2.0
        ell_dist = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)

        oval_moat = np.exp(-((ell_dist - 1.01) / 0.048) ** 2)
        oval_gold_rim = np.exp(-((ell_dist - 0.955) / 0.028) ** 2)
        inside_oval = ell_dist < 0.96

        gray = np.asarray(canvas.convert("L").filter(ImageFilter.GaussianBlur(radius=1.8)), dtype=np.float32) / 255.0
        dome = np.clip(1.0 - ell_dist ** 2, 0.0, 1.0)

        outside_carve = np.clip((color_dist - 26.0) / 55.0, 0.0, 1.0) * (~inside_oval).astype(np.float32) * inner_valid.astype(np.float32)
        outside_carve_blur = np.asarray(
            Image.fromarray((outside_carve * 255.0).astype(np.uint8), mode="L").filter(ImageFilter.GaussianBlur(radius=2.8)),
            dtype=np.float32,
        ) / 255.0

        height_map = np.where(
            inside_oval,
            0.52 + dome * 0.28 + (gray - 0.5) * 0.34 + oval_gold_rim * 0.14,
            0.88 - outside_carve_blur * 0.72 - oval_moat * 0.76,
        )
        height_map = np.clip(height_map, 0.0, 1.0)
        disp_smooth = np.asarray(
            Image.fromarray(np.clip(height_map * 255.0, 0, 255).astype(np.uint8), mode="L").filter(ImageFilter.GaussianBlur(radius=4.5)),
            dtype=np.float32,
        ) / 255.0

        gy, gx = np.gradient(height_map)
        slope_light = (gx * 0.72 + gy * 0.72) * 10.0
        ring_zone = ((ell_dist > 0.90) & (ell_dist < 1.10)) | (outside_carve_blur > 0.08)
        shadow_m = np.clip(-slope_light, 0.0, 1.0) * ring_zone.astype(np.float32)
        high_m = np.clip(slope_light, 0.0, 1.0) * ring_zone.astype(np.float32)

        shaded = arr.copy()
        for c_i, umb in enumerate([26.0, 16.0, 12.0]):
            shaded[:, :, c_i] = shaded[:, :, c_i] * (1.0 - shadow_m * 0.48) + umb * (shadow_m * 0.48)
        for c_i, gld in enumerate([255.0, 215.0, 120.0]):
            shaded[:, :, c_i] = shaded[:, :, c_i] * (1.0 - high_m * 0.42) + gld * (high_m * 0.42)
        out_canvas = Image.fromarray(np.clip(shaded, 0, 255).astype(np.uint8))

    out_canvas.save(TILES_DIR / f"{tile_id}.png", "PNG")

    # Save Smooth 8-bit 3D Vertex Displacement Map (`_depth.png`)
    depth_u8 = np.clip(disp_smooth * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(depth_u8, mode="L").save(DEPTH_DIR / f"{tile_id}_depth.png", "PNG")

    # Save Crisp High-Slope Tangent-Space Normal Map (`_normal.png`)
    norm_im = height_to_normal_map(height_map, strength=18.0)
    norm_im.save(NORMALS_DIR / f"{tile_id}_normal.png", "PNG")


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
    - The portrait/emblem is softly infused into the white stone like an ethereal watercolor/memory wash.
    """
    canvas = Image.new("RGB", (W, H), (252, 249, 243))
    draw = ImageDraw.Draw(canvas)
    for y in range(H):
        t = y / (H - 1)
        c = (int(253 - 4 * t), int(250 - 5 * t), int(244 - 6 * t))
        draw.line([(0, y), (W, y)], fill=c)

    soft_gold = (226, 202, 145)
    draw.rounded_rectangle([24, 24, W - 25, H - 25], radius=32, outline=soft_gold, width=2)

    wash_w, wash_h = int(W * 0.62), int(H * 0.52)
    wx0 = (W - wash_w) // 2
    wy0 = int(H * 0.23)

    im_fit = ImageOps.fit(src_crop, (wash_w, wash_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.42))
    im_soft = im_fit.filter(ImageFilter.GaussianBlur(radius=0.9))
    arr = np.asarray(im_soft, dtype=np.float32) / 255.0
    luma = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]

    pastel = np.zeros_like(arr)
    tint = np.array([col_rgb[0] / 255.0, col_rgb[1] / 255.0, col_rgb[2] / 255.0], dtype=np.float32)
    for c_i in range(3):
        pastel[:, :, c_i] = arr[:, :, c_i] * 0.74 + (luma * 0.85 + tint[c_i] * 0.15) * 0.26
    pastel = 1.0 - (1.0 - pastel) * 0.76
    pastel_im = Image.fromarray(np.clip(pastel * 255.0, 0, 255).astype(np.uint8))

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

    soft_col = (
        int(col_rgb[0] * 0.72 + 55),
        int(col_rgb[1] * 0.72 + 50),
        int(col_rgb[2] * 0.72 + 50),
    )
    draw.text((52, 40), glyph_left, font=latin_font(62, bold=True), fill=soft_col)
    draw.text((W - 122, 42), glyph_right, font=cjk_font(62, glyph_right), fill=soft_col)

    out_path = ONIRICA_DIR / f"{tile_id}.png"
    canvas.save(out_path, "PNG")
    if ARTIFACT_DIR.exists():
        shutil.copy2(out_path, ARTIFACT_DIR / f"onirica_{tile_id}.png")


def draw_imperial_cloud_flourishes(draw: ImageDraw.ImageDraw, cx: float, cy: float, rx: float, ry: float, col: tuple[int, int, int], gold: tuple[int, int, int]):
    """Draws curved Imperial cloud-scroll & scalloped guilloché arcs around calligraphy so 3D normal/depth maps have 360° curved grooves."""
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=gold, width=4)
    draw.ellipse([cx - rx * 0.93, cy - ry * 0.93, cx + rx * 0.93, cy + ry * 0.93], outline=col, width=3)
    # 8 scalloped cloud-scroll petals along the ring perimeter
    for k in range(8):
        ang = k * (math.pi / 4.0)
        px = cx + math.cos(ang) * (rx * 0.965)
        py = cy + math.sin(ang) * (ry * 0.965)
        draw.ellipse([px - 14, py - 14, px + 14, py + 14], fill=(244, 238, 225), outline=gold, width=4)
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=col)


def composite_ornate_dragon_emblem(canvas: Image.Image, emblem_path: Path, box: tuple[int, int, int, int]):
    """Seamlessly mats a 2D ornate Dragon + Calligraphy relief emblem (on ivory-white #FAF6EE) onto the marble tile canvas."""
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    emb = Image.open(emblem_path).convert("RGB")
    ew, eh = emb.size
    # Tight crop around the ornate dragon artwork
    emb_crop = emb.crop((int(ew * 0.06), int(eh * 0.08), int(ew * 0.94), int(eh * 0.92))).resize((tw, th), Image.Resampling.LANCZOS)
    emb_np = np.asarray(emb_crop, dtype=np.float32)

    # Sample corner background of the emblem to compute exact pigment alpha
    corners = np.concatenate([
        emb_np[:20, :20].reshape(-1, 3),
        emb_np[:20, -20:].reshape(-1, 3),
        emb_np[-20:, :20].reshape(-1, 3),
        emb_np[-20:, -20:].reshape(-1, 3),
    ], axis=0)
    bg_rgb = np.median(corners, axis=0)
    dist = np.sqrt(np.sum((emb_np - bg_rgb) ** 2, axis=-1))

    # Soft elliptical edge feather so outer border blends 100% into the marble canvas
    yy, xx = np.mgrid[0:th, 0:tw]
    nx = (xx - tw * 0.5) / (tw * 0.49)
    ny = (yy - th * 0.5) / (th * 0.49)
    rad = np.sqrt(nx * nx + ny * ny)
    feather = np.clip((1.02 - rad) / 0.12, 0.0, 1.0)

    alpha = np.clip((dist - 14.0) / 32.0, 0.0, 1.0) * feather
    alpha_u8 = Image.fromarray(np.clip(alpha * 255.0, 0, 255).astype(np.uint8), mode="L").filter(ImageFilter.GaussianBlur(radius=0.8))
    canvas.paste(emb_crop, (x0, y0), alpha_u8)


def generate_original_mahjong_suits() -> list[dict]:
    print("[MahjongArt] Generating 34 Original Suit & Honour Tiles (Ornate 3D Carved Dragons, MaShanZheng Brush Calligraphy, V-Groove Carving)...")
    W, H = 768, 1024
    RED = (196, 30, 30)
    GREEN = (20, 132, 58)
    BLUE = (26, 70, 178)
    INK = (24, 26, 36)
    GOLD = (204, 158, 56)

    manifest = []

    # 1. Characters / Wan (一萬 .. 九萬) — Brush Calligraphy + Curved Cloud-Scroll Seals
    cn_nums = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
    for idx, cn in enumerate(cn_nums, start=1):
        tid = f"char_{idx}"
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=GOLD)
        draw.text((48, 38), str(idx), font=latin_font(72, bold=True), fill=INK)
        draw.text((W - 124, 40), cn, font=cjk_font(64, cn), fill=BLUE)
        # Curved cloud-scroll seal rings around top numeral & bottom Wan
        draw_imperial_cloud_flourishes(draw, W * 0.5, H * 0.34, 178, 142, BLUE, GOLD)
        draw_imperial_cloud_flourishes(draw, W * 0.5, H * 0.72, 196, 168, RED, GOLD)
        draw_centered_text(draw, (W / 2, H * 0.34), cn, font=cjk_font(272, cn), fill=BLUE, stroke_fill=GOLD, stroke_width=3)
        draw_centered_text(draw, (W / 2, H * 0.71), "萬", font=cjk_font(278, "萬"), fill=RED, stroke_fill=GOLD, stroke_width=3)
        apply_incandescent_pen_carving(canvas, tid)
        shutil.copy2(TILES_DIR / f"{tid}.png", ONIRICA_DIR / f"{tid}.png")
        if ARTIFACT_DIR.exists() and idx in (1, 8):
            shutil.copy2(TILES_DIR / f"{tid}.png", ARTIFACT_DIR / f"{tid}.png")
        manifest.append({"id": tid, "suit": "characters", "matchGroup": tid, "cardinality": 2, "glyph": f"{idx}萬", "title": f"{idx} Characters ({cn}萬)", "coupled": False})

    # 2. Circles / Dots (一筒 .. 九筒) — Significantly Larger 2-Circles (r=148) & 4-Circles (r=124) & Fuller Layouts!
    dot_layouts = {
        1: [(0.50, 0.54, 192, RED)],
        2: [(0.50, 0.34, 148, GREEN), (0.50, 0.72, 148, BLUE)],
        3: [(0.27, 0.30, 108, BLUE), (0.50, 0.54, 108, RED), (0.73, 0.78, 108, GREEN)],
        4: [(0.31, 0.36, 124, BLUE), (0.69, 0.36, 124, GREEN), (0.31, 0.72, 124, GREEN), (0.69, 0.72, 124, BLUE)],
        5: [(0.28, 0.32, 102, BLUE), (0.72, 0.32, 102, GREEN), (0.50, 0.54, 102, RED), (0.28, 0.76, 102, GREEN), (0.72, 0.76, 102, BLUE)],
        6: [(0.31, 0.30, 96, GREEN), (0.69, 0.30, 96, GREEN), (0.31, 0.55, 96, RED), (0.69, 0.55, 96, RED), (0.31, 0.79, 96, RED), (0.69, 0.79, 96, RED)],
        7: [(0.24, 0.27, 78, GREEN), (0.50, 0.35, 78, GREEN), (0.76, 0.43, 78, GREEN), (0.32, 0.61, 86, RED), (0.68, 0.61, 86, RED), (0.32, 0.81, 86, RED), (0.68, 0.81, 86, RED)],
        8: [(0.32, y, 74, BLUE) for y in [0.25, 0.44, 0.63, 0.82]] + [(0.68, y, 74, BLUE) for y in [0.25, 0.44, 0.63, 0.82]],
        9: [(x, 0.28, 78, GREEN) for x in [0.24, 0.50, 0.76]] + [(x, 0.54, 78, RED) for x in [0.24, 0.50, 0.76]] + [(x, 0.80, 78, BLUE) for x in [0.24, 0.50, 0.76]],
    }
    for idx in range(1, 10):
        tid = f"dots_{idx}"
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=GOLD)
        draw.text((48, 38), str(idx), font=latin_font(72, bold=True), fill=INK)
        draw.text((W - 124, 40), "筒", font=cjk_font(62, "筒"), fill=RED)
        if idx == 1:
            cx, cy = W * 0.5, H * 0.54
            draw.ellipse([cx - 236, cy - 236, cx + 236, cy + 236], fill=GREEN, outline=GOLD, width=8)
        for nx, ny, rad, col in dot_layouts[idx]:
            draw_mahjong_circle(draw, W * nx, H * ny, rad, col)
        apply_incandescent_pen_carving(canvas, tid)
        shutil.copy2(TILES_DIR / f"{tid}.png", ONIRICA_DIR / f"{tid}.png")
        manifest.append({"id": tid, "suit": "dots", "matchGroup": tid, "cardinality": 2, "glyph": f"{idx}筒", "title": f"{idx} Circles ({cn_nums[idx-1]}筒)", "coupled": False})

    # 3. Bamboos / Tiao (一索 .. 九索) — Larger Stalks on 5..9 & Special Comedic Carved Bamboo & Gold Emblems on 1..4!
    bam_layouts = {
        2: [(0.50, 0.36, 275, BLUE), (0.50, 0.72, 275, GREEN)],
        3: [(0.50, 0.34, 250, BLUE), (0.31, 0.72, 250, GREEN), (0.69, 0.72, 250, GREEN)],
        4: [(0.32, 0.36, 250, BLUE), (0.68, 0.36, 250, GREEN), (0.32, 0.72, 250, GREEN), (0.68, 0.72, 250, BLUE)],
        5: [(0.26, 0.36, 238, GREEN), (0.74, 0.36, 238, BLUE), (0.50, 0.54, 238, RED), (0.26, 0.72, 238, BLUE), (0.74, 0.72, 238, GREEN)],
        6: [(x, 0.36, 244, GREEN) for x in [0.25, 0.50, 0.75]] + [(x, 0.72, 244, BLUE) for x in [0.25, 0.50, 0.75]],
        7: [(0.50, 0.26, 190, RED)] + [(x, 0.52, 190, GREEN) for x in [0.25, 0.50, 0.75]] + [(x, 0.78, 190, BLUE) for x in [0.25, 0.50, 0.75]],
        8: [(x, 0.36, 218, GREEN) for x in [0.21, 0.40, 0.60, 0.79]] + [(x, 0.72, 218, BLUE) for x in [0.21, 0.40, 0.60, 0.79]],
        9: [(x, 0.28, 192, RED if x == 0.50 else GREEN) for x in [0.25, 0.50, 0.75]]
        + [(x, 0.54, 192, RED if x == 0.50 else BLUE) for x in [0.25, 0.50, 0.75]]
        + [(x, 0.80, 192, RED if x == 0.50 else GREEN) for x in [0.25, 0.50, 0.75]],
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
        draw.text((48, 38), str(idx), font=latin_font(72, bold=True), fill=INK)
        draw.text((W - 124, 40), "索", font=cjk_font(62, "索"), fill=GREEN)
        if idx in special_bamboos and special_bamboos[idx][0].exists():
            emb_path, cbox, custom_title = special_bamboos[idx]
            oval_w, oval_h = int(W * 0.82), int(H * 0.73)
            ox0, oy0 = (W - oval_w) // 2, int(H * 0.15)
            ox1, oy1 = ox0 + oval_w, oy0 + oval_h
            sp_im = Image.open(emb_path).convert("RGB")
            sw, sh = sp_im.size
            sp_crop = sp_im.crop((int(sw * cbox[0]), int(sh * cbox[1]), int(sw * cbox[2]), int(sh * cbox[3])))
            sp_resized = sp_crop.resize((oval_w, oval_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (oval_w, oval_h), 0)
            ImageDraw.Draw(mask).ellipse([4, 4, oval_w - 5, oval_h - 5], fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(radius=1.5))
            canvas.paste(sp_resized, (ox0, oy0), mask)
            draw.ellipse([ox0 - 7, oy0 - 7, ox1 + 7, oy1 + 7], outline=GREEN, width=6)
            draw.ellipse([ox0, oy0, ox1, oy1], outline=GOLD, width=5)
            apply_incandescent_pen_carving(canvas, tid, is_oval=True, oval_box=(ox0, oy0, ox1, oy1))
            build_onirica_tile(W, H, sp_crop, str(idx), "索", GREEN, tid, max_opacity=0.42)
            if ARTIFACT_DIR.exists():
                shutil.copy2(TILES_DIR / f"{tid}.png", ARTIFACT_DIR / f"{tid}.png")
            manifest.append({"id": tid, "suit": "bamboo", "matchGroup": tid, "cardinality": 2, "glyph": f"{idx}索", "title": custom_title, "coupled": False})
        else:
            for nx, ny, bh, col in bam_layouts.get(idx, bam_layouts[2]):
                draw_bamboo_stalk(draw, W * nx, H * ny, bh, col)
            apply_incandescent_pen_carving(canvas, tid)
            shutil.copy2(TILES_DIR / f"{tid}.png", ONIRICA_DIR / f"{tid}.png")
            manifest.append({"id": tid, "suit": "bamboo", "matchGroup": tid, "cardinality": 2, "glyph": f"{idx}索", "title": f"{idx} Bamboo ({cn_nums[idx-1]}索)", "coupled": False})

    # 4. Four Winds (東 南 西 北) — Brush Calligraphy + Curved Guilloché Wind Medallion
    winds = [
        ("wind_E", "東", "E", "East Wind (東)"),
        ("wind_S", "南", "S", "South Wind (南)"),
        ("wind_W", "西", "W", "West Wind (西)"),
        ("wind_N", "北", "N", "North Wind (北)"),
    ]
    for tid, hanzi, let, label in winds:
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=GOLD)
        draw.text((48, 38), let, font=latin_font(72, bold=True), fill=BLUE)
        draw.text((W - 124, 40), "風", font=cjk_font(62, "風"), fill=INK)
        draw_imperial_cloud_flourishes(draw, W * 0.5, H * 0.54, 248, 268, BLUE, GOLD)
        draw_centered_text(draw, (W / 2, H * 0.54), hanzi, font=cjk_font(425, hanzi), fill=INK, stroke_fill=GOLD, stroke_width=4)
        apply_incandescent_pen_carving(canvas, tid)
        shutil.copy2(TILES_DIR / f"{tid}.png", ONIRICA_DIR / f"{tid}.png")
        manifest.append({"id": tid, "suit": "winds", "matchGroup": tid, "cardinality": 2, "glyph": hanzi, "title": label, "coupled": False})

    # 5. Three Dragons (中 發 白) — Bespoke Ornate 3D Carved Chinese Dragon & Brush Calligraphy Relief Emblems!
    dragons = [
        ("dragon_red", "中", "C", RED, "Red Dragon • Ornate Carved Shenlong (紅中)", PORTRAITS_DIR / "dragon_red_ornate_emblem.png"),
        ("dragon_green", "發", "F", GREEN, "Green Dragon • Imperial Jade Shenlong (發財)", PORTRAITS_DIR / "dragon_green_ornate_emblem.png"),
        ("dragon_white", "白", "P", BLUE, "White Dragon • Sapphire & Pearl Twin Dragons (白板)", PORTRAITS_DIR / "dragon_white_ornate_emblem.png"),
    ]
    for tid, hanzi, let, col, label, emb_path in dragons:
        canvas, draw = make_marble_face_canvas(W, H, accent_rgb=col)
        draw.text((48, 38), let, font=latin_font(72, bold=True), fill=col)
        draw.text((W - 124, 40), hanzi, font=cjk_font(62, hanzi), fill=col)
        if emb_path.exists():
            composite_ornate_dragon_emblem(canvas, emb_path, (48, 122, W - 48, H - 56))
        else:
            draw_centered_text(draw, (W / 2, H * 0.54), hanzi, font=cjk_font(462, hanzi), fill=col, stroke_fill=GOLD, stroke_width=4)
        apply_incandescent_pen_carving(canvas, tid, is_oval=False)
        shutil.copy2(TILES_DIR / f"{tid}.png", ONIRICA_DIR / f"{tid}.png")
        if ARTIFACT_DIR.exists():
            shutil.copy2(TILES_DIR / f"{tid}.png", ARTIFACT_DIR / f"{tid}.png")
            shutil.copy2(DEPTH_DIR / f"{tid}_depth.png", ARTIFACT_DIR / f"{tid}_depth.png")
        manifest.append({"id": tid, "suit": "dragons", "matchGroup": tid, "cardinality": 2, "glyph": hanzi, "title": label, "coupled": False})

    return manifest


def slice_diptyque_half(scene_path: Path, side: str | tuple[float, float, float, float]) -> Image.Image:
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
    print("[OvalCameo] Building 16 Non-Identical Family Tiles (Larger Oval Cameo + 3D Carved Moat + Modalità Onirica A/B Set)...")

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

        # Top-Left: Coupled/Quartet Code (+8% larger: 66px)
        draw.text((46, 36), glyph, font=latin_font(66, bold=True), fill=col_rgb)
        # Top-Right: Authentic Mahjong Season/Flower Hanzi (+8% larger: 68px)
        draw.text((W - 124, 38), hanzi, font=cjk_font(68, hanzi), fill=col_rgb)

        # Enlarged Center Gold-Rimmed OVAL Cameo Medallion (0.83 x 0.71 — less empty white margin!)
        oval_w, oval_h = int(W * 0.83), int(H * 0.71)
        ox0 = (W - oval_w) // 2
        oy0 = int(H * 0.145)
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
        draw.rounded_rectangle([42, H - 114, W - 42, H - 44], radius=18, fill=(240, 234, 220), outline=col_rgb, width=3)
        draw_centered_text(draw, (W / 2, H - 79), subtitle, font=latin_font(24, bold=True), fill=(32, 28, 36))

        apply_incandescent_pen_carving(canvas, tid, is_oval=True, oval_box=(ox0, oy0, ox1, oy1))
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
    print(f"[Done] Generated {full_manifest['tileCount']} tile textures + 3D depth maps + incandescent normal maps + 2K PBR base maps!")


if __name__ == "__main__":
    main()
