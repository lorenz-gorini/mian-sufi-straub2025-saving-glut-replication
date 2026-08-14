# T-001: Crosswalk the Selected 2025 Results to Usable 2021 Inputs

## Objective

Determine, for the already selected Figures 1, 5, and 8, whether the February
2021 package contains enough data to compute the July 2025 definition over the
overlapping sample. For every gap, distinguish a code/transformation change, a
changed economic definition or group, a pure 2017--2019 vintage extension, and
an input that is absent from the supplied package.

The exhibit selection and the old/new feasibility crosswalk are complete for
all three core figures. This record now preserves the classification evidence
and the exact boundary between reconstruction and proxy.

## Source status

- `MSS_SGR_July242025.pdf` is the authoritative 66-page target paper, dated
  July 25, 2025. Its main results are presented in Figures 1-13. Use the
  already parsed
  `/Users/lorenzogorini/Library/CloudStorage/OneDrive-UniversitàCommercialeLuigiBocconi/PhD/research-wiki/papers/inequality/mian-2025-saving-glut-rich/full.md`
  for text search and section reading; re-open the PDF only for authoritative
  pages, equations, figures, footnotes, or visual layout.
- `NotebookLM-Present-Unveiling_the_Rich_Saving_Glut.pdf` is a 15-page,
  image-only NotebookLM
  synthesis of that paper. It is useful for conceptual orientation only.
- `MSS2021Febreplicationkit/` is the authors' February 2021 replication package.
  Its scripts name the earlier draft *The Saving Glut of the Rich and the Rise
  in Household Debt*, generally use data through 2016, and generate the older
  paper's Figures 1-12 and Tables 1-9.
- The 2025 paper's first-page note says it is a heavily revised version of that
  earlier draft. The revised paper uses data through 2019, adopts a
  matrix/Leontief unveiling exposition incorporating Batty et al. (2023), drops
  the older main state-analysis section, and adds international evidence.
  Therefore the old kit is a partial lineage and benchmark source, not the exact
  replication package for every 2025 exhibit.

## Selection criteria

Score candidate exhibits on:

1. **Scientific centrality:** is the exhibit necessary to support the paper's
   main conclusion?
2. **Methodological coverage:** does it teach a distinct part of the
   measurement, accounting, unveiling, or validation strategy?
3. **Feasibility:** are the needed inputs supplied, and can the result be
   reconstructed within a course project?
4. **Independence:** can we do more than replot an authors' final file?
5. **Diagnostic value:** if our result differs, will the discrepancy identify a
   meaningful assumption or data step?

Prefer a compact portfolio of complementary results over several exhibits that
repeat the same construction.

## Approved 2025 scope

The user approved the following scope on 2026-07-24:

| Decision | Claim | 2025 exhibit | Closest old-kit precursor | Learning value |
| --- | --- | --- | --- | --- |
| Selected - core | The share and scale of household assets held indirectly rose strongly before 2008, making unveiling economically important. | Figure 1 | No direct equivalent; old Figure 6 (`fig_owndet.eps`) documents direct ownership composition under the earlier procedure. | Teaches the paper's main methodological contribution: direct ownership, intermediary cross-holdings, the unveiling operator, and final ownership. |
| Selected - core | Saving by the top 1 percent diverges sharply from the bottom 99 percent after 1982. | Figure 5 | Old Figures 1, 3, and 4 (`fig_glut.eps`, `fig_hh_*.eps`, `fig_bottomline.eps`) contain precursor measures but use older periods/smoothing. | Teaches wealth-based saving measurement, valuation adjustments, group aggregation, normalization, and moving averages. |
| Selected - core | The top 1 percent accumulates net household-debt claims while the bottom 99 percent, especially the middle class, becomes a net borrower. | Figure 8 | Old Figure 7 (`fig_nhhd.eps`) and Table 7 (`tab_nhhd_.tex`). | Applies the unveiled ownership matrix to a central economic result and makes asset-versus-liability signs concrete. |
| Selected - extension if time permits | Debt-financed expenditure by the bottom 99 percent rises, and the top 1 percent finances a large share. | Figure 9 | Old Table 7 provides flow components, but the exact 10-year-moving-average exhibit is revised. | Naturally extends Figure 8 from debt stocks to annual financing flows without opening a separate empirical branch. |

Figures 10-13 and the older state-level analysis are deferred. Do not add them
before the three core figures are complete. Figure 9 may begin only when its
inputs can reuse the verified Figure 8 pipeline.

