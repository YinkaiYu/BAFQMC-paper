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
PLAQUE_MARGIN = 28
PLAQUE_BOX = (108+PLAQUE_MARGIN, 112+PLAQUE_MARGIN, 300, 50)
CONTENT_SHIFT_Y = -40
YLABEL_SHIFT_Y = -55

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
                  linespacing=1.6, **kwargs)
    texts.append(obj)
    return obj


def rounded(box, **kwargs):
    x, y, w, h = box
    patch = FancyBboxPatch((x, y), w, h,
                          boxstyle=f"round,pad=0,rounding_size={CARD_RADIUS}",
                          **kwargs)
    ax.add_patch(patch)
    return patch


def card_shadow(box, offset, blur, opacity, zorder):
    """A single diffuse edge shadow, strongest below the raised card."""
    x, y, w, h = box
    scale, pad = 2, 42
    shape = (round((w+2*pad)*scale), round((h+2*pad)*scale))
    mask = Image.new("L", shape)
    bounds = (pad*scale, pad*scale, (pad+w)*scale, (pad+h)*scale)
    ImageDraw.Draw(mask).rounded_rectangle(bounds, radius=CARD_RADIUS*scale, fill=255)
    shifted = Image.new("L", shape)
    shifted.paste(mask, (0, round(offset*scale)))
    shadow = np.asarray(shifted.filter(ImageFilter.GaussianBlur(blur*scale)), dtype=float)/255
    shadow *= 1-np.asarray(mask, dtype=float)/255
    rgba = np.zeros((*shadow.shape, 4), dtype=np.uint8)
    rgba[:, :, :3] = [47, 67, 80]
    rgba[:, :, 3] = (shadow*opacity*255).astype(np.uint8)
    ax.imshow(rgba, extent=(x-pad, x+w+pad, y+h+pad, y-pad), zorder=zorder)


# Stack actual translucent gradients: grey backing, gold, then blue.
# The overlap is solely the source-over composite of these layers.
gy, gx = np.mgrid[0:600, 0:600]/599
blend = np.clip((gx+1-gy)/1.44, 0, 1)
blend = blend*blend*(3-2*blend)
gray = np.array([200, 208, 217])[None, None, :]/255*(1-blend[:, :, None])+blend[:, :, None]
ax.imshow(gray, extent=(164, 906, 910, 168), interpolation="bicubic", zorder=0)
boxes = {"gold": (SPLIT_X, 140, 934-SPLIT_X, 798),
         "blue": (108, 112, 854, SPLIT_Y-112)}
cards = {}
for name, z in [("gold", 1), ("blue", 2)]:
    x, y, w, h = boxes[name]
    card_shadow(boxes[name], offset=9 if name == "blue" else 6,
                blur=7 if name == "blue" else 6,
                opacity=.20 if name == "blue" else .13, zorder=z)
    cards[name] = rounded(boxes[name], linewidth=0, facecolor="none", zorder=z+.1)
    v, u = np.mgrid[0:600, 0:800]/np.array([599, 799])[:, None, None]
    if name == "blue":
        t = .62*u+.38*v
        light, deep = np.array([124, 218, 250])/255, np.array([30, 159, 215])/255
        opacity = .40+.13*t+.04*v
    else:
        t = .23*u+.77*(1-v)
        light, deep = np.array([255, 225, 128])/255, np.array([247, 188, 41])/255
        opacity = .54+.14*t
    t = (t*t*(3-2*t))[:, :, None]
    rgb = light*(1-t)+deep*t
    # Broad, restrained reflection across the same continuous card surface.
    sheen = (.08*np.exp(-((v-(.07+.13*u))/.29)**2))[:, :, None]
    rgb = rgb*(1-sheen)+sheen
    rgba = np.concatenate([rgb, opacity[:, :, None]], axis=2)
    im = ax.imshow(rgba, extent=(x, x+w, y+h, y), interpolation="bicubic", zorder=z+.1)
    im.set_clip_path(cards[name])
    # The gold rim is seen through the blue layer. The blue lower edge stays
    # uninterrupted across both underlying regions and casts its shadow.
    if name == "blue":
        r, bottom = CARD_RADIUS, y+h+1.2
        rim = MplPath([(x, bottom-r), (x, bottom), (x+r, bottom),
                       (x+w-r, bottom), (x+w, bottom), (x+w, bottom-r),
                       (x+w, y+r)],
                      [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3,
                       MplPath.LINETO, MplPath.CURVE3, MplPath.CURVE3, MplPath.LINETO])
        ax.add_patch(PathPatch(rim, fill=False, linewidth=.55, edgecolor="#4E87A7",
                               alpha=.26, zorder=z+.2))
    rounded(boxes[name], fill=False, linewidth=.45 if name == "blue" else .35,
            edgecolor="white", alpha=.78 if name == "blue" else .62, zorder=z+.3)


