# Production schematic motif assets

The current compositor is `../schematic-concepts/build_cards_v14.py`.

- `triangle-lattice.png`: transparent triangular-lattice render with soft fading,
  shadows, purple bosons, and purple halos, composed from `render_triangle_focus.py` and
  `compose_triangle_focus.py` in `../schematic-concepts/`.
- `triangle-annotation.json`: projected vector outline of the single nearest-
  neighbour hopping arrow and its `t > 0` label. Positive hopping refers to
  `H_t = +t sum_<ij> (b_i^+ b_j + b_j^+ b_i)`.

The production palette is the original color-study option B, without color grading:
bosons `#7851A8`, halos `#AC8ACE`, arrow `#C8473B`, and label `#B43B31`.

The following original motif assets are retained for historical compositors,
including `../schematic-concepts/build_cards_v13.py`:

- `interaction.png`: three identical bosons with continuous wavy interactions.
- `field.png`: bosons coupled individually to a fluctuating auxiliary-field net.
- `loop.png`: four identical bosons with the same interactions on a square.

Their geometry generator is `../schematic-concepts/render_c_refined.py`.
These are explanatory symbols, not sampled trajectories or numerical data.
There are no direct particle-particle links in the fixed-field illustration.
