#!/usr/bin/env python3
"""
Milestone 2: Headless Blender 5.0.1 Asset, Rigging, Topology Audit & Cycles Master Render Pipeline.
Generates:
  1. public/models/tile_generic_white_marble_obsidian.glb
     - Canonical manifold 3D Mahjong tile (0.96m x 1.28m x 0.56m)
     - Creamy Imperial White Marble body + Volcanic Black Obsidian & Gold Kintsugi backing/finiture
     - Decoupled 2D Oval Cameo / Traditional Card Face Overlay + Bassorilievo normal map
     - Hierarchical 4-bone Armature (Root_Bone -> Tile_Body_Bone -> Face_Overlay_Bone + Alphabet_Glyph_Bone)
     - 4 baked NLA Animation Actions: Idle, Select, Pair, Disappear
  2. public/models/tile_coupled_showcase.glb
     - Auto-rotating showcase of Coupled Family Pairs (A1↔A2 Tang Silk, B1↔B2 Great Wall, C1↔C2 Cantonese Rice, H1↔H2 Mum & Dad)
  3. public/models/temple_environment.glb
     - 3D Chinese Temple Courtyard with Low Carved Rosewood/Jade Table + Sacred Flagstone Pavement + Crimson Pillars & Silk Lanterns
  4. public/models/topology_audit.json
     - BMesh manifold, UV, scale, and bone hierarchy verification report
  5. public/renders/cycles/cycles_cam1_hero.png .. cycles_cam4_tile_macro.png
     - Offline Blender Cycles path-traced master ground-truth renders from the 4 canonical camera angles
"""

import json
import math
from pathlib import Path
import bpy
import bmesh
from mathutils import Euler, Vector

PROJECT_DIR = Path(__file__).resolve().parents[2]
MODELS_DIR = PROJECT_DIR / "public" / "models"
TEXTURES_DIR = PROJECT_DIR / "public" / "textures"
CYCLES_DIR = PROJECT_DIR / "public" / "renders" / "cycles"
ARTIFACT_DIR = Path("/Users/ricc/.gemini/antigravity/brain/9efaaa30-d5fa-49dc-b7c4-7292c03768b3")

for d in [MODELS_DIR, CYCLES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Canonical Shared Tile Scale Contract (in Blender/Three.js scene units)
TILE_W = 0.96
TILE_H = 1.28
TILE_D = 0.56


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_pbr_material(
    name: str,
    base_color=(0.95, 0.93, 0.88, 1.0),
    roughness=0.15,
    metallic=0.0,
    coat_weight=0.25,
    emission_color=None,
    emission_strength=0.0,
    tex_path: Path | None = None,
    normal_path: Path | None = None,
    normal_strength: float = 0.35,
):
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
    if "Coat Weight" in bsdf.inputs:
        bsdf.inputs["Coat Weight"].default_value = coat_weight
    if emission_color and "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = emission_color
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    if tex_path and tex_path.exists():
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(str(tex_path), check_existing=True)
        links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])

    if normal_path and normal_path.exists():
        norm_tex = nodes.new("ShaderNodeTexImage")
        norm_tex.image = bpy.data.images.load(str(normal_path), check_existing=True)
        norm_tex.image.colorspace_settings.name = "Non-Color"
        norm_map = nodes.new("ShaderNodeNormalMap")
        norm_map.inputs["Strength"].default_value = normal_strength
        links.new(norm_tex.outputs["Color"], norm_map.inputs["Color"])
        links.new(norm_map.outputs["Normal"], bsdf.inputs["Normal"])

    return mat


def create_box_uv_unwrap(obj):
    """Assigns clean non-overlapping UVs to a mesh object, with planar top-face UVs on +Z faces."""
    me = obj.data
    if not me.uv_layers:
        me.uv_layers.new(name="UVMap")
    uv_layer = me.uv_layers.active.data

    bbox_min = Vector((min(v.co.x for v in me.vertices), min(v.co.y for v in me.vertices), min(v.co.z for v in me.vertices)))
    bbox_max = Vector((max(v.co.x for v in me.vertices), max(v.co.y for v in me.vertices), max(v.co.z for v in me.vertices)))
    span = Vector((max(1e-4, bbox_max.x - bbox_min.x), max(1e-4, bbox_max.y - bbox_min.y), max(1e-4, bbox_max.z - bbox_min.z)))

    for poly in me.polygons:
        n = poly.normal
        for loop_idx in poly.loop_indices:
            v = me.vertices[me.loops[loop_idx].vertex_index].co
            if abs(n.z) >= abs(n.x) and abs(n.z) >= abs(n.y):
                u = (v.x - bbox_min.x) / span.x
                v_coord = (v.y - bbox_min.y) / span.y
            elif abs(n.x) >= abs(n.y):
                u = (v.y - bbox_min.y) / span.y
                v_coord = (v.z - bbox_min.z) / span.z
            else:
                u = (v.x - bbox_min.x) / span.x
                v_coord = (v.z - bbox_min.z) / span.z
            uv_layer[loop_idx].uv = (u, v_coord)


