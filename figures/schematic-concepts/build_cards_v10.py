"""Compose the focused C figure from 3D glass, 3D motifs and vector labels."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

import fitz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from PIL import Image, ImageFilter
from matplotlib.patches import FancyBboxPatch, Rectangle, PathPatch
from matplotlib.path import Path as MplPath


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "pdf" / "schematic-concepts"
ASSETS = OUT / "C_refined_v5_assets"
parser = argparse.ArgumentParser()
parser.add_argument("--background", choices=["glass", "cards"], default="cards")
args = parser.parse_args()
NAME = "C_refined_cards_v10_raised_type"
if args.background != "cards":
    raise ValueError("This revision targets the selected card design.")
# Register an installed open font explicitly; Matplotlib's cache may predate it.
font_path = Path("/usr/share/fonts/truetype/freefont/FreeSans.ttf")
if font_path.exists():
    font_manager.fontManager.addfont(str(font_path))


plt.rcParams.update({
    "font.family": "FreeSans",
    "mathtext.fontset": "dejavusans",
    "svg.fonttype": "path",
    "pdf.fonttype": 42,
    "image.composite_image": False,
    "savefig.facecolor": "white",
})

W, H, MM = 1000, 1000, 86
fig = plt.figure(figsize=(MM/25.4, MM/25.4))
ax = fig.add_axes([0, 0, 1, 1])
ax.set(xlim=(0, W), ylim=(H, 0), aspect="equal")
ax.axis("off")
texts = []


def text(x, y, value, size=8.8, color="#282b32", weight="normal", **kwargs):
    obj = ax.text(x, y, value, fontsize=size, color=color,
                  ha=kwargs.pop("ha", "center"), va="center",
                  weight=weight, **kwargs)
    texts.append(obj)


def motif(path, box, glow=False):
    """Trim transparent margins while retaining a small margin for soft shadows."""
    rgba = np.array(Image.open(path).convert("RGBA"))
    # Remove the faint denoising matte offset before finding the footprint;
    # otherwise the shadow catcher can leave a rectangular cut edge.
    rgba[:,:,3] = np.clip((rgba[:,:,3].astype(float)-12)*255/243, 0, 255).astype(np.uint8)
    mask = rgba[:,:,3] > 0
    ys, xs = np.nonzero(mask)
    if not len(xs):
        raise ValueError(f"Empty 3D render: {path}")
    pad = 12
    left, right = max(0, xs.min()-pad), min(rgba.shape[1], xs.max()+pad+1)
    top, bottom = max(0, ys.min()-pad), min(rgba.shape[0], ys.max()+pad+1)
    crop = rgba[top:bottom, left:right]
    x0, y0, x1, y1 = box
    factor = min((x1-x0)/crop.shape[1], (y1-y0)/crop.shape[0])
    dw, dh = crop.shape[1]*factor, crop.shape[0]*factor
    cx, cy = (x0+x1)/2, (y0+y1)/2
    if glow:
        # Light follows the mesh and particle silhouettes, never a spotlight disk.
        padding=170
        alpha=np.pad(crop[:,:,3],padding)
        halo=Image.fromarray(alpha).filter(ImageFilter.MaxFilter(41)).filter(ImageFilter.GaussianBlur(48))
        light=np.zeros((*alpha.shape,4),dtype=np.uint8)
        light[:,:,:3]=(223,252,255)
        light[:,:,3]=(np.asarray(halo).astype(float)*.85).astype(np.uint8)
        px,py=padding*factor,padding*factor
        ax.imshow(light,extent=(cx-dw/2-px,cx+dw/2+px,cy+dh/2+py,cy-dh/2-py),
                  interpolation="antialiased",zorder=4)
    ax.imshow(crop, extent=(cx-dw/2, cx+dw/2, cy+dh/2, cy-dh/2),
              interpolation="antialiased", zorder=5)
    return {
        "source": path.name,
        "crop_pixels": [int(crop.shape[1]), int(crop.shape[0])],
        "placed_mm": [round(dw*MM/W,2), round(dh*MM/H,2)],
        "effective_dpi": round(crop.shape[1]/(dw*MM/W/25.4)),
    }


# Independently colored layers prevent the neutral base from dulling the cards.
background = None
# Neutral diagonal gradient, darkest at lower left and lightest at upper right.
# Confined to the exposed base so it cannot alter the independent card hues.
gy,gx=np.mgrid[0:600,0:600]/599
blend=(gx+1-gy)/2
blend=blend*blend*(3-2*blend)
dark=np.array([200,208,217])/255
pale=np.array([239,242,246])/255
gray=dark[None,None,:]*(1-blend[:,:,None])+pale[None,None,:]*blend[:,:,None]
ax.imshow(gray,extent=(164,548,910,538),interpolation="bicubic",zorder=0)
cards={}
for name,box,color,z in [("gold",(548,140,386,798),"#f8d479",1),
                         ("blue",(108,112,854,426),"#99d1f5",2)]:
    x,y,w,h=box
    for spread in range(12,0,-1):
        ax.add_patch(FancyBboxPatch((x-spread,y+8-spread),w+2*spread,h+2*spread,
            boxstyle="round,pad=0,rounding_size=20",linewidth=0,
            facecolor="#344253",alpha=.003,zorder=z))
    card=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=20",
        linewidth=0,facecolor=color,zorder=z+.1)
    ax.add_patch(card)
    cards[name]=card
# The visible intersection is given a clean third hue, independent of gray.
overlap=FancyBboxPatch((548,140),386,798,
    boxstyle="round,pad=0,rounding_size=20",linewidth=0,
    facecolor="#a2dccd",zorder=2.2)
ax.add_patch(overlap)
overlap.set_clip_path(cards["blue"])
# Only exterior card rims are drawn; no hidden base edges show through.
for box,z in [((548,140,386,798),1.2),((108,112,854,426),2.3)]:
    x,y,w,h=box
    ax.add_patch(FancyBboxPatch((x,y),w,h,
        boxstyle="round,pad=0,rounding_size=20",fill=False,
        linewidth=.35,edgecolor="white",alpha=.85,zorder=z))

text(326, 72, "Frustrated", size=7.9)
text(747, 72, "Unfrustrated", size=7.9)
text(65, 325, "Within symmetry criteria", size=7.9, rotation=90)
text(65, 737, "Outside symmetry criteria", size=7.9, rotation=90)

text(333, 493, "Sign-free for BAFQMC", size=7.6, color="#1265a2")
text(741, 339, "Sign-free for both", size=7.6, color="#24745b")
text(741, 869, "Sign-free for WLQMC/SSE", size=7.6, color="#8b6006")
text(356, 724, "Sign-problematic", size=7.6, color="#626b75")

placements = [
    motif(ASSETS / "interaction.png", (181, 157, 281, 227)),
    motif(ASSETS / "field.png", (191, 247, 548, 441), glow=True),
    motif(ASSETS / "loop.png", (628, 628.2, 852, 781.8)),
]
# A curved ribbon widens toward the foreground; the distant end is almost a point.
vertices=[(286,286),(300,288),(316,296),(329,306),
          (334,301),(349,326),(323,315),(328,312),
          (314,302),(299,292),(286,288),(286,286)]
vertices=[(x,y-80) for x,y in vertices]
codes=[MplPath.MOVETO]+[MplPath.CURVE4]*3+[MplPath.LINETO]*4+[MplPath.CURVE4]*3+[MplPath.CLOSEPOLY]
ribbon=PathPatch(MplPath(vertices,codes),facecolor="none",edgecolor="#377fab",linewidth=.25,zorder=8)
ax.add_patch(ribbon)
gradient=np.zeros((160,160,4))
gradient[:,:,:3]=np.linspace([.53,.78,.92],[.12,.40,.62],160)[:,None,:]
gradient[:,:,3]=np.linspace(.38,.92,160)[:,None]
im=ax.imshow(gradient,extent=(258,373,268,193),zorder=7,interpolation="bicubic")
im.set_clip_path(ribbon)

fig.canvas.draw()
# Check the two one-line headings against their glass interiors.
for obj in texts:
    if obj.get_text() in ("Sign-free for BAFQMC", "Sign-free for WLQMC/SSE"):
        bounds = obj.get_window_extent(fig.canvas.get_renderer()).transformed(ax.transData.inverted())
        left, right = ((128, 534) if "BAFQMC" in obj.get_text() else (560, 922))
        if bounds.x0 < left or bounds.x1 > right:
            raise AssertionError(f"Coverage label exceeds glass interior: {obj.get_text()}")

renderer = fig.canvas.get_renderer()
for obj in texts:
    bounds = obj.get_window_extent(renderer)
    if bounds.x0 < 0 or bounds.y0 < 0 or bounds.x1 > fig.bbox.x1 or bounds.y1 > fig.bbox.y1:
        raise AssertionError(f"Clipped text: {obj.get_text()}")

pdf_path = OUT / f"{NAME}.pdf"
fig.savefig(pdf_path, dpi=900, metadata={
    "Title": "Sign-free bosonic QMC: focused three-dimensional concept C",
    "Author": "BAFQMC manuscript figure study",
})
fig.savefig(OUT / f"{NAME}.svg", dpi=900, metadata={
    "Title": "Focused three-dimensional concept C",
    "Description": (
        "Offset upper and right half-planes with two physical motifs only: "
        "an HS transformation into a fixed-field bosonic scene in the frustrated TRS/RP region and "
        "four equal interacting bosons in the unfrustrated local-weight region."
    ),
})
plt.close(fig)

subprocess.run([
    "pdftoppm", "-singlefile", "-r", "450", "-png",
    str(pdf_path), str(OUT / NAME),
], check=True)

doc = fitz.open(pdf_path)
if len(doc) != 1:
    raise AssertionError("Expected one-page figure")
page = doc[0]
if abs(page.rect.width*25.4/72-MM) > .01:
    raise AssertionError("Wrong physical width")
manifest = {
    "width_mm": MM, "height_mm": MM,
    "font_min_pt": min(t.get_fontsize() for t in texts),
    "text_count": len(texts),
    "illustrated_quadrants": ["upper-left", "lower-right"],
    "physical_motif_count": 2,
    "directional_arrows": 1,
    "background_pixels": list(background.size) if background else None,
    "background_dpi": round(background.width/(MM/25.4)) if background else None,
    "render_placements": placements,
    "background_style": args.background,
    "format": "3D physics motifs with vector labels and glass or vector-card background",
    "bounds_check": "pass",
    "pdf_pages": len(doc),
}
(OUT / f"{NAME}_manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
doc.close()
print(json.dumps(manifest, indent=2))
