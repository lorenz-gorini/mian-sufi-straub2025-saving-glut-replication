# Figure 8: 2021 Direct-Cell Full-Leontief Data Contract

## Role and economic object

This is the third Figure 8 route: **2021-kit direct cells + full Leontief**. It
is designed to be the closest feasible old-vintage test of the operator change.
It is separate from both:

1. the **2021-kit seven-round proxy**, which reads the authors' downstream
   wealth-group positions; and
2. the **public-FWTW full-Leontief rerun**, which uses a June 2026 public
   bilateral dataset.

For wealth group $g$ and year $t$, the estimand remains

$$
ND_{gt}=A^D_{gt}-D_{gt},
$$

where $A^D_{gt}$ is aggregate household debt ultimately owned by group $g$ and
$D_{gt}$ is debt owed by that group. The displayed series is

$$
\frac{ND_{gt}}{NI_t}-\frac{ND_{g,1982}}{NI_{1982}}.
$$

Stocks and national income are millions of current dollars. The chart unit is
percentage points of national income relative to 1982.

## Exact reconstruction boundary

The old Stata program starts from `LQpanel_2019Q1.dta`, completes bilateral
positions using exact identities, proportional allocations, and residuals,
and then unveils selected intermediary blocks in seven sequential rounds. It
does **not** save a general annual 34-instrument-by-27-sector cube.

`Yunveilhhd.dta` nevertheless preserves the completed direct cells and issuer
liability margins used before each round. This route reads 351 such fields and
reconstructs eight coarsened intermediary rows:

- mortgage complex: GSEs, agency pools, ABS issuers, finance companies, and
  mortgage/other REITs;
- monetary authority;
- money-market funds;
- mutual funds;
- private depositories;
- nonfinancial corporate business;
- nonfinancial noncorporate business; and
- property-casualty insurance.

The loader explicitly excludes every `*_hhd1` through `*_hhd7` field, final
`a_hh_hhd`, final government/rest-of-world/other allocations, and every
wealth-group `*_hhdSZ` output. The annual diagnostics record
`round_variables_read = 0`.

This is further upstream than the seven-round proxy, but it is not an exact
reconstruction of the paper's Batty-completed 34-by-27 network. The matrix is
coarsened because the old code saved a sequence of purpose-built cell blocks,
not the target paper's general matrix object.

## Input inventory

| Dataset | Unit/key and coverage | Fields used | Role |
| --- | --- | --- | --- |
| `MSS2021Febreplicationkit/data/finalfiles/Yunveilhhd.dta` | Year; unique; selected sample 1963--2016 | 351 direct positions, issuer margins, household mortgage/consumer-credit positions, and raw mutual-fund portfolio fields | Saved snapshot of the old Stata direct-cell preprocessing; SHA-256 `ef4da4...054` |
| `MSS2021Febreplicationkit/data/PSZusdina/Yszshares_fine.dta` | Year; unique; 1962--2016 | Fine-cohort asset and debt shares | Expand household-holder cells and liabilities to top 1%, next 9%, next 40%, and bottom 50%; SHA-256 `983d4a...842` |
| `MSS2021Febreplicationkit/data/finalfiles/YwealthFOF.dta` | Year; unique; 1960--2016 | `NatInc` | Current-dollar national-income denominator; SHA-256 `b01bd0...00d` |
| `MSS2021Febreplicationkit/code/build_fa_unveiling_data.do` | Stata source | Section 1, lines 19--2405 | Authoritative lineage for completed cells, proportionality assumptions, residuals, and seven-round boundary |
| `MSS_SGR_July242025.pdf` | Target paper | Sections 2.1--2.2 and 4.1--4.2; Figure 8 | Full-operator method and target definition |

The authors-kit directory is read only. All new artifacts are written under
`Data/`, `Results_Proposal/`, and `Presentation/`.

## Direct-cell completion used here

For an old-kit issuer block $i$ and liability component $\ell$, let
$x^\ell_{ij,t}$ be the saved direct holder position and
$L^\ell_{i,t}$ the saved issuer margin. Negative direct weights are clipped,
then the nonnegative positions are rescaled to the margin:

$$
\widetilde x^\ell_{ij,t}
=L^\ell_{i,t}
\frac{\max\{x^\ell_{ij,t},0\}}
     {\sum_k\max\{x^\ell_{ik,t},0\}}.
$$

This rule preserves every nonnegative direct proportion and the authors-kit
issuer margin. It is required because some old Financial Accounts positions
are signed and the coarsened saved blocks no longer retain enough information
to reorient a negative cell to a fully specified counterparty issuer row.
Unlike the public-FWTW route, direction reversal would therefore invent
missing rows. Clipping is explicit and material: the absolute clipped mass is
8.5%--37.8% of aggregate household debt across years. The generated component
audit reports every affected block.