def build_manifold_mahjong_tile_mesh(
    name_prefix: str,
    tile_id: str = "coupled_A1",
    marble_mat=None,
    obsidian_mat=None,
    gold_mat=None,
    bassorilievo_strength: float = 0.28,
):
    """
    Creates the 3 manifold mesh parts of a Canonical Mahjong Tile at world origin:
      1. Tile_Body_Mesh: Beveled White Imperial Marble body + Black Obsidian backing + Gold Kintsugi trim
      2. Face_Overlay_Mesh: Front face plane mapped to the 2D Oval Cameo / Traditional Mahjong card texture + normal map
      3. Alphabet_Glyph_Mesh: Raised 3D golden top-center crown inlay bar (never occluding top-left/top-right corner glyphs!)
    """
    if marble_mat is None:
        marble_mat = make_pbr_material(
            "Imperial_White_Marble",
            base_color=(0.96, 0.94, 0.90, 1.0),
            roughness=0.14,
            metallic=0.0,
            coat_weight=0.35,
            tex_path=TEXTURES_DIR / "pbr" / "marble_basecolor_2k.png",
            normal_path=TEXTURES_DIR / "pbr" / "marble_normal_2k.png",
            normal_strength=0.18,
        )
    if obsidian_mat is None:
        obsidian_mat = make_pbr_material(
            "Volcanic_Black_Obsidian",
            base_color=(0.05, 0.05, 0.07, 1.0),
            roughness=0.09,
            metallic=0.22,
            coat_weight=0.50,
            tex_path=TEXTURES_DIR / "pbr" / "obsidian_basecolor_2k.png",
            normal_path=TEXTURES_DIR / "pbr" / "obsidian_normal_2k.png",
            normal_strength=0.22,
        )
    if gold_mat is None:
        gold_mat = make_pbr_material(
            "Imperial_Gold_Kintsugi",
            base_color=(0.94, 0.78, 0.32, 1.0),
            roughness=0.18,
            metallic=0.92,
            coat_weight=0.25,
        )

    face_mat = make_pbr_material(
        f"TileFace_{tile_id}",
        base_color=(1.0, 1.0, 1.0, 1.0),
        roughness=0.16,
        metallic=0.02,
        coat_weight=0.30,
        tex_path=TEXTURES_DIR / "tiles" / f"{tile_id}.png",
        normal_path=TEXTURES_DIR / "tiles_normal" / f"{tile_id}_normal.png",
        normal_strength=bassorilievo_strength,
    )

    # 1. Tile_Body_Mesh (Manifold beveled block 0.96 x 1.28 x 0.56)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.0))
    body_obj = bpy.context.active_object
    body_obj.name = f"{name_prefix}_Body_Mesh"
    body_obj.scale = (TILE_W, TILE_H, TILE_D)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bevel = body_obj.modifiers.new(name="Bevel", type="BEVEL")
    bevel.width = 0.048
    bevel.segments = 3
    bevel.limit_method = "ANGLE"
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    bpy.ops.object.shade_smooth()

    body_obj.data.materials.append(marble_mat)    # slot 0: White Imperial Marble
    body_obj.data.materials.append(obsidian_mat)  # slot 1: Black Obsidian back & rim sfumature
    body_obj.data.materials.append(gold_mat)      # slot 2: Gold Kintsugi seam

    for poly in body_obj.data.polygons:
        zc = poly.center.z
        if zc < -TILE_D * 0.16:
            poly.material_index = 1  # Volcanic Black Obsidian backing
        elif -TILE_D * 0.16 <= zc <= -TILE_D * 0.08:
            poly.material_index = 2  # Gold Kintsugi waist seam
        else:
            poly.material_index = 0  # Creamy Imperial White Marble upper body
    create_box_uv_unwrap(body_obj)

    # 2. Face_Overlay_Mesh (Manifold thin beveled plaque on the top +Z face so all meshes are 100% closed manifold solids!)
    plaque_w = TILE_W * 0.89
    plaque_h = TILE_H * 0.91
    plaque_d = 0.012
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, TILE_D * 0.5 + plaque_d * 0.45))
    face_obj = bpy.context.active_object
    face_obj.name = f"{name_prefix}_Face_Overlay_Mesh"
    face_obj.scale = (plaque_w, plaque_h, plaque_d)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    face_obj.data.materials.append(face_mat)
    face_obj.data.materials.append(gold_mat)
    create_box_uv_unwrap(face_obj)
    for poly in face_obj.data.polygons:
        poly.material_index = 0 if poly.normal.z > 0.7 else 1

    # 3. Alphabet_Glyph_Mesh (Raised 3D top-center golden crown inlay bar between top-left & top-right corner glyphs)
    badge_w, badge_h, badge_d = 0.24, 0.032, 0.016
    bx = 0.0
    by = TILE_H * 0.422
    bz = TILE_D * 0.5 + plaque_d + badge_d * 0.45
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, bz))
    glyph_obj = bpy.context.active_object
    glyph_obj.name = f"{name_prefix}_Alphabet_Glyph_Mesh"
    glyph_obj.scale = (badge_w, badge_h, badge_d)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    g_bev = glyph_obj.modifiers.new(name="Bevel", type="BEVEL")
    g_bev.width = 0.004
    g_bev.segments = 2
    bpy.ops.object.modifier_apply(modifier=g_bev.name)
    glyph_obj.data.materials.append(gold_mat)
    glyph_obj.data.materials.append(obsidian_mat)
    for poly in glyph_obj.data.polygons:
        poly.material_index = 0 if poly.normal.z > 0.5 else 1
    create_box_uv_unwrap(glyph_obj)

    return body_obj, face_obj, glyph_obj


