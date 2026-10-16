#!/usr/bin/env python3
"""
Headless Blender 5.0.1 — 3D Incandescent-Pen Carved Intaglio Showcase Builder & Cycles Macro Renderer.
Builds:
  1. public/models/tile_carved_intaglio_showcase.glb
     - 3 Showcase Tiles (`dots_2` 二筒, `dots_4` 四筒, `char_8` 八萬) with REAL 3D vertex-excavated grooves
       ('come se una penna incandescente avesse scavato il tile un pochettino, che si vede il buco bassorilievo ruotando')
  2. public/renders/cycles/cycles_cam5_carved_intaglio.png
     - Oblique raking-light Blender Cycles macro render proving the physical 3D carved cavities and enlarged motifs.
"""
import math
import shutil
from pathlib import Path
import numpy as np
from PIL import Image
import bpy
import bmesh
from mathutils import Euler, Vector

PROJECT_DIR = Path(__file__).resolve().parents[2]
MODELS_DIR = PROJECT_DIR / "public" / "models"
TEXTURES_DIR = PROJECT_DIR / "public" / "textures"
CYCLES_DIR = PROJECT_DIR / "public" / "renders" / "cycles"
ARTIFACT_DIR = Path("/Users/ricc/.gemini/antigravity/brain/9efaaa30-d5fa-49dc-b7c4-7292c03768b3")

TILE_W = 0.96
TILE_H = 1.28
TILE_D = 0.56


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_pbr_mat(name, base_color=(0.96, 0.94, 0.90, 1.0), roughness=0.15, metallic=0.0, tex_path=None, norm_path=None, norm_strength=1.45):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = base_color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    if tex_path and Path(tex_path).exists():
        tn = nodes.new("ShaderNodeTexImage")
        tn.image = bpy.data.images.load(str(tex_path), check_existing=True)
        links.new(tn.outputs["Color"], bsdf.inputs["Base Color"])

    if norm_path and Path(norm_path).exists():
        nn = nodes.new("ShaderNodeTexImage")
        nn.image = bpy.data.images.load(str(norm_path), check_existing=True)
        nn.image.colorspace_settings.name = "Non-Color"
        nm = nodes.new("ShaderNodeNormalMap")
        nm.inputs["Strength"].default_value = norm_strength
        links.new(nn.outputs["Color"], nm.inputs["Color"])
        links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])

    return mat


