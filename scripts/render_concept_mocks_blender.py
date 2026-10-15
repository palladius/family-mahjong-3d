#!/usr/bin/env python3
"""
Renders the 4 Concept & Track Design Mocks using Headless Blender 5.0.1 (Cycles)
and PIL composition with authentic Carlesso Family reference photos (Ale, Sebi, Riccardo, Kate, Ghigna, Pupurabbu).
Saves directly to both the Artifact directory and public/concepts/ so they can be embedded in the Plan .md artifact.
"""
import math
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import bpy

ARTIFACT_DIR = Path("/usr/local/google/home/ricc/.gemini/jetski/brain/9ef9919c-2c1e-4390-86c1-6df5d260d22f")
PROJECT_DIR = Path("/usr/local/google/home/ricc/.gemini/jetski/scratch/family-mahjong-3d")
CONCEPTS_DIR = PROJECT_DIR / "public" / "concepts"
CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

ALE_DIR = Path("/usr/local/google/home/ricc/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/alessandro")
SEBI_DIR = Path("/usr/local/google/home/ricc/git/gic/private/projects/git-privatize/github.com__palladius__media-arneis/data/characters/sebastian")
FAMILY_SKILL_ASSETS = Path("/usr/local/google/home/ricc/git/gemini-cli-palladius-private-goodies/skills/carlesso-family/assets")


def get_font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size=size)
    return ImageFont.load_default()