def rig_and_animate_canonical_tile(body_obj, face_obj, glyph_obj):
    """
    Creates the 4-bone hierarchical Armature:
      Root_Bone -> Tile_Body_Bone -> Face_Overlay_Bone + Alphabet_Glyph_Bone
    Binds the 3 meshes via vertex groups + Armature modifiers, and bakes 4 NLA Actions:
      Idle, Select, Pair, Disappear
    """
    bpy.ops.object.armature_add(enter_editmode=True, location=(0.0, 0.0, 0.0))
    arm_obj = bpy.context.active_object
    arm_obj.name = "MahjongTileRig"
    arm_data = arm_obj.data
    arm_data.name = "MahjongTileArmature"

    edit_bones = arm_data.edit_bones
    for b in list(edit_bones):
        edit_bones.remove(b)

    b_root = edit_bones.new("Root_Bone")
    b_root.head = (0.0, 0.0, -TILE_D * 0.5)
    b_root.tail = (0.0, 0.0, 0.0)

    b_body = edit_bones.new("Tile_Body_Bone")
    b_body.head = (0.0, 0.0, 0.0)
    b_body.tail = (0.0, 0.0, TILE_D * 0.5)
    b_body.parent = b_root

    b_face = edit_bones.new("Face_Overlay_Bone")
    b_face.head = (0.0, 0.0, TILE_D * 0.5)
    b_face.tail = (0.0, 0.0, TILE_D * 0.5 + 0.12)
    b_face.parent = b_body

    b_glyph = edit_bones.new("Alphabet_Glyph_Bone")
    b_glyph.head = (0.0, TILE_H * 0.422, TILE_D * 0.5 + 0.01)
    b_glyph.tail = (0.0, TILE_H * 0.422, TILE_D * 0.5 + 0.15)
    b_glyph.parent = b_body

    bpy.ops.object.mode_set(mode="OBJECT")

    # Bind each mesh to its dedicated bone via 1.0 weight vertex group + Armature modifier
    bindings = [
        (body_obj, "Tile_Body_Bone"),
        (face_obj, "Face_Overlay_Bone"),
        (glyph_obj, "Alphabet_Glyph_Bone"),
    ]
    for mesh_obj, bone_name in bindings:
        mesh_obj.parent = arm_obj
        for bname in ["Root_Bone", "Tile_Body_Bone", "Face_Overlay_Bone", "Alphabet_Glyph_Bone"]:
            vg = mesh_obj.vertex_groups.new(name=bname)
            if bname == bone_name:
                vg.add(list(range(len(mesh_obj.data.vertices))), 1.0, "REPLACE")
        mod = mesh_obj.modifiers.new(name="Armature", type="ARMATURE")
        mod.object = arm_obj

    # Bake 4 Animation Actions onto Pose Bones
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode="POSE")
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = "XYZ"

    pb_root = arm_obj.pose.bones["Root_Bone"]
    pb_body = arm_obj.pose.bones["Tile_Body_Bone"]
    pb_face = arm_obj.pose.bones["Face_Overlay_Bone"]
    pb_glyph = arm_obj.pose.bones["Alphabet_Glyph_Bone"]

    def reset_pose():
        for pb in [pb_root, pb_body, pb_face, pb_glyph]:
            pb.location = (0.0, 0.0, 0.0)
            pb.rotation_euler = (0.0, 0.0, 0.0)
            pb.scale = (1.0, 1.0, 1.0)

    def key_all(frame: int):
        for pb in [pb_root, pb_body, pb_face, pb_glyph]:
            pb.keyframe_insert(data_path="location", frame=frame)
            pb.keyframe_insert(data_path="rotation_euler", frame=frame)
            pb.keyframe_insert(data_path="scale", frame=frame)

    if not arm_obj.animation_data:
        arm_obj.animation_data_create()

    # Action 1: Idle (60 frames subtle breathing & glyph shimmer)
    act_idle = bpy.data.actions.new(name="Idle")
    arm_obj.animation_data.action = act_idle
    reset_pose()
    key_all(1)
    pb_body.location = (0.0, 0.0, 0.025)
    pb_body.rotation_euler = (0.015, -0.015, 0.0)
    pb_glyph.location = (0.0, 0.0, 0.012)
    key_all(30)
    reset_pose()
    key_all(60)

    # Action 2: Select (60 frames hover lift + tilt toward camera + corner badge pop)
    act_select = bpy.data.actions.new(name="Select")
    arm_obj.animation_data.action = act_select
    reset_pose()
    key_all(1)
    pb_root.location = (0.0, 0.0, 0.34)
    pb_body.rotation_euler = (math.radians(12.0), 0.0, math.radians(3.0))
    pb_face.location = (0.0, 0.0, 0.015)
    pb_glyph.location = (0.0, 0.0, 0.045)
    pb_glyph.scale = (1.15, 1.15, 1.15)
    key_all(25)
    pb_root.location = (0.0, 0.0, 0.30)
    pb_body.rotation_euler = (math.radians(10.0), 0.0, math.radians(-2.0))
    key_all(45)
    reset_pose()
    key_all(60)

    # Action 3: Pair (60 frames celebratory coupled match arc + 360 spin)
    act_pair = bpy.data.actions.new(name="Pair")
    arm_obj.animation_data.action = act_pair
    reset_pose()
    key_all(1)
    pb_root.location = (0.0, 0.0, 0.65)
    pb_body.rotation_euler = (math.radians(18.0), 0.0, math.radians(180.0))
    pb_glyph.location = (0.0, 0.0, 0.06)
    pb_glyph.scale = (1.25, 1.25, 1.25)
    key_all(30)
    pb_root.location = (0.0, 0.0, 0.0)
    pb_body.rotation_euler = (0.0, 0.0, math.radians(360.0))
    pb_glyph.location = (0.0, 0.0, 0.0)
    pb_glyph.scale = (1.0, 1.0, 1.0)
    key_all(60)

    # Action 4: Disappear (60 frames implosive spiral vanish after pair match)
    act_disappear = bpy.data.actions.new(name="Disappear")
    arm_obj.animation_data.action = act_disappear
    reset_pose()
    key_all(1)
    pb_root.location = (0.0, 0.0, 0.45)
    pb_body.rotation_euler = (math.radians(25.0), math.radians(15.0), math.radians(120.0))
    pb_body.scale = (1.08, 1.08, 1.08)
    key_all(18)
    pb_root.location = (0.0, 0.0, 1.10)
    pb_body.rotation_euler = (math.radians(55.0), math.radians(-35.0), math.radians(540.0))
    pb_body.scale = (0.02, 0.02, 0.02)
    pb_face.scale = (0.02, 0.02, 0.02)
    pb_glyph.scale = (0.02, 0.02, 0.02)
    key_all(60)

    # Push all 4 actions to NLA tracks so glTF exporter includes all 4 animations
    reset_pose()
    for act in [act_idle, act_select, act_pair, act_disappear]:
        track = arm_obj.animation_data.nla_tracks.new()
        track.name = act.name
        strip = track.strips.new(act.name, 1, act)
        strip.name = act.name

    arm_obj.animation_data.action = act_idle
    bpy.ops.object.mode_set(mode="OBJECT")
    return arm_obj


