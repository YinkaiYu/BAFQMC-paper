"""Production classification figure with a prominent frustrated BAFQMC region."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess

import fitz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, patheffects
from matplotlib.patches import FancyBboxPatch, PathPatch
from matplotlib.path import Path as MplPath
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "pdf" / "schematic-concepts"
ASSETS = ROOT / "figures" / "schematic-assets"
NAME = "C_cards_v14_this_work"
MM, W, H = 86, 1000, 1000
CARD_RADIUS = 20
SPLIT_X, SPLIT_Y = 626, 662

parser = argparse.ArgumentParser()
parser.add_argument("--publish", action="store_true")
parser.add_argument("--asset-dir", type=Path, default=ASSETS)
args = parser.parse_args()
OUT.mkdir(parents=True, exist_ok=True)
for name in ("FreeSans.ttf", "FreeSansOblique.ttf", "FreeSansBold.ttf"):
    font_manager.fontManager.addfont(f"/usr/share/fonts/truetype/freefont/{name}")
plt.rcParams.update({"font.family": "FreeSans", "mathtext.fontset": "stixsans",
                     "svg.fonttype": "path", "pdf.fonttype": 42,
                     "image.composite_image": False})
fig = plt.figure(figsize=(MM/25.4, MM/25.4), facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set(xlim=(0, W), ylim=(H, 0), aspect="equal")
ax.axis("off")
texts = []


def text(x, y, value, size=7.9, color="#282b32", **kwargs):
    obj = ax.text(x, y, value, fontsize=size, color=color, ha="center", va="center",
                  linespacing=1.25, **kwargs)
    texts.append(obj)
    return obj


def rounded(box, **kwargs):
    x, y, w, h = box
    patch = FancyBboxPatch((x, y), w, h,
                          boxstyle=f"round,pad=0,rounding_size={CARD_RADIUS}",
                          **kwargs)
    ax.add_patch(patch)
    return patch


# Keep the selected overlapping half-plane cards and their layer order.
gy, gx = np.mgrid[0:600, 0:600]/599
blend = np.clip((gx+1-gy)/1.44, 0, 1)
blend = blend*blend*(3-2*blend)
gray = np.array([200, 208, 217])[None, None, :]/255*(1-blend[:, :, None])+blend[:, :, None]
ax.imshow(gray, extent=(164, 906, 910, 168), interpolation="bicubic", zorder=0)
boxes = {"gold": (SPLIT_X, 140, 934-SPLIT_X, 798),
         "blue": (108, 112, 854, SPLIT_Y-112)}
cards = {}
for name, opacity, z in [("gold", .64, 1), ("blue", .48, 2)]:
    x, y, w, h = boxes[name]
    for spread in range(12, 0, -1):
        rounded((x-spread, y+8-spread, w+2*spread, h+2*spread),
                linewidth=0, facecolor="#344253", alpha=.003, zorder=z)
    cards[name] = rounded(boxes[name], linewidth=0, facecolor="none", zorder=z+.1)
    t = np.linspace(0, 1, 700)
    if name == "blue":
        t = t[None, :, None]
        light, deep = np.array([104, 203, 255])/255, np.array([15, 119, 207])/255
    else:
        t = (1-t)[:, None, None]
        light, deep = np.array([255, 226, 142])/255, np.array([232, 163, 12])/255
    rgb = light*(1-t)+deep*t
    rgba = np.concatenate([rgb, np.full((*rgb.shape[:2], 1), opacity)], axis=2)
    im = ax.imshow(rgba, extent=(x, x+w, y+h, y), interpolation="bicubic", zorder=z+.1)
    im.set_clip_path(cards[name])
overlap = rounded(boxes["gold"], linewidth=0, facecolor="#a3e3cd", zorder=2.2)
overlap.set_clip_path(cards["blue"])
for name, z in [("gold", 1.2), ("blue", 2.3)]:
    rounded(boxes[name], fill=False, linewidth=.35, edgecolor="white", alpha=.85, zorder=z)


def inset_plaque(box):
    """A recessed plate: shadow on its upper/left inner rim, light below/right."""
    x, y, w, h = box
    scale, pad = 4, 40
    shape = (round(w*scale)+2*pad, round(h*scale)+2*pad)
    mask_image = Image.new("L", shape)
    ImageDraw.Draw(mask_image).rounded_rectangle(
        (pad, pad, shape[0]-pad-1, shape[1]-pad-1), radius=CARD_RADIUS*scale, fill=255)
    mask = np.asarray(mask_image, dtype=float)/255
    def shifted(dx, dy, blur):
        canvas = Image.new("L", shape)
        canvas.paste(mask_image, (round(dx*scale), round(dy*scale)))
        return np.asarray(canvas.filter(ImageFilter.GaussianBlur(blur*scale)), dtype=float)/255
    shadow = mask*(1-shifted(3.0, 3.0, 2.3))
    light = mask*(1-shifted(-1.6, -1.6, 1.2))
    rgba = np.empty((*mask.shape, 4), dtype=np.uint8)
    color = np.array([133, 191, 224])/255
    rgb = color[None, None, :]*(1-.30*shadow[:, :, None])
    rgb = rgb*(1-.40*light[:, :, None])+.40*light[:, :, None]
    rgba[:, :, :3] = np.clip(rgb*255, 0, 255).astype(np.uint8)
    rgba[:, :, 3] = (mask*255).astype(np.uint8)
    padding = pad/scale
    ax.imshow(rgba, extent=(x-padding, x+w+padding, y+h+padding, y-padding), zorder=7)
    text(x+w/2, y+h/2+1, "This work", size=8.8, color="#164F72", weight="bold", zorder=8)


inset_plaque((252, 149, 230, 70))

# The rendered lattice remains RGBA; the card shows through all faded pixels.
motif = Image.open(args.asset_dir / "triangle-lattice.png").convert("RGBA")
annotation = json.loads((args.asset_dir / "triangle-annotation.json").read_text())
pixels = np.asarray(motif).copy()
pixel_h, pixel_w = pixels.shape[:2]
left, top, motif_w = -35, 107, 800
motif_h = motif_w*pixel_h/pixel_w
yy, xx = np.mgrid[0:pixel_h, 0:pixel_w]
canvas_x = left+(xx+.5)/pixel_w*motif_w
canvas_y = top+(yy+.5)/pixel_h*motif_h
edge = np.minimum.reduce([(canvas_x-122)/36, (619-canvas_x)/36,
                          (canvas_y-236)/24, (584-canvas_y)/42])
edge = np.clip(edge, 0, 1)
edge = edge*edge*(3-2*edge)
pixels[:, :, 3] = (pixels[:, :, 3]*edge).astype(np.uint8)
ax.imshow(pixels, extent=(left, left+motif_w, top+motif_h, top), zorder=4)

def motif_coords(points):
    return np.asarray(points)*[motif_w, motif_h]+[left, top]

for outline in annotation["arrows"]:
    points = motif_coords(outline)
    codes = [MplPath.MOVETO]+[MplPath.LINETO]*(len(points)-2)+[MplPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MplPath(points, codes), facecolor="#7835A0", edgecolor="none",
                           zorder=5, path_effects=[patheffects.Stroke(linewidth=.7, foreground="white"),
                                                  patheffects.Normal()]))
label_x, label_y = motif_coords(annotation["label"])
text(label_x, label_y, r"$t>0$", size=9.8, color="#6B278F", zorder=6,
     path_effects=[patheffects.Stroke(linewidth=1.0, foreground="white"),
                   patheffects.Stroke(linewidth=.23, foreground="#6B278F"), patheffects.Normal()])

# Centres and text wrapping follow the revised region sizes.
text((108+SPLIT_X)/2, 72, "Frustrated")
text((SPLIT_X+934)/2, 72, "Unfrustrated")
text(65, (112+SPLIT_Y)/2, "Respect TRS/RP criteria", rotation=90)
text(65, (SPLIT_Y+938)/2, "Violate TRS/RP criteria", rotation=90)
status_texts = [
    (text(367, 612, "Sign-free for BAFQMC", size=7.6, color="#1265a2", fontstyle="italic"),
     (130, 596)),
    (text(780, 400, "Sign-free\nfor both", size=7.6, color="#24745b", fontstyle="italic"),
     (646, 914)),
    (text(780, 785, "Sign-free for\nWLQMC/SSE", size=7.6, color="#8b6006", fontstyle="italic"),
     (646, 914)),
    (text(395, 785, "Sign-problematic", size=7.6, color="#626b75", fontstyle="italic"),
     (184, 606)),
]
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for obj, (xmin, xmax) in status_texts:
    bounds = obj.get_window_extent(renderer).transformed(ax.transData.inverted())
    assert bounds.x0 >= xmin and bounds.x1 <= xmax, obj.get_text()
for obj in texts:
    bounds = obj.get_window_extent(renderer)
    assert bounds.x0 >= 0 and bounds.y0 >= 0, obj.get_text()
    assert bounds.x1 <= fig.bbox.x1 and bounds.y1 <= fig.bbox.y1, obj.get_text()

pdf_path = OUT / f"{NAME}.pdf"
fig.savefig(pdf_path, dpi=650, metadata={"Title": "Sign-free bosonic QMC: frustrated territory unlocked by BAFQMC"})
svg_path = OUT / f"{NAME}.svg"
fig.savefig(svg_path, dpi=650, metadata={
    "Title": "Sign-free bosonic QMC classification",
    "Description": "Enlarged frustrated TRS/RP region, recessed This work plaque, and triangular-lattice hopping."})
svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines())+"\n")
plt.close(fig)
subprocess.run(["pdftoppm", "-singlefile", "-r", "450", "-png", str(pdf_path), str(OUT / NAME)], check=True)
with fitz.open(pdf_path) as doc:
    assert len(doc) == 1 and abs(doc[0].rect.width*25.4/72-MM) < .01
manifest = {"width_mm": MM, "height_mm": MM, "split_x": SPLIT_X, "split_y": SPLIT_Y,
            "upper_left_area_fraction": round((SPLIT_X-108)*(SPLIT_Y-112)/(854*826), 3),
            "card_radius": CARD_RADIUS, "plaque_radius": CARD_RADIUS,
            "illustrated_quadrants": ["upper-left"], "hopping_arrows": len(annotation["arrows"]),
            "font_min_pt": min(t.get_fontsize() for t in texts), "bounds_check": "pass",
            "lattice_effective_dpi": round(pixel_w/(motif_w/W*MM/25.4)),
            "caption_convention": annotation["convention"]}
(OUT / f"{NAME}_manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
print(json.dumps(manifest, indent=2))
if args.publish:
    for extension in ("pdf", "svg", "png"):
        shutil.copy2(OUT / f"{NAME}.{extension}", ROOT / "figures" / f"schematic.{extension}")
    print("Updated production schematic PDF, SVG and local PNG preview.")