def create_themed_coupled_card(
    photo_a: Path,
    photo_b: Path,
    badge_code: str,
    theme_title: str,
    pose_subtitle: str,
    border_rgb: tuple[int, int, int],
    bg_tint: tuple[int, int, int],
    motif_type: str,
    size: tuple[int, int] = (512, 680),
) -> Path:
    """Create a rich Chinese/Asian-themed coupled tile face texture featuring Ale & Sebi."""
    w, h = size
    card = Image.new("RGB", (w, h), bg_tint)
    draw = ImageDraw.Draw(card)

    # Rich Chinese silk / brocade background gradient + subtle pattern
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(bg_tint[0] * (1 - 0.35 * t) + 18 * t)
        g = int(bg_tint[1] * (1 - 0.35 * t) + 14 * t)
        b = int(bg_tint[2] * (1 - 0.35 * t) + 12 * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Decorative Chinese cloud / lattice watermark circles
    for cx in range(40, w, 80):
        for cy in range(40, h, 80):
            draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], outline=(border_rgb[0], border_rgb[1], border_rgb[2]), width=1)

    # Load and composite the two character reference images in a coupled Asian vignette
    def load_crop_face(p: Path, target_w: int, target_h: int) -> Image.Image:
        if p.exists():
            im = Image.open(p).convert("RGB")
            iw, ih = im.size
            aspect = target_w / target_h
            if iw / ih > aspect:
                new_w = int(ih * aspect)
                left = (iw - new_w) // 2
                im = im.crop((left, 0, left + new_w, ih))
            else:
                new_h = int(iw / aspect)
                top = max(0, (ih - new_h) // 4)
                im = im.crop((0, top, iw, top + new_h))
            im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
            return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.12)).enhance(1.15)
        return Image.new("RGB", (target_w, target_h), (120, 80, 60))

    # Coupled dual-frame or single hero composition inside the tile art
    inner_margin = 36
    art_top = 115
    art_bottom = h - 115
    art_w = w - 2 * inner_margin
    art_h = art_bottom - art_top

    half_w = (art_w - 10) // 2
    im_a = load_crop_face(photo_a, half_w, art_h)
    im_b = load_crop_face(photo_b, half_w, art_h)

    card.paste(im_a, (inner_margin, art_top))
    card.paste(im_b, (inner_margin + half_w + 10, art_top))

    # Gold divider between coupled portraits
    draw.rectangle(
        [inner_margin + half_w + 2, art_top, inner_margin + half_w + 7, art_bottom],
        fill=(235, 195, 95),
    )

    # Theme-specific illustrated props overlay (Chinese lanterns, Cantonese rice bowl, Bamboo/Panda, Great Wall battlements, Kung Fu aura)
    if motif_type == "tang_silk":
        # Red & Gold silk lanterns at top of frame
        for lx in [inner_margin + 35, w - inner_margin - 35]:
            draw.ellipse([lx - 26, art_top - 18, lx + 26, art_top + 28], fill=(210, 35, 35), outline=(250, 210, 90), width=3)
            draw.rectangle([lx - 10, art_top - 24, lx + 10, art_top - 17], fill=(245, 200, 75))
    elif motif_type == "sightseeing":
        # Great Wall battlements along bottom of frame + camera icon
        bx0 = inner_margin
        while bx0 < w - inner_margin - 24:
            draw.rectangle([bx0, art_bottom - 26, bx0 + 18, art_bottom], fill=(165, 145, 120), outline=(90, 75, 60), width=2)
            bx0 += 28
    elif motif_type == "cantonese_rice":
        # Porcelain bowl of Cantonese fried rice with golden egg, peas, shrimp & chopsticks at bottom center
        cx, cy = w // 2, art_bottom - 18
        draw.chord([cx - 65, cy - 42, cx + 65, cy + 38], start=0, end=180, fill=(215, 45, 45), outline=(250, 215, 100), width=3)
        draw.ellipse([cx - 62, cy - 22, cx + 62, cy + 8], fill=(252, 232, 155), outline=(220, 175, 70), width=2)
        # Chopsticks
        draw.line([(cx + 10, cy - 12), (cx + 85, cy - 55)], fill=(185, 125, 65), width=5)
        draw.line([(cx + 20, cy - 5), (cx + 92, cy - 42)], fill=(185, 125, 65), width=5)
    elif motif_type == "kungfu":
        # Golden dragon chi aura arcs
        draw.arc([inner_margin + 10, art_top + 10, w - inner_margin - 10, art_bottom - 10], start=200, end=340, fill=(255, 195, 50), width=5)
    elif motif_type == "panda":
        # Green bamboo stalks on sides
        for bx in [inner_margin + 8, w - inner_margin - 14]:
            draw.rectangle([bx, art_top + 10, bx + 8, art_bottom - 10], fill=(75, 175, 85), outline=(35, 100, 45), width=1)

    # Outer ornate Imperial Obsidian & Gold border
    draw.rectangle([8, 8, w - 9, h - 9], outline=(28, 28, 34), width=12)
    draw.rectangle([20, 20, w - 21, h - 21], outline=border_rgb, width=5)
    draw.rectangle([inner_margin - 3, art_top - 3, w - inner_margin + 3, art_bottom + 3], outline=(238, 198, 98), width=3)

    # Top-left Hierarchical Alphabet Badge backing
    draw.rounded_rectangle([28, 28, 138, 98], radius=12, fill=(22, 22, 28), outline=(245, 205, 95), width=3)
    draw.text((42, 38), badge_code, fill=(255, 220, 110), font=get_font(44, bold=True))

    # Top-right Theme Title
    draw.text((152, 36), theme_title, fill=(255, 245, 220), font=get_font(24, bold=True))
    draw.text((152, 68), pose_subtitle, fill=(235, 195, 115), font=get_font(18, bold= False))

    # Bottom banner with coupled pair explanation
    draw.rounded_rectangle([28, h - 96, w - 28, h - 26], radius=10, fill=(20, 20, 26), outline=border_rgb, width=2)
    draw.text((44, h - 86), f"ALE & SEBI • {theme_title.upper()}", fill=(255, 238, 195), font=get_font(20, bold=True))
    draw.text((44, h - 56), f"Coupled Pair Match: {badge_code[0]}1 ↔ {badge_code[0]}2  |  Marble + Obsidian Trim", fill=(195, 210, 225), font=get_font(15, bold=False))

    out_path = CONCEPTS_DIR / f"tex_tile_{badge_code}.png"
    card.save(out_path, "PNG")
    return out_path


