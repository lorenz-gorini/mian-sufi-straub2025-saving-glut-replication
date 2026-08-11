# Figure 6 Exact-Method Reconstruction: Data Contract

## Role and economic object

This pipeline reconstructs the July 2025 paper's Figure 6 method with the
February 2021 authors-kit inputs. It is an **exact-method, older-input
reconstruction**: the rate definition, percentile bins, valuation treatment,
and period averaging follow the 2025 paper, but the available data end in 2016
rather than 2019.

For wealth cohort $i$ in year $t$, the paper defines net saving and disposable
income as

$$
\Theta_{it}=\sum_j\left[W_{ijt}-(1+\pi_{ijt})W_{ij,t-1}\right],
$$

$$
Z^d_{it}=Z^{d,p}_{it}+Z^{d,\pi}_{it},
\qquad
s^N_{it}=\frac{\Theta_{it}}{Z^d_{it}}.
$$

$W_{ijt}$ is the current-dollar end-of-year stock of asset or liability $j$,
$\pi_{ijt}$ is its valuation return, $Z^{d,p}_{it}$ is personal disposable
income, and $Z^{d,\pi}_{it}$ is corporate disposable income attributable to
shareholders. The plotted period rate is the simple mean of annual cohort
rates, matching the old authors-code averaging convention:

$$
\bar s^N_{iP}=\frac{1}{|P|}\sum_{t\in P}s^N_{it}.
$$

The windows are 1963--1982 and 1983--2016. The paper's second window continues
through 2019.

For the time-evolution diagnostic, the same annual rate is averaged over a
trailing five-year window:

$$
\bar s^N_{i,t;5}=\frac{1}{5}\sum_{\tau=t-4}^{t}s^N_{i\tau}.
$$

No new numerator, denominator, weighting, or smoothing assumption enters. A
window is emitted only when all five consecutive years are present, so the
diagnostic covers window ends 1967--2016.

## Input inventory

All source inputs are immutable files from the February 2021 authors' package.

| Dataset | Unit/key and coverage | Used fields | Role |
| --- | --- | --- | --- |
| `data/PSZusdina/usdina19622016.dta` | DINA micro-record; 11,810,928 rows; observed years 1962, 1964, and 1966--2016 | year, integer wealth percentile, frequency weight, nine balance-sheet components, four personal-income components | Reconstruct bottom-40 and one-percentile allocation shares from the earliest feasible supplied input |
| `data/PSZusdina/Yszshares_fine.dta` | year; unique; 1962--2016 | prepared shares for the same asset and disposable-income classes | Independent aggregation check only; never enters the calculation |
| `data/finalfiles/YwealthFOF.dta` | year; unique; usable 1962--2016 | 29 `h...all` stocks, `NatInc`, `szponog` | Aggregate balance sheets and personal disposable income; stocks and `NatInc` are millions, `szponog` is billions of current dollars |
| `data/finalfiles/Ywealthreturns.dta` | year; unique | housing capital gain and top-10/bottom-90 debt write-down factors | Known valuation adjustments |
| `data/finalfiles/YinequalityNIPAanalysis.dta` | year; unique; usable 1962--2016 | `PersSaving`, `SavingBus` | NIPA personal and business saving; `SavingBus` also measures aggregate corporate disposable income; billions of current dollars |
| `data/PSZusdina/parameters_mss.csv` | year; unique; usable 1962--2016 | `totadults20`, `nideflator` | Adults aged 20 or older, in thousands, and current-to-2018-dollar deflator |
| `MSS_SGR_July242025.pdf` | target paper | embedded Figure 6 image on physical page 24 | External digitized benchmark only |

## Paper-curve digitization

The paper benchmark is not read from a screenshot. Poppler's `pdfimages`
extracts the original 1047-by-698 RGB raster embedded on physical PDF page 24.
The script then:

1. calibrates percentile 40 to raster column 125 and percentile 100 to column
   1006;
2. calibrates a zero saving rate to row 504 and a one-unit rate change to 775
   vertical pixels;
