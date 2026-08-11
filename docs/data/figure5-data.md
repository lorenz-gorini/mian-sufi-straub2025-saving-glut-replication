# Figure 5 Data Contract

## Economic object

Figure 5 asks how much active saving comes from each wealth group after
removing valuation gains from changes in wealth. For group $g$, asset or
liability $j$, and year $t$,

$$
\Theta_{gjt}=W_{gjt}-(1+\pi_{gjt})W_{gj,t-1}.
$$

$W_{gjt}$ is a current-dollar stock in millions and $\pi_{gjt}$ is the annual
valuation factor. Summing over assets gives $\Theta_{gt}$. The plotted series
is the trailing ten-year mean of $\Theta_{gt}/NI_t$, less its 1982 value.
The first plotted year is therefore 1972, which averages 1963--1972.

Liabilities enter $W$ with a negative balance-sheet sign. A negative saving
contribution from debt therefore means additional borrowing.

## Input inventory

All inputs are immutable files from the February 2021 authors' package. The
analysis uses their older vintage through 2016 but implements the July 2025
paper's group and display transformations.

| Dataset | Unit/key and coverage | Used fields | Role |
| --- | --- | --- | --- |
| `data/finalfiles/YwealthFOF.dta` | year; unique; usable 1962--2016 | `year`, `NatInc`, 29 `h...all` aggregate asset/liability stocks | Financial Accounts/B.101 wealth totals; millions of current dollars |
| `data/PSZusdina/Yszshares_fine.dta` | year; unique; 1962--2016 | 21 fine-cohort shares for each of ten DINA asset classes | Allocates every aggregate stock to top 1%, next 9%, next 40%, and bottom 50% |
| `data/finalfiles/Ywealthreturns.dta` | year; unique | `JST_housing_capgain`, four `ZIP_*_wd*` series | Housing valuation and top-10/bottom-90 debt write-down factors |
| `data/finalfiles/YinequalityNIPAanalysis.dta` | year; unique; usable 1962--2016 | `PersSaving`, `SavingBus` | NIPA personal plus business saving; supplied billions converted to millions |
| `data/finalfiles/Ysavingwealth.dta` | year; unique; 1963--2016 | `saving_12NI`, `saving_92NI`, `saving_902NI` | Validation only: older coarse-group Stata saving ratios |
| `MSS_SGR_July242025.pdf` | paper Figure 5, physical page 22 | embedded raster | Approximate visual benchmark only; never an empirical input |

The year merges are one-to-one. Aggregate wealth and fine shares overlap in
1962--2016; the lag in the saving identity makes 1963--2016 the annual saving
sample. A complete trailing ten-year window makes 1972--2016 the displayed
sample.

## Fine cohorts and paper groups

| Paper group | Supplied fine cohorts |
| --- | --- |
| Bottom 50% | `f10`, `f20`, `f30`, `f35`, `f40`, `f45`, `f50` |
| Next 40% / 51--90% | `f55`, `f60`, `f65`, `f70`, `f75`, `f80`, `f85`, `f90` |
| Next 9% | `f95`, `f99` |
| Top 1% | `f999`, `f9999`, `f99999`, `f00001` |

The partition is validated once in `Code/unveiling/wealth_groups.py`: every
fine cohort appears exactly once. Bottom 99% is the sum of the other three
groups.

## Asset mapping and valuation rules

`Code/unveiling/figure5_authors.py` maps the 29 supplied balance-sheet
categories to the same DINA share classes used by the kit's
`build_wealth_saving_data.do`.

- Owner-occupied real estate uses the supplied JST housing capital gain.
- Fixed-income assets use zero price inflation, matching the old pipeline.
- Household liabilities use negative cohort-specific write-down rates: top 1%
  and next 9% use the top-10 series; the lower groups use the bottom-90 series.
- Seven equity-like categories share a residual price inflation. It is chosen
  annually so the sum of reconstructed group saving equals NIPA personal plus
  business saving.

The last rule is an accounting closure, not a fitted behavioral model. If
$E_t$ is aggregate equity-like wealth and $\Theta_t^{K}$ is active saving in
the categories with known valuation factors, the residual factor is

$$
\pi_t^E=\frac{E_t-(S_t^p+S_t^\pi-\Theta_t^K)}{E_{t-1}}-1.
$$

## Boundaries and invariants

The boundary loaders require the named columns, unique integer years, finite
required values, and fine shares that sum to one by asset class. The pipeline
then verifies:

1. group allocations sum back to each aggregate asset or liability stock;
2. annual reconstructed saving equals NIPA private saving to less than
   $10^{-10}$ of national income;
3. the 1982 displayed value is zero for every group; and
4. the fine-share reconstruction remains within 0.3 percentage points of
   national income of the old coarse Stata series. The observed maximum is
   0.289 percentage points in 1987 for the top 1%.

The fourth comparison is deliberately not an equality test: the supplied fine
shares required for the 2025 four-group display are not identical to the old
coarse allocation.

## Generated outputs

| Output | Contents | Producer |
| --- | --- | --- |
| `Data/processed/figure5_authors_annual.csv` | annual group saving, NIPA closure, and residual equity factor; 1963--2016 | `Code/scripts/build_figure5_authors_data.py` |
| `Data/processed/figure5_authors_data.csv` | ten-year means and 1982-relative display series; 1972--2016 | same |
| `Data/processed/figure5_saving_validation.csv` | Python fine-share versus older Stata coarse ratios | same |
| `Data/processed/figure5_paper_digitized.csv` | approximate 2025 paper series; 1972--2019 | same |
| `Data/processed/figure5_authors_comparison.csv` | common-period paper/reconstruction values and errors | same |
| `Results_Proposal/figures/figure5_authors_data_reconstruction.png` | standalone five-group reconstruction | same |
| `Results_Proposal/figures/figure5_authors_data_comparison.png` | headline top-1/bottom-99 comparison | same |

The digitized paper series are benchmark evidence only. Their 1982 pixels are
renormalized to zero to impose the figure's stated definition and avoid
counting raster placement error as an economic discrepancy.
