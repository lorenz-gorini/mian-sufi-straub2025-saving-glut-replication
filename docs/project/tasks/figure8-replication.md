# T-004 / R-003: Figure 8 Replication

## Objective and classification

Apply the July 2025 Figure 8 definition and keep three empirical routes
separate:

1. **2021-kit seven-round proxy:** downstream authors-kit debt positions;
2. **2021 direct cells + full Leontief:** closest-feasible old-vintage operator
   comparison; and
3. **public FWTW + full Leontief:** newer-public-data robustness route.

The main methodological comparison is now route 2 versus route 1 because the
data vintage is held fixed as far upstream as the saved old-kit cells permit.
Route 3 shows what the full method produces from a later public matrix. The
exact authors' 2025 matrices, custom equity treatment, and crosswalk remain
unavailable, so none is labelled an exact numerical reproduction.

## Target definition

Paper: July 25, 2025 draft, Sections 4.1--4.2, Figure 8, physical PDF page 29.

$$
ND_{gt}=A^D_{gt}-D_{gt}.
$$

$A^D_{gt}$ is household debt held as an asset by group $g$ after the financial
system is unveiled; $D_{gt}$ is the group's own household debt liability.
Stocks are divided by aggregate national income and expressed relative to
1982. Positive values mean net lending to other households; negative values
mean net borrowing.

## Required-versus-available crosswalk

| 2025 requirement | February 2021 availability | Decision |
| --- | --- | --- |
| Exact authors-vintage completed annual instrument-by-sector matrices | Not supplied | Cannot reproduce the authors' exact 34-instrument, 27-sector network |
| Old-kit completed direct cells and issuer margins | Preserved in `Yunveilhhd.dta`, alongside the later round outputs | Reconstruct eight coarsened intermediary rows while explicitly excluding every round output |
| Current public completed FWTW matrices | Available separately: 31 instruments and 25 substantive sectors | Can support a mixed-vintage reconstruction after a documented crosswalk |
| Augmented household wealth-group columns | DINA asset-class shares are supplied; exact 2025 mapping is not | Rebuild with an explicit public-FWTW-to-DINA mapping |
| Fine-cohort unveiled household-debt assets | Supplied downstream in `YinequalityFAanalysis.dta` | Reuse with an explicit old-seven-round label |
| Fine-cohort debt liabilities | Supplied in the same file | Subtract as positive liability stocks |
| National income and 1982 base | Supplied in the same file | Apply the 2025 scale and display rule |

The proxy stops after the old seven-round procedure. The new old-vintage route
moves upstream to the saved direct-cell blocks, but those blocks are not the
paper's general 34-by-27 matrix. Reprocessing the 2021 kit therefore supports
a coarsened full solve, not recovery of the unavailable Batty-completed target
vintage. The public release supports a second full solve with a different
instrument/sector taxonomy and a 2016 distributional endpoint.

## 2021-direct-cell full-Leontief reconstruction

`Code/scripts/build_figure8_2021_direct.py` reads 351 pre-unveiling direct
positions, liability margins, household-debt cells, and raw mutual-fund
portfolio fields from `Yunveilhhd.dta`. Its explicit source contract excludes
all `*_hhd1`--`*_hhd7`, final owner allocations, and wealth-group unveiled
outputs. The saved purpose-built Stata blocks are aggregated into eight
intermediary rows, household-holder positions are split with supplied DINA
shares, and the infinite solve

$$
\Omega_t=(I-Q_t)^{-1}B_t
$$

replaces the seven-round sequence.

The old saved blocks include signed cells but not enough counterparty rows to
reorient them after coarsening. The baseline therefore clips negative direct
weights and rescales the remaining positions to each authors-kit issuer
margin. Brokers, holding/funding companies, nonprofits, and unidentified
residual claims are kept in an explicit `unassigned` ultimate-owner column.
The clipped mass and unassigned ownership share are material and generated as
diagnostics; this is consequently a same-vintage, closest-feasible operator
comparison, not a causal code-only experiment.

The full solve closes to machine precision; the maximum spectral radius is
0.180. Against the paper, the top-1 correlation/MAE are 0.994/2.33 percentage
points and the bottom-99 values are 0.995/1.31. Relative to the seven-round
proxy, mean absolute differences are only 0.26 and 0.75 points. This suggests
that finite-round truncation is not the main source of the remaining paper
gap in the coarsened 2021 network.

## Public-FWTW full-method reconstruction

The follow-on is now implemented separately in
`Code/scripts/build_figure8_public_fwtw.py`. It pivots the pinned public FWTW
long file into instrument-by-issuer-by-holder positions, maps the public
taxonomy to supplied DINA asset classes, augments the household-holder column
by wealth group, normalizes the direct matrix, and applies the full Leontief
inverse. It is labelled **public-FWTW full-Leontief reconstruction**, never
“exact 2025 replication.”

The public file's negative levels are reoriented in the primary build, as the
Federal Reserve technical note recommends; zero clipping is retained as a
sensitivity. The public discrepancy pseudo-sector is excluded from the
economic network. Direct rows, unveiled ownership, primary-asset allocation,
and household-debt liability allocation all satisfy their accounting
invariants.

The public result improves the common-period top-1 fit against the digitized paper
(correlation 0.998, MAE 2.12 percentage points versus 0.993 and 2.41 for the
old proxy). The old proxy remains closer for bottom 99 in levels (MAE 1.38
versus 1.98). This mixed result is consistent with simultaneous changes in the
operator, public input vintage, sector taxonomy, and instrument crosswalk.

## Seven-round proxy lineage