def audit_current_scene_meshes(asset_name: str) -> dict:
    """Runs BMesh manifold, degenerate face, UV, scale, and bone hierarchy audit on the active scene."""
    mesh_reports = []
    total_verts = 0
    total_faces = 0
    total_non_manifold = 0
    total_degenerate = 0

    for obj in bpy.data.objects:
        if obj.type == "MESH":
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            bm.edges.ensure_lookup_table()
            bm.faces.ensure_lookup_table()
            non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
            degenerate = sum(1 for f in bm.faces if f.calc_area() < 1e-8)
            loose_verts = sum(1 for v in bm.verts if len(v.link_edges) == 0)
            verts = len(bm.verts)
            faces = len(bm.faces)
            bm.free()

            scale_ok = all(abs(s - 1.0) < 1e-4 for s in obj.scale)
            has_uv = len(obj.data.uv_layers) > 0
            total_verts += verts
            total_faces += faces
            total_non_manifold += non_manifold
            total_degenerate += degenerate
            mesh_reports.append({
                "mesh": obj.name,
                "vertices": verts,
                "faces": faces,
                "nonManifoldEdges": non_manifold,
                "degenerateFaces": degenerate,
                "looseVertices": loose_verts,
                "uvLayerPresent": has_uv,
                "unitScaleApplied": scale_ok,
            })

    armatures = [obj for obj in bpy.data.objects if obj.type == "ARMATURE"]
    bones = [b.name for arm in armatures for b in arm.data.bones]
    actions = [a.name for a in bpy.data.actions]

    return {
        "asset": asset_name,
        "meshCount": len(mesh_reports),
        "totalVertices": total_verts,
        "totalFaces": total_faces,
        "totalNonManifoldEdges": total_non_manifold,
        "totalDegenerateFaces": total_degenerate,
        "manifoldPass": total_non_manifold == 0 and total_degenerate == 0,
        "bones": bones,
        "actions": actions,
        "meshes": mesh_reports,
    }


