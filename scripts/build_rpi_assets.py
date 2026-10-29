#!/usr/bin/env python3
"""
🍓 Build "Qualità Raspberry / Sguisatazzo Mode" Low-Spec 3D GLB & Texture Assets (`scripts/build_rpi_assets.py`)
Target Hardware: Alessandro's Raspberry Pi 400 Rev 1.0 (`Sguisatazzo` / ex `ghigna`)
- CPU: Broadcom BCM2711 Quad-Core Cortex-A72 @ 1.80 GHz (1 MiB shared L2 cache)
- RAM: 4 GB LPDDR4-3200 (~2.8 GiB MemAvailable, Chromium `--enable-low-end-device-mode`)
- GPU: Broadcom V3D 4.2 (VideoCore VI @ 500 MHz), 1920x1080 @ 60Hz GWD ARZOPA Monitor

Produces:
1. `public/models/*_rpi.glb`:
   Re-packs all 4 canonical `.glb` files with downscaled Raspberry-quality embedded textures
   (128x128 for PBR/environment maps, 192x256 for showcase tile faces, 0% normal-map bloat)
   while preserving 100% manifold geometry, node hierarchy, bones, and animations.
2. `public/textures/tiles_rpi/*.png`:
   256x342 crisp Lanczos-downscaled 8-bit quantized tile textures (9x fewer pixels than 768x1024).
3. `public/textures/pbr_rpi/*.png`:
   256x256 lightweight PBR basecolor textures (64x fewer pixels than 2048x2048).
"""

import io
import json
import struct
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / "public" / "models"
TILES_DIR = ROOT / "public" / "textures" / "tiles"
TILES_ONIRICA_DIR = ROOT / "public" / "textures" / "tiles_onirica"
PBR_DIR = ROOT / "public" / "textures" / "pbr"

TILES_RPI_DIR = ROOT / "public" / "textures" / "tiles_rpi"
TILES_ONIRICA_RPI_DIR = ROOT / "public" / "textures" / "tiles_onirica_rpi"
PBR_RPI_DIR = ROOT / "public" / "textures" / "pbr_rpi"


def pad4(data: bytes, pad_byte: bytes = b"\x00") -> bytes:
    rem = len(data) % 4
    return data if rem == 0 else data + pad_byte * (4 - rem)


def repack_glb_for_rpi(src_glb: Path, dst_glb: Path, max_tex_dim: int = 128, jpeg_quality: int = 72) -> tuple[int, int]:
    """
    Parses a glTF 2.0 binary (.glb), downscales all embedded image bufferViews to `max_tex_dim`
    (encoding opaque textures as compact baseline JPEG and alpha textures as quantized 8-bit PNG),
    updates bufferView byteOffsets/byteLengths with strict 4-byte alignment, and writes `dst_glb`.
    """
    raw = src_glb.read_bytes()
    magic, version, total_len = struct.unpack_from("<III", raw, 0)
    if magic != 0x46546C67:
        raise ValueError(f"{src_glb} is not a valid GLB file")

    json_len, json_type = struct.unpack_from("<II", raw, 12)
    json_bytes = raw[20 : 20 + json_len]
    gltf = json.loads(json_bytes.decode("utf-8"))

    bin_chunk_offset = 20 + json_len
    bin_len, bin_type = struct.unpack_from("<II", raw, bin_chunk_offset)
    bin_data = raw[bin_chunk_offset + 8 : bin_chunk_offset + 8 + bin_len]

    # Map bufferView index -> image object(s)
    image_bv_map: dict[int, list[dict]] = {}
    for img_obj in gltf.get("images", []):
        bv_idx = img_obj.get("bufferView")
        if bv_idx is not None:
            image_bv_map.setdefault(bv_idx, []).append(img_obj)

    new_bin = bytearray()
    for bv_idx, bv in enumerate(gltf.get("bufferViews", [])):
        old_offset = bv.get("byteOffset", 0)
        old_length = bv["byteLength"]
        chunk = bin_data[old_offset : old_offset + old_length]

        if bv_idx in image_bv_map:
            try:
                with Image.open(io.BytesIO(chunk)) as im:
                    w, h = im.size
                    scale = min(1.0, max_tex_dim / float(max(w, h)))
                    nw = max(16, int(round(w * scale)))
                    nh = max(16, int(round(h * scale)))
                    im_resized = im.resize((nw, nh), Image.Resampling.LANCZOS)

                    out_buf = io.BytesIO()
                    has_alpha = im_resized.mode in ("RGBA", "LA") or (
                        im_resized.mode == "P" and "transparency" in im_resized.info
                    )
                    if has_alpha:
                        im_q = im_resized.convert("RGBA").quantize(colors=128, method=Image.Quantize.FASTOCTREE)
                        im_q.save(out_buf, format="PNG", optimize=True)
                        new_mime = "image/png"
                    else:
                        im_resized.convert("RGB").save(out_buf, format="JPEG", quality=jpeg_quality, optimize=True)
                        new_mime = "image/jpeg"

                    chunk = out_buf.getvalue()
                    for img_obj in image_bv_map[bv_idx]:
                        img_obj["mimeType"] = new_mime
            except Exception as exc:
                print(f"  [warn] Could not downscale bufferView {bv_idx} in {src_glb.name}: {exc}")

        # Align start of every bufferView to 4 bytes
        while len(new_bin) % 4 != 0:
            new_bin.append(0)

        bv["byteOffset"] = len(new_bin)
        bv["byteLength"] = len(chunk)
        new_bin.extend(chunk)

    while len(new_bin) % 4 != 0:
        new_bin.append(0)

    if gltf.get("buffers"):
        gltf["buffers"][0]["byteLength"] = len(new_bin)

    new_json_raw = json.dumps(gltf, separators=(",", ":")).encode("utf-8")
    new_json_padded = pad4(new_json_raw, b" ")
    new_bin_bytes = bytes(new_bin)

    new_total_len = 12 + 8 + len(new_json_padded) + 8 + len(new_bin_bytes)
    out = bytearray()
    out.extend(struct.pack("<III", 0x46546C67, 2, new_total_len))
    out.extend(struct.pack("<II", len(new_json_padded), 0x4E4F534A))
    out.extend(new_json_padded)
    out.extend(struct.pack("<II", len(new_bin_bytes), 0x004E4942))
    out.extend(new_bin_bytes)

    dst_glb.write_bytes(out)
    return len(raw), len(out)