def build_displaced_carved_tile(tile_id: str, loc=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0), carve_depth_m: float = 0.088):
    """
    Builds a single closed manifold 3D Mahjong tile whose top face is a 84x112 grid
    physically excavated along Z using `public/textures/tiles_depth/{tile_id}_depth.png`!
    """
    depth_path = TEXTURES_DIR / "tiles_depth" / f"{tile_id}_depth.png"
    depth_im = Image.open(depth_path).convert("L")
    depth_np = np.asarray(depth_im, dtype=np.float32) / 255.0
    dh, dw = depth_np.shape

    marble_mat = make_pbr_mat(
        f"Marble_{tile_id}",
        roughness=0.14,
        tex_path=TEXTURES_DIR / "pbr" / "marble_basecolor_2k.png",
        norm_path=TEXTURES_DIR / "pbr" / "marble_normal_2k.png",
        norm_strength=0.22,
    )
    obsidian_mat = make_pbr_mat(
        f"Obsidian_{tile_id}",
        base_color=(0.05, 0.05, 0.07, 1.0),
        roughness=0.10,
        metallic=0.22,
        tex_path=TEXTURES_DIR / "pbr" / "obsidian_basecolor_2k.png",
    )
    face_mat = make_pbr_mat(
        f"CarvedFace_{tile_id}",
        roughness=0.16,
        metallic=0.08,
        tex_path=TEXTURES_DIR / "tiles" / f"{tile_id}.png",
        norm_path=TEXTURES_DIR / "tiles_normal" / f"{tile_id}_normal.png",
        norm_strength=1.55,
    )

    # Create a watertight subdivided box whose top (+Z) face has 120x160 subdivisions and is smoothly displaced by depth_np!
    bm = bmesh.new()
    nx, ny = 120, 160
    hw, hh, hd = TILE_W * 0.5, TILE_H * 0.5, TILE_D * 0.5

    top_verts = [[None] * (nx + 1) for _ in range(ny + 1)]
    bot_verts = [[None] * (nx + 1) for _ in range(ny + 1)]

    for j in range(ny + 1):
        v_norm = j / ny  # 0 at bottom (-hh), 1 at top (+hh)
        y = -hh + v_norm * TILE_H
        for i in range(nx + 1):
            u_norm = i / nx  # 0 at left (-hw), 1 at right (+hw)
            x = -hw + u_norm * TILE_W

            # Sample depth_np with bilinear interpolation and smooth border feathering
            if 2 <= i <= nx - 2 and 2 <= j <= ny - 2:
                fx = np.clip(u_norm * (dw - 1), 0.0, dw - 1.001)
                fy = np.clip((1.0 - v_norm) * (dh - 1), 0.0, dh - 1.001)
                x0, y0 = int(fx), int(fy)
                tx, ty = fx - x0, fy - y0
                d_val = float(
                    (1 - tx) * (1 - ty) * depth_np[y0, x0]
                    + tx * (1 - ty) * depth_np[y0, x0 + 1]
                    + (1 - tx) * ty * depth_np[y0 + 1, x0]
                    + tx * ty * depth_np[y0 + 1, x0 + 1]
                )
                dz = (d_val - 0.88) * carve_depth_m
            else:
                dz = 0.0

            top_verts[j][i] = bm.verts.new((x, y, hd + dz))
            bot_verts[j][i] = bm.verts.new((x, y, -hd))

    bm.verts.ensure_lookup_table()
    uv_layer = bm.loops.layers.uv.new("UVMap")

    # 1. Top Carved Face (+Z, material index 2 = face_mat)
    for j in range(ny):
        for i in range(nx):
            v00 = top_verts[j][i]
            v10 = top_verts[j][i + 1]
            v11 = top_verts[j + 1][i + 1]
            v01 = top_verts[j + 1][i]
            f = bm.faces.new((v00, v10, v11, v01))
            f.material_index = 2
            f.smooth = True
            coords = [(i / nx, j / ny), ((i + 1) / nx, j / ny), ((i + 1) / nx, (j + 1) / ny), (i / nx, (j + 1) / ny)]
            for loop, uv in zip(f.loops, coords):
                loop[uv_layer].uv = uv

    # 2. Bottom Obsidian Face (-Z, material index 1 = obsidian_mat)
    for j in range(ny):
        for i in range(nx):
            v00 = bot_verts[j][i]
            v01 = bot_verts[j + 1][i]
            v11 = bot_verts[j + 1][i + 1]
            v10 = bot_verts[j][i + 1]
            f = bm.faces.new((v00, v01, v11, v10))
            f.material_index = 1

    # 3. Four Perimeter Side Walls (material index 0 = marble_mat)
    for i in range(nx):
        f = bm.faces.new((bot_verts[0][i], bot_verts[0][i + 1], top_verts[0][i + 1], top_verts[0][i]))
        f.material_index = 0
    for i in range(nx):
        f = bm.faces.new((top_verts[ny][i], top_verts[ny][i + 1], bot_verts[ny][i + 1], bot_verts[ny][i]))
        f.material_index = 0
    for j in range(ny):
        f = bm.faces.new((bot_verts[j + 1][0], bot_verts[j][0], top_verts[j][0], top_verts[j + 1][0]))
        f.material_index = 0
    for j in range(ny):
        f = bm.faces.new((bot_verts[j][nx], bot_verts[j + 1][nx], top_verts[j + 1][nx], top_verts[j][nx]))
        f.material_index = 0

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    me = bpy.data.meshes.new(f"Carved_Tile_{tile_id}_Mesh")
    bm.to_mesh(me)
    bm.free()

    obj = bpy.data.objects.new(f"Carved_Tile_{tile_id}", me)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(marble_mat)
    obj.data.materials.append(obsidian_mat)
    obj.data.materials.append(face_mat)
    obj.location = Vector(loc)
    obj.rotation_euler = Euler(rot, "XYZ")
    return obj