def export_canonical_generic_tile_glb() -> dict:
    print("[Blender] Building & Rigging Canonical Generic Mahjong Tile GLB...")
    clear_scene()
    body_obj, face_obj, glyph_obj = build_manifold_mahjong_tile_mesh("CanonicalTile", tile_id="coupled_A1", bassorilievo_strength=0.30)
    rig_and_animate_canonical_tile(body_obj, face_obj, glyph_obj)
    report = audit_current_scene_meshes("tile_generic_white_marble_obsidian.glb")

    out_path = MODELS_DIR / "tile_generic_white_marble_obsidian.glb"
    bpy.ops.export_scene.gltf(
        filepath=str(out_path),
        export_format="GLB",
        export_apply=False,
        export_animations=True,
        export_nla_strips=True,
    )
    if ARTIFACT_DIR.exists():
        (ARTIFACT_DIR / out_path.name).write_bytes(out_path.read_bytes())
    print(f"[Blender] Exported {out_path.name} ({out_path.stat().st_size // 1024} KB)")
    return report


def export_coupled_showcase_glb() -> dict:
    print("[Blender] Building Coupled Family Quartets & Diptyque Pairs Showcase GLB (S1..S4, M1..M2, E1↔E2)...")
    clear_scene()

    # Rosewood & Celadon Jade display plinth
    rosewood_mat = make_pbr_material(
        "Showcase_Rosewood",
        base_color=(0.24, 0.08, 0.05, 1.0),
        roughness=0.22,
        tex_path=TEXTURES_DIR / "pbr" / "rosewood_basecolor_2k.png",
    )
    jade_mat = make_pbr_material(
        "Showcase_Jade",
        base_color=(0.35, 0.56, 0.44, 1.0),
        roughness=0.18,
        tex_path=TEXTURES_DIR / "pbr" / "jade_basecolor_2k.png",
    )

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, -0.42))
    plinth = bpy.context.active_object
    plinth.name = "Rosewood_Jade_Plinth"
    plinth.scale = (9.6, 2.4, 0.28)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bev = plinth.modifiers.new(name="Bevel", type="BEVEL")
    bev.width = 0.04
    bev.segments = 2
    bpy.ops.object.modifier_apply(modifier=bev.name)
    plinth.data.materials.append(rosewood_mat)
    plinth.data.materials.append(jade_mat)
    for poly in plinth.data.polygons:
        poly.material_index = 1 if poly.normal.z > 0.7 else 0
    create_box_uv_unwrap(plinth)

    showcase_tiles = [
        ("coupled_A1", -3.9, 0.0),
        ("coupled_A2", -2.8, 0.0),
        ("coupled_B1", -1.4, 0.0),
        ("coupled_B2", -0.3, 0.0),
        ("coupled_C1", 1.1, 0.0),
        ("coupled_C2", 2.2, 0.0),
        ("coupled_E1", 3.5, 0.0),
        ("coupled_E2", 4.6, 0.0),
    ]
    for tid, x_pos, y_pos in showcase_tiles:
        b, f, g = build_manifold_mahjong_tile_mesh(f"Show_{tid}", tile_id=tid, bassorilievo_strength=0.32)
        for part in (b, f, g):
            part.location.x += x_pos - 0.35
            part.location.y += y_pos
            part.rotation_euler = (math.radians(58.0), 0.0, 0.0)
            bpy.context.view_layer.objects.active = part
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    report = audit_current_scene_meshes("tile_coupled_showcase.glb")
    out_path = MODELS_DIR / "tile_coupled_showcase.glb"
    bpy.ops.export_scene.gltf(filepath=str(out_path), export_format="GLB", export_apply=True)
    if ARTIFACT_DIR.exists():
        (ARTIFACT_DIR / out_path.name).write_bytes(out_path.read_bytes())
    print(f"[Blender] Exported {out_path.name} ({out_path.stat().st_size // 1024} KB)")
    return report