def build_mahjong_tile_mesh(
    name: str,
    location: tuple[float, float, float],
    marble_mat,
    obsidian_mat,
    gold_mat,
    face_tex_path: Path | None = None,
    badge_code: str = "A1",
):
    """
    Creates a manifold beveled Mahjong tile:
    - Body: Creamy Imperial White Marble (0.90 x 1.20 x 0.65)
    - Finiture / Sfumature: Sleek Volcanic Black Obsidian back & beveled trim ring + Gold Kintsugi inlay
    - Hierarchical 3D Alphabet Overlay: Raised 3D metallic badge at top-left corner of face
    """
    W, H, D = 0.90, 1.20, 0.65
    # 1. White Marble Main Body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    body = bpy.context.active_object
    body.name = f"{name}_MarbleBody"
    body.scale = (W * 0.5, H * 0.5, D * 0.5)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bevel = body.modifiers.new(name="Bevel", type="BEVEL")
    bevel.width = 0.055
    bevel.segments = 3
    bpy.ops.object.modifier_apply(modifier="Bevel")
    body.data.materials.append(marble_mat)

    # 2. Black Obsidian Backing & Bevel Finiture Collar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(location[0], location[1], location[2] - D * 0.36))
    obs_back = bpy.context.active_object
    obs_back.name = f"{name}_ObsidianFiniture"
    obs_back.scale = (W * 0.495, H * 0.495, D * 0.14)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    b2 = obs_back.modifiers.new(name="Bevel", type="BEVEL")
    b2.width = 0.035
    b2.segments = 2
    bpy.ops.object.modifier_apply(modifier="Bevel")
    obs_back.data.materials.append(obsidian_mat)
    obs_back.parent = body

    # 3. Black Obsidian & Gold Frame Rim around Front Face
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(location[0], location[1], location[2] + D * 0.48))
    rim = bpy.context.active_object
    rim.name = f"{name}_ObsidianRim"
    rim.scale = (W * 0.45, H * 0.45, 0.025)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    rim.data.materials.append(obsidian_mat)
    rim.parent = body

    # 4. Hierarchical 3D Alphabet Corner Badge Overlay
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(location[0] - W * 0.27, location[1] + H * 0.32, location[2] + D * 0.525),
    )
    badge = bpy.context.active_object
    badge.name = f"{name}_AlphabetOverlay_{badge_code}"
    badge.scale = (0.11, 0.09, 0.022)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    badge.data.materials.append(gold_mat)
    badge.parent = body

    # 5. Front Face Artwork Plane
    if face_tex_path and face_tex_path.exists():
        bpy.ops.mesh.primitive_plane_add(
            size=1.0,
            location=(location[0], location[1], location[2] + D * 0.508),
        )
        face = bpy.context.active_object
        face.name = f"{name}_FaceArt"
        face.scale = (W * 0.84, H * 0.84, 1.0)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        fmat = bpy.data.materials.new(name=f"Mat_Face_{name}")
        fmat.use_nodes = True
        nodes = fmat.node_tree.nodes
        links = fmat.node_tree.links
        bsdf = nodes.get("Principled BSDF")
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(str(face_tex_path))
        links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.22
        face.data.materials.append(fmat)
        face.parent = body

    return body


def make_pbr_materials():
    # 1. Creamy Imperial White Marble
    marble = bpy.data.materials.new(name="Imperial_White_Marble")
    marble.use_nodes = True
    bsdf = marble.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.95, 0.93, 0.89, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.16
    if "Coat Weight" in bsdf.inputs:
        bsdf.inputs["Coat Weight"].default_value = 0.65

    # 2. Volcanic Black Obsidian Finiture / Sfumature
    obsidian = bpy.data.materials.new(name="Volcanic_Black_Obsidian")
    obsidian.use_nodes = True
    obs_bsdf = obsidian.node_tree.nodes.get("Principled BSDF")
    obs_bsdf.inputs["Base Color"].default_value = (0.04, 0.04, 0.055, 1.0)
    obs_bsdf.inputs["Metallic"].default_value = 0.25
    obs_bsdf.inputs["Roughness"].default_value = 0.12

    # 3. Imperial Gold Kintsugi & Alphabet Overlay
    gold = bpy.data.materials.new(name="Imperial_Gold_Kintsugi")
    gold.use_nodes = True
    g_bsdf = gold.node_tree.nodes.get("Principled BSDF")
    g_bsdf.inputs["Base Color"].default_value = (0.94, 0.76, 0.28, 1.0)
    g_bsdf.inputs["Metallic"].default_value = 0.92
    g_bsdf.inputs["Roughness"].default_value = 0.18

    # 4. Carved Rosewood Table
    rosewood = bpy.data.materials.new(name="Carved_Rosewood_Table")
    rosewood.use_nodes = True
    r_bsdf = rosewood.node_tree.nodes.get("Principled BSDF")
    r_bsdf.inputs["Base Color"].default_value = (0.20, 0.06, 0.04, 1.0)
    r_bsdf.inputs["Roughness"].default_value = 0.28

    # 5. Celadon Jade Inlay
    jade = bpy.data.materials.new(name="Celadon_Jade_Mat")
    jade.use_nodes = True
    j_bsdf = jade.node_tree.nodes.get("Principled BSDF")
    j_bsdf.inputs["Base Color"].default_value = (0.14, 0.36, 0.28, 1.0)
    j_bsdf.inputs["Roughness"].default_value = 0.32

    # 6. Sacred Temple Flagstone Pavement
    pavement = bpy.data.materials.new(name="Sacred_Stone_Pavement")
    pavement.use_nodes = True
    p_bsdf = pavement.node_tree.nodes.get("Principled BSDF")
    p_bsdf.inputs["Base Color"].default_value = (0.16, 0.17, 0.19, 1.0)
    p_bsdf.inputs["Roughness"].default_value = 0.65

    # 7. Crimson Temple Pillar
    crimson = bpy.data.materials.new(name="Crimson_Temple_Lacquer")
    crimson.use_nodes = True
    c_bsdf = crimson.node_tree.nodes.get("Principled BSDF")
    c_bsdf.inputs["Base Color"].default_value = (0.58, 0.07, 0.07, 1.0)
    c_bsdf.inputs["Roughness"].default_value = 0.25

    return marble, obsidian, gold, rosewood, jade, pavement, crimson