def inset_plaque(box):
    """A shallow transparent recess following the card's surface and corner path."""
    x, y, w, h = box
    scale, pad = 4, 40
    shape = (round(w*scale)+2*pad, round(h*scale)+2*pad)
    padding = pad/scale
    clip = rounded(box, linewidth=0, facecolor="none", zorder=7)
    yy, xx = np.mgrid[0:shape[1], 0:shape[0]]
    positions = np.column_stack(((x-padding+(xx+.5)/scale).ravel(),
                                 (y-padding+(yy+.5)/scale).ravel()))
    mask = clip.get_path().contains_points(positions).reshape(yy.shape).astype(float)
    mask_image = Image.fromarray((mask*255).astype(np.uint8))
    def shifted(dx, dy, blur):
        canvas = Image.new("L", shape)
        canvas.paste(mask_image, (round(dx*scale), round(dy*scale)))
        return np.asarray(canvas.filter(ImageFilter.GaussianBlur(blur*scale)), dtype=float)/255
    shadow = mask*(1-shifted(2.4, 3.0, 1.35))
    light = mask*(1-shifted(-.45, -.55, .65))
    diagonal = np.clip(.62*(xx-pad)/(w*scale)+.38*(yy-pad)/(h*scale), 0, 1)
    # Transparent tint preserves the actual blue-card gradient and its backing.
    # A very small additional darkening toward the lower right follows the light.
    overlay = Image.new("RGBA", shape)
    for color, alpha in [([50, 109, 139], mask*(.075+.025*diagonal)),
                          ([33, 76, 102], .44*shadow),
                          ([255, 255, 255], .11*light)]:
        rgba = np.empty((*mask.shape, 4), dtype=np.uint8)
        rgba[:, :, :3] = color
        rgba[:, :, 3] = (alpha*255).astype(np.uint8)
        overlay = Image.alpha_composite(overlay, Image.fromarray(rgba))
    im = ax.imshow(overlay, extent=(x-padding, x+w+padding, y+h+padding, y-padding), zorder=7)
    im.set_clip_path(clip)
    text(x+w/2, y+h/2+1, "New sign-free regime", size=6.6, color="#285D76", zorder=8)


inset_plaque(PLAQUE_BOX)

# The rendered lattice remains RGBA; the card shows through all faded pixels.
motif = Image.open(args.asset_dir / "triangle-lattice.png").convert("RGBA")
annotation = json.loads((args.asset_dir / "triangle-annotation.json").read_text())
pixels = np.asarray(motif).copy()
pixel_h, pixel_w = pixels.shape[:2]
left, top, motif_w = 71, 168+CONTENT_SHIFT_Y, 640
motif_h = motif_w*pixel_h/pixel_w
yy, xx = np.mgrid[0:pixel_h, 0:pixel_w]
canvas_x = left+(xx+.5)/pixel_w*motif_w
canvas_y = top+(yy+.5)/pixel_h*motif_h
# Wider, twice-smooth feathering removes abrupt peripheral rod endings.
# Multiply the edge fades so their corners also transition smoothly.
edge = np.ones_like(canvas_x)
for distance in [(canvas_x-196)/66, (594-canvas_x)/66,
                 (canvas_y-(270+CONTENT_SHIFT_Y))/48,
                 (550+CONTENT_SHIFT_Y-canvas_y)/64]:
    s = np.clip(distance, 0, 1)
    edge *= s*s*s*(s*(6*s-15)+10)
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
# Optical correction for the italic t overhang plus the broad white outline.
text(label_x, label_y, r"$t\,>0$", size=9.8, color="#6B278F", zorder=6,
     path_effects=[patheffects.Stroke(linewidth=1.0, foreground="white"),
                   patheffects.Stroke(linewidth=.23, foreground="#6B278F"), patheffects.Normal()])

# Centres and text wrapping follow the revised region sizes.
text((108+SPLIT_X)/2, 72, "Frustrated", color="#1265a2", weight="bold")
text((SPLIT_X+934)/2, 72, "Unfrustrated", color="#8b6006", weight="bold")
text(65, (112+SPLIT_Y)/2+YLABEL_SHIFT_Y, "Satisfy TRS/RP criteria", color="#1265a2", weight="bold", rotation=90)
text(65, (SPLIT_Y+938)/2+YLABEL_SHIFT_Y, "Violate TRS/RP criteria", color="#626b75", weight="bold", rotation=90)
status_texts = [
    (text(367, 612+CONTENT_SHIFT_Y, "Sign-free for BAFQMC", size=7.6, color="#1265a2", fontstyle="italic"),
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
    "Description": "Enlarged frustrated TRS/RP region, recessed New sign-free regime plaque, and triangular-lattice hopping."})
svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines())+"\n")
plt.close(fig)
subprocess.run(["pdftoppm", "-singlefile", "-r", "450", "-png", str(pdf_path), str(OUT / NAME)], check=True)
with fitz.open(pdf_path) as doc:
    assert len(doc) == 1 and abs(doc[0].rect.width*25.4/72-MM) < .01
manifest = {"width_mm": MM, "height_mm": MM, "split_x": SPLIT_X, "split_y": SPLIT_Y,
            "upper_left_area_fraction": round((SPLIT_X-108)*(SPLIT_Y-112)/(854*826), 3),
            "card_radius": CARD_RADIUS, "plaque_radius": CARD_RADIUS,
            "plaque_text": "New sign-free regime", "plaque_left_top_margin": PLAQUE_MARGIN,
            "plaque_corner_path": "same FancyBboxPatch path as cards",
            "plaque_font_pt": 6.6, "plaque_weight": "normal",
            "content_shift_y": CONTENT_SHIFT_Y,
            "ylabel_shift_y": YLABEL_SHIFT_Y,
            "motif_width": motif_w,
            "motif_fade_bounds": [196, 594, 270+CONTENT_SHIFT_Y, 550+CONTENT_SHIFT_Y],
            "motif_feather_widths": [66, 66, 48, 64],
            "status_linespacing": 1.6,
            "card_stack": ["grey backing", "translucent gold", "translucent blue"],
            "overlap_color": "source-over composite of two continuous 2D gradients",
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