3. selects the exact orange `(200, 82, 0)` and blue `(95, 162, 206)` curve
   colors, avoiding black axes and gray grid lines;
4. samples an eleven-pixel-wide strip around every integer percentile and uses
   the median matching row as the curve center; at percentile 100, where the
   steep final segment enters a large endpoint marker, it instead uses the
   marker's widest horizontal rows to avoid pulling the estimate down the
   connecting segment; and
5. applies the affine pixel-to-data transformation

$$
s^N_i=\frac{504-y_i}{775}.
$$

The implementation retains an interpolation fallback for a percentile falling
inside a rasterized dash gap. The Figure 6 audit finds exact-color pixels in
all 61 sampling strips for both curves, so none of the published Figure 6
coordinates actually require that fallback. One vertical pixel is about 0.129
percentage points. The overlay diagnostic draws the recovered solid
centerlines over the original dashed paper curves; it is a visual audit of the
digitization, not independent evidence about the empirical reconstruction.

Digitization remains approximate because the paper provides pixels rather than
the underlying numerical series. Axis calibration, line thickness, and raster
rounding imply uncertainty of a few tenths of a percentage point in ordinary
parts of the curve, potentially more near the large top-1 endpoint marker. The
comparison statistics should therefore be read at the reported precision, not
as exact equality tests.

## Raw-data reconstruction

`Code/scripts/build_figure6_percentile_shares.py` reads the 16 GB DINA file in
one-million-row chunks and never modifies it. The authors' Stata frequency
weight is reproduced as `round(dweght / 100000)`. Missing component values are
zero within weighted sums, while missing keys fail loudly.

The paper bins are:

- one bottom-40% bin, plotted at percentile 40;
- one bin for every percentile from 40--41 through 98--99; and
- one top-1% bin, plotted at percentile 100.

For each asset or income class $k$, weighted bin totals are normalized within
year to obtain $a_{ikt}$. Personal disposable income is reconstructed at the
micro level as

$$
\texttt{ponog}
=\texttt{poinc}-\texttt{colexp}-\texttt{govin}-\texttt{prisupgov}.
$$

The raw source omits 1963 and 1965. Those two years alone are linearly
interpolated between adjacent annual shares, reproducing the authors'
preparation rule. Every annual share class and the population shares must then
sum to one.

## Disposable-income allocation and valuation closure

Aggregate personal disposable income is allocated with `ponog` shares:

$$
Z^{d,p}_{it}=\texttt{szponog}_t\,a^{ponog}_{it}.
$$

Corporate disposable income is NIPA business saving and is attributed with
corporate-equity shares:

$$
Z^{d,\pi}_{it}=\texttt{SavingBus}_t\,a^{equity}_{it}.
$$

Both aggregate series are converted from billions to millions before
allocation. Housing uses the supplied housing capital gain. Mortgage and
nonmortgage debt use the top-10 or bottom-90 write-down factor according to
the cohort. The common residual equity valuation rate is solved on the exact
Figure 6 percentile allocation so that active saving closes to NIPA personal
plus business saving.

The implementation verifies annually:

$$
\sum_i W_{it}=W_t,
\qquad
\sum_i Z^{d,p}_{it}=Z^{d,p}_t,
\qquad
\sum_i Z^{d,\pi}_{it}=Z^{d,\pi}_t,
$$

$$
\sum_i \Theta_{it}=S^p_t+S^\pi_t,
\qquad
\sum_i s^N_{it}Z^d_{it}=S^p_t+S^\pi_t.
$$

The final equality is the paper's equation (9c).

## Merge contracts

The reconstructed share table has a unique `(year, percentile_bin)` key. It is
merged many-to-one by year with aggregate wealth, valuation inputs, NIPA
saving, disposable income, and demographics. The lagged active-saving
identity yields 3,294 annual observations: 54 years times 61 bins for
1963--2016. No unmatched annual input is allowed in the usable period.

## Validation evidence

