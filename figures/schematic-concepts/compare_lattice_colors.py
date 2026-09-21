"""Four controlled color studies; never publishes a manuscript figure."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import fitz
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "pdf" / "schematic-color-study"
ASSETS = ROOT / "figures" / "schematic-assets"
BLENDER = ROOT / ".build" / "tools" / "blender-4.3.2-linux-x64" / "blender"
PALETTES = [
    dict(id="A", name="current", sphere="#C75B4F", halo="#EF8372",
         arrow="#7835A0", label="#6B278F", render=None,
         title="A  现有：珊瑚红小球 · 紫色跃迁", english="A  Current: coral / purple"),
    dict(id="B", name="purple_red", sphere="#7851A8", halo="#AC8ACE",
         arrow="#C8473B", label="#B43B31", render="purple",
         title="B  紫色小球 · 红色跃迁", english="B  Purple / red"),
    dict(id="C", name="blue_purple", sphere="#274780", halo="#688ED0",
         arrow="#7835A0", label="#6B278F", render="blue",
         title="C  深蓝小球 · 紫色跃迁", english="C  Deep blue / purple"),
    dict(id="D", name="blue_blue", sphere="#274780", halo="#688ED0",
         arrow="#294F89", label="#234579", render="blue",
         title="D  深蓝小球 · 深蓝跃迁", english="D  Deep blue / deep blue"),
]

parser = argparse.ArgumentParser()
parser.add_argument("--render", action="store_true", help="Render both new sphere colors with Blender first")
args = parser.parse_args()
OUT.mkdir(parents=True, exist_ok=True)


def run(command, logfile):
    with logfile.open("w") as log:
        subprocess.run([str(part) for part in command], cwd=ROOT, stdout=log,
                       stderr=subprocess.STDOUT, check=True)


production = {suffix: hashlib.sha256((ROOT / "figures" / f"schematic.{suffix}").read_bytes()).hexdigest()
              for suffix in ("pdf", "svg", "png")}
prepared = {}
layout_reference = None
for palette in PALETTES:
    render_name = palette["render"]
    if render_name is None:
        asset_dir = ASSETS
    elif render_name in prepared:
        asset_dir = prepared[render_name]
    else:
        render_dir = OUT / f"render-{render_name}"
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
assert Image.open(OUT / "A_current.png").tobytes() == Image.open(ROOT / "figures/schematic.png").tobytes()

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
            image = image.crop(tuple(round(value*image.width/1000) for value in (108, 112, 626, 645)))
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
}, ensure_ascii=False, indent=2)+"\n")
print(full)
print(detail)
