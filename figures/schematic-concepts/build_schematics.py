#!/usr/bin/env python3
"""Vector concept studies for BAFQMC Fig. 1; run in the repository's WSL env."""

from __future__ import annotations

import json
from pathlib import Path

import fitz
import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Polygon, Rectangle


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "pdf" / "schematic-concepts"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#23394c"
MUTED = "#64737e"
LINE = "#aebbc1"
RED = "#bf514c"
RED_LIGHT = "#fae9e6"
TEAL = "#177d88"
TEAL_DARK = "#155c68"
TEAL_LIGHT = "#e7f4f5"
GOLD = "#a77b31"
GOLD_LIGHT = "#f6eedc"
SAGE = "#edf1e3"
PURPLE = "#836b99"
GRAY = "#f1f2f2"
WHITE = "#ffffff"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
        "svg.fonttype": "path",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.linewidth": 0.6,
        "savefig.facecolor": WHITE,
        "path.simplify": False,
    }
)


class Canvas:
    def __init__(self, width, height, width_mm, title):
        self.width, self.height = width, height
        self.width_mm = width_mm
        self.title = title
        self.fig = plt.figure(
            figsize=(width_mm / 25.4, width_mm * height / width / 25.4)
        )
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set(xlim=(0, width), ylim=(height, 0), aspect="equal")
        self.ax.axis("off")
        self.texts = []

    def text(self, x, y, value, size=8, color=INK, weight="normal", **kwargs):
        obj = self.ax.text(
            x, y, value, fontsize=size, color=color, weight=weight,
            ha=kwargs.pop("ha", "center"), va=kwargs.pop("va", "center"),
            **kwargs,
        )
        self.texts.append(obj)
        return obj

    def line(self, a, b, color=LINE, lw=0.7, **kwargs):
        return self.ax.plot(
            [a[0], b[0]], [a[1], b[1]], color=color, lw=lw,
            solid_capstyle="round", **kwargs,
        )[0]

    def arrow(self, a, b, color=INK, lw=1.0, head=7, **kwargs):
        patch = FancyArrowPatch(
            a, b, arrowstyle="-|>", mutation_scale=head,
            color=color, linewidth=lw, shrinkA=0, shrinkB=0, **kwargs
        )
        self.ax.add_patch(patch)
        return patch

    def polygon(self, points, fill, edge="none", lw=0.6, **kwargs):
        p = Polygon(points, closed=True, facecolor=fill, edgecolor=edge,
                    linewidth=lw, **kwargs)
        self.ax.add_patch(p)
        return p

    def circle(self, x, y, r, fill=WHITE, edge=INK, lw=0.7, **kwargs):
        p = Circle((x, y), r, facecolor=fill, edgecolor=edge,
                   linewidth=lw, **kwargs)
        self.ax.add_patch(p)
        return p

    def save(self, stem):
        self.fig.canvas.draw()
        renderer = self.fig.canvas.get_renderer()
        bounds = self.fig.bbox
        failures = []
        for item in self.texts:
            box = item.get_window_extent(renderer)
            if (box.x0 < bounds.x0 - 0.3 or box.y0 < bounds.y0 - 0.3
                    or box.x1 > bounds.x1 + 0.3 or box.y1 > bounds.y1 + 0.3):
                failures.append(item.get_text())
        if failures:
            raise RuntimeError(f"{stem}: text outside canvas: {failures}")
        pdf = OUT / f"{stem}.pdf"
        self.fig.savefig(
            pdf, metadata={"Title": self.title,
                           "Author": "BAFQMC figure concept study"}
        )
        self.fig.savefig(
            OUT / f"{stem}.svg",
            metadata={
                "Title": self.title,
                "Description": (
                    "Conceptual, not numerical: local negative hopping loops "
                    "versus a fixed-field global trace under TRS or RP."
                ),
            },
        )
        self.fig.savefig(OUT / f"{stem}.png", dpi=360)
        record = {
            "name": stem, "title": self.title,
            "width_mm": self.width_mm,
            "height_mm": round(self.width_mm * self.height / self.width, 2),
            "minimum_font_pt": min(x.get_fontsize() for x in self.texts),
            "text_bounds": "pass",
        }
        plt.close(self.fig)
        return record