## Selection rationale

The three core figures form a coherent teaching sequence:

1. **Figure 1 explains the method:** why direct balance sheets are insufficient
   and how financial intermediation is unveiled.
2. **Figure 5 explains the main measured fact:** how wealth changes and
   valuation effects imply distributional saving.
3. **Figure 8 explains the main economic application:** who ultimately holds
   household debt and who owes it.

This scope prioritizes methodological breadth and economic understanding over
the number of replicated outputs. Figure 9 is a disciplined extension because
it transforms the Figure 8 stock result into a flow interpretation.

## Required result record

For every selected exhibit, add a section to
`Results_Proposal/major_results.md` with:

- exact paper version, section, page, caption, and claim;
- authors' analysis-code location and output path;
- input and intermediate data lineage;
- sample, groups, units, normalization/base period, weighting, and uncertainty;
- benchmark values or series;
- independent code and output paths;
- verification statistic and tolerance;
- interpretation of discrepancies.

## Current Figure 1 lineage evidence

The Sections 2.1--2.2 operator and old/new code lineage were completed on
2026-08-02. Evidence is linked from the R-001 record in
`Results_Proposal/major_results.md` and includes:

- the tested Python implementation in `Code/unveiling/network.py`;
- the equation, invariant, and data-contract note in
  `docs/methods/leontief-unveiling.md`;
- the exact seven-round trace added to
  `docs/reference/author-kit-map.md`; and
- the visually verified initial module in `Presentation/presentation.pdf`.

The 2026-08-03 teaching revision adds a complete matrix-to-network mapping and
a generated direct-plus-indirect reconciliation. `Report/report.tex` now also
records the precise evidence boundary: fixed-matrix round recursion is
algebraically equivalent to the Leontief solve, while numerical equality with
the actual 2021 Stata pipeline remains untested until common inputs exist.

The Python implementation is packaged by the project-level `pyproject.toml`.
An editable installation in the recorded `general` Conda environment exposes
the `unveiling` import to examples, scripts, tests, and interactive work without
requiring a repository-specific `PYTHONPATH`.

On 2026-08-05 the empirical lineage advanced with an explicitly non-exact
public-data robustness reconstruction:

- `Code/unveiling/figure1.py` defines, validates, aggregates, and plots the two
  Figure 1 series;
- `Code/scripts/build_figure1.py` reads pinned Federal Reserve FWTW and
  BEA/FRED national-income inputs and writes the processed series and chart;
- `docs/data/figure1-data.md` documents the input/output contracts, selective
  old-kit inventory, checksums, and update-as-discovered rule; and
- three new tests verify the issuer-set numerator, domestic denominator,
  national-income unit conversion, and duplicate-key boundary.

The 1963--2019 series rises from 47.5% to a 70.1% peak in 2009 and ends at
66.2%. It recovers the target's central long rise and approximate peak
magnitude, but not its exact timing or recent level.

On 2026-08-09, after the full authors' data tree became local, a closer
authors-data reconstruction was added. It begins from the authors' prepared
wide Financial Accounts panel, retains the central intermediary-instrument
aggregation, rebuilds financial equity from the supplied CRSP file, and uses
their national-income series. Its 1963--2016 stock-to-national-income curve has
correlation 0.995 and mean absolute error 5.3 percentage points of national
income relative to the digitized paper curve. Its broad-denominator ownership
share has mean absolute error 3.2 percentage points. This materially strengthens
the Figure 1 evidence, while the missing 2025 completed 34-instrument,
27-sector matrices and denominator crosswalk still preclude an exact label.

## 2021-input feasibility protocol

Apply the following sequence to Figure 1, then Figure 5, then Figure 8:

1. Write the 2025 plotted object as an equation and define the period, wealth
   groups, units, normalization, smoothing, and sign convention.
2. Identify the earliest supplied 2021-package files that contain each input
   over the common sample through 2016. Treat the absence of 2017--2019 data as
   a vintage limitation, not automatically as a failure to reconstruct the
   earlier years.
3. Trace the old Stata construction and list every place where it differs from
   the 2025 definition. Do not assume a changed figure number or similar
   caption implies the same object.
4. Recompute the 2025 definition on the old inputs where the mapping is
   identified. If an input is unavailable, stop at the first unsupported
   transformation and record the exact failure boundary.
5. Classify the result as one of: exact February 2021 benchmark; old-input
   reconstruction of a July 2025 definition; close proxy; or infeasible with
   the supplied data.
