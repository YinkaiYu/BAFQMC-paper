"""Four controlled color studies; never publishes a manuscript figure."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import fitz
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
STUDY = ROOT / "pdf" / "schematic-color-study"
ASSETS = ROOT / "figures" / "schematic-assets"
BLENDER = ROOT / ".build" / "tools" / "blender-4.3.2-linux-x64" / "blender"
PALETTES = [
    dict(id="A", name="current", sphere="#C75B4F", halo="#EF8372",
         arrow="#7835A0", label="#6B278F", render="coral",
         title="A  珊瑚红小球 · 紫色跃迁", english="A  Coral / purple"),
    dict(id="B", name="purple_red", sphere="#7851A8", halo="#AC8ACE",
         arrow="#C8473B", label="#B43B31", render="purple",
         title="B  现有：紫色小球 · 红色跃迁", english="B  Current: purple / red"),
    dict(id="C", name="blue_purple", sphere="#274780", halo="#688ED0",
         arrow="#7835A0", label="#6B278F", render="blue",
         title="C  深蓝小球 · 紫色跃迁", english="C  Deep blue / purple"),
    dict(id="D", name="blue_blue", sphere="#274780", halo="#688ED0",
         arrow="#294F89", label="#234579", render="blue",
         title="D  深蓝小球 · 深蓝跃迁", english="D  Deep blue / deep blue"),
]

parser = argparse.ArgumentParser()
parser.add_argument("--render", action="store_true", help="Render all three sphere colors with Blender first")
tone = parser.add_mutually_exclusive_group()
tone.add_argument("--muted", action="store_true", help="Strong chroma reduction for the earlier review")
tone.add_argument("--balanced", action="store_true", help="Gently soften and brighten colors while retaining color clarity")
args = parser.parse_args()
graded = args.muted or args.balanced
OUT = STUDY / "balanced" if args.balanced else STUDY / "muted" if args.muted else STUDY
motif_chroma = .88 if args.balanced else .52
annotation_chroma = .94 if args.balanced else .70
motif_lightness = .035 if args.balanced else 0
annotation_lightness = .015 if args.balanced else 0
OUT.mkdir(parents=True, exist_ok=True)


def grade_rgb(rgb, factor, lightness_lift=0):
    """Grade OKLab chroma and colored midtones; rgb is an sRGB array in [0, 1]."""
    linear = np.where(rgb <= .04045, rgb/12.92, ((rgb+.055)/1.055)**2.4)
    rgb_to_lms = np.array([[.4122214708, .5363325363, .0514459929],
                           [.2119034982, .6806995451, .1073969566],
                           [.0883024619, .2817188376, .6299787005]])
    lms_to_lab = np.array([[.2104542553, .7936177850, -.0040720468],
                           [1.9779984951, -2.4285922050, .4505937099],
                           [.0259040371, .7827717662, -.8086757660]])
    lab = np.cbrt(linear @ rgb_to_lms.T) @ lms_to_lab.T
    color_strength = np.clip(np.linalg.norm(lab[..., 1:], axis=-1)/.06, 0, 1)
    lab[..., 0] += lightness_lift*color_strength*4*lab[..., 0]*(1-lab[..., 0])
    lab[..., 1:] *= factor
    result = (lab @ np.linalg.inv(lms_to_lab).T)**3 @ np.linalg.inv(rgb_to_lms).T
    result = np.clip(result, 0, 1)
    srgb = np.where(result <= .0031308, 12.92*result, 1.055*result**(1/2.4)-.055)
    return np.clip(np.rint(srgb*255), 0, 255).astype(np.uint8)


def graded_hex(value):
    rgb = np.array([int(value[k:k+2], 16) for k in (1, 3, 5)])/255
    return "#"+"".join(f"{int(channel):02X}" for channel in grade_rgb(rgb, annotation_chroma, annotation_lightness))


if graded:
    names = (["珊瑚红小球 · 紫色跃迁", "紫色小球 · 红色跃迁",
              "蓝色小球 · 紫色跃迁", "蓝色小球 · 蓝色跃迁"] if args.balanced else
             ["柔和砖红小球 · 灰梅紫跃迁", "灰紫小球 · 陶土红跃迁",
              "石板蓝小球 · 灰梅紫跃迁", "石板蓝小球 · 灰蓝跃迁"])
    for palette, title in zip(PALETTES, names):
        palette["title"] = f"{palette['id']}  {title}"
        palette["english"] = palette["english"].replace("Current: ", "")+(" (balanced)" if args.balanced else " (muted)")
        palette["arrow"] = graded_hex(palette["arrow"])
        palette["label"] = graded_hex(palette["label"])
        palette["motif_chroma_scale"] = motif_chroma
        palette["motif_lightness_lift"] = motif_lightness


def run(command, logfile):
    with logfile.open("w") as log:
        subprocess.run([str(part) for part in command], cwd=ROOT, stdout=log,
                       stderr=subprocess.STDOUT, check=True)


production = {suffix: hashlib.sha256((ROOT / "figures" / f"schematic.{suffix}").read_bytes()).hexdigest()
              for suffix in ("pdf", "svg", "png")}
prepared = {}
graded_assets = {}
layout_reference = None
for palette in PALETTES:
    render_name = palette["render"]
    if render_name in prepared:
        asset_dir = prepared[render_name]
    else:
        render_dir = STUDY / f"render-{render_name}"
        if args.render:
            run([BLENDER, "-b", "--threads", "8", "--python", HERE / "render_triangle_focus.py",
                 "--", "--final", "--output-dir", render_dir, "--sphere-color", palette["sphere"]],
                OUT / f"render-{render_name}.log")
        if not (render_dir / "lattice-render.png").exists():
            raise FileNotFoundError(f"Missing {render_name} render; run with --render")
        metadata = json.loads((render_dir / "projection.json").read_text())
        assert metadata["sphere_color"] == palette["sphere"]
        run([sys.executable, "-W", "error", HERE / "compose_triangle_focus.py",
             "--output-dir", render_dir, "--halo-color", palette["halo"],
             "--arrow-color", palette["arrow"], "--label-color", palette["label"]],
            OUT / f"compose-{render_name}.log")
        asset_dir = render_dir / "assets"
        asset_dir.mkdir(exist_ok=True)
        shutil.copy2(render_dir / "lattice-motif.png", asset_dir / "triangle-lattice.png")
        shutil.copy2(render_dir / "motif-annotation.json", asset_dir / "triangle-annotation.json")
        assert json.loads((asset_dir / "triangle-annotation.json").read_text()) == json.loads(
            (ASSETS / "triangle-annotation.json").read_text()), "Projected hopping geometry changed"
        prepared[render_name] = asset_dir
    if graded:
        key = render_name or "coral"
        if key not in graded_assets:
            graded_dir = OUT / f"assets-{key}"
            graded_dir.mkdir(exist_ok=True)
            pixels = np.array(Image.open(asset_dir / "triangle-lattice.png").convert("RGBA"))
            rgba = pixels.copy()
            rgba[..., :3] = grade_rgb(pixels[..., :3]/255, motif_chroma, motif_lightness)
            assert np.array_equal(rgba[..., 3], pixels[..., 3]), "Opacity or fading changed"
            Image.fromarray(rgba).save(graded_dir / "triangle-lattice.png")
            shutil.copy2(asset_dir / "triangle-annotation.json", graded_dir / "triangle-annotation.json")
            graded_assets[key] = graded_dir
        asset_dir = graded_assets[key]
    stem = f"{palette['id']}_{palette['name']}"
    run([sys.executable, "-W", "error", HERE / "build_cards_v14.py", "--asset-dir", asset_dir,
         "--output-dir", OUT, "--name", stem, "--arrow-color", palette["arrow"],
         "--label-color", palette["label"]], OUT / f"{stem}.log")
    with fitz.open(OUT / f"{stem}.pdf") as document:
        layout = [(span["text"], tuple(round(v, 3) for v in span["bbox"]))
                  for block in document[0].get_text("dict")["blocks"] if "lines" in block
                  for line in block["lines"] for span in line["spans"]]
    if layout_reference is None:
        layout_reference = layout
    else:
        assert layout == layout_reference, "Text positions changed between palettes"
    print(f"Completed palette {palette['id']}", flush=True)

# The default palette must remain identical to the current production preview.
if not graded:
    assert Image.open(OUT / "B_purple_red.png").tobytes() == Image.open(ROOT / "figures/schematic.png").tobytes()

font_path = "/mnt/c/Windows/Fonts/msyh.ttc"
title_font = ImageFont.truetype(font_path, 28)


def make_board(focus):
    tile_w, tile_h = (800, 820) if focus else (880, 880)
    margin, gap, heading = 28, 28, 60
    board = Image.new("RGB", (2*tile_w+2*margin+gap, 2*(tile_h+heading)+2*margin+gap), "#f1f4f7")
    draw = ImageDraw.Draw(board)
    for index, palette in enumerate(PALETTES):
        x, y = margin+(index % 2)*(tile_w+gap), margin+(index // 2)*(tile_h+heading+gap)
        draw.text((x+14, y+10), palette["title"], font=title_font, fill="#263747")
        image = Image.open(OUT / f"{palette['id']}_{palette['name']}.png").convert("RGB")
        if focus:
            manifest = json.loads((OUT / f"{palette['id']}_{palette['name']}_manifest.json").read_text())
            crop_top = manifest["canvas_crop"][1]
            image = image.crop(tuple(round(value*image.width/1000)
                                     for value in (108, 112-crop_top, 626, 645-crop_top)))
        image.thumbnail((tile_w, tile_h), Image.Resampling.LANCZOS)
        board.paste(image, (x+(tile_w-image.width)//2, y+heading+(tile_h-image.height)//2))
    path = OUT / ("four-palettes-detail.png" if focus else "four-palettes-full.png")
    board.save(path)
    return path


full = make_board(False)
detail = make_board(True)

# Preserve the individual vector figures in a compact 2x2 review PDF.
with fitz.open() as document:
    page = document.new_page(width=536, height=588)
    for index, palette in enumerate(PALETTES):
        x, y = 16+(index % 2)*260, 16+(index // 2)*284
        page.insert_text((x, y+12), palette["english"], fontsize=10, fontname="hebo", color=(.15, .21, .28))
        with fitz.open(OUT / f"{palette['id']}_{palette['name']}.pdf") as figure:
            page.show_pdf_page(fitz.Rect(x, y+24, x+244, y+268), figure, 0)
    document.save(OUT / "four-palettes-comparison.pdf", garbage=4, deflate=True)

for suffix, original in production.items():
    assert hashlib.sha256((ROOT / "figures" / f"schematic.{suffix}").read_bytes()).hexdigest() == original
(OUT / "palette-manifest.json").write_text(json.dumps({
    "palettes": PALETTES, "layout_comparison": "identical", "production_preview": "unchanged",
    "render_settings": "2000 x 1545, 128 Cycles samples, identical geometry, lighting and materials except base color",
    "color_grading": {"motif_chroma_scale": motif_chroma, "annotation_chroma_scale": annotation_chroma,
                      "motif_max_lightness_lift": motif_lightness,
                      "annotation_max_lightness_lift": annotation_lightness,
                      "alpha": "preserved"} if graded else "none",
}, ensure_ascii=False, indent=2)+"\n")
print(full)
print(detail)