def particle(c, x, y, r=9, color=INK, dimensional=False):
    if dimensional:
        c.ax.add_patch(
            Ellipse((x + 1.1, y + r * 1.6), r * 2.2, r * 0.6,
                    color=INK, alpha=0.065, lw=0)
        )
    c.circle(x, y, r, color, edge=WHITE, lw=0.65)
    if dimensional:
        c.circle(x - r * 0.28, y - r * 0.29, r * 0.27,
                 WHITE, edge="none", alpha=0.42)


def wavy(c, a, b, amplitude=3, cycles=4, color=PURPLE, lw=1.0):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    normal = np.array([-d[1], d[0]]) / np.linalg.norm(d)
    t = np.linspace(0.08, 0.92, 180)
    envelope = np.clip(np.sin(np.pi * (t - 0.08) / 0.84), 0, None) ** 0.4
    pts = a + t[:, None] * d + (
        amplitude * np.sin(2 * np.pi * cycles * (t - 0.08) / 0.84)
        * envelope
    )[:, None] * normal
    c.ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw,
              solid_capstyle="round")


def interaction(c, cx, cy, scale=1, count=2, dimensional=False):
    if count == 2:
        points = [(cx, cy - 28 * scale), (cx, cy + 28 * scale)]
        wavy(c, *points, amplitude=3.7 * scale)
    else:
        points = [
            (cx - 38 * scale, cy - 20 * scale),
            (cx + 40 * scale, cy - 5 * scale),
            (cx - 7 * scale, cy + 43 * scale),
        ]
        for i in range(3):
            wavy(c, points[i], points[(i + 1) % 3],
                 amplitude=2.8 * scale)
    for x, y in points:
        particle(c, x, y, 8.5 * scale, dimensional=dimensional)
    return points


def loop(c, cx, cy, radius=66, n=3, signs=True, negative=True,
         dimensional=False, faint=False, ghost_lattice=False):
    color = RED if negative else GOLD
    if faint:
        color = "#b17d77"
    angle = -np.pi / 2 + np.arange(n) * 2 * np.pi / n
    if n == 4:
        angle += np.pi / 4
    points = np.column_stack(
        [cx + radius * np.cos(angle), cy + radius * np.sin(angle)]
    )
    if ghost_lattice and n == 3:
        # A small triangular patch makes the highlighted cycle a local object.
        spacing = radius * np.sqrt(3)
        grid = []
        for j in range(-2, 3):
            for i in range(-2, 3):
                p = np.array([cx + spacing * (i + j / 2),
                              cy - radius + spacing * np.sqrt(3) * j / 2])
                if abs(p[0] - cx) < radius * 1.62 and abs(p[1] - cy) < radius * 1.42:
                    grid.append(p)
        for i, a in enumerate(grid):
            for b in grid[i + 1:]:
                if np.isclose(np.linalg.norm(a - b), spacing):
                    c.line(a, b, "#dbe2e4", 0.55, zorder=-2)
        for x, y in grid:
            c.circle(x, y, radius * 0.030, "#e2e7e9", "none", zorder=-1)
    c.polygon(points, RED_LIGHT if negative else GOLD_LIGHT, alpha=0.65)
    for i, a in enumerate(points):
        b = points[(i + 1) % n]
        c.line(a, b, LINE, 0.65)
        d = b - a
        mid = (a + b) / 2
        normal = (mid - [cx, cy])
        normal /= np.linalg.norm(normal)
        offset = normal * radius * 0.06
        c.arrow(a + 0.20 * d + offset, a + 0.77 * d + offset,
                color, lw=1.2, head=6.5)
        if signs:
            q = mid + normal * radius * 0.25
            c.text(*q, r"$-$", size=8.5, color=color)
    for i, (x, y) in enumerate(points):
        if i == n - 1:
            particle(c, x, y, radius * 0.10, RED if negative else GOLD,
                     dimensional=dimensional)
        else:
            c.circle(x, y, radius * 0.077, WHITE, INK, lw=0.65)
    return points


