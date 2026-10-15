#!/usr/bin/env python3
"""
Demonstrates the Decoupled 2D-to-3D Pipeline requested by RiccardinoCM26:
1. Pure 2D portrait (from Nano Banana + Character Consistency refs, NEVER asking Nano Banana to draw a mahjong tile!)
2. Masked into an ornate Gold-Rimmed OVAL Cameo Medallion (plus optional Bassorilievo normal/bump map)
3. Applied in 2D onto a Generic 3D White Imperial Marble + Black Obsidian Finiture Mahjong Tile in Blender 5.0.1 Cycles.
"""
import glob
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import bpy

ARTIFACT_DIR = Path("/usr/local/google/home/ricc/.gemini/jetski/brain/9ef9919c-2c1e-4390-86c1-6df5d260d22f")
PROJECT_DIR = Path("/usr/local/google/home/ricc/.gemini/jetski/scratch/family-mahjong-3d")
CONCEPTS_DIR = PROJECT_DIR / "public" / "concepts"
CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)


def get_font(size: int, bold: bool = False):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if Path(p).exists():
        return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def build_oval_medallion_textures(src_2d_path: Path, badge_code: str, border_rgb=(220, 170, 55)) -> tuple[Path, Path]:
    """
    Takes a pure 2D portrait image and produces:
    1) A 1024x1365 tile face texture with creamy White Imperial Marble background and a crisp OVAL portrait cameo in the center
    2) A matching 1024x1365 tangent-space Normal/Height map for the optional Bassorilievo cameo mode!
    """
    W, H = 768, 1024
    # Creamy white marble base canvas
    canvas = Image.new("RGB", (W, H), (244, 240, 232))
    draw = ImageDraw.Draw(canvas)

    # Subtle procedural marble veins on the 2D tile face canvas
    rng = np.random.default_rng(42)
    for _ in range(14):
        x0, y0 = int(rng.integers(0, W)), int(rng.integers(0, H))
        x1, y1 = min(W, max(0, x0 + int(rng.integers(-300, 300)))), min(H, max(0, y0 + int(rng.integers(-300, 300))))
        draw.line([(x0, y0), (x1, y1)], fill=(228, 222, 210), width=2)

    # Load pure 2D portrait
    im = Image.open(src_2d_path).convert("RGB")
    iw, ih = im.size
    # Oval bounding box in center-lower of tile face (leaving top-left for 3D alphabet glyph)
    oval_w, oval_h = int(W * 0.78), int(H * 0.72)
    oval_x0 = (W - oval_w) // 2
    oval_y0 = int(H * 0.19)
    oval_x1 = oval_x0 + oval_w
    oval_y1 = oval_y0 + oval_h

    # Center-crop source 2D portrait to oval aspect
    target_aspect = oval_w / oval_h
    if iw / ih > target_aspect:
        new_w = int(ih * target_aspect)
        left = (iw - new_w) // 2
        im_crop = im.crop((left, 0, left + new_w, ih))
    else:
        new_h = int(iw / target_aspect)
        top = (ih - new_h) // 2
        im_crop = im.crop((0, top, iw, top + new_h))
    im_crop = im_crop.resize((oval_w, oval_h), Image.Resampling.LANCZOS)

    # Create anti-aliased oval mask
    mask = Image.new("L", (oval_w, oval_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse([4, 4, oval_w - 5, oval_h - 5], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=1.5))

    # Paste 2D portrait inside the Oval on the tile face
    canvas.paste(im_crop, (oval_x0, oval_y0), mask)

    # Ornate concentric Oval Cameo Rings (Obsidian inner hairline + Gold Kintsugi rim + Theme color accent)
    draw.ellipse([oval_x0 - 8, oval_y0 - 8, oval_x1 + 8, oval_y1 + 8], outline=(24, 24, 30), width=8)
    draw.ellipse([oval_x0 - 3, oval_y0 - 3, oval_x1 + 3, oval_y1 + 3], outline=border_rgb, width=6)
    draw.ellipse([oval_x0 + 4, oval_y0 + 4, oval_x1 - 4, oval_y1 - 4], outline=(250, 220, 125), width=3)

    albedo_path = CONCEPTS_DIR / f"oval_face_albedo_{badge_code}.png"
    canvas.save(albedo_path, "PNG")

    # Build a Bassorilievo normal map from luminance inside the oval + bevel rim
    gray = np.asarray(im_crop.convert("L"), dtype=np.float32) / 255.0
    # Smooth slightly for clean cameo relief (avoiding noisy skin pores)
    gray_pil = Image.fromarray((gray * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=2.2))
    h_oval = np.asarray(gray_pil, dtype=np.float32) / 255.0

    full_h = np.full((H, W), 0.5, dtype=np.float32)
    mask_np = np.asarray(mask, dtype=np.float32) / 255.0
    full_h[oval_y0:oval_y1, oval_x0:oval_x1] = 0.5 + (h_oval - 0.5) * 0.45 * mask_np + 0.15 * mask_np

    # Compute Sobel gradients -> tangent space normal map (R=X, G=Y, B=Z)
    gy, gx = np.gradient(full_h * 14.0)
    nx = -gx
    ny = gy
    nz = np.ones_like(nx)
    length = np.sqrt(nx * nx + ny * ny + nz * nz) + 1e-6
    nx, ny, nz = nx / length, ny / length, nz / length
    norm_rgb = np.stack([(nx * 0.5 + 0.5) * 255, (ny * 0.5 + 0.5) * 255, (nz * 0.5 + 0.5) * 255], axis=-1).astype(np.uint8)
    normal_path = CONCEPTS_DIR / f"oval_face_normal_{badge_code}.png"
    Image.fromarray(norm_rgb).save(normal_path, "PNG")

    return albedo_path, normal_path


def render_comparison(src_2d_path: Path):
    albedo_path, normal_path = build_oval_medallion_textures(src_2d_path, "C1")

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 32
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720

    world = bpy.data.worlds.new("StudioWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.08, 0.07, 0.10, 1.0)
    bg.inputs["Strength"].default_value = 1.1

    # Materials
    marble = bpy.data.materials.new("WhiteMarble")
    marble.use_nodes = True
    m_bsdf = marble.node_tree.nodes.get("Principled BSDF")
    m_bsdf.inputs["Base Color"].default_value = (0.95, 0.93, 0.89, 1.0)
    m_bsdf.inputs["Roughness"].default_value = 0.15

    obsidian = bpy.data.materials.new("BlackObsidian")
    obsidian.use_nodes = True
    o_bsdf = obsidian.node_tree.nodes.get("Principled BSDF")
    o_bsdf.inputs["Base Color"].default_value = (0.035, 0.035, 0.045, 1.0)
    o_bsdf.inputs["Roughness"].default_value = 0.12
    o_bsdf.inputs["Metallic"].default_value = 0.25

    gold = bpy.data.materials.new("GoldBadge")
    gold.use_nodes = True
    g_bsdf = gold.node_tree.nodes.get("Principled BSDF")
    g_bsdf.inputs["Base Color"].default_value = (0.95, 0.78, 0.30, 1.0)
    g_bsdf.inputs["Metallic"].default_value = 0.94
    g_bsdf.inputs["Roughness"].default_value = 0.18

    rosewood = bpy.data.materials.new("Rosewood")
    rosewood.use_nodes = True
    r_bsdf = rosewood.node_tree.nodes.get("Principled BSDF")
    r_bsdf.inputs["Base Color"].default_value = (0.18, 0.06, 0.04, 1.0)
    r_bsdf.inputs["Roughness"].default_value = 0.28

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.45))
    tbl = bpy.context.active_object
    tbl.scale = (6.0, 4.0, 0.15)
    tbl.data.materials.append(rosewood)

    def spawn_generic_tile(x_pos: float, use_bassorilievo: bool, label: str):
        W, H, D = 0.96, 1.28, 0.56
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0, 0))
        body = bpy.context.active_object
        body.scale = (W, H, D)
        bpy.ops.object.transform_apply(scale=True)
        bev = body.modifiers.new("Bevel", "BEVEL")
        bev.width = 0.055
        bev.segments = 4
        bpy.ops.object.modifier_apply(modifier="Bevel")
        body.data.materials.append(marble)

        # Obsidian backing finiture
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0, -D * 0.38))
        back = bpy.context.active_object
        back.scale = (W * 0.99, H * 0.99, D * 0.26)
        bpy.ops.object.transform_apply(scale=True)
        bev2 = back.modifiers.new("Bevel", "BEVEL")
        bev2.width = 0.035
        bev2.segments = 3
        bpy.ops.object.modifier_apply(modifier="Bevel")
        back.data.materials.append(obsidian)
        back.parent = body

        # Raised 3D Alphabet Corner Badge
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos - W * 0.30, H * 0.36, D * 0.515))
        badge = bpy.context.active_object
        badge.scale = (0.20, 0.15, 0.035)
        bpy.ops.object.transform_apply(scale=True)
        bev3 = badge.modifiers.new("Bevel", "BEVEL")
        bev3.width = 0.01
        bev3.segments = 2
        bpy.ops.object.modifier_apply(modifier="Bevel")
        badge.data.materials.append(gold)
        badge.parent = body

        # 2D Oval Face Plane on Generic Tile
        bpy.ops.mesh.primitive_plane_add(size=1.0, location=(x_pos, 0, D * 0.503))
        face = bpy.context.active_object
        face.scale = (W * 0.86, H * 0.86, 1.0)
        bpy.ops.object.transform_apply(scale=True)

        fmat = bpy.data.materials.new(f"Mat_{label}")
        fmat.use_nodes = True
        nodes = fmat.node_tree.nodes
        links = fmat.node_tree.links
        bsdf = nodes.get("Principled BSDF")
        tex = nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(str(albedo_path))
        links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.22

        if use_bassorilievo:
            ntex = nodes.new("ShaderNodeTexImage")
            ntex.image = bpy.data.images.load(str(normal_path))
            ntex.image.colorspace_settings.name = "Non-Color"
            nmap = nodes.new("ShaderNodeNormalMap")
            nmap.inputs["Strength"].default_value = 1.65
            links.new(ntex.outputs["Color"], nmap.inputs["Color"])
            links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])

        face.data.materials.append(fmat)
        face.parent = body
        body.rotation_euler = (0.30, 0.0, 0.08 if not use_bassorilievo else -0.08)

    spawn_generic_tile(-0.68, use_bassorilievo=False, label="Flat2D_Oval")
    spawn_generic_tile(0.68, use_bassorilievo=True, label="Bassorilievo_Oval")

    bpy.ops.object.light_add(type="AREA", location=(-1.2, -3.2, 3.6))
    l1 = bpy.context.active_object
    l1.data.energy = 260.0
    l1.data.size = 3.5
    l1.data.color = (1.0, 0.95, 0.86)
    l1.rotation_euler = (0.68, 0.0, -0.25)

    bpy.ops.object.light_add(type="AREA", location=(2.2, -2.5, 2.8))
    l2 = bpy.context.active_object
    l2.data.energy = 160.0
    l2.data.color = (0.85, 0.92, 1.0)

    bpy.ops.object.camera_add(location=(0.0, -2.55, 2.35), rotation=(0.76, 0.0, 0.0))
    cam = bpy.context.active_object
    cam.data.lens = 38
    scene.camera = cam

    raw_render = CONCEPTS_DIR / "oval_demo_raw.png"
    scene.render.filepath = str(raw_render)
    bpy.ops.render.render(write_still=True)

    # Composite final presentation sheet: Left = Pure 2D Portrait + Oval Mask, Right = Blender 3D Generic Tile Render (2D Oval vs Bassorilievo)
    render_im = Image.open(raw_render).convert("RGB").resize((890, 656), Image.Resampling.LANCZOS)
    sheet = Image.new("RGB", (1280, 720), (14, 12, 18))
    sheet.paste(render_im, (390, 64))

    # Left sidebar showing Stage 1 (Pure 2D Image) -> Stage 2 (Oval Medallion Texture)
    draw = ImageDraw.Draw(sheet)
    draw.rectangle([0, 0, 390, 720], fill=(18, 16, 24))
    draw.line([(390, 68), (390, 720)], fill=(235, 190, 80), width=2)

    p2d = Image.open(src_2d_path).convert("RGB").resize((160, 160), Image.Resampling.LANCZOS)
    sheet.paste(p2d, (24, 108))
    draw.rectangle([24, 108, 184, 268], outline=(235, 190, 80), width=2)
    draw.text((24, 84), "1. Pure 2D Portrait", fill=(255, 220, 115), font=get_font(15, bold=True))

    oval_preview = Image.open(albedo_path).convert("RGB").resize((150, 200), Image.Resampling.LANCZOS)
    sheet.paste(oval_preview, (212, 88))
    draw.rectangle([212, 88, 362, 288], outline=(235, 190, 80), width=2)
    draw.text((212, 68), "2. Oval Medallion", fill=(255, 220, 115), font=get_font(15, bold=True))

    norm_preview = Image.open(normal_path).convert("RGB").resize((150, 200), Image.Resampling.LANCZOS)
    sheet.paste(norm_preview, (212, 330))
    draw.rectangle([212, 330, 362, 530], outline=(130, 180, 255), width=2)
    draw.text((212, 308), "3. Optional Bassorilievo", fill=(165, 205, 255), font=get_font(14, bold=True))

    draw.text((24, 330), "Decoupled Pipeline:", fill=(255, 235, 190), font=get_font(15, bold=True))
    draw.text((24, 356), "• Nano Banana ONLY", fill=(200, 210, 225), font=get_font(13))
    draw.text((24, 376), "  renders pure 2D scene", fill=(200, 210, 225), font=get_font(13))
    draw.text((24, 402), "• Cropped to Oval Cameo", fill=(200, 210, 225), font=get_font(13))
    draw.text((24, 428), "• Mapped onto 1 Generic", fill=(200, 210, 225), font=get_font(13))
    draw.text((24, 448), "  3D Marble Tile in GLB", fill=(200, 210, 225), font=get_font(13))

    # Top header bar
    draw.rectangle([0, 0, 1280, 64], fill=(12, 10, 16))
    draw.line([(0, 64), (1280, 64)], fill=(235, 190, 80), width=2)
    draw.text((24, 12), "CONCEPT MOCK 06 • DECOUPLED PIPELINE: PURE 2D OVAL MEDALLION ON GENERIC 3D MARBLE TILE", fill=(255, 220, 115), font=get_font(19, bold=True))
    draw.text((24, 38), "Left: Pure 2D CC Portrait → Oval Medallion Mask   |   Center 3D Tile: Clean 2D Oval Render   |   Right 3D Tile: Subtle Bassorilievo Normal Relief", fill=(215, 222, 235), font=get_font(14))

    out_art = ARTIFACT_DIR / "mock_06_generic_tile_with_2d_oval_and_bassorilievo.png"
    out_pub = CONCEPTS_DIR / "mock_06_generic_tile_with_2d_oval_and_bassorilievo.png"
    sheet.save(out_art, "PNG")
    sheet.save(out_pub, "PNG")
    print("Saved:", out_art)


if __name__ == "__main__":
    cands = sorted(glob.glob(str(ARTIFACT_DIR / "portrait_cantonese_rice_pure2d*")))
    src = Path(cands[-1]) if cands else (ARTIFACT_DIR / "ref_ale_ghigna_sebi_pupurabbu.jpg")
    render_comparison(src)