def main():
    clear_scene()

    # Build Carved Rosewood & Jade Showcase Plinth
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, -0.42))
    plinth = bpy.context.active_object
    plinth.name = "Carved_Showcase_Plinth"
    plinth.scale = (3.8, 2.3, 0.16)
    bpy.ops.object.transform_apply(scale=True)
    plinth_mat = make_pbr_mat(
        "Rosewood_Plinth",
        base_color=(0.18, 0.06, 0.04, 1.0),
        roughness=0.22,
        tex_path=TEXTURES_DIR / "pbr" / "rosewood_basecolor_2k.png",
    )
    plinth.data.materials.append(plinth_mat)

    # Build 3 Showcase Tiles with Real 3D Excavated Grooves ('buco bassorilievo'):
    # 1. Left: dots_2 (2-Pallini enlarged + 3D carved)
    build_displaced_carved_tile(
        "dots_2",
        loc=(-1.12, 0.04, 0.05),
        rot=(math.radians(24), math.radians(15), math.radians(-6)),
        carve_depth_m=0.078,
    )
    # 2. Center Hero: dots_4 (4-Pallini enlarged + 3D carved, tilted toward raking light!)
    build_displaced_carved_tile(
        "dots_4",
        loc=(0.0, -0.10, 0.12),
        rot=(math.radians(30), math.radians(-12), math.radians(3)),
        carve_depth_m=0.082,
    )
    # 3. Right: char_8 (8-Characters +10% larger Hanzi + 3D carved)
    build_displaced_carved_tile(
        "char_8",
        loc=(1.12, 0.04, 0.05),
        rot=(math.radians(24), math.radians(-16), math.radians(6)),
        carve_depth_m=0.078,
    )

    # Export 3D Carved Intaglio Showcase GLB
    glb_path = MODELS_DIR / "tile_carved_intaglio_showcase.glb"
    bpy.ops.export_scene.gltf(
        filepath=str(glb_path),
        export_format="GLB",
        export_apply=True,
    )
    if ARTIFACT_DIR.exists():
        shutil.copy2(glb_path, ARTIFACT_DIR / "tile_carved_intaglio_showcase.glb")
    print(f"[Blender 3D Carving] Exported {glb_path} ({glb_path.stat().st_size / 1e6:.2f} MB)")

    # Setup Raking Incandescent Key Light + Fill Light + Camera for Cycles Ground-Truth Render
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720

    world = bpy.data.worlds.new("CarvedStudioWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.04, 0.03, 0.05, 1.0)
        bg.inputs["Strength"].default_value = 0.75

    # Raking incandescent gold sun/key light from low side angle to throw strong 3D shadows inside the carved holes!
    key_data = bpy.data.lights.new("Incandescent_Raking_Key", type="AREA")
    key_data.energy = 260.0
    key_data.color = (1.0, 0.85, 0.58)
    key_data.size = 1.8
    key_obj = bpy.data.objects.new("Incandescent_Raking_Key", key_data)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (2.8, -2.5, 1.40)
    direction = Vector((0.0, 0.0, 0.05)) - key_obj.location
    key_obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    # Cool rim light from opposite side
    rim_data = bpy.data.lights.new("Jade_Rim_Light", type="AREA")
    rim_data.energy = 120.0
    rim_data.color = (0.75, 0.88, 1.0)
    rim_data.size = 2.4
    rim_obj = bpy.data.objects.new("Jade_Rim_Light", rim_data)
    bpy.context.collection.objects.link(rim_obj)
    rim_obj.location = (-2.6, 1.8, 2.2)
    r_dir = Vector((0.0, 0.0, 0.05)) - rim_obj.location
    rim_obj.rotation_euler = r_dir.to_track_quat("-Z", "Y").to_euler()

    # Macro Camera framed to capture all 3 tilted 3D carved tiles completely
    cam_data = bpy.data.cameras.new("Cam5_Carved_Intaglio")
    cam_data.lens = 38.0
    cam_obj = bpy.data.objects.new("Cam5_Carved_Intaglio", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = (0.0, -3.55, 1.95)
    c_dir = Vector((0.0, -0.02, 0.04)) - cam_obj.location
    cam_obj.rotation_euler = c_dir.to_track_quat("-Z", "Y").to_euler()
    scene.camera = cam_obj

    out_png = CYCLES_DIR / "cycles_cam5_carved_intaglio.png"
    scene.render.filepath = str(out_png)
    bpy.ops.render.render(write_still=True)
    if ARTIFACT_DIR.exists():
        shutil.copy2(out_png, ARTIFACT_DIR / "cycles_cam5_carved_intaglio.png")
    print(f"[Blender Cycles] Rendered {out_png}")


if __name__ == "__main__":
    main()