def flat_field(c, cx, cy, width=128, height=100, square=False):
    left, top = cx - width / 2, cy - height / 2
    nx, ny = 5, 4
    for j in range(ny):
        for i in range(nx):
            a = 0.08 + 0.10 * (
                0.5 + 0.5 * np.sin((i + 1) * 1.4 + j * 1.9)
            )
            c.polygon(
                [(left + i * width / nx, top + j * height / ny),
                 (left + (i + 1) * width / nx, top + j * height / ny),
                 (left + (i + 1) * width / nx, top + (j + 1) * height / ny),
                 (left + i * width / nx, top + (j + 1) * height / ny)],
                TEAL, alpha=a,
            )
    # The background encodes phi; thin lattice bonds survive decoupling.
    pts = np.array(
        [[cx, cy - height * .30], [cx + width * .30, cy + height * .29],
         [cx - width * .30, cy + height * .29]]
    )
    if square:
        pts = np.array(
            [[cx - width*.26, cy - height*.27],
             [cx + width*.26, cy - height*.27],
             [cx + width*.26, cy + height*.27],
             [cx - width*.26, cy + height*.27]]
        )
    for i, p in enumerate(pts):
        c.line(p, pts[(i + 1) % len(pts)], "#77a7ad", 0.65)
    for p in pts:
        c.circle(*p, 4.2, WHITE, TEAL, 0.6)
    # Each particle couples to the same fixed-field background, not to another
    # particle through a direct interaction line.
    for p in [pts[0], pts[-1]]:
        q = p + [0, -13]
        c.line(q, p, TEAL, 0.8)
        particle(c, *q, r=7.1)
    c.text(left + width + 7, top + 8, r"$\phi$", size=8.2, color=TEAL)


def field_surface(c, cx, cy, scale=80, layers=1, particles=True,
                  square=False, amplitude=0.12, particle_count=2):
    def project(u, v, layer):
        z = amplitude * np.sin(2.2 * u + 0.6) * np.cos(2.0 * v - 0.3)
        return np.array([
            cx + scale * (u + 0.48 * v),
            cy + scale * (0.46 * v - z) + layer * scale * 0.37,
        ])

    # Schematic time slices, deterministic for reproducible vector export.
    nu, nv = 9, 6
    us, vs = np.linspace(-1, 1, nu + 1), np.linspace(-1, 1, nv + 1)
    for layer in reversed(range(layers)):
        for j in reversed(range(nv)):
            for i in range(nu):
                u0, u1, v0, v1 = us[i], us[i + 1], vs[j], vs[j + 1]
                p = [project(u0, v0, layer), project(u1, v0, layer),
                     project(u1, v1, layer), project(u0, v1, layer)]
                shade = 0.13 + .22 * (
                    .5 + .5 * np.sin(2.7 * (u0 + u1) / 2 + 1.3 * layer)
                    * np.cos(2.1 * (v0 + v1) / 2 - 0.7)
                )
                rgb = np.array(mcolors.to_rgb(TEAL))
                face = 1 - shade * (1 - rgb)
                c.polygon(p, face, edge=WHITE, lw=.18,
                          alpha=1 if layer == 0 else .58)
        if layer == 0:
            edges = [
                [project(u, -1, layer) for u in us],
                [project(u, 1, layer) for u in us],
                [project(-1, v, layer) for v in vs],
                [project(1, v, layer) for v in vs],
            ]
            for pp in edges:
                pp = np.array(pp)
                c.ax.plot(pp[:, 0], pp[:, 1], color="#9bbec2", lw=.5)

    if square:
        lattice = [(-.50, -.52), (.52, -.52), (.52, .52), (-.50, .52)]
    else:
        lattice = [(-.55, -.48), (.55, -.48), (0.0, .57)]
    projected = [project(u, v, 0) for u, v in lattice]
    for i, p in enumerate(projected):
        c.line(p, projected[(i + 1) % len(projected)], "#6e9aa3", .75)
    for i, p in enumerate(projected):
        c.ax.add_patch(
            Ellipse(p, scale*.10, scale*.05, facecolor=WHITE,
                    edgecolor=TEAL, lw=.55)
        )
    if particles:
        occupied = list(range(len(lattice))) if particle_count == 3 else [0, len(lattice) - 1]
        for i in occupied:
            p = projected[i]
            q = p + [0, -scale * .23]
            c.line(q, p, TEAL, .8)
            particle(c, *q, r=scale*.085, dimensional=True)
    c.text(cx + scale * 1.38, cy - scale * .60, r"$\phi$",
           size=8.4, color=TEAL)
    return project


