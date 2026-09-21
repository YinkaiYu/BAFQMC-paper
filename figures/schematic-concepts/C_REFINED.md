# Production figure: enlarged frustrated region

The current production builder is `build_cards_v14.py`. It retains the selected
overlapping-card design, shifts the boundaries to give the upper-left region
about 40 percent of the classification map, and adds a recessed
`New sign-free regime` plaque with the same 20-unit corner radius and vector
corner path as the cards. The compact plaque has equal 28-unit left and top
margins, regular 6.6-point text, and a shallow recess defined by a tight upper/left
inner shadow and a narrow, subdued lower/right highlight. Its transparent
tint preserves the underlying card gradient and gently darkens toward the lower
right, following the overall illumination.

The background consists of a grey backing, a translucent gold card, and a
translucent blue card on top. Both cards use continuous two-dimensional color
and opacity gradients with a restrained broad reflection. Their green overlap
comes directly from alpha compositing, without a separate filled patch.
The gold rim is tinted by the overlying blue surface; the blue card has a
continuous bright lower rim and a diffuse shadow falling onto the gold card
and grey backing to make the stacking order visible.
The overlap is warmer at the upper left and cooler at the lower right because
the gold is stronger toward its top and the blue becomes deeper and less
transparent toward its lower right; this hue direction follows their gradients.

Only the upper-left region contains an illustration. It uses the independently
developed triangular lattice with purple bosons, matte grey bonds, and one red tapered
hopping arrow. The motif is reduced by 20 percent from its initial integration,
with transparent peripheral fading kept inside the grey backing card and clear
of the quadrant boundary. A broad quintic feather fades the outer bonds smoothly;
the four directional fades multiply for smooth corners. The motif and its BAFQMC
coverage label are both shifted upward by 40 design units. The arrow and `t > 0`
remain vector artwork. A thin space after the italic `t` balances the visible
gaps on either side of `>` despite the broad white outline. The lower-right
interaction sketch has been removed.
Coverage labels use the original
7.6-point typography, with the right-column labels wrapped for the narrower
regions and a 1.6 line-spacing factor.
Both vertical axis labels are shifted upward by 55 design units to give the
long lower label clearance from the bottom edge.
All four axis labels are bold. Their colors match the region text: blue for
`Frustrated` and `Satisfy TRS/RP criteria`, dark gold for `Unfrustrated`, and grey for
`Violate TRS/RP criteria`.

The RGBA motif and annotation coordinates are tracked in
`figures/schematic-assets/triangle-lattice.png` and `triangle-annotation.json`.
Regenerate those from the standalone study as documented in `TRIANGLE_FOCUS.md`.
The production builder requires only those tracked assets, not Blender or ignored
draft outputs.

```powershell
.\scripts\run-in-wsl.ps1 'PYTHONPATH=.build/schematic-exploration/vendor python3 -W error figures/schematic-concepts/build_cards_v14.py --publish'
.\scripts\build-manuscript.ps1
```

Publishing synchronizes `figures/schematic.pdf`, its self-contained SVG, and the
ignored PNG preview. Figure-only rounds do not refresh the diff PDF, following the
author's instruction. The caption identifies the triangular-lattice hopping and
uses `regions` for the unequal divisions. Earlier compositions are documented in
[the design history](archive/DESIGN_HISTORY.md).
