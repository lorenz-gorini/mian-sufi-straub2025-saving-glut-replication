# Presentation equation assets

`equations.tex` is the single source for mathematical expressions embedded in
the PowerPoint decks. Each `slidemath` environment becomes one tightly cropped
SVG page. The numbered comments are the stable mapping used by the presentation
builder.

The equations follow the July 25, 2025 paper's notation. In particular,
Equation (4) retains the paper's row-scaling operator
`(1/L_t)^T \odot (...)`; the block representation
`Omega_t = (I_k-Q_t)^{-1} B_t` is shown as the equivalent ultimate-owner
submatrix used by the Python implementation.

Regenerate vector assets in a temporary directory with:

```sh
latex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/mss-equations equations.tex
dvisvgm --no-fonts --page=1- --output=/tmp/mss-equations/equation-%p.svg /tmp/mss-equations/equations.dvi
```

The SVGs are embedded in the PowerPoints. They remain vector graphics, so
subscripts, superscripts, sums, fractions, matrices, and Greek symbols retain
LaTeX geometry at any display size.