def tiny_lattice(c, cx, cy, radius=13, n=3, color=TEAL):
    angles = -np.pi / 2 + np.arange(n) * 2 * np.pi / n
    if n == 4:
        angles += np.pi / 4
    pp = np.column_stack(
        [cx + radius * np.cos(angles), cy + radius * np.sin(angles)]
    )
    for i, p in enumerate(pp):
        c.line(p, pp[(i + 1) % n], color, .5, alpha=.6)
        c.circle(*p, radius*.09, color, "none")


def classification(c, x, y, w, h, font=7.3, heading=False,
                   side_labels=True, icons=True):
    colors = [TEAL_LIGHT, SAGE, GRAY, GOLD_LIGHT]
    for row in range(2):
        for col in range(2):
            xx, yy = x + col * w/2, y + row*h/2
            c.ax.add_patch(
                Rectangle((xx, yy), w/2, h/2,
                          facecolor=colors[row*2 + col],
                          edgecolor=WHITE, lw=2)
            )
    c.ax.add_patch(
        Rectangle((x+1.5, y+1.5), w/2-3, h/2-3,
                  fill=False, edgecolor=TEAL, lw=.95)
    )
    c.text(x+w/4, y-19, "Frustrated", size=font)
    c.text(x+w*3/4, y-19, "Unfrustrated", size=font)
    if side_labels:
        c.text(x-12, y+h/4, "TRS / RP", size=font-0.1, ha="right")
        c.text(x-12, y+h*3/4, "Neither", size=font-0.1, ha="right",
               color=MUTED)
    else:
        c.text(x-17, y+h/4, "TRS / RP", size=font-.2, rotation=90)
        c.text(x-17, y+h*3/4, "Neither", size=font-.2,
               rotation=90, color=MUTED)
    for row in range(2):
        for col in range(2):
            cx, cy = x+(col+.5)*w/2, y+(row+.5)*h/2
            if icons:
                tiny_lattice(c, cx, cy-17, radius=12,
                             n=3 if col == 0 else 4,
                             color=TEAL if row == 0 else MUTED if col == 0 else GOLD)
    dy = 11 if icons else 0
    c.text(x+w/4, y+h/4+dy, "BAFQMC", size=font+.5,
           color=TEAL_DARK, weight="medium")
    c.text(x+w*3/4, y+h/4+dy, "Both", size=font+.5)
    c.text(x+w*3/4, y+h*3/4+dy, "WL / SSE", size=font+.2, color=GOLD)


def make_a():
    c = Canvas(600, 624, 86, "A — Local loop and global field")
    c.text(24, 23, "(a)", size=7.6, ha="left", weight="bold")
    c.text(164, 23, "Local weights", size=8.8, weight="medium")
    c.text(164, 51, "World-line / SSE", size=7.0, color=MUTED)
    c.text(310, 23, "(b)", size=7.6, ha="left", weight="bold")
    c.text(456, 23, "Global weight", size=8.8, weight="medium")
    c.text(456, 51, "BAFQMC", size=7.0, color=TEAL)
    loop(c, 163, 157, radius=69)
    c.text(164, 256, r"$w_{\rm loop}<0$", size=9.0, color=RED)

    interaction(c, 334, 159, scale=.86)
    c.arrow((367, 157), (414, 157), INK, 0.9, head=6.3)
    c.text(389, 135, "HS", size=7.1, color=MUTED)
    flat_field(c, 497, 161, width=123, height=103)
    c.arrow((497, 221), (497, 240), TEAL, .7, head=5.5)
    c.text(523, 229, r"$\mathrm{Tr}$", size=7.0, color=TEAL_DARK)
    c.text(455, 264, r"$\mathrm{TRS\ or\ RP}\;\Rightarrow\;W(\phi)\geq0$",
           size=7.65, color=TEAL_DARK)
    c.line((22, 292), (578, 292), "#d9dfe2", .55)
    c.text(24, 320, "(c)", size=7.6, ha="left", weight="bold")
    c.text(80, 320, "Sign-free regimes", size=8.2, ha="left")
    classification(c, 135, 373, 434, 214, font=7.25)
    return c.save("A_local_global")