- Input:
  `MSS2021Febreplicationkit/data/finalfiles/YinequalityFAanalysis.dta`.
- Old unveiling builder:
  `MSS2021Febreplicationkit/code/build_fa_unveiling_data.do`.
- Old analysis precursor:
  `MSS2021Febreplicationkit/code/mss_analysis.do`, Figure 7 and Table 7 blocks.
- Python transformation: `Code/unveiling/figure8_authors.py`.
- Reproducible entry point:
  `Code/scripts/build_figure8_authors_data.py`.
- Tests: `Code/tests/test_figure8_authors.py` and
  `Code/tests/test_wealth_groups.py`.
- Detailed field contract: `docs/data/figure8-data.md`.

The unit of observation is year. The 21 fine cohorts partition top 1%, next
9%, next 40%, and bottom 50%; bottom 99% is their lower-three-group sum.

## Verification and result

- Sample: 1963--2016, 54 annual observations.
- Fine-to-coarse validation: maximum absolute error $1 million; maximum
  relative error $3.18\times10^{-7}$ across assets and liabilities.
- All five displayed series equal zero in 1982.
- Digitized-paper comparison:
  - top-1 correlation 0.993; mean absolute error 2.41 percentage points;
  - bottom-99 correlation 0.995; mean absolute error 1.38 points.
- 2007 levels relative to 1982:
  - top 1%: proxy +12.03 points; paper +18.02;
  - bottom 99%: proxy -38.88 points; paper -38.76.
- 2016 levels relative to 1982:
  - top 1%: proxy +13.00 points; paper +17.80;
  - bottom 99%: proxy -33.36 points; paper -34.80.

The old-vintage result strongly reproduces the direction, timing, and
bottom-99 magnitude. Its top-1 asset position is systematically smaller. That
is exactly the dimension most exposed to the revised financial-network and
wealth-group allocation; the gap is therefore informative but cannot be
called a causal code-only effect.

## Outputs

- `Data/processed/figure8_authors_proxy.csv`
- `Data/processed/figure8_aggregation_validation.csv`
- `Data/processed/figure8_paper_digitized.csv`
- `Data/processed/figure8_authors_proxy_comparison.csv`
- `Results_Proposal/figures/figure8_authors_proxy.png`
- `Results_Proposal/figures/figure8_authors_proxy_comparison.png`

The two full-Leontief routes are documented separately in
[`../../data/figure8-2021-direct-data.md`](../../data/figure8-2021-direct-data.md)
and
[`../../data/figure8-public-fwtw-data.md`](../../data/figure8-public-fwtw-data.md).
Their route-specific producers write no shared outputs. The separate
`Code/scripts/build_figure8_method_comparison.py` entry point reads all three
processed series and writes the aligned comparison, fit metrics,
same-vintage operator metrics, and presentation figures.

## Definition of done

- [x] Target equation, units, sign, groups, and base year documented.
- [x] Exact missing-input boundary identified before implementation.
- [x] Best-feasible fine-cohort proxy implemented and labelled in code/output.
- [x] Fine-to-coarse aggregation and accounting signs tested.
- [x] Paper curve digitized only as an external benchmark.
- [x] Common-sample comparison generated with declared metrics.
- [x] Remaining limitation documented: the exact authors-vintage result is
      unavailable, while a mixed-vintage public-FWTW method reconstruction is
      feasible as a separate follow-on.
- [x] Separate public-FWTW full-Leontief pipeline implemented and tested.
- [x] Instrument-to-DINA and household-liability mappings documented.
- [x] Negative public levels and the discrepancy pseudo-sector treated
      explicitly, with a generated sensitivity.
- [x] Old-kit completed direct cells reconstructed without reading a
      seven-round or final unveiled household-debt field.
- [x] Coarsened old-vintage full-Leontief matrix, signed-cell treatment,
      residual owner, DINA augmentation, and accounting invariants documented.
- [x] Three routes compared against the same digitized target through a
      comparison-only entry point.

## Session note: 2026-08-13 public-FWTW implementation

- Goal: implement the paper's full augmented Leontief method without changing
  the retained seven-round proxy.
- Changed: new reusable module, entry point, tests, data contract, processed
  outputs, diagnostics, figures, and a method-comparison presentation.
- Validation: all source keys and share partitions pass; the maximum spectral
  radius is 0.504; matrix and ownership closure errors are below
  $9\times10^{-16}$; reorientation versus clipping changes a headline series
  by at most 0.17 percentage points.
- Limitation: the result uses a June 2026 public FWTW vintage with 31
  instruments and 25 substantive sectors plus 2021 DINA/NIPA through 2016,
  rather than the authors' unavailable 34-instrument, 27-sector 2025 vintage.

## Session note: 2026-08-14 old-vintage full-Leontief implementation

- Goal: move upstream of the seven-round output and test the full operator on
  the 2021 direct-cell vintage while preserving the public-FWTW route.
- Changed: new direct-cell module, route-only entry point, comparison module
  and entry point, tests, data contract, annual/component diagnostics,
  processed output, generated charts, and three-route presentation update.
- Validation: 54 annual observations; zero round-output fields read; eight
  coarsened intermediary rows; maximum spectral radius 0.180; direct,
  unveiled, primary-asset, and debt-liability closure at or below
  $4.44\times10^{-16}$ apart from the documented $2$ million source-margin
  rounding difference.
- Limitation: signed positions are clipped and component-balanced because the
  saved coarsened blocks cannot be direction-reversed into absent counterparty
  rows; an explicit residual owner retains 3.17%--9.97% of ultimate household
  debt.