def build_rpi_textures():
    TILES_RPI_DIR.mkdir(parents=True, exist_ok=True)
    TILES_ONIRICA_RPI_DIR.mkdir(parents=True, exist_ok=True)
    PBR_RPI_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Downscale all 53 tile faces (including dragon_*_ornate.png) from 768x1024 -> 256x342 (9x fewer pixels!)
    tile_count = 0
    for src_png in sorted(TILES_DIR.glob("*.png")):
        with Image.open(src_png) as im:
            im_small = im.convert("RGB").resize((256, 342), Image.Resampling.LANCZOS)
            im_q = im_small.quantize(colors=192, method=Image.Quantize.MEDIANCUT)
            im_q.save(TILES_RPI_DIR / src_png.name, format="PNG", optimize=True)
            tile_count += 1

    # 2. Downscale Onirica tile faces -> 256x342 (loaded lazily only if Onirica mode is toggled)
    onirica_count = 0
    for src_png in sorted(TILES_ONIRICA_DIR.glob("*.png")):
        with Image.open(src_png) as im:
            im_small = im.convert("RGB").resize((256, 342), Image.Resampling.LANCZOS)
            im_q = im_small.quantize(colors=160, method=Image.Quantize.MEDIANCUT)
            im_q.save(TILES_ONIRICA_RPI_DIR / src_png.name, format="PNG", optimize=True)
            onirica_count += 1

    # 3. Downscale PBR base maps from 2048x2048 -> 256x256 (64x fewer pixels!)
    pbr_count = 0
    for src_png in sorted(PBR_DIR.glob("*.png")):
        with Image.open(src_png) as im:
            im_small = im.convert("RGB").resize((256, 256), Image.Resampling.LANCZOS)
            im_q = im_small.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
            im_q.save(PBR_RPI_DIR / src_png.name, format="PNG", optimize=True)
            pbr_count += 1

    print(
        f"[RPi Textures] Generated {tile_count} tiles_rpi (256x342), "
        f"{onirica_count} tiles_onirica_rpi (256x342), and {pbr_count} pbr_rpi (256x256)!"
    )


def build_rpi_glbs():
    glb_specs = [
        ("temple_environment.glb", "temple_environment_rpi.glb", 128, 68),
        ("tile_generic_white_marble_obsidian.glb", "tile_generic_white_marble_obsidian_rpi.glb", 96, 65),
        ("tile_coupled_showcase.glb", "tile_coupled_showcase_rpi.glb", 160, 70),
        ("tile_carved_intaglio_showcase.glb", "tile_carved_intaglio_showcase_rpi.glb", 160, 70),
    ]
    for src_name, dst_name, max_dim, q in glb_specs:
        src_p = MODELS_DIR / src_name
        dst_p = MODELS_DIR / dst_name
        if not src_p.exists():
            continue
        old_sz, new_sz = repack_glb_for_rpi(src_p, dst_p, max_tex_dim=max_dim, jpeg_quality=q)
        ratio = (1.0 - new_sz / max(1, old_sz)) * 100.0
        print(
            f"[RPi GLB] {src_name} ({old_sz / 1024:.1f} KB) -> {dst_name} ({new_sz / 1024:.1f} KB) [-{ratio:.1f}%]"
        )


if __name__ == "__main__":
    build_rpi_textures()
    build_rpi_glbs()