def make_b():
    c = Canvas(1240, 490, 178, "B — Auxiliary-field landscape")
    c.text(27, 26, "(a)", size=8.5, ha="left", weight="bold")
    c.text(151, 26, "Local weights", size=9.5, weight="medium")
    c.text(151, 56, "World-line / SSE", size=7.5, color=MUTED)
    loop(c, 153, 225, radius=86, ghost_lattice=True, dimensional=True)
    c.text(151, 396, r"$w_{\rm loop}<0$", size=10, color=RED)

    c.line((301, 84), (301, 433), "#d9dfe2", .5)
    c.text(335, 26, "(b)", size=8.5, ha="left", weight="bold")
    c.text(613, 26, "Global weight", size=9.5, weight="medium")
    c.text(613, 56, "BAFQMC", size=7.5, color=TEAL)
    interaction(c, 415, 204, scale=1.25, count=3, dimensional=True)
    c.arrow((498, 215), (571, 215), INK, 1.05, head=8)
    c.text(535, 188, "HS", size=8.2, color=MUTED)
    field_surface(c, 738, 194, scale=102, layers=3, amplitude=.15, particle_count=3)

    # The brace encompasses the whole set of field slices, not a local path.
    c.line((593, 335), (593, 346), TEAL, .65)
    c.line((593, 346), (884, 346), TEAL, .65)
    c.line((884, 346), (884, 335), TEAL, .65)
    c.arrow((738, 352), (738, 379), TEAL, .7, head=5.5)
    c.text(765, 363, r"$\mathrm{Tr}$", size=7.5, color=TEAL_DARK)
    c.text(738, 405, r"$W(\phi)\geq0$", size=11.0, color=TEAL_DARK)
    c.text(738, 445, "TRS or RP", size=7.7, color=TEAL_DARK)

    c.line((922, 84), (922, 433), "#d9dfe2", .5)
    c.text(946, 26, "(c)", size=8.5, ha="left", weight="bold")
    c.text(1088, 26, "Sign-free regimes", size=8.6, weight="medium")
    classification(c, 975, 140, 238, 242, font=7.1, side_labels=False)
    return c.save("B_field_landscape")


def make_c():
    c = Canvas(920, 776, 128, "C — Illustrated sign-free regimes")
    x, y, w, h = 103, 69, 790, 663
    cw, rh = w/2, h/2
    for row, col, fill in [
        (0, 0, TEAL_LIGHT), (0, 1, SAGE),
        (1, 0, GRAY), (1, 1, GOLD_LIGHT),
    ]:
        c.ax.add_patch(
            Rectangle((x+col*cw, y+row*rh), cw, rh,
                      facecolor=fill, edgecolor=WHITE, lw=3)
        )
    c.ax.add_patch(
        Rectangle((x+2, y+2), cw-4, rh-4,
                  fill=False, edgecolor=TEAL, lw=1.1)
    )
    c.text(x+cw/2, 35, "Frustrated", size=10, weight="medium")
    c.text(x+cw*1.5, 35, "Unfrustrated", size=10, weight="medium")
    c.text(50, y+rh/2, "TRS / RP", size=9.3, rotation=90)
    c.text(50, y+rh*1.5, "Neither", size=9.3, rotation=90, color=MUTED)

    c.text(302, 106, "BAFQMC", size=10.5, color=TEAL_DARK, weight="medium")
    # HS operates inside a criterion-satisfying cell. It never points from a
    # 'neither' model to a criterion-satisfying one.
    points = loop(c, 161, 229, radius=44, signs=False)
    wavy(c, points[0] + [6, 0], points[2] + [6, 0],
         amplitude=2.4, cycles=3, lw=.8)
    for p in [points[0], points[2]]:
        particle(c, *p, r=5.5)
    c.arrow((211, 230), (241, 230), INK, .9, head=6.5)
    c.text(225, 209, "HS", size=7.5, color=MUTED)
    field_surface(c, 364, 225, scale=73, layers=2)
    c.arrow((364, 297), (364, 321), TEAL, .7, head=5.5)
    c.text(387, 308, r"$\mathrm{Tr}$", size=7.5, color=TEAL_DARK)
    c.text(307, 350, r"$W(\phi)\geq0$", size=10.4, color=TEAL_DARK)

    c.text(698, 106, "Both", size=10.5, color=INK, weight="medium")
    # Two small independent icons identify the two available formulations.
    loop(c, 595, 225, radius=47, n=4, signs=False, negative=False)
    field_surface(c, 784, 225, scale=56, layers=2, square=True, amplitude=.10)
    c.text(699, 350, r"$W\geq0$", size=10.4, color=TEAL_DARK)

    loop(c, 302, 557, radius=80, dimensional=False)
    c.text(302, 697, r"$w_{\rm loop}<0$", size=10.0, color=RED)
    c.text(697, 440, "WL / SSE", size=10.0, color=GOLD, weight="medium")
    loop(c, 697, 557, radius=80, n=4, signs=True, negative=False)
    c.text(697, 697, r"$w_{\rm loop}>0$", size=10.0, color=GOLD)
    return c.save("C_illustrated_map")