For sectors that the old procedure does not itself unveil—brokers,
holding/funding companies, nonprofits, and unidentified liability residuals—
the reconstruction uses an explicit `unassigned` ultimate-owner column. That
column ultimately owns 3.17%--9.97% of household debt. It is retained for
accounting closure and excluded from the four household wealth groups.

These two choices mean the comparison with the seven-round proxy is a
**same-vintage, closest-feasible operator comparison**, not a causal code-only
experiment.

## Household augmentation and asset mapping

Household direct-holder cells are split before matrix normalization. The DINA
crosswalk follows the old Stata distribution block:

| Direct household claim | DINA distribution |
| --- | --- |
| Mortgages, GSE/bond/CP claims, time deposits, MMF shares, and property-insurance claims | Taxable bonds |
| Checkable deposits and currency | Currency |
| Bank and corporate equity; NFC other loans | Equity |
| Noncorporate equity | Business wealth |
| Life-insurance, private-pension, and government-retirement claims | Pension wealth |
| Mutual-fund shares | Equity, taxable-bond, and municipal shares combined using the old portfolio composition |

The mutual-fund composition is reimplemented from eight raw Financial
Accounts fields preserved in `Yunveilhhd.dta`. The pre-1991 extrapolation
matches the old Stata `ipolate ..., epolate` construction within
$2\times10^{-7}$ of the saved ancillary weights. No unveiled debt field is
used for this validation.

Household home-mortgage and consumer-credit holder cells form the primary
asset vector. Debt owed is allocated with DINA owner-mortgage and nonmortgage
shares, respectively. The saved asset and liability household-debt margins
agree within $2$ million, or less than $3.22\times10^{-7}$ proportionally.

## Full-Leontief solve

Summing completed components and normalizing each active issuer row produces
$\bar M_t=[B_t,Q_t]$, with owner columns first. The new operator is

$$
\Omega_t=(I-Q_t)^{-1}B_t.
$$

If $P^D_t$ is the direct intermediary share of household debt and
$\Lambda^D_t$ its direct owner share, final debt ownership is

$$
A^D_t=D^{HH}_t\left(P^D_t\Omega_t+\Lambda^D_t\right).
$$

This is an infinite-chain solve; no round truncation enters the computation.

## Validation and observed result

- Sample: 54 annual observations, 1963--2016.
- Network: eight coarsened intermediary rows; seven or eight active by year;
  eight ultimate-owner columns including `unassigned`.
- Maximum spectral radius of $Q_t$: 0.180.
- Maximum direct-row closure error: $2.22\times10^{-16}$.
- Maximum unveiled-row closure error: $4.44\times10^{-16}$.
- All primary-asset and debt-liability partitions close, and every displayed
  series is exactly zero in 1982.
- No component falls back to an undocumented distribution.

Against the digitized 2025 paper through 2016:

| Group | Correlation | MAE, percentage points |
| --- | ---: | ---: |
| Top 1% | 0.994 | 2.33 |
| Bottom 99% | 0.995 | 1.31 |

Compared with the old seven-round proxy on the same vintage, the mean absolute
difference is 0.26 points for the top 1% and 0.75 points for the bottom 99%; the
maximum differences are 1.02 and 2.42 points. Thus the infinite-chain
correction is modest in this coarsened old network. The larger paper gap,
especially for the top 1%, is more consistent with matrix-vintage, sector,
instrument, and wealth-mapping changes than with truncating after seven rounds
alone.

## Generated outputs

| Output | Contents |
| --- | --- |
| `Data/processed/figure8_2021_direct_full_leontief.csv` | Annual four-group and bottom-99 asset, liability, net-debt, national-income, and 1982-relative series |
| `Data/interim/figure8_2021_direct_network_diagnostics.csv` | Annual source boundary, dimensions, clipped mass, spectral radius, closure, unassigned share, and portfolio weights |
| `Data/interim/figure8_2021_direct_component_diagnostics.csv` | Year-intermediary-component issuer margin, allocated total, negative-cell mass, and fallback flag |
| `Results_Proposal/figures/figure8_2021_direct_full_leontief.png` | Standalone third-route figure |
| `Data/processed/figure8_2021_operator_comparison_metrics.csv` | Same-vintage full-Leontief minus seven-round differences |
| `Results_Proposal/figures/figure8_2021_operator_comparison.png` | Focused same-vintage comparison |

Route producer: `Code/scripts/build_figure8_2021_direct.py`. Reusable module:
`Code/unveiling/figure8_2021_direct.py`. The comparison producer is separate:
`Code/scripts/build_figure8_method_comparison.py`.

The wide route output now also preserves `home_mortgage` and
`consumer_credit` asset, liability, and net-position columns before summing to
the original total. The selected research extension reshapes and documents
those columns separately in
[`debt-composition-extension-data.md`](debt-composition-extension-data.md); it
does not change the aggregate Figure 8 estimand or comparison route.
