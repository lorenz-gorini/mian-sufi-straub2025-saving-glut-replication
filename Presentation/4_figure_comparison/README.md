# Figure Comparison Deck

`presentation.pptx` is the seven-slide, comparison-only module for the four
implemented paper figures. Each empirical slide puts the July 2025 target on
the left and our implementation on the right, reports common-sample fit, and
states the remaining data-vintage or network boundary.

## Current sequence

1. comparison-only title and common reading rule;
2. evidence contract for Figures 1, 5, 6, and 8;
3. Figure 1 indirect household ownership;
4. Figure 5 saving by wealth group;
5. Figure 6 saving rates by wealth percentile;
6. Figure 8 net debt from 2021 direct cells and the full Leontief inverse; and
7. synthesis of what survives independent implementation.

Figures 1, 5, and 6 recompute the 2025 objects with the February 2021
authors-kit inputs, so the common sample ends in 2016. Figure 8 uses the
earliest feasible saved direct/pre-round cells and replaces the old seven-round
operator with the full inverse. Its network remains coarsened to eight
intermediary blocks and therefore is not the unavailable 2025 34-instrument,
27-sector matrix.

The Figure 6 paper-raster audit, wealth-level view, and trailing-five-year
heat map are intentionally excluded. The economically interpretive
wealth-level and time-evolution views now live in
[`../7_debt_composition_extension/presentation.pptx`](../7_debt_composition_extension/presentation.pptx).
The focused three-route Figure 8 lineage and robustness audit remains in
[`../6_figure8_method_comparison/presentation.pptx`](../6_figure8_method_comparison/presentation.pptx).

The principal comparison statistics are:

- Figure 1 level: correlation 0.995 and mean absolute error 5.3 percentage
  points over 1963--2016;
- Figure 5 top 1% / bottom 99%: correlations 0.992 / 0.997 and mean absolute
  errors 0.40 / 0.42 percentage points;
- Figure 6 pre/post curves: correlations 0.991 / 0.969 and mean absolute errors
  1.46 / 1.22 percentage points; and
- Figure 8 top 1% / bottom 99%: correlations 0.994 / 0.995 and mean absolute
  errors 2.33 / 1.31 percentage points. In 2007 the reconstructed top-1
  position is +11.47 points of national income versus +18.02 in the paper.

## Generated inputs

- `Results_Proposal/figures/figure1_authors_data_reconstruction.png`
- `Results_Proposal/figures/figure5_authors_data_reconstruction.png`
- `Results_Proposal/figures/figure6_authors_data_percentiles.png`
- `Results_Proposal/figures/figure8_2021_direct_full_leontief.png`
- `MSS_SGR_July242025.pdf`, Figures 1, 5, 6, and 8, physical PDF pages 11, 22,
  24, and 29

The producing scripts and comparison tables are documented in the four figure
task records under `docs/project/tasks/`. The paper and replication kit remain
read-only.

## Validation

All seven slides were rendered and inspected individually on 2026-08-16. The
deck passes template-plan, template-fidelity, overflow, unresolved-placeholder,
speaker-note source, and PowerPoint-archive checks.

## Editable source

Durable authoring files are stored in `source/`. Run
`source/rebuild_presentation.zsh` after loading the presentation runtime
dependencies. The build selects seven inherited slides from the frozen
18-slide visual source, edits only the declared targets, and regenerates the
render and layout QA artifacts in an isolated `/private/tmp` workspace.