def build_temple_environment_objects():
    """Builds the 3D Chinese Temple Courtyard, Sacred Stone Pavement, and Low Carved Rosewood & Jade Table."""
    pavement_mat = make_pbr_material(
        "Sacred_Temple_Stone_Pavement",
        base_color=(0.30, 0.29, 0.27, 1.0),
        roughness=0.68,
        metallic=0.02,
        coat_weight=0.05,
        tex_path=TEXTURES_DIR / "pbr" / "pavement_basecolor_2k.png",
        normal_path=TEXTURES_DIR / "pbr" / "pavement_normal_2k.png",
        normal_strength=0.45,
    )
    rosewood_mat = make_pbr_material(
        "Carved_Imperial_Rosewood",
        base_color=(0.24, 0.07, 0.05, 1.0),
        roughness=0.22,
        metallic=0.04,
        coat_weight=0.40,
        tex_path=TEXTURES_DIR / "pbr" / "rosewood_basecolor_2k.png",
    )
    jade_mat = make_pbr_material(
        "Celadon_Jade_Table_Mat",
        base_color=(0.32, 0.52, 0.41, 1.0),
        roughness=0.20,
        metallic=0.02,
        coat_weight=0.35,
        tex_path=TEXTURES_DIR / "pbr" / "jade_basecolor_2k.png",
    )
    crimson_mat = make_pbr_material(
        "Crimson_Temple_Lacquer",
        base_color=(0.56, 0.07, 0.06, 1.0),
        roughness=0.20,
        metallic=0.05,
        coat_weight=0.45,
    )
    gold_mat = make_pbr_material(
        "Temple_Gilded_Bronze",
        base_color=(0.90, 0.72, 0.25, 1.0),
        roughness=0.22,
        metallic=0.88,
        coat_weight=0.25,
    )
    lantern_mat = make_pbr_material(
        "Warm_Silk_Lantern",
        base_color=(0.98, 0.36, 0.12, 1.0),
        roughness=0.35,
        emission_color=(1.0, 0.45, 0.14, 1.0),
        emission_strength=3.5,
    )

    # 1. Sacred Temple Stone Pavement Floor (z top at -0.45)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, -0.70))
    pavement = bpy.context.active_object
    pavement.name = "Temple_Stone_Pavement"
    pavement.scale = (28.0, 24.0, 0.50)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    pavement.data.materials.append(pavement_mat)
    create_box_uv_unwrap(pavement)

    # 2. Low Carved Rosewood & Celadon Jade Table (z top at 0.0, resting on pavement at -0.45)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, -0.14))
    table_top = bpy.context.active_object
    table_top.name = "Low_Rosewood_Jade_Table"
    table_top.scale = (14.8, 10.6, 0.28)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    t_bev = table_top.modifiers.new(name="Bevel", type="BEVEL")
    t_bev.width = 0.05
    t_bev.segments = 3
    bpy.ops.object.modifier_apply(modifier=t_bev.name)
    table_top.data.materials.append(rosewood_mat)
    table_top.data.materials.append(jade_mat)
    table_top.data.materials.append(gold_mat)
    for poly in table_top.data.polygons:
        if poly.normal.z > 0.85:
            poly.material_index = 1  # Celadon Jade playing surface
        elif abs(poly.center.z - (-0.02)) < 0.04:
            poly.material_index = 2  # Gold trim
        else:
            poly.material_index = 0  # Carved Rosewood frame
    create_box_uv_unwrap(table_top)

    # 4 Carved Rosewood Table Legs
    leg_coords = [(-6.6, -4.6), (6.6, -4.6), (-6.6, 4.6), (6.6, 4.6)]
    for idx, (lx, ly) in enumerate(leg_coords):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, -0.36))
        leg = bpy.context.active_object
        leg.name = f"Rosewood_Table_Leg_{idx+1}"
        leg.scale = (0.65, 0.65, 0.22)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        leg.data.materials.append(rosewood_mat)
        create_box_uv_unwrap(leg)

    # 3. Four Crimson Temple Dragon Pillars + Stone Plinths + Glowing Silk Lanterns
    pillar_coords = [(-10.2, -7.2), (10.2, -7.2), (-10.2, 7.2), (10.2, 7.2)]
    for idx, (px, py) in enumerate(pillar_coords):
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.62, depth=7.5, location=(px, py, 3.3))
        pil = bpy.context.active_object
        pil.name = f"Temple_Crimson_Pillar_{idx+1}"
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        pil.data.materials.append(crimson_mat)
        pil.data.materials.append(gold_mat)
        for poly in pil.data.polygons:
            if poly.center.z < 0.2 or poly.center.z > 6.4:
                poly.material_index = 1
        create_box_uv_unwrap(pil)

        # Hanging Silk Lantern inward from each pillar
        lx = px * 0.78
        ly = py * 0.78
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=0.48, location=(lx, ly, 4.4))
        lant = bpy.context.active_object
        lant.name = f"Temple_Silk_Lantern_{idx+1}"
        lant.scale = (1.0, 1.0, 1.25)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        lant.data.materials.append(lantern_mat)
        create_box_uv_unwrap(lant)