6. Compare the generated series with the digitized 2025 curve using declared
   metrics, then attribute discrepancies only to changes supported by code,
   data, or paper evidence.

The economic invariant differs by exhibit: Figure 1 must preserve ownership
row sums and aggregation; Figure 5 must reconcile wealth change into active
saving plus valuation effects; Figure 8 must reconcile unveiled household-debt
assets minus group liabilities with the plotted net position.

## Completed Figure 5 and 8 feasibility classification

The 2026-08-10 implementation audit resolves the remaining two core figures:

| Figure | Classification | Earliest feasible supplied input | Verified boundary |
| --- | --- | --- | --- |
| Figure 5 | Old-input reconstruction of the July 2025 definition | `YwealthFOF.dta`, fine DINA shares, `Ywealthreturns.dta`, and NIPA saving | Annual saving closes to NIPA; 10-year/1982 display implemented through 2016; top-1 and bottom-99 correlations with the digitized target are 0.992 and 0.997 |
| Figure 8 | Primary 2021-direct/full-inverse reconstruction; retained old-unveiling benchmark; public-FWTW robustness | 351 direct/pre-unveiling fields in `Yunveilhhd.dta`; downstream fine debt positions for the benchmark; public completed FWTW for robustness; supplied DINA/NIPA for all routes | The primary route is the closest same-vintage operator test but reconstructs only eight coarsened intermediary rows; the exact authors-vintage 34-instrument, 27-sector matrices remain unavailable |

Figure 5 can therefore be called our reconstruction of the revised method on
the older authors' data. Figure 8 has three labels: the old-kit downstream
output is the seven-round benchmark; the 2021 direct-cell/full-inverse route
is the primary closest-feasible operator test; and the public-FWTW build is a
mixed-vintage robustness reconstruction. The absent exact 2017--2019
extension, full saved old direct cube, authors' instrument/sector vintage, and
equity crosswalk prevent an exact numerical reproduction, not implementation
of the operator itself.

## Definition of done

- [x] The exact full article version is present and identified.
- [x] The selected exhibits have been checked against the actual paper, not
      only the synthesis or code comments.
- [x] The core set contains a methodology result, a distributional-saving
      result, and a debt-financing/unveiling result.
- [x] Figure 9 is explicitly a time-permitting extension rather than a core
      commitment.
- [x] Each selected result has a complete initial lineage to authors' code and
      files.
- [x] The old/new version boundary, missing newer code or data, and any private
      inputs are explicit.
- [x] The user has approved the final scope.
- [x] `docs/project/progress.md` marks T-001 through T-004 complete and links
      the three figure-specific data and replication records.
- [x] Figure 5 has a required-versus-available input table, an exact old/new
      transformation crosswalk, and a feasibility classification.
- [x] Figure 8 has a required-versus-available input table, an exact old/new
      transformation crosswalk, and a feasibility classification.

## Decision log

