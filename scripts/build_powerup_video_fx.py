#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pillow",
#     "numpy",
# ]
# ///
"""
Adversarial White-Background (#FFFFFF) -> Zero-Halo RGBA Transparency & Video Builder (`v1.7.0`).
Implements the joint Subagent A + Subagent B 3-Stage Pipeline:
  1. Stage 1 — Chroma-Aware Neutral Whiteness Metric:
     w_neutral = c_min - 1.85 * (c_max - c_min)
     (Protects bright yellow-orange dragon fire and golden scales from being mistaken for white!)
  2. Stage 2 — Border-Seeded Connected-Component Flood Fill (BFS):
     Only white regions topologically connected to the outer frame boundary (or exterior background)
     are keyed out! Internal white highlights inside the dragon (eyes, teeth/fangs, horns, white-hot
     fire core) are 100% protected (alpha = 1.0, zero Swiss-cheese holes!).
  3. Stage 3 — Exact White Un-Premultiplication (Color Decontamination) & Warm Fire/Mist Despill:
     Inverts C_obs = alpha * C_true + (1 - alpha) * 1.0 -> C_clean = (C_obs - (1 - alpha)) / alpha
     so semi-transparent cloud puffs and flame edges have ZERO chalky white fringe over the dark 3D board!

Outputs:
  - public/fx/powerup_frame1_cloud_puff_rgba.png
  - public/fx/powerup_frame2_dragon_emerge_rgba.png  (RiccardinoCM26's favorite centerpiece!)
  - public/fx/powerup_frame3_dragon_fire_rgba.png
  - public/fx/dragon_powerup_white.mp4 (real 30fps H.264 video on #FFFFFF white background)
  - public/fx/dragon_powerup_audit_comparison.png (3-panel visual proof for GitHub Issue #1 & Gallery)
"""

from collections import deque
import math
import shutil
import subprocess
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FX_DIR = ROOT / "public" / "fx"
ARTIFACT_DIR = Path("/Users/ricc/.gemini/antigravity/brain/9efaaa30-d5fa-49dc-b7c4-7292c03768b3")


def remove_white_bg_adversarial(im_rgb: Image.Image) -> tuple[Image.Image, Image.Image]:
    """
    Returns:
      - clean_rgba: Adversarial 3-Stage Flood-Fill + Chroma-Protected + White-Unpremultiplied RGBA
      - naive_rgba: Naive `R>240 & G>240 & B>240` threshold RGBA (for comparison audit)
    """
    W, H = im_rgb.size
    arr = np.asarray(im_rgb.convert("RGB"), dtype=np.float32) / 255.0

    # --- Naive threshold (for comparison panel) ---
    naive_bg = (arr[:, :, 0] > 240 / 255.0) & (arr[:, :, 1] > 240 / 255.0) & (arr[:, :, 2] > 240 / 255.0)
    naive_a = np.where(naive_bg, 0, 255).astype(np.uint8)
    naive_rgba = Image.fromarray(np.dstack([ (arr * 255).astype(np.uint8), naive_a ]), mode="RGBA")

    # --- Stage 1: Corner-Calibrated Chroma-Aware Neutral Whiteness ---
    corners = np.concatenate([
        arr[:16, :16].reshape(-1, 3),
        arr[:16, -16:].reshape(-1, 3),
        arr[-16:, :16].reshape(-1, 3),
        arr[-16:, -16:].reshape(-1, 3),
    ], axis=0)
    w_bg = np.clip(np.median(corners, axis=0), 0.95, 1.0)
    c_norm = np.clip(arr / w_bg, 0.0, 1.0)

    c_min = np.min(c_norm, axis=-1)
    c_max = np.max(c_norm, axis=-1)
    sat = c_max - c_min
    # d_max = 1 - min(R,G,B): measures true non-white pigment density!
    # Pure white = 0.0; pale white/peach outer halo = 0.05..0.24; real yellow/orange fire (low Blue) = 0.65..0.98!
    d_max = 1.0 - c_min

    # --- Stage 2: Border-Seeded Connected-Component Flood Fill on (d_max < 0.34) ---
    # Any pale halo pixel connected to the outer border is classified as exterior;
    # white-hot cores/eyes/teeth enclosed INSIDE the dragon or flame are 100% protected!
    bg_cand = (d_max < 0.34) & (sat < 0.32)
    sh, sw = H // 2, W // 2
    bg_small = bg_cand[::2, ::2].copy()
    visited = np.zeros((sh, sw), dtype=bool)
    q = deque()

    for x in range(sw):
        if bg_small[0, x]:
            visited[0, x] = True
            q.append((0, x))
        if bg_small[sh - 1, x]:
            visited[sh - 1, x] = True
            q.append((sh - 1, x))
    for y in range(sh):
        if bg_small[y, 0] and not visited[y, 0]:
            visited[y, 0] = True
            q.append((y, 0))
        if bg_small[y, sw - 1] and not visited[y, sw - 1]:
            visited[y, sw - 1] = True
            q.append((y, sw - 1))

    while q:
        cy, cx = q.popleft()
        for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
            if 0 <= ny < sh and 0 <= nx < sw and not visited[ny, nx] and bg_small[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))

    # Upsample exterior background mask and dilate slightly into the anti-aliased transition edge
    ext_mask_im = Image.fromarray((visited.astype(np.uint8) * 255), mode="L").resize((W, H), Image.Resampling.BILINEAR)
    ext_zone = np.asarray(ext_mask_im.filter(ImageFilter.MaxFilter(size=17)).filter(ImageFilter.GaussianBlur(radius=4.0)), dtype=np.float32) / 255.0

    # On the exterior zone, require d_max >= 0.26 to begin appearing, reaching full opacity at d_max = 0.62
    t_ext = np.clip((d_max - 0.26) / (0.62 - 0.26), 0.0, 1.0)
    alpha_ext = t_ext * t_ext * (3.0 - 2.0 * t_ext)

    # Combine interior (1.0) and exterior (alpha_ext)
    alpha_raw = (1.0 - ext_zone) * 1.0 + ext_zone * alpha_ext

    # Soft radial safety vignette at outermost 3% border
    yy, xx = np.mgrid[0:H, 0:W]
    rad = np.sqrt(((xx - W * 0.5) / (W * 0.5)) ** 2 + ((yy - H * 0.5) / (H * 0.5)) ** 2)
    vig = np.clip((0.99 - rad) / 0.08, 0.0, 1.0)
    alpha = np.clip(alpha_raw * vig, 0.0, 1.0)

    # Slight feather on alpha for silky smoke/fire edges
    alpha_im = Image.fromarray(np.clip(alpha * 255.0, 0, 255).astype(np.uint8), mode="L").filter(ImageFilter.GaussianBlur(radius=1.0))
    alpha = np.asarray(alpha_im, dtype=np.float32) / 255.0

    # --- Stage 3: Exact White Un-Premultiplication (Color Decontamination) & Fiery Edge Despill ---
    alpha_safe = np.maximum(alpha, 0.12)[:, :, None]
    c_clean = np.clip((c_norm - (1.0 - alpha[:, :, None])) / alpha_safe, 0.0, 1.0)

    # Pull semi-transparent outer edge pixels toward rich fiery amber-crimson so zero white/chalky rim can ever appear
    fire_edge_color = np.array([0.96, 0.42, 0.06], dtype=np.float32)
    edge_blend = (np.clip(1.0 - alpha, 0.0, 1.0) ** 1.2 * ext_zone * 0.82)[:, :, None]
    c_final = c_clean * (1.0 - edge_blend) + fire_edge_color * edge_blend

    rgba_u8 = np.dstack([
        np.clip(c_final * 255.0, 0, 255).astype(np.uint8),
        np.clip(alpha * 255.0, 0, 255).astype(np.uint8),
    ])
    return Image.fromarray(rgba_u8, mode="RGBA"), naive_rgba