def export_temple_environment_glb() -> dict:
    print("[Blender] Building & Exporting 3D Chinese Temple Environment GLB...")
    clear_scene()
    build_temple_environment_objects()
    report = audit_current_scene_meshes("temple_environment.glb")
    out_path = MODELS_DIR / "temple_environment.glb"
    bpy.ops.export_scene.gltf(filepath=str(out_path), export_format="GLB", export_apply=True)
    if ARTIFACT_DIR.exists():
        (ARTIFACT_DIR / out_path.name).write_bytes(out_path.read_bytes())
    print(f"[Blender] Exported {out_path.name} ({out_path.stat().st_size // 1024} KB)")
    return report


def render_cycles_ground_truth_suite():
    """
    Renders the 4 Offline Blender Cycles Master Ground-Truth Images from the 4 canonical camera angles:
      1. cycles_cam1_hero.png (Hero 3/4 Temple & Imperial Turtle Track)
      2. cycles_cam2_topdown.png (Top-Down Solitaire Zen View)
      3. cycles_cam3_low_pavement.png (Low Pavement & Rosewood Table Closeup)
      4. cycles_cam4_tile_macro.png (Macro Coupled Family Oval Medallion & Bassorilievo)
    """
    print("[Cycles] Building Full Temple + Imperial Turtle Solitaire Scene for Offline Cycles Ground Truth...")
    clear_scene()
    build_temple_environment_objects()

    marble_mat = make_pbr_material(
        "Cycles_White_Marble",
        base_color=(0.96, 0.94, 0.90, 1.0),
        roughness=0.14,
        coat_weight=0.35,
        tex_path=TEXTURES_DIR / "pbr" / "marble_basecolor_2k.png",
        normal_path=TEXTURES_DIR / "pbr" / "marble_normal_2k.png",
        normal_strength=0.18,
    )
    obsidian_mat = make_pbr_material(
        "Cycles_Black_Obsidian",
        base_color=(0.05, 0.05, 0.07, 1.0),
        roughness=0.09,
        metallic=0.22,
        coat_weight=0.50,
        tex_path=TEXTURES_DIR / "pbr" / "obsidian_basecolor_2k.png",
        normal_path=TEXTURES_DIR / "pbr" / "obsidian_normal_2k.png",
        normal_strength=0.22,
    )
    gold_mat = make_pbr_material(
        "Cycles_Gold_Kintsugi",
        base_color=(0.94, 0.78, 0.32, 1.0),
        roughness=0.18,
        metallic=0.92,
        coat_weight=0.25,
    )

    # Curated deck of Coupled Family Oval tiles + Traditional Mahjong Suits for the 4-layer Pyramid
    deck = [
        "coupled_A1", "coupled_A2", "coupled_B1", "coupled_B2",
        "coupled_C1", "coupled_C2", "coupled_D1", "coupled_D2",
        "coupled_E1", "coupled_E2", "coupled_F1", "coupled_F2",
        "coupled_G1", "coupled_G2", "coupled_H1", "coupled_H2",
        "char_1", "char_9", "dots_5", "dots_8", "bamboo_1", "bamboo_8",
        "wind_E", "wind_S", "dragon_red", "dragon_green", "dragon_white",
    ]

    # Build a template mesh per unique tile_id in `deck` and instance it across the 4-layer Imperial Turtle layout
    templates = {}
    for tid in deck:
        b, f, g = build_manifold_mahjong_tile_mesh(
            f"Tpl_{tid}",
            tile_id=tid,
            marble_mat=marble_mat,
            obsidian_mat=obsidian_mat,
            gold_mat=gold_mat,
            bassorilievo_strength=0.30,
        )
        # Join the 3 parts into a single render mesh for fast instancing in Cycles
        bpy.ops.object.select_all(action="DESELECT")
        b.select_set(True)
        f.select_set(True)
        g.select_set(True)
        bpy.context.view_layer.objects.active = b
        bpy.ops.object.join()
        b.location = (0, 0, -50)  # Park template out of view
        templates[tid] = b

    # Place tiles in a 4-layer Imperial Turtle Solitaire formation on the table (z base = TILE_D * 0.5)
    layers = [
        # (layer_z_index, cols, rows)
        (0, 8, 5),
        (1, 6, 4),
        (2, 4, 2),
        (3, 2, 1),
    ]
    tile_counter = 0
    sx = TILE_W * 1.04
    sy = TILE_H * 1.04
    sz = TILE_D * 1.02

    for l_idx, cols, rows in layers:
        for r in range(rows):
            for c in range(cols):
                tid = deck[tile_counter % len(deck)]
                tile_counter += 1
                tpl = templates[tid]
                inst = tpl.copy()
                bpy.context.collection.objects.link(inst)
                x = (c - (cols - 1) / 2.0) * sx
                y = (r - (rows - 1) / 2.0) * sy
                z = TILE_D * 0.5 + l_idx * sz
                inst.location = (x, y, z)

    # Place the complete Carlesso Family Seasons Quartet (S1 Papà, S2 Mamma, S3 Ale, S4 Sebi) at the front edge for macro inspection
    front_showcase = [
        ("coupled_A1", -1.65, -3.75, TILE_D * 0.5, math.radians(18.0)),
        ("coupled_A2", -0.58, -3.75, TILE_D * 0.5, math.radians(18.0)),
        ("coupled_B1", 0.58, -3.75, TILE_D * 0.5, math.radians(18.0)),
        ("coupled_B2", 1.65, -3.75, TILE_D * 0.5, math.radians(18.0)),
    ]
    for tid, fx, fy, fz, tilt_x in front_showcase:
        inst = templates[tid].copy()
        bpy.context.collection.objects.link(inst)
        inst.location = (fx, fy, fz + 0.08)
        inst.rotation_euler = (tilt_x, 0.0, 0.0)

    # Lighting matching our WebGL Studio defaults
    world = bpy.data.worlds.new("TempleGoldenHourWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.14, 0.10, 0.09, 1.0)
        bg.inputs["Strength"].default_value = 1.15

    # Warm Golden-Hour Sun Light
    bpy.ops.object.light_add(type="SUN", location=(8.0, -9.0, 11.0))
    sun = bpy.context.active_object
    sun.name = "Temple_Golden_Sun"
    sun.data.energy = 3.8
    sun.data.color = (1.0, 0.91, 0.78)
    sun.data.angle = math.radians(8.0)
    sun.rotation_euler = (math.radians(46.0), math.radians(18.0), math.radians(32.0))

    # Warm Silk Lantern Point/Area Fill
    bpy.ops.object.light_add(type="AREA", location=(-4.5, -5.0, 5.5))
    fill = bpy.context.active_object
    fill.name = "Lantern_Warm_Fill"
    fill.data.energy = 260.0
    fill.data.size = 4.5
    fill.data.color = (1.0, 0.72, 0.45)
    fill.rotation_euler = (math.radians(42.0), 0.0, math.radians(-35.0))

    # Cool Jade Sky Rim Light
    bpy.ops.object.light_add(type="AREA", location=(0.0, 7.5, 6.0))
    rim = bpy.context.active_object
    rim.name = "Sky_Jade_Rim"
    rim.data.energy = 180.0
    rim.data.size = 6.0
    rim.data.color = (0.78, 0.90, 1.0)
    rim.rotation_euler = (math.radians(-48.0), 0.0, 0.0)

    # Configure Cycles
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 28
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = "PNG"

    bpy.ops.object.camera_add()
    cam = bpy.context.active_object
    scene.camera = cam

    def aim_camera(pos: tuple, target: tuple, lens_mm: float = 42.0):
        cam.location = Vector(pos)
        direction = Vector(target) - cam.location
        rot_quat = direction.to_track_quat("-Z", "Y")
        cam.rotation_euler = rot_quat.to_euler()
        cam.data.lens = lens_mm

    cameras = [
        ("cycles_cam1_hero.png", (0.0, -9.6, 6.4), (0.0, -0.3, 0.8), 38.0),
        ("cycles_cam2_topdown.png", (0.0, -0.8, 10.2), (0.0, -0.2, 0.6), 40.0),
        ("cycles_cam3_low_pavement.png", (5.4, -7.8, 2.2), (0.0, -1.2, 0.4), 36.0),
        ("cycles_cam4_tile_macro.png", (0.0, -5.8, 1.95), (0.0, -3.65, 0.35), 48.0),
    ]

    for fname, pos, tgt, lens in cameras:
        aim_camera(pos, tgt, lens)
        out_file = CYCLES_DIR / fname
        scene.render.filepath = str(out_file)
        print(f"[Cycles] Rendering {fname}...")
        bpy.ops.render.render(write_still=True)
        # Also copy to Artifact dir so it can be embedded directly in Markdown artifacts
        if ARTIFACT_DIR.exists():
            (ARTIFACT_DIR / fname).write_bytes(out_file.read_bytes())


def main():
    rep_tile = export_canonical_generic_tile_glb()
    rep_show = export_coupled_showcase_glb()
    rep_env = export_temple_environment_glb()

    audit_summary = {
        "blenderVersion": bpy.app.version_string,
        "allManifoldPass": rep_tile["manifoldPass"] and rep_show["manifoldPass"] and rep_env["manifoldPass"],
        "assets": [rep_tile, rep_show, rep_env],
    }
    audit_path = MODELS_DIR / "topology_audit.json"
    audit_path.write_text(json.dumps(audit_summary, indent=2))
    print(f"[TopologyAudit] Saved {audit_path} (allManifoldPass={audit_summary['allManifoldPass']})")

    render_cycles_ground_truth_suite()
    print("[Done] Milestone 2 Headless Blender 5.0.1 Pipeline Complete!")


if __name__ == "__main__":
    main()
