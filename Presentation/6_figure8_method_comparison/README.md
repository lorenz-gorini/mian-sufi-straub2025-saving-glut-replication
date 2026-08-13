# Figure 8 Method Comparison

`presentation.pptx` is the focused eight-slide comparison of two deliberately
separate Figure 8 implementations:

1. **Preferred:** public completed FWTW bilateral positions, 2021 DINA/NIPA,
   and the July 2025 paper's full Leontief operator.
2. **Retained lineage:** the 2021 authors-kit final debt positions after its
   older seven-round unveiling, followed by the same 2025 net-debt display
   rule.

Both use the same sign convention, national-income scale, wealth groups, and
1982 normalization. The preferred route rebuilds the direct network; the
retained proxy starts after the old unveiling. Neither is labelled an exact
numerical reproduction of the authors' unavailable 34-instrument, 27-sector,
through-2019 matrices.

The deck contains the common estimand, a method/data crosswalk, the preferred
operator, the exact-vintage boundary, paper comparisons for top 1% and bottom
99%, signed-level sensitivity, accounting checks, and the final submission
recommendation. Every slide contains a `[Sources]` block in speaker notes.

## Generated inputs

- `Results_Proposal/figures/figure8_method_comparison_top1.png`
- `Results_Proposal/figures/figure8_method_comparison_bottom99.png`
- `Results_Proposal/figures/figure8_public_fwtw_full_leontief.png`
- `Results_Proposal/figures/figure8_public_fwtw_sensitivity.png`
- `Data/processed/figure8_method_comparison_metrics.csv`
- `Data/interim/figure8_public_fwtw_network_diagnostics.csv`

Rebuild the empirical inputs with
`Code/scripts/build_figure8_public_fwtw.py`, then rebuild the deck with
`source/rebuild_presentation.zsh`. The editable Artifact Tool source, starter,
frame map, template audit, deviation log, and provenance notes are retained in
`source/`.

## Validation

All eight slides were rendered and inspected individually on 2026-08-13. The
deck passed template-fidelity, overflow, unresolved-placeholder,
source-note, and PowerPoint-archive checks.