| Date | Decision | Rationale | Evidence |
| --- | --- | --- | --- |
| 2026-07-24 | Treat `MSS_SGR_July242025.pdf` as the target paper. | It is the complete July 25, 2025 manuscript matching the user's replication objective. | Title page, abstract, and full text. |
| 2026-07-24 | Treat the February 2021 kit as a partial older-version reference. | The 2025 paper explicitly says it heavily revises the earlier title used by the kit; samples, exposition, and exhibits differ. | 2025 title-page note, package read-me, and old `mss_analysis.do`. |
| 2026-07-24 | Select Figures 1, 5, and 8 as the core replication scope. | Together they teach the unveiling method, the measurement of distributional saving, and the main debt-financing application. | User decision and paper Sections 2-4. |
| 2026-07-24 | Keep Figure 9 as a time-permitting extension. | It reuses Figure 8 inputs and changes the interpretation from debt stocks to financing flows without broadening the project substantially. | User decision and paper Section 4.2. |
| 2026-08-02 | Treat the Leontief operator as verified but Figure 1 as empirically open. | Equations (1)--(4), orientation, and invariants are tested; the old kit lacks the completed 2025 annual matrices needed for the plotted series. | Python tests, method note, authors' code trace, and rendered teaching module. |
| 2026-08-03 | Do not interpret a difference from the 2021 rounds as evidence against the 2025 paper. | The two versions use different representations and empirical rules; a defensible numerical claim requires a common-input experiment. | Method note, report comparison section, and old-kit line trace. |
| 2026-08-03 | Install the independent implementation as an editable local distribution. | A declared package and dependency contract makes `unveiling` importable throughout the recorded environment while retaining live, reviewable source under `Code/`. | `pyproject.toml`, `Code/README.md`, example invocation, and test suite. |
| 2026-08-05 | Treat the current Figure 1 output as an independent trend reconstruction, not an exact authors' benchmark. | A later public FWTW vintage recovers the central rise but has 21 rather than 23 intermediary sectors, later revisions, and no authors' corporate-equity extension. | Pinned inputs, processed annual series, generated figure, data note, and report comparison. |
| 2026-08-09 | Add an authors-data reconstruction between the historical package benchmark and the new-data robustness result. | Prepared author files let us skip mechanical cleaning while explicitly reconstructing the economically central instrument aggregate and testing it against the paper curve. | `figure1_authors.py`, generated comparison files, tests, report, and deck. |
| 2026-08-10 | Recast the remaining task as a 2021-input feasibility audit for the fixed 2025 scope. | The full Stata run establishes that the old package works for the 2021 paper; the unresolved question is whether its data can identify the revised Figure 5 and 8 definitions over the common sample. | Completed T-007 benchmark, author-output crosswalk, and user direction. |
| 2026-08-10 | Classify Figure 5 as a reconstruction and Figure 8 as a proxy. | Figure 5's wealth, valuation, fine-share, and NIPA inputs identify the revised saving/display procedure through 2016. Figure 8's downstream fine debt positions are usable, but its revised completed matrices are absent. | Generated pipelines, tests, data contracts, and digitized-paper comparisons. |
| 2026-08-14 | Refine Figure 8 to three routes and make the 2021-direct/full-inverse route primary. | `Yunveilhhd.dta` preserves enough pre-round direct fields to reconstruct a coarsened old-vintage network without reading any round outputs. This is closer to the requested operator comparison than changing to the public FWTW vintage. | Direct-cell module and tests, component/network diagnostics, comparison-only build, and focused three-route deck. |

## Session record: 2026-08-10 task refresh

- Starting version: the workspace is not recognized as a Git worktree, so no
  branch or commit identifier is available.
- Goal: reconcile the completed February 2021 benchmark with today's attempt
  to reproduce the selected July 2025 results from the supplied old-vintage
  data.
- Result: exhibit selection is fixed; T-001 now owns the figure-by-figure
  feasibility classifications and exact failure boundaries for Figures 5 and
  8, after a review of the existing Figure 1 reconstruction.
- Next action: write the Figure 5 target equation and required-versus-available
  input table before implementing further code.

## Session record: 2026-08-10 author-kit quickstart

- Starting version: the workspace is not recognized as a Git worktree, so no
  branch or commit identifier is available.
- Goal: give future agents a compact, evidence-linked description of the 2021
  Stata pipeline, its preprocessing, and its relationship to the July 2025
  methodology.
- Changed files: `docs/reference/author-kit-quickstart.md`, the two
  documentation indexes, this task record, and `docs/project/progress.md`.
- Reasoning: the old wealth-based pipeline implements the 2025 Appendix Table
  A1 allocation and saving/valuation closure closely enough to support an
  old-input Figure 5 reconstruction through 2016. The old debt-specific
  seven-round outputs remain useful benchmarks, but they are lossy downstream
  objects and cannot substitute for the completed 2025 direct-ownership and
  primary-asset matrices required by Figure 8.
- Validation: checked the authors' one-page read-me visually, traced the DINA
  collapse and asset mapping in `build_fa_unveiling_data.do`, traced the
  valuation and NIPA closure in `build_wealth_saving_data.do`, and verified the
  year coverage and annual-key uniqueness of seven compact prepared files.
  Across 29 DINA share triplets the largest share-sum error is
  $1.19\times10^{-7}$; the maximum cohort-to-NIPA saving-closure error is
  $1.16\times10^{-7}$, and the largest checked wealth-change identity error
  is $5.22\times10^{-8}$.
- Result: future agents now have one short routing document with explicit
  benchmark/reconstruction/proxy labels and a selective lookup protocol.
- Remaining issue: the Figure 5 and 8 classifications are methodological
  feasibility judgments until their exact used-column inventories and
  regenerated 2025-display series are computed and compared.
- Next action: inventory the Figure 5 variables in `Ysavingwealth.dta`, rebuild
  the top-1/bottom-99 trailing moving averages through 2016, and test the
  accounting closure before beginning the Figure 8 proxy.