def comparison(records):
    page_w, page_h = 1000, 970
    doc = fitz.open()
    page = doc.new_page(width=page_w, height=page_h)
    gray = (.34, .40, .45)
    navy = (.13, .22, .29)
    page.insert_text((35, 34), "BAFQMC  /  FIGURE 1 CONCEPT STUDIES",
                     fontsize=11, fontname="hebo", color=navy)
    page.insert_text((35, 54), "Vector originals. Labels below belong to this review sheet only.",
                     fontsize=9, color=gray)

    def place(stem, rect):
        src = fitz.open(OUT / f"{stem}.pdf")
        page.show_pdf_page(fitz.Rect(rect), src, 0, keep_proportion=True)
        src.close()

    page.insert_text((35, 84), "A   Local loop + field", fontsize=11, fontname="hebo", color=navy)
    page.insert_text((35, 102), "86 mm / compact single column", fontsize=9, color=gray)
    place("A_local_global", (35, 120, 377, 474))
    page.insert_text((479, 84), "C   Illustrated classification", fontsize=11, fontname="hebo", color=navy)
    page.insert_text((479, 102), "128 mm / physics inside the map", fontsize=9, color=gray)
    place("C_illustrated_map", (479, 120, 925, 496))

    page.draw_line((35, 512), (965, 512), color=(.84,.87,.88), width=.6)
    page.insert_text((35, 545), "B   Auxiliary-field landscape", fontsize=11, fontname="hebo", color=navy)
    page.insert_text((35, 564), "178 mm / wide composition with vector depth", fontsize=9, color=gray)
    place("B_field_landscape", (35, 591, 965, 959))
    doc.set_metadata({"title": "BAFQMC schematic: three visual directions"})
    doc.save(OUT / "comparison.pdf", garbage=4, deflate=True)
    page.get_pixmap(matrix=fitz.Matrix(1.8, 1.8), alpha=False).save(OUT / "comparison.png")
    doc.close()


def validate(records):
    for record in records:
        doc = fitz.open(OUT / f"{record['name']}.pdf")
        if len(doc) != 1:
            raise AssertionError(record["name"])
        page = doc[0]
        if page.get_images():
            raise AssertionError(f"{record['name']} unexpectedly contains raster graphics")
        actual_mm = page.rect.width * 25.4 / 72
        if abs(actual_mm-record["width_mm"]) > .03:
            raise AssertionError(f"Incorrect physical dimensions: {record['name']}")
        record["pdf_vector_only"] = True
        record["pdf_page_count"] = 1
        record["pdf_size_bytes"] = (OUT / f"{record['name']}.pdf").stat().st_size
        doc.close()
    (OUT / "manifest.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    candidates = [make_a(), make_b(), make_c()]
    comparison(candidates)
    validate(candidates)
    print(json.dumps(candidates, indent=2))
