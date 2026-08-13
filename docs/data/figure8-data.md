# Figure 8 Data Contract

## Economic object and feasibility boundary

For wealth group $g$, the 2025 paper defines net household debt as

$$
ND_{gt}=A^D_{gt}-D_{gt},
$$

where $A^D_{gt}$ is household debt held as an asset after unveiling and
$D_{gt}$ is debt owed by the group. Positive values identify a net lender;
negative values identify a net borrower. Figure 8 plots $ND_{gt}/NI_t$ less
its 1982 level.

The February 2021 package does **not** contain the exact Batty-completed annual
instrument-level bilateral matrices, authors' equity treatment, or crosswalk
used by the revised 2025 augmented Leontief solve. It does contain fine-cohort
debt assets produced by the older seven-round unveiling. Consequently the
current pipeline is a close, explicitly labelled proxy: it applies the 2025
net-debt equation, groups, sign convention, national-income scaling, and 1982
normalization to the older unveiled stocks. It is not a rerun of the 2025
matrix methodology.

This is an exact-vintage boundary, not a methodological impossibility. The
pinned current public FWTW release contains completed bilateral estimates for
31 instruments and 25 substantive sectors. Combined with the 2021 DINA/NIPA
inputs, it can support a separate full-Leontief mixed-vintage reconstruction
after an explicit instrument/sector-to-DINA crosswalk. That pipeline is not yet
part of the outputs documented below.

## Input inventory

| Dataset | Unit/key and coverage | Used fields | Role |
| --- | --- | --- | --- |
| `data/finalfiles/YinequalityFAanalysis.dta` | year; unique; 1963--2016 after boundary filter | `fa896140001a`; 21 `a_hh*_hhdSZ`; 21 `d_hh*_hhdSZ`; six coarse validation cells | National income, old-unveiling debt assets, positive debt liabilities, and coarse checks; stocks in current-dollar millions |
| `MSS_SGR_July242025.pdf` | paper Figure 8, physical page 29 | embedded raster | Approximate visual benchmark only; never an empirical input |

The fine cohort-to-group mapping is identical to Figure 5 and is defined once
in `Code/unveiling/wealth_groups.py`. Bottom 99% is next 9% plus next 40% plus
bottom 50%.

## Transformation

For each group and year, Python performs four transparent operations:

1. sum the supplied fine-cohort old-unveiling asset cells;
2. sum the supplied fine-cohort positive liability cells;
3. subtract liabilities from assets and divide by current national income; and
4. subtract the unique 1982 ratio.

The old Stata code instead flips the liability sign and adds it. These are
algebraically identical because the stored liability cells are positive.

## Invariants and observed validation

- Required columns are selected explicitly, cast to double precision, checked
  for finite values, and keyed by a unique annual integer.
- Fine-cohort asset and liability sums are compared with supplied top-1,
  next-9, and bottom-90 cells. Across 324 group-side-year checks, the maximum
  absolute difference is $1 million and the maximum relative difference is
  $3.18\times10^{-7}$, consistent with Stata single-precision rounding.
- Every displayed group is exactly zero in 1982.
- Bottom-99 assets, liabilities, and net debt equal the sum of its three
  component groups.

The common-period comparison with the digitized 2025 figure has correlation
0.993 for the top 1% and 0.995 for the bottom 99%. Mean absolute errors are
2.41 and 1.38 percentage points of national income, respectively. In 2007 the
bottom-99 proxy is -38.88 points versus -38.76 in the digitized paper, while
the top-1 proxy is +12.03 versus +18.02. The close bottom-99 match and smaller
top-1 asset position are evidence about the old/new input and unveiling
boundary; they do not identify a pure code effect.

## Generated outputs

| Output | Contents | Producer |
| --- | --- | --- |
| `Data/processed/figure8_authors_proxy.csv` | fine-group assets, liabilities, net debt, and 1982-relative ratios; 1963--2016 | `Code/scripts/build_figure8_authors_data.py` |
| `Data/processed/figure8_aggregation_validation.csv` | fine-versus-coarse asset/liability checks | same |
| `Data/processed/figure8_paper_digitized.csv` | approximate paper series; 1963--2019 | same |
| `Data/processed/figure8_authors_proxy_comparison.csv` | common-period paper/proxy values and errors | same |
| `Results_Proposal/figures/figure8_authors_proxy.png` | standalone five-group proxy | same |
| `Results_Proposal/figures/figure8_authors_proxy_comparison.png` | headline top-1/bottom-99 comparison | same |

The output names retain `proxy` so downstream slides and reports cannot
silently relabel this result as a 2025-method reconstruction.
