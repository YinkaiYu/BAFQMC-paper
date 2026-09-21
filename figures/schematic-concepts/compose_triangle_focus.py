"""Overlay crisp hopping notation on the standalone Blender design study."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MplPath
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "pdf" / "triangle-focus-draft"
data = json.loads((OUT / "projection.json").read_text())
render = Image.open(OUT / "lattice-render.png").convert("RGBA")
width, height = render.size
# The rods are rendered with one opaque material. Apply a common editorial fade
# to the finished image, using distance in the lattice plane, so the three
# surrounding triangles recede consistently despite their perspective sizes.
pixels = np.asarray(render).copy()
y_grid, x_grid = np.mgrid[0:height, 0:width]
rows, values = [], []
for reference in data["plane_reference"]:
    x, y = reference["world"]
    u, v = reference["image"]
    rows += [[x, y, 1, 0, 0, 0, -u*x, -u*y],
             [0, 0, 0, x, y, 1, -v*x, -v*y]]
    values += [u, v]
homography = np.append(np.linalg.solve(rows, values), 1).reshape(3, 3)
inverse = np.linalg.inv(homography)
u, v = (x_grid+.5)/width, (y_grid+.5)/height
denominator = inverse[2, 0]*u + inverse[2, 1]*v + inverse[2, 2]
world_x = (inverse[0, 0]*u + inverse[0, 1]*v + inverse[0, 2])/denominator
world_y = (inverse[1, 0]*u + inverse[1, 1]*v + inverse[1, 2])/denominator
distance = np.full((height, width), np.inf)
cross_products = []
triangle = np.asarray(data["core_world"])
for start, end in zip(triangle, np.roll(triangle, -1, axis=0)):
    edge = end-start
    dx, dy = world_x-start[0], world_y-start[1]
    fraction = np.clip((dx*edge[0]+dy*edge[1])/np.dot(edge, edge), 0, 1)
    distance = np.minimum(distance, np.hypot(dx-fraction*edge[0], dy-fraction*edge[1]))
    cross_products.append(edge[0]*dy-edge[1]*dx)
inside = np.logical_and.reduce([cross >= 0 for cross in cross_products])
inside |= np.logical_and.reduce([cross <= 0 for cross in cross_products])
distance[inside] = 0
lattice_fade = .65*np.exp(-(distance/1.05)**2) + .35*np.exp(-(distance/1.65)**2)
radius = np.sqrt(((x_grid/width-.5)/.5)**2 + ((y_grid/height-.55)/.42)**2)
fade = np.clip((1.0-radius)/.34, 0, 1)
fade = fade*fade*(3-2*fade)
pixels[:, :, 3] = (pixels[:, :, 3]*fade*lattice_fade).astype(np.uint8)
render = Image.fromarray(pixels)
# Warm, low-intensity halos follow the projected sphere sizes and the same fade.
halo_alpha = np.zeros((height, width))
for site in data["halo_sites"]:
    cx, cy = site["center"]
    rx = site["radius_x"]
    ry = rx*width/height
    squared_radius = ((u-cx)/rx)**2 + ((v-cy)/ry)**2
    halo_alpha = np.maximum(halo_alpha, .48*np.exp(-squared_radius/(2*1.20**2)))
halo = np.zeros((height, width, 4), dtype=np.uint8)
halo[:, :, :3] = [239, 131, 114]
halo[:, :, 3] = (255*halo_alpha*fade*lattice_fade).astype(np.uint8)
plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "stixsans",
                     "svg.fonttype": "path", "pdf.fonttype": 42})
crop = (0, 1, .15, .98)
fig = plt.figure(figsize=(11, 11*height/width*(crop[3]-crop[2])/(crop[1]-crop[0])),
                 facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set(xlim=crop[:2], ylim=(crop[3], crop[2]), aspect="auto")
ax.axis("off")
ax.imshow(halo, extent=(0, 1, 1, 0), aspect="auto", zorder=1)
ax.imshow(render, extent=(0, 1, 1, 0), aspect="auto", zorder=2)
for points in data["arcs"]:
    # Construct a smoothly tapering ribbon in image pixels, then map back to
    # normalized coordinates. Its width stays physical under perspective/crop.
    scale = np.array([width, height])
    center = np.asarray(points)*scale
    # The 3D curve runs exactly between site centres. Clip it to the projected
    # sphere silhouettes, with a small overlap so neither end floats off-site.
    source, target = data["hopping_sites"]
    source_distance = np.linalg.norm(center-np.asarray(source["center"])*scale, axis=1)
    target_distance = np.linalg.norm(center-np.asarray(target["center"])*scale, axis=1)
    source_radius = .92*source["radius_x"]*width
    target_radius = .88*target["radius_x"]*width
    first = int(np.flatnonzero(source_distance >= source_radius)[0])
    last = int(np.flatnonzero(target_distance >= target_radius)[-1])
    start_fraction = ((source_radius-source_distance[first-1]) /
                      (source_distance[first]-source_distance[first-1]))
    end_fraction = ((target_distance[last]-target_radius) /
                    (target_distance[last]-target_distance[last+1]))
    start = center[first-1] + start_fraction*(center[first]-center[first-1])
    end = center[last] + end_fraction*(center[last+1]-center[last])
    center = np.vstack([start, center[first:last+1], end])
    tangent = np.gradient(center, axis=0)
    tangent /= np.linalg.norm(tangent, axis=1)[:, None]
    normal = np.column_stack([-tangent[:, 1], tangent[:, 0]])
    length = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(center, axis=0), axis=1))])
    fraction = length/length[-1]
    neck = int(np.searchsorted(fraction, .865))
    half_width = width*(.0004 + .0068*np.sin(np.pi*fraction)**.85)
    upper = center[:neck+1] + normal[:neck+1]*half_width[:neck+1, None]
    lower = center[:neck+1] - normal[:neck+1]*half_width[:neck+1, None]
    head_width = width*.0145
    outline = np.vstack([upper, center[neck]+normal[neck]*head_width,
                         center[-1], center[neck]-normal[neck]*head_width,
                         lower[::-1], upper[:1]])/scale
    codes = [MplPath.MOVETO] + [MplPath.LINETO]*(len(outline)-2) + [MplPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MplPath(outline, codes), facecolor="#7835A0",
                           edgecolor="none", zorder=3,
                           path_effects=[path_effects.Stroke(linewidth=2.2, foreground="white"),
                                         path_effects.Normal()]))
x, y = data["hopping_label"]
ax.text(x, y, r"$t>0$", ha="center", va="center", fontsize=40,
        color="#6B278F", zorder=4,
        path_effects=[path_effects.Stroke(linewidth=4, foreground="white"),
                      path_effects.Stroke(linewidth=.9, foreground="#6B278F"),
                      path_effects.Normal()])
fig.savefig(OUT / "triangle-focus-draft.png", dpi=200)
fig.savefig(OUT / "triangle-focus-draft.pdf", dpi=400,
            metadata={"Title": "Frustrated triangular-lattice hopping: standalone design study"})
plt.close(fig)
print(OUT / "triangle-focus-draft.png")
