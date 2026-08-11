# Figure Comparison Deck

`presentation.pptx` is the maintained comparison deck for the three core
empirical outputs. It begins by separating four evidence roles that must not be
called interchangeable replications:

1. the July 2025 paper's Figure 1, which is the authoritative target;
2. the February 2021 package's old Figure 6, which is an authors-old
   methodological precursor with a different dependent variable;
3. our later-vintage public-data robustness build; and
4. our primary Python reconstruction of the 2025 definition from the authors'
   February 2021 inputs.

The main comparison is item 4 versus item 1. Items 2 and 3 are supporting
diagnostics for method lineage and data-vintage robustness. They cannot isolate
a pure methodology effect because inputs, classifications, denominators, and
estimands change together. Not every role exists for every figure.

## Current sequence

The 12 slides establish the taxonomy and then compare the paper with our
authors-data results for Figures 1, 5, and 8. Figure 1 retains the older Stata
and public-data outputs as supporting diagnostics. Figure 5 is classified as a
reconstruction because the supplied wealth, fine-share, valuation, and NIPA
inputs identify the revised saving object through 2016. Figure 8 is classified
as a bounded proxy because its unveiled asset stocks come from the older
seven-round procedure rather than the unavailable 2025 completed matrices.

The paper graphs on the primary comparison slides are cropped to remove their
printed captions. Their meaning, sample, and units are restated in editable
slide text. Every slide contains a `[Sources]` block in speaker notes.

The principal comparison statistics are:

- Figure 1 level: correlation 0.995 and mean absolute error 5.3 percentage
  points over the common 1963--2016 sample;
- Figure 5 top 1% / bottom 99%: correlations 0.992 / 0.997 and mean absolute
  errors 0.40 / 0.42 percentage points; and
- Figure 8 proxy top 1% / bottom 99%: correlations 0.993 / 0.995, with the
  2007 top-1 lending position understated by about 6 percentage points.

## Generated inputs

- `Results_Proposal/figures/figure1_authors_data_reconstruction.png`
- `Results_Proposal/figures/figure1_authors_data_comparison.png`
- `Results_Proposal/figures/figure1_indirect_household_ownership.png`
- `Results_Proposal/figures/figure5_authors_data_reconstruction.png`
- `Results_Proposal/figures/figure8_authors_proxy.png`
- `MSS2021Febreplicationkit/output/fig_owndet.eps`
- `MSS_SGR_July242025.pdf`, Figures 1, 5, and 8, physical PDF pages 11, 22,
  and 29

The Python figures are rebuilt by `Code/scripts/build_figure1_authors_data.py`
and `Code/scripts/build_figure1.py`,
`Code/scripts/build_figure5_authors_data.py`, and
`Code/scripts/build_figure8_authors_data.py`. The source paper and replication
kit remain read-only.

## Validation

All 12 slides were rendered and inspected individually on 2026-08-10. The deck
passes the template-fidelity, overflow, unresolved-placeholder, source-note,
and PowerPoint-archive checks. Future extensions must retain the role labels
and may not silently promote the Figure 8 proxy to a reconstruction.
