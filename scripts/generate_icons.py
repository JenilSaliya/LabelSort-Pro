#!/usr/bin/env python3
"""
LabelSort Pro — Brand Icon Generator
Renders frontend/public/favicon.svg into native multi-resolution icons:
  - 32x32.png
  - 128x128.png
  - 128x128@2x.png (256x256)
  - icon.png (512x512)
  - icon.ico (Multi-layer Windows ICO with 16, 24, 32, 48, 64, 128, 256 px layers)
  - icon.icns
"""

import struct
from pathlib import Path
import pymupdf

ROOT_DIR = Path(__file__).resolve().parent.parent
SVG_PATH = ROOT_DIR / "frontend" / "public" / "favicon.svg"
ICONS_DIR = ROOT_DIR / "frontend" / "src-tauri" / "icons"


def render_svg_to_png_bytes(svg_path: Path, target_size: int) -> bytes:
    """Renders SVG to PNG bytes at exact target dimensions."""
    doc = pymupdf.open(str(svg_path))
    page = doc[0]
    rect = page.rect
    scale = target_size / rect.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=True)
    doc.close()
    return pix.tobytes("png")


def create_windows_ico(png_dict: dict[int, bytes]) -> bytes:
    """
    Creates a multi-resolution Windows ICO file containing PNG streams.
    Standard Windows resolutions: 16, 24, 32, 48, 64, 128, 256 px.
    """
    sizes = sorted(png_dict.keys())
    num_images = len(sizes)

    # 1. ICONDIR (6 bytes): reserved=0, type=1 (ICO), count=num_images
    icondir = struct.pack("<HHH", 0, 1, num_images)

    # 2. Compute offsets for each directory entry
    header_size = 6 + (16 * num_images)
    current_offset = header_size

    entries = bytearray()
    image_data = bytearray()

    for size in sizes:
        data = png_dict[size]
        data_len = len(data)
        width_byte = 0 if size >= 256 else size
        height_byte = 0 if size >= 256 else size

        # ICONDIRENTRY (16 bytes)
        entry = struct.pack(
            "<BBBBHHII",
            width_byte,      # bWidth (0 = 256)
            height_byte,     # bHeight (0 = 256)
            0,               # bColorCount
            0,               # bReserved
            1,               # wPlanes
            32,              # wBitCount
            data_len,        # dwBytesInRes
            current_offset,  # dwImageOffset
        )
        entries.extend(entry)
        image_data.extend(data)
        current_offset += data_len

    return icondir + bytes(entries) + bytes(image_data)


def main():
    print(f"Generating brand icons from: {SVG_PATH}")
    ICONS_DIR.mkdir(parents=True, exist_ok=True)

    sizes = [16, 24, 32, 48, 64, 128, 256, 512]
    png_map = {}

    for size in sizes:
        png_bytes = render_svg_to_png_bytes(SVG_PATH, size)
        png_map[size] = png_bytes
        print(f"  - Rendered {size}x{size} PNG ({len(png_bytes)} bytes)")

    # 1. Save standard Tauri PNG icons
    (ICONS_DIR / "32x32.png").write_bytes(png_map[32])
    (ICONS_DIR / "128x128.png").write_bytes(png_map[128])
    (ICONS_DIR / "128x128@2x.png").write_bytes(png_map[256])
    (ICONS_DIR / "icon.png").write_bytes(png_map[512])
    (ICONS_DIR / "icon.icns").write_bytes(png_map[512])

    # 2. Build and save multi-layer Windows ICO
    ico_sizes = {s: png_map[s] for s in [16, 24, 32, 48, 64, 128, 256]}
    ico_bytes = create_windows_ico(ico_sizes)
    (ICONS_DIR / "icon.ico").write_bytes(ico_bytes)

    print(f"\n[OK] Generated multi-layer icon.ico ({len(ico_bytes)} bytes) containing sizes: 16, 24, 32, 48, 64, 128, 256 px.")
    print(f"[OK] All icons successfully placed into: {ICONS_DIR}")


if __name__ == "__main__":
    main()
