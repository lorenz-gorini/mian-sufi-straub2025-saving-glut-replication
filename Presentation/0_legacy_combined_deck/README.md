# Legacy Combined Progress Deck

This folder preserves the superseded 24-slide Beamer deck that previously sat
at the root of `Presentation/`. It combines theoretical methodology, data
architecture, implementation, and early Figure 1 progress. It remains useful
for provenance but is not an editable source module for the current numbered
PowerPoint presentations.

## Contents and dependencies

- `presentation.tex` is the historical 16:9 Beamer entry point.
- `presentation.pdf` is its compiled artifact.
- `sections/replication_strategy.tex` is imported only by this deck.
- `assets/` preserves two conceptual images created for this deck. The current
  source uses native TikZ schematics instead, so the images are retained as
  historical deck-owned assets rather than active dependencies.
- `../generated/` remains at the collection root because its numerical LaTeX
  macros are also imported by the report and the historical theory deck.
- The Figure 1 comparison graphic remains under `Results_Proposal/figures/`
  because it is a generated research result, not a presentation-owned asset.

The former root `benchmark_comparison/` directory was empty and unreferenced,
so it was not carried into this archive.

## Rebuild

Run from this folder:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error presentation.tex
```

Do not add new topic-specific material here. Use the numbered folder that owns
the relevant presentation purpose.