def setup_cycles_scene(res_x=1280, res_y=720, samples=24):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = False
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.render.resolution_percentage = 100

    world = bpy.data.worlds.new("TempleWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.09, 0.06, 0.08, 1.0)
    bg.inputs["Strength"].default_value = 1.1
    return scene


def generate_all():
    # Prepare coupled Ale & Sebi textures from authentic reference photos
    ale_1 = ALE_DIR / "PXL_20260218_151036231.jpg"
    ale_2 = ALE_DIR / "PXL_20260403_100103962.jpg"
    ale_3 = ALE_DIR / "PXL_20260220_061600965.jpg"
    ale_4 = ALE_DIR / "PXL_20260419_080152278.jpg"

    sebi_1 = SEBI_DIR / "PXL_20260310_195345815-seby-felice-con-mac.jpg"
    sebi_2 = SEBI_DIR / "seby-ritaglio-foto-classe-26.jpg"
    sebi_3 = SEBI_DIR / "20260418_094506-seby-lingua.jpg"
    sebi_4 = SEBI_DIR / "seby-irlandese-celtico.jpg"

    ghigna_pupu = FAMILY_SKILL_ASSETS / "compagni-magici" / "ale_ghigna_sebi_pupurabbu_google.jpg"
    pranzo_pupu = FAMILY_SKILL_ASSETS / "compagni-magici" / "pranzo_google_ghigna_pupurabbu.jpg"

    tex_A1 = create_themed_coupled_card(ale_1, sebi_1, "A1", "Imperial Tang Silk", "Pose 1: Temple Arch", (215, 50, 50), (110, 24, 28), "tang_silk")
    tex_A2 = create_themed_coupled_card(ale_2, sebi_2, "A2", "Imperial Tang Silk", "Pose 2: Lantern Bow", (215, 50, 50), (110, 24, 28), "tang_silk")

    tex_B1 = create_themed_coupled_card(ale_3, sebi_3, "B1", "Great Wall Sightseeing", "Pose 1: Pagoda View", (55, 185, 125), (24, 78, 62), "sightseeing")
    tex_B2 = create_themed_coupled_card(ale_4, sebi_4, "B2", "Great Wall Sightseeing", "Pose 2: Watchtower", (55, 185, 125), (24, 78, 62), "sightseeing")

    tex_C1 = create_themed_coupled_card(ale_1, sebi_2, "C1", "Cantonese Rice Feast", "Pose 1: Chopstick Toast", (235, 180, 55), (98, 64, 18), "cantonese_rice")
    tex_C2 = create_themed_coupled_card(pranzo_pupu, sebi_1, "C2", "Cantonese Rice Feast", "Pose 2: Dim Sum Table", (235, 180, 55), (98, 64, 18), "cantonese_rice")

    tex_D1 = create_themed_coupled_card(ale_2, sebi_3, "D1", "Shaolin Kung Fu", "Pose 1: Dragon Stance", (240, 120, 40), (95, 42, 18), "kungfu")
    tex_D2 = create_themed_coupled_card(ale_4, sebi_1, "D2", "Shaolin Kung Fu", "Pose 2: Tiger Leap", (240, 120, 40), (95, 42, 18), "kungfu")

    tex_E1 = create_themed_coupled_card(ghigna_pupu, ale_3, "E1", "Panda & Compagni", "Pose 1: Ghigna & Bamboo", (155, 95, 235), (58, 32, 92), "panda")
    tex_E2 = create_themed_coupled_card(pranzo_pupu, sebi_4, "E2", "Panda & Compagni", "Pose 2: Pupurabbu Hug", (155, 95, 235), (58, 32, 92), "panda")

    all_tex = [tex_A1, tex_A2, tex_B1, tex_B2, tex_C1, tex_C2, tex_D1, tex_D2, tex_E1, tex_E2]

    # =========================================================================
    # MOCK 3: Macro Studio Render of 6 Coupled White Marble + Obsidian Finiture Tiles (A1/A2, B1/B2, C1/C2)
    # =========================================================================
    print("Rendering Mock 3 (Coupled White Marble + Obsidian Trim Tiles A1/A2, B1/B2, C1/C2)...")
    scene = setup_cycles_scene(1280, 720, samples=28)
    marble, obsidian, gold, rosewood, jade, pavement, crimson = make_pbr_materials()

    # Rosewood & Stone base
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.42))
    table = bpy.context.active_object
    table.scale = (8.5, 4.5, 0.16)
    table.data.materials.append(rosewood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.62))
    floor = bpy.context.active_object
    floor.scale = (14.0, 9.0, 0.1)
    floor.data.materials.append(pavement)

    pair_Configs = [
        ("Tile_A1", (-2.35, 0.15, 0.0), tex_A1, "A1", 0.12),
        ("Tile_A2", (-1.30, -0.10, 0.0), tex_A2, "A2", -0.10),
        ("Tile_B1", (-0.50, 0.15, 0.0), tex_B1, "B1", 0.08),
        ("Tile_B2", (0.55, -0.10, 0.0), tex_B2, "B2", -0.08),
        ("Tile_C1", (1.35, 0.15, 0.0), tex_C1, "C1", 0.10),
        ("Tile_C2", (2.40, -0.10, 0.0), tex_C2, "C2", -0.12),
    ]
    for name, loc, tpath, bcode, rot_z in pair_Configs:
        t = build_mahjong_tile_mesh(name, loc, marble, obsidian, gold, tpath, bcode)
        t.rotation_euler = (0.32, 0.0, rot_z)

    # Studio Lights
    bpy.ops.object.light_add(type="AREA", location=(0.0, -4.2, 4.5))
    key = bpy.context.active_object
    key.data.energy = 380.0
    key.data.size = 5.0
    key.data.color = (1.0, 0.95, 0.86)
    key.rotation_euler = (0.68, 0.0, 0.0)

    bpy.ops.object.light_add(type="AREA", location=(-4.0, 2.0, 3.0))
    rim_l = bpy.context.active_object
    rim_l.data.energy = 220.0
    rim_l.data.color = (0.85, 0.92, 1.0)

    bpy.ops.object.camera_add(location=(0.0, -4.15, 2.85), rotation=(0.92, 0.0, 0.0))
    cam = bpy.context.active_object
    cam.data.lens = 42
    scene.camera = cam

    mock3_raw = CONCEPTS_DIR / "mock_03_raw.png"
    scene.render.filepath = str(mock3_raw)
    bpy.ops.render.render(write_still=True)

    # Annotate Mock 3 with crisp luxury header & callouts
    im3 = Image.open(mock3_raw).convert("RGB")
    d3 = ImageDraw.Draw(im3)
    d3.rectangle([0, 0, 1280, 66], fill=(14, 12, 18))
    d3.line([(0, 66), (1280, 66)], fill=(235, 190, 80), width=2)
    d3.text((24, 14), "CONCEPT MOCK 03 • WHITE IMPERIAL MARBLE ARCHETYPE + BLACK OBSIDIAN FINITURE", fill=(255, 220, 115), font=get_font(22, bold=True))
    d3.text((24, 42), "Coupled Non-Identical Ale & Sebi Pairs:  [A1 ↔ A2] Imperial Tang Silk   |   [B1 ↔ B2] Great Wall Sightseeing   |   [C1 ↔ C2] Cantonese Fried Rice", fill=(220, 225, 235), font=get_font(15))
    for p_out in [CONCEPTS_DIR / "mock_03_white_marble_obsidian_coupled_tiles.png", ARTIFACT_DIR / "mock_03_white_marble_obsidian_coupled_tiles.png"]:
        im3.save(p_out, "PNG")

    # =========================================================================
    # MOCK 4: Kung Fu (D1/D2) & Chengdu Pandas + Ghigna & Pupurabbu (E1/E2)
    # =========================================================================
    print("Rendering Mock 4 (Kung Fu D1/D2 & Panda Sanctuary + Ghigna & Pupurabbu E1/E2)...")
    scene = setup_cycles_scene(1280, 720, samples=28)
    marble, obsidian, gold, rosewood, jade, pavement, crimson = make_pbr_materials()

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.42))
    table = bpy.context.active_object
    table.scale = (7.0, 4.2, 0.16)
    table.data.materials.append(jade)

    pair_d_e = [
        ("Tile_D1", (-1.75, 0.10, 0.0), tex_D1, "D1", 0.14),
        ("Tile_D2", (-0.65, -0.08, 0.0), tex_D2, "D2", -0.10),
        ("Tile_E1", (0.65, 0.10, 0.0), tex_E1, "E1", 0.10),
        ("Tile_E2", (1.75, -0.08, 0.0), tex_E2, "E2", -0.14),
    ]
    for name, loc, tpath, bcode, rot_z in pair_d_e:
        t = build_mahjong_tile_mesh(name, loc, marble, obsidian, gold, tpath, bcode)
        t.rotation_euler = (0.35, 0.0, rot_z)

    bpy.ops.object.light_add(type="AREA", location=(0.0, -3.8, 4.2))
    key = bpy.context.active_object
    key.data.energy = 360.0
    key.data.size = 4.5
    key.data.color = (1.0, 0.94, 0.84)
    key.rotation_euler = (0.68, 0.0, 0.0)

    bpy.ops.object.camera_add(location=(0.0, -3.55, 2.45), rotation=(0.92, 0.0, 0.0))
    cam = bpy.context.active_object
    cam.data.lens = 45
    scene.camera = cam

    mock4_raw = CONCEPTS_DIR / "mock_04_raw.png"
    scene.render.filepath = str(mock4_raw)
    bpy.ops.render.render(write_still=True)

    im4 = Image.open(mock4_raw).convert("RGB")
    d4 = ImageDraw.Draw(im4)
    d4.rectangle([0, 0, 1280, 66], fill=(14, 12, 18))
    d4.line([(0, 66), (1280, 66)], fill=(235, 190, 80), width=2)
    d4.text((24, 14), "CONCEPT MOCK 04 • SHAOLIN KUNG FU (D1↔D2) & PANDA SANCTUARY + GHIGNA & PUPURABBU (E1↔E2)", fill=(255, 220, 115), font=get_font(20, bold=True))
    d4.text((24, 42), "Validated with Character Consistency Reference Photos • White Marble Body + Obsidian Back/Rim Sfumature + 3D Alphabet Badges", fill=(220, 225, 235), font=get_font(15))
    for p_out in [CONCEPTS_DIR / "mock_04_kungfu_panda_ghigna_pupurabbu_tiles.png", ARTIFACT_DIR / "mock_04_kungfu_panda_ghigna_pupurabbu_tiles.png"]:
        im4.save(p_out, "PNG")

    # =========================================================================
    # MOCK 1: 3D Chinese Temple Setting + Low Carved Rosewood/Jade Table on Sacred Stone Pavement (Imperial Turtle Track)
    # =========================================================================
    print("Rendering Mock 1 (3D Chinese Temple + Low Carved Table on Stone Pavement + Imperial Turtle Track)...")
    scene = setup_cycles_scene(1280, 720, samples=24)
    marble, obsidian, gold, rosewood, jade, pavement, crimson = make_pbr_materials()

    # Sacred Temple Flagstone Courtyard Pavement
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -1.05))
    pav = bpy.context.active_object
    pav.scale = (26.0, 26.0, 0.2)
    pav.data.materials.append(pavement)

    # Low Carved Rosewood Table + Celadon Jade Playfield Mat
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.52))
    tbl = bpy.context.active_object
    tbl.scale = (13.6, 9.6, 0.35)
    tbl.data.materials.append(rosewood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.32))
    jmat = bpy.context.active_object
    jmat.scale = (12.4, 8.4, 0.08)
    jmat.data.materials.append(jade)

    # 4 Crimson Temple Pillars + Gold Bases & Lanterns
    for px, py in [(-8.2, 6.2), (8.2, 6.2), (-9.5, -4.5), (9.5, -4.5)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=9.0, location=(px, py, 3.5))
        pil = bpy.context.active_object
        pil.data.materials.append(crimson)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.72, depth=0.45, location=(px, py, -0.75))
        base = bpy.context.active_object
        base.data.materials.append(gold)

    # Build 5-layer Imperial Turtle Pyramid on the Low Table
    layer_dims = [
        (0, 8, 6),
        (1, 6, 4),
        (2, 4, 3),
        (3, 2, 2),
        (4, 1, 1),
    ]
    idx = 0
    for z_layer, nx, ny in layer_dims:
        for ix in range(nx):
            for iy in range(ny):
                tx = (ix - (nx - 1) / 2.0) * 0.96
                ty = (iy - (ny - 1) / 2.0) * 1.26
                tz = z_layer * 0.66
                tpath = all_tex[idx % len(all_tex)]
                bcode = f"{chr(65 + (idx % 5))}{(idx % 2) + 1}"
                build_mahjong_tile_mesh(f"Turtle_{z_layer}_{ix}_{iy}", (tx, ty, tz), marble, obsidian, gold, tpath, bcode)
                idx += 1

    # Warm Golden-Hour Temple Lighting
    bpy.ops.object.light_add(type="SUN", location=(6.0, -8.0, 10.0), rotation=(0.65, 0.25, 0.4))
    sun = bpy.context.active_object
    sun.data.energy = 3.8
    sun.data.color = (1.0, 0.88, 0.68)

    bpy.ops.object.light_add(type="AREA", location=(0.0, -7.5, 6.5), rotation=(0.78, 0.0, 0.0))
    fill = bpy.context.active_object
    fill.data.energy = 450.0
    fill.data.size = 8.0
    fill.data.color = (1.0, 0.92, 0.80)

    bpy.ops.object.camera_add(location=(0.0, -10.8, 7.6), rotation=(0.86, 0.0, 0.0))
    cam = bpy.context.active_object
    cam.data.lens = 35
    scene.camera = cam

    mock1_raw = CONCEPTS_DIR / "mock_01_raw.png"
    scene.render.filepath = str(mock1_raw)
    bpy.ops.render.render(write_still=True)

    im1 = Image.open(mock1_raw).convert("RGB")
    d1 = ImageDraw.Draw(im1)
    d1.rectangle([0, 0, 1280, 68], fill=(14, 12, 18))
    d1.line([(0, 68), (1280, 68)], fill=(235, 190, 80), width=2)
    d1.text((24, 12), "CONCEPT MOCK 01 • 3D CHINESE TEMPLE & LOW CARVED ROSEWOOD/JADE TABLE ON STONE PAVEMENT", fill=(255, 220, 115), font=get_font(20, bold=True))
    d1.text((24, 42), "Master 5-Layer 'Imperial Turtle' Solitaire Track • White Marble Tiles with Black Obsidian & Gold Kintsugi Finiture", fill=(220, 225, 235), font=get_font(15))
    for p_out in [CONCEPTS_DIR / "mock_01_temple_imperial_turtle_track.png", ARTIFACT_DIR / "mock_01_temple_imperial_turtle_track.png"]:
        im1.save(p_out, "PNG")

    # =========================================================================
    # MOCK 2: 4 Multi-Difficulty Solitaire Track Layouts Blueprint Sheet
    # (1: Easy 36-Tile Lotus, 2: Medium 72-Tile Jade Pagoda, 3: Hard 108-Tile Twin Dragon Bridge, 4: Master 144-Tile Imperial Turtle)
    # =========================================================================
    print("Composing Mock 2 (4 Multi-Difficulty Track Blueprint Sheet)...")
    sheet = Image.new("RGB", (1280, 720), (16, 15, 22))
    ds = ImageDraw.Draw(sheet)
    ds.rectangle([0, 0, 1280, 64], fill=(12, 10, 16))
    ds.line([(0, 64), (1280, 64)], fill=(235, 190, 80), width=2)
    ds.text((24, 12), "CONCEPT MOCK 02 • 4 MULTI-DIFFICULTY SOLITAIRE TRACK LAYOUTS (100% REVERSE-PEEL SOLVABLE)", fill=(255, 220, 115), font=get_font(20, bold=True))
    ds.text((24, 40), "Switchable Surface: Low Carved Rosewood & Jade Table ↔ Direct Sacred Temple Stone Pavement", fill=(205, 215, 230), font=get_font(15))

    quads = [
        (20, 80, 625, 385, "1. EASY • LOTUS COURTYARD (36 Tiles / 18 Coupled Pairs)", "3 Layers • Blooming Lotus Formation • Kid-Friendly Quick Play", "lotus"),
        (655, 80, 1260, 385, "2. MEDIUM • JADE PAGODA (72 Tiles / 36 Coupled Pairs)", "4 Layers • Stepped Temple Pyramid • Balanced Tactical Depth", "pagoda"),
        (20, 400, 625, 705, "3. HARD • TWIN DRAGON BRIDGE (108 Tiles / 54 Coupled Pairs)", "5 Layers • Dual-Arch Span Connected by Bridge Crown", "bridge"),
        (655, 400, 1260, 705, "4. MASTER • IMPERIAL TURTLE (144 Tiles / 72 Coupled Pairs)", "5 Layers • Classic Full Mahjong Solitaire Citadel", "turtle"),
    ]
    layer_colors = [
        (235, 230, 218),  # Layer 0: White Marble base
        (242, 238, 226),  # Layer 1
        (248, 245, 235),  # Layer 2
        (252, 250, 242),  # Layer 3
        (255, 235, 175),  # Layer 4: Crown apex
    ]
    for x0, y0, x1, y1, title, sub, kind in quads:
        ds.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=(26, 24, 34), outline=(215, 175, 75), width=2)
        ds.text((x0 + 16, y0 + 12), title, fill=(255, 222, 120), font=get_font(16, bold=True))
        ds.text((x0 + 16, y0 + 34), sub, fill=(185, 195, 210), font=get_font(13))

        cx = (x0 + x1) // 2
        cy = (y0 + y1) // 2 + 22
        tw, th = 26, 34

        coords = []
        if kind == "lotus":
            for r in range(-2, 3):
                for c in range(-3, 4):
                    if abs(r) + abs(c) <= 4:
                        coords.append((c, r, 0))
                    if abs(r) + abs(c) <= 2:
                        coords.append((c, r, 1))
            coords.append((0, 0, 2))
        elif kind == "pagoda":
            for z, (rx, ry) in enumerate([(4, 2), (3, 2), (2, 1), (1, 1)]):
                for r in range(-ry, ry + 1):
                    for c in range(-rx, rx + 1):
                        coords.append((c, r, z))
        elif kind == "bridge":
            for c in range(-5, 6):
                for r in range(-2, 3):
                    if abs(c) >= 2 or abs(r) <= 1:
                        coords.append((c, r, 0))
                    if abs(c) in (2, 3, 4) and abs(r) <= 1:
                        coords.append((c, r, 1))
                    if abs(c) <= 2 and r == 0:
                        coords.append((c, r, 2))
                        coords.append((c, r, 3))
            coords.append((0, 0, 4))
        else:  # turtle
            for z, (rx, ry) in enumerate([(5, 3), (3, 2), (2, 1), (1, 1), (0, 0)]):
                for r in range(-ry, ry + 1):
                    for c in range(-rx, rx + 1):
                        coords.append((c, r, z))
            coords.extend([(-6, 0, 0), (6, 0, 0), (7, 0, 0)])

        coords.sort(key=lambda item: (item[2], item[1], item[0]))
        for c, r, z in coords:
            px = cx + c * (tw + 3) - z * 3
            py = cy + r * (th + 3) - z * 4
            # Obsidian shadow/finiture
            ds.rounded_rectangle([px - tw // 2 + 2, py - th // 2 + 3, px + tw // 2 + 2, py + th // 2 + 3], radius=4, fill=(18, 18, 24), outline=(215, 175, 70), width=1)
            # White Marble tile top
            ds.rounded_rectangle([px - tw // 2, py - th // 2, px + tw // 2, py + th // 2], radius=4, fill=layer_colors[min(z, 4)], outline=(40, 40, 52), width=1)
            # Gold corner alphabet dot
            ds.rectangle([px - tw // 2 + 3, py - th // 2 + 3, px - tw // 2 + 8, py - th // 2 + 8], fill=(225, 170, 45))

    for p_out in [CONCEPTS_DIR / "mock_02_four_difficulty_tracks_blueprint.png", ARTIFACT_DIR / "mock_02_four_difficulty_tracks_blueprint.png"]:
        sheet.save(p_out, "PNG")

    print("All 4 Blender Cycles & Family Reference Concept Mocks generated successfully!")


if __name__ == "__main__":
    generate_all()