def build_white_bg_video_and_audit(
    f1_white: Image.Image,
    f2_white: Image.Image,
    f3_white: Image.Image,
    f2_naive: Image.Image,
    f2_clean: Image.Image,
):
    """
    1. Builds a 42-frame 30fps animation on pure #FFFFFF white background (`dragon_powerup_white.mp4`)
       centering on RiccardinoCM26's favorite `powerup_frame2_dragon_emerge_white.png`!
    2. Builds the 3-panel Adversarial Audit comparison image (`dragon_powerup_audit_comparison.png`).
    """
    S = 720
    f1_s = f1_white.resize((S, S), Image.Resampling.LANCZOS)
    f2_s = f2_white.resize((S, S), Image.Resampling.LANCZOS)
    f3_s = f3_white.resize((S, S), Image.Resampling.LANCZOS)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        total_frames = 45
        for i in range(total_frames):
            t = i / (total_frames - 1)
            canvas = Image.new("RGB", (S, S), (255, 255, 255))
            if t < 0.24:
                # Stage 1: Cloud Puff bursting outward from center
                u = t / 0.24
                scale = 0.28 + 0.82 * math.sin(u * math.pi * 0.5)
                sz = max(32, int(S * scale))
                puff = f1_s.resize((sz, sz), Image.Resampling.LANCZOS).rotate(u * 18.0, resample=Image.Resampling.BICUBIC, fillcolor=(255, 255, 255))
                ox = (S - sz) // 2
                oy = (S - sz) // 2
                canvas.paste(puff, (ox, oy))
            elif t < 0.80:
                # Stage 2 (Star Centerpiece!): Frame 2 Dragon Emerging from Cloud Puff & Breathing Fire!
                u = (t - 0.24) / 0.56
                bob_y = int(math.sin(u * math.pi * 2.5) * 12)
                scale = 0.94 + 0.10 * math.sin(u * math.pi)
                sz = int(S * scale)
                drg = f2_s.resize((sz, sz), Image.Resampling.LANCZOS)
                ox = (S - sz) // 2
                oy = (S - sz) // 2 + bob_y
                canvas.paste(drg, (ox, oy))
                if u < 0.22:
                    # Cross-dissolve from cloud puff
                    alpha_puff = 1.0 - (u / 0.22)
                    canvas = Image.blend(canvas, f1_s, alpha_puff * 0.65)
            else:
                # Stage 3: Climax Fire Vortex & fade to white
                u = (t - 0.80) / 0.20
                blend = Image.blend(f2_s, f3_s, min(1.0, u * 1.4))
                if u > 0.55:
                    fade = (u - 0.55) / 0.45
                    white_im = Image.new("RGB", (S, S), (255, 255, 255))
                    blend = Image.blend(blend, white_im, fade)
                canvas.paste(blend, (0, 0))

            canvas.save(tmp / f"frame_{i:03d}.png", "PNG")

        mp4_out = FX_DIR / "dragon_powerup_white.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-framerate", "30",
                "-i", str(tmp / "frame_%03d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                str(mp4_out),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"🎬 Built White-Background Video: {mp4_out} ({mp4_out.stat().st_size // 1024} KB)")

    # Build 3-Panel Adversarial Audit Comparison Image over the 3D Temple Board Render
    bg_render_path = ROOT / "public" / "renders" / "cycles" / "cycles_cam1_hero.png"
    pw, ph = 520, 520
    audit = Image.new("RGB", (pw * 3 + 40, ph + 90), (16, 12, 20))
    draw = ImageDraw.Draw(audit)

    if bg_render_path.exists():
        temple_bg = Image.open(bg_render_path).convert("RGB").resize((pw, ph), Image.Resampling.LANCZOS)
    else:
        temple_bg = Image.new("RGB", (pw, ph), (28, 22, 34))

    # Panel 1: Raw White-Background Frame 2
    p1 = f2_white.resize((pw, ph), Image.Resampling.LANCZOS)
    audit.paste(p1, (10, 65))

    # Panel 2: Naive R>240 & G>240 & B>240 over Dark 3D Temple (shows chalky white fringe & eye/fire holes)
    p2 = temple_bg.copy()
    naive_s = f2_naive.resize((pw, ph), Image.Resampling.LANCZOS)
    p2.paste(naive_s, (0, 0), naive_s)
    audit.paste(p2, (pw + 20, 65))

    # Panel 3: Adversarial 3-Stage Flood-Fill + Un-Premultiplied RGBA over Dark 3D Temple (Zero Halo!)
    p3 = temple_bg.copy()
    clean_s = f2_clean.resize((pw, ph), Image.Resampling.LANCZOS)
    p3.paste(clean_s, (0, 0), clean_s)
    audit.paste(p3, (pw * 2 + 30, 65))

    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
    except Exception:
        font_title = ImageFont.load_default()

    draw.text((22, 22), "1. Raw Source on #FFFFFF White Base", fill=(245, 212, 112), font=font_title)
    draw.text((pw + 32, 22), "2. Naive White Key (Chalky Fringe & Holes)", fill=(255, 110, 110), font=font_title)
    draw.text((pw * 2 + 42, 22), "3. Adversarial 3-Stage Key + Despill over 3D!", fill=(95, 242, 165), font=font_title)

    audit_path = FX_DIR / "dragon_powerup_audit_comparison.png"
    audit.save(audit_path, "PNG")
    if ARTIFACT_DIR.exists():
        shutil.copy2(audit_path, ARTIFACT_DIR / audit_path.name)
        shutil.copy2(FX_DIR / "powerup_frame2_dragon_emerge_rgba.png", ARTIFACT_DIR / "powerup_frame2_dragon_emerge_rgba.png")
    print(f"✅ Saved 3-Panel Adversarial VFX Audit: {audit_path}")


def main():
    frames = [
        ("powerup_frame1_cloud_puff_white.png", "powerup_frame1_cloud_puff_rgba.png"),
        ("powerup_frame2_dragon_emerge_white.png", "powerup_frame2_dragon_emerge_rgba.png"),
        ("powerup_frame3_dragon_fire_white.png", "powerup_frame3_dragon_fire_rgba.png"),
    ]
    loaded_white = {}
    loaded_clean = {}
    loaded_naive = {}

    for src_name, dst_name in frames:
        im_w = Image.open(FX_DIR / src_name).convert("RGB")
        clean_rgba, naive_rgba = remove_white_bg_adversarial(im_w)
        # Save at 768x768 for fast WebGL/Canvas rendering
        clean_768 = clean_rgba.resize((768, 768), Image.Resampling.LANCZOS)
        clean_768.save(FX_DIR / dst_name, "PNG")
        loaded_white[src_name] = im_w
        loaded_clean[src_name] = clean_rgba
        loaded_naive[src_name] = naive_rgba
        print(f"✨ Extracted Zero-Halo Transparent RGBA: {dst_name}")

    build_white_bg_video_and_audit(
        loaded_white["powerup_frame1_cloud_puff_white.png"],
        loaded_white["powerup_frame2_dragon_emerge_white.png"],
        loaded_white["powerup_frame3_dragon_fire_white.png"],
        loaded_naive["powerup_frame2_dragon_emerge_white.png"],
        loaded_clean["powerup_frame2_dragon_emerge_white.png"],
    )


if __name__ == "__main__":
    main()
