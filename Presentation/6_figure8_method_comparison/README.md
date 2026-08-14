# Figure 8 Method Comparison

`presentation.pptx` is the focused eight-slide comparison of three deliberately
separate Figure 8 implementations:

1. **Primary same-vintage test:** 351 direct/pre-unveiling fields retained in
   the 2021 authors' kit, 2021 DINA/NIPA, and the July 2025 paper's full
   Leontief operator.
2. **Retained old-pipeline benchmark:** the 2021 authors-kit final debt
   positions after its
   older seven-round unveiling, followed by the same 2025 net-debt display
   rule.
3. **Public-data robustness:** current public completed FWTW bilateral
   positions, 2021 DINA/NIPA, and the full Leontief operator.

All three use the same sign convention, national-income scale, wealth groups,
and 1982 normalization. The primary route is the closest feasible operator
comparison because it restarts before the old unveiling; the retained proxy
starts after it; the public route changes both data vintage and taxonomy. None
is labelled an exact numerical reproduction of the authors' unavailable
34-instrument, 27-sector, through-2019 matrices.

The deck contains the common estimand, a three-route crosswalk, the new
2021-direct reconstruction, the public-data boundary, paper comparisons for
top 1% and bottom 99%, the closest same-vintage operator comparison, accounting
limitations, and the final submission recommendation. Every slide contains a
`[Sources]` block in speaker notes.

## Generated inputs

- `Results_Proposal/figures/figure8_method_comparison_top1.png`
- `Results_Proposal/figures/figure8_method_comparison_bottom99.png`
- `Results_Proposal/figures/figure8_2021_operator_comparison.png`
- `Results_Proposal/figures/figure8_2021_direct_full_leontief.png`
- `Data/processed/figure8_method_comparison_metrics.csv`
- `Data/processed/figure8_2021_operator_comparison_metrics.csv`
- `Data/interim/figure8_2021_direct_network_diagnostics.csv`

Rebuild the three empirical inputs with
`Code/scripts/build_figure8_authors_data.py`,
`Code/scripts/build_figure8_2021_direct.py`, and
`Code/scripts/build_figure8_public_fwtw.py`. Then run
`Code/scripts/build_figure8_method_comparison.py` and rebuild the deck with
`source/rebuild_presentation.zsh`. The editable Artifact Tool source, starter,
frame map, template audit, deviation log, and provenance notes are retained in
`source/`.

## Validation

All eight slides were rendered and inspected individually on 2026-08-14. The
deck passed template-fidelity, overflow, unresolved-placeholder,
source-note, and PowerPoint-archive checks.
