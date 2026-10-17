#!/usr/bin/env python3
"""
Builds the epic composite showcase screenshot for Vetrina & README:
- public/renders/vetrina_hero_showcase.jpg
- /Users/ricc/git/vetrina/assets/screenshots/family-mahjong-3d.jpg
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
VETRINA_SHOT = Path("/Users/ricc/git/vetrina/assets/screenshots/family-mahjong-3d.jpg")
LOCAL_SHOT = ROOT / "public/renders/vetrina_hero_showcase.jpg"


def load_font(size: int, bold: bool = True):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def add_rounded_card(base: Image.Image, img: Image.Image, box: tuple[int, int, int, int], radius: int = 18, border_color=(245, 212, 112, 235), border_w: int = 3):
    x1, y1, x2, y2 = box
    w, h = x2 - x1, y2 - y1
    resized = img.convert("RGBA").resize((w, h), Image.Resampling.LANCZOS)

    mask = Image.new("L", (w, h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)

    # Drop shadow
    shadow = Image.new("RGBA", (w + 36, h + 36), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle((18, 22, 18 + w, 22 + h), radius=radius, fill=(0, 0, 0, 185))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    base.alpha_composite(shadow, (x1 - 18, y1 - 18))

    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    card.paste(resized, (0, 0), mask)
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle((1, 1, w - 2, h - 2), radius=radius, outline=border_color, width=border_w)
    base.alpha_composite(card, (x1, y1))


def main():
    W, H = 1600, 1000
    canvas = Image.new("RGBA", (W, H), (14, 10, 18, 255))

    # 1. Background: Cycles Cam 1 Hero 3D Temple Board
    bg_path = ROOT / "public/renders/cycles/cycles_cam1_hero.png"
    bg = Image.open(bg_path).convert("RGBA").resize((W, H), Image.Resampling.LANCZOS)
    canvas.alpha_composite(bg, (0, 0))

    # Top and bottom dark luxury gradients so header and family tile dock pop with 100% clarity
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grad)
    for y in range(180):
        alpha = int(225 * (1.0 - y / 180.0) ** 1.4)
        gdraw.line([(0, y), (W, y)], fill=(12, 9, 16, alpha))
    for y in range(H - 310, H):
        u = (y - (H - 310)) / 310.0
        alpha = int(242 * (u ** 1.25))
        gdraw.line([(0, y), (W, y)], fill=(12, 9, 16, alpha))
    canvas.alpha_composite(grad, (0, 0))

    # 2. Left Inset Card: 3D Incandescent-Pen Carved Intaglio Macro (4 Circles, Ornate 3D Red Dragon, 8 Wan)
    cam5 = Image.open(ROOT / "public/renders/cycles/cycles_cam5_carved_intaglio.png").convert("RGBA")
    add_rounded_card(canvas, cam5, (38, 148, 638, 486), radius=20, border_color=(255, 208, 96, 245), border_w=4)

    draw = ImageDraw.Draw(canvas)
    f_tag = load_font(18, bold=True)
    draw.rounded_rectangle((54, 162, 540, 198), radius=10, fill=(18, 12, 22, 225), outline=(245, 212, 112, 215), width=2)
    draw.text((68, 170), "3D CARVED INTAGLIO: 4 DOTS • RED DRAGON • 8 WAN", font=f_tag, fill=(255, 224, 130, 255))

    # 3. Right Hero Transparent Effect: Frame 2 Dragon Emerge (Riccardino's favorite!) bursting over the 3D Temple Board!
    glow = Image.new("RGBA", (620, 620), (0, 0, 0, 0))
    g2 = ImageDraw.Draw(glow)
    g2.ellipse((70, 70, 550, 550), fill=(255, 168, 36, 95))
    g2.ellipse((140, 140, 480, 480), fill=(235, 52, 24, 115))
    glow = glow.filter(ImageFilter.GaussianBlur(42))
    canvas.alpha_composite(glow, (945, 78))

    dragon_emerge = Image.open(ROOT / "public/fx/powerup_frame2_dragon_emerge_rgba.png").convert("RGBA")
    dragon_resized = dragon_emerge.resize((540, 540), Image.Resampling.LANCZOS)
    canvas.alpha_composite(dragon_resized, (990, 108))

    # Pill banner under the emerging dragon
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((1005, 608, 1545, 654), radius=22, fill=(22, 12, 16, 232), outline=(255, 205, 88, 245), width=3)
    draw.text((1028, 620), "BIRIBIP POWER-UP! • Transparent 2D-over-3D FX", font=f_tag, fill=(255, 232, 150, 255))

    # 4. Top Header Bar
    f_title = load_font(42, bold=True)
    f_sub = load_font(22, bold=True)
    draw.text((42, 28), "CARLESSO FAMILY 3D MAHJONG SOLITAIRE", font=f_title, fill=(248, 218, 120, 255))
    draw.text(
        (44, 84),
        "Imperial Marble & Obsidian 3D Tiles • Blender 5.0.1 Cycles • Three.js • Family Quartets & Diptyques",
        font=f_sub,
        fill=(235, 228, 215, 245),
    )

    # Top-right live badge
    draw.rounded_rectangle((1248, 28, 1562, 82), radius=14, fill=(185, 32, 32, 240), outline=(255, 215, 100, 255), width=3)
    draw.text((1272, 43), "50 CUSTOM 3D TILES", font=load_font(24, bold=True), fill=(255, 245, 210, 255))

    # 5. Bottom Dock: 9 Signature Tiles (Papà S1 Winner, Mamma S2, Ale S3, Sebi S4, Ale+Ghigna M1, Sebi+Pupurabbu M2, Pandas H1+H2, Red Dragon)
    showcase_tiles = [
        ("coupled_A1_top3.png", "S1 • Papà Riccardo"),
        ("coupled_A2.png", "S2 • Mamma Kate"),
        ("coupled_B1.png", "S3 • Solo Ale"),
        ("coupled_B2.png", "S4 • Solo Sebi"),
        ("coupled_C1.png", "M1 • Ale & Ghigna"),
        ("coupled_C2.png", "M2 • Sebi & Pupurabbu"),
        ("coupled_H1.png", "H1 • Panda Ale (Sx)"),
        ("coupled_H2.png", "H2 • Panda Sebi (Dx)"),
        ("dragon_red.png", "C • 3D Red Dragon"),
    ]

    tile_w, tile_h = 148, 198
    gap = 22
    total_w = len(showcase_tiles) * tile_w + (len(showcase_tiles) - 1) * gap
    start_x = (W - total_w) // 2
    y_top = 735
    f_lbl = load_font(15, bold=True)

    for idx, (fname, label) in enumerate(showcase_tiles):
        tx = start_x + idx * (tile_w + gap)
        t_img = Image.open(ROOT / "public/textures/tiles" / fname).convert("RGBA")
        b_col = (255, 230, 0, 255) if idx in (0, 6, 7, 8) else (245, 212, 112, 220)
        add_rounded_card(canvas, t_img, (tx, y_top, tx + tile_w, y_top + tile_h), radius=14, border_color=b_col, border_w=3)
        draw = ImageDraw.Draw(canvas)
        bbox = draw.textbbox((0, 0), label, font=f_lbl)
        tw = bbox[2] - bbox[0]
        draw.text((tx + (tile_w - tw) // 2, y_top + tile_h + 10), label, font=f_lbl, fill=(248, 225, 152, 255))

    rgb = canvas.convert("RGB")
    LOCAL_SHOT.parent.mkdir(parents=True, exist_ok=True)
    rgb.save(LOCAL_SHOT, quality=92, optimize=True)
    if VETRINA_SHOT.parent.exists():
        rgb.save(VETRINA_SHOT, quality=92, optimize=True)
    print(f"✅ Saved epic showcase screenshot to:\n  - {LOCAL_SHOT}\n  - {VETRINA_SHOT}")


if __name__ == "__main__":
    main()
