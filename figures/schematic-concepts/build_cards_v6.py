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
NAME = "C_refined_cards_v6"
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
        padding=80
        alpha=np.pad(crop[:,:,3],padding)
        halo=Image.fromarray(alpha).filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.GaussianBlur(22))
        light=np.zeros((*alpha.shape,4),dtype=np.uint8)
        light[:,:,:3]=(223,252,255)
        light[:,:,3]=(np.asarray(halo).astype(float)*.72).astype(np.uint8)
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


# Offset, beveled glass half-planes retain the original layered classification.
# Their overlap represents the two available sign-free routes.
background = None
if args.background == "glass":
    background = Image.open(ASSETS / "background.png")
    ax.imshow(background, extent=(0,W,H,0), interpolation="antialiased", zorder=0)
    for box, color in [((548,140,386,798), "#c8bb94"),
                       ((108,112,854,426), "#a5c8e3")]:
        x,y,w,h=box
        ax.add_patch(FancyBboxPatch((x,y),w,h,
            boxstyle="round,pad=0,rounding_size=32", fill=False,
            linewidth=.28, edgecolor=color, alpha=.52, zorder=1))
else:
    # Flat cards: depth is conveyed only by consistent overhang and soft shadows.
    ax.add_patch(Rectangle((164,168),742,742,facecolor="#f0f2f5",edgecolor="none",zorder=0))
    for box,color,opacity,z in [((548,140,386,798),"#ffc342",.64,1),
                                ((108,112,854,426),"#39a8f5",.48,2)]:
        x,y,w,h=box
        for spread in range(12,0,-1):
            ax.add_patch(FancyBboxPatch((x-spread,y+8-spread),w+2*spread,h+2*spread,
                boxstyle="round,pad=0,rounding_size=20", linewidth=0,
                facecolor="#344253",alpha=.004,zorder=z))
        ax.add_patch(FancyBboxPatch((x,y),w,h,
            boxstyle="round,pad=0,rounding_size=20",linewidth=.35,
            edgecolor="white",facecolor=color,alpha=opacity,zorder=z+.1))

text(326, 72, "Frustrated", size=9.1)
text(747, 72, "Unfrustrated", size=9.1)
text(65, 325, "Within symmetry criteria", size=7.9, rotation=90)
text(65, 737, "Outside symmetry criteria", size=7.9, rotation=90)

text(333, 198, "Sign-free for BAFQMC", size=7.6, color="#1265a2")
text(741, 339, "Sign-free for both", size=8.7, color="#282b32")
text(741, 611, "Sign-free for WLQMC/SSE", size=7.6, color="#8b6006")
text(356, 724, "Sign-problematic", size=8.7, color="#282b32")

placements = [
    motif(ASSETS / "interaction.png", (181, 237, 281, 307)),
    motif(ASSETS / "field.png", (191, 327, 548, 521), glow=True),
    motif(ASSETS / "loop.png", (600, 678, 880, 870)),
]
# A curved ribbon widens toward the foreground; the distant end is almost a point.
vertices=[(281,286),(300,286),(315,293),(337,310),
          (344,301),(369,344),(321,326),(330,320),
          (313,304),(298,290),(281,288),(281,286)]
codes=[MplPath.MOVETO]+[MplPath.CURVE4]*3+[MplPath.LINETO]*4+[MplPath.CURVE4]*3+[MplPath.CLOSEPOLY]
ribbon=PathPatch(MplPath(vertices,codes),facecolor="none",edgecolor="#377fab",linewidth=.25,zorder=8)
ax.add_patch(ribbon)
gradient=np.zeros((160,160,4))
gradient[:,:,:3]=np.linspace([.53,.78,.92],[.12,.40,.62],160)[:,None,:]
gradient[:,:,3]=np.linspace(.38,.92,160)[:,None]
im=ax.imshow(gradient,extent=(258,373,348,273),zorder=7,interpolation="bicubic")
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