Reaggregating the raw percentile shares to the coarser boundaries in the
authors' prepared `Yszshares_fine.dta` file gives maximum absolute differences
between $8.23\times10^{-9}$ and $7.24\times10^{-8}$ across the eleven used
share classes. The largest discrepancy is for equity and is far below the
$10^{-6}$ declared tolerance. The generated validation table records the
worst year and bin for every class.

Against the digitized 2025 Figure 6 curves:

| Window | Common-bin correlation | Mean absolute error |
| --- | ---: | ---: |
| 1963--1982 | 0.991 | 1.46 percentage points |
| 1983--2016 versus paper 1983--2019 | 0.969 | 1.22 percentage points |

Most of the shape is reproduced. The largest gap is the top 1%: the
older-input reconstruction rises from 28.8% to 36.2%, while the paper reports
approximately 43% to 54%. This residual cannot be assigned solely to code
because the paper uses a later data vintage and the digitized benchmark is
approximate.

## Outputs and producers

| Output | Unit/key and contents | Producer |
| --- | --- | --- |
| `Data/interim/figure6_percentile_shares.csv` | year-percentile; asset, income, and population shares; 1962--2016 | `Code/scripts/build_figure6_percentile_shares.py` |
| `Data/interim/figure6_percentile_share_validation.csv` | share class; maximum and mean discrepancy against prepared fine shares | same |
| `Data/processed/figure6_authors_annual.csv` | year-percentile; wealth, active saving, personal/corporate disposable income, net saving rate, mean real wealth; 1963--2016 | `Code/scripts/build_figure6_authors_data.py` |
| `Data/processed/figure6_authors_data.csv` | window-percentile; mean annual rate, pooled diagnostic, mean real wealth | same |
| `Data/processed/figure6_paper_digitized.csv` | percentile; two approximate paper curves | same |
| `Data/processed/figure6_digitization_audit.csv` | period; direct-match and interpolation counts plus pixel scale | same |
| `Data/processed/figure6_authors_comparison.csv` | percentile; aligned paper/ours rates and errors | same |
| `Data/processed/figure6_authors_rolling5.csv` | window-end-percentile; trailing five-year simple mean of the exact annual net-saving rate; 1967--2016 | same |
| `Results_Proposal/figures/figure6_authors_data_percentiles.png` | paper-definition percentile view | same |
| `Results_Proposal/figures/figure6_authors_data_wealth_levels.png` | identical cohort rates indexed by mean real wealth | same |
| `Results_Proposal/figures/figure6_percentile_vs_wealth_level.png` | two-panel comparison holding numerator and denominator fixed | same |
| `Results_Proposal/figures/figure6_authors_data_comparison.png` | reconstructed versus digitized paper curves | same |
| `Results_Proposal/figures/figure6_digitization_overlay.png` | recovered centerlines over the original embedded paper raster | same |
| `Results_Proposal/figures/figure6_digitization_overlay_slide.png` | compact version of the same audit for the comparison deck | same |
| `Results_Proposal/figures/figure6_rolling5_evolution.png` | two-panel five-year evolution diagnostic | same |
| `Results_Proposal/figures/figure6_rolling5_heatmap.png` | all percentile bins over five-year window ends | same |
| `Results_Proposal/figures/figure6_rolling5_selected_percentiles.png` | 80th, 90th, 99th, and top-1 five-year rates | same |

The wealth-level panel changes only the horizontal coordinate. It is therefore
directly comparable with the percentile panel, but its points remain
percentile cohorts located at their mean wealth. It is not yet a fixed-real-
dollar-bin estimate of a household saving schedule $s(w)$.

The trailing-five-year outputs are descriptive diagnostics rather than an
additional paper replication target. They show whether the two paper windows
hide a smooth transition, temporary fluctuation, or heterogeneous paths across
percentiles. They do not identify a structural break or a causal trend.

The earlier pretax-income diagnostic is preserved for audit history in
[`figure6-wealth-level-diagnostic.md`](figure6-wealth-level-diagnostic.md), but
it is superseded for substantive Figure 6 interpretation.
