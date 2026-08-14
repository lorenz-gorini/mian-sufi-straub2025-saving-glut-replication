# Figure 8 Public-FWTW Data Contract

## Classification and estimand

This pipeline is the **newer-public-data full-Leontief robustness route** for
the July 2025 Figure 8 method. It is intentionally separate from the retained
**2021-kit seven-round proxy** documented in
[`figure8-data.md`](figure8-data.md) and the closest-feasible
**2021-direct-cell full-Leontief** route documented in
[`figure8-2021-direct-data.md`](figure8-2021-direct-data.md).

For wealth group $g$ and year $t$,

$$
ND_{gt}=A^D_{gt}-D_{gt},
$$

where $A^D_{gt}$ is the amount of aggregate household debt ultimately owned by
group $g$ after the full financial network is unveiled and $D_{gt}$ is debt
owed by that group. The plotted quantity is

$$
\frac{ND_{gt}}{NI_t}-\frac{ND_{g,1982}}{NI_{1982}}.
$$

All balance-sheet stocks and national income are in millions of current
dollars. The display is in percentage points of national income relative to
1982. Positive values mean net lending to other households; negative values
mean net borrowing.

The result is not labelled an exact numerical reproduction. It implements the
paper's operation on a different input vintage: the paper reports a custom
34-instrument, 27-sector network through 2019, while the pinned public release
has 31 instruments, 25 substantive sectors, and is combined with supplied DINA
and national-income inputs through 2016.

## Input inventory

| Dataset | Unit/key and coverage | Used fields | Role |
| --- | --- | --- | --- |
| `Data/raw/fwtw/fwtw_data_2026-06-18.csv` | instrument-holder-issuer-quarter; unique; 1945Q4--2026Q1 | instrument, holder, issuer, date, level | Published completed bilateral positions; June 18, 2026 Federal Reserve vintage; levels in current-dollar millions; SHA-256 `ca1305...892` |
| `MSS2021Febreplicationkit/data/PSZusdina/Yszshares_fine.dta` | year; unique; 1962--2016 | fine-cohort shares for currency, taxable bonds, munis, equity, pensions, business, financial assets, owner mortgage debt, and nonmortgage debt | Split the household holder and household liabilities across four wealth groups; SHA-256 `983d4a...842` |
| `MSS2021Febreplicationkit/data/finalfiles/YwealthFOF.dta` | year; unique; 1960--2016 | `NatInc` | Authors-kit national income in current-dollar millions; used only as denominator |
| `MSS_SGR_July242025.pdf` | target paper | Sections 2.1--2.2, 4.1--4.2, Table A1, Figure 8 | Authoritative method, mapping, target, and digitized external benchmark |

The Federal Reserve states that the public FWTW estimates combine identified
bilateral relationships, institutional exclusions, and proportional balancing
to Financial Accounts issuer and holder totals. The CSV is therefore treated
as the completed direct-position input, not as raw margins that this project
must complete again.

## Unit, keys, and filters

- FWTW unit: one completed instrument-holder-issuer-quarter level.
- FWTW primary key: `Instrument Code`, `Holder Code`, `Issuer Code`, `Date`.
- Annualization: fourth-quarter stocks, 1963--2016.
- Public total sector 89 and accounting-discrepancy sector 90 are excluded from
  the economic network.
- Owner sectors before the wealth split are households 15, federal government
  31, state/local government 21, and rest of world 26.
- Every other substantive sector is an intermediary when it has positive
  issuer activity that year. Inactive early sectors are omitted for that year.
- After the household split there are seven ultimate owners: top 1%, next 9%,
  next 40%, bottom 50%, federal government, state/local government, and rest of
  world.

## Instrument-to-DINA crosswalk

The paper's Table A1 determines the mapping. The current public taxonomy
requires the following explicit approximations:

| DINA class | Public FWTW instruments |
| --- | --- |
| Currency | Checkable deposits and currency |
| Taxable bonds | Federal funds/repos; gold/SDRs; time, savings, and other deposits; MMF shares; Treasury, GSE, corporate/foreign bonds; mortgages; consumer credit; loans; open-market paper; trade credit; taxes payable; FDI debt; net interbank |
| Municipal securities | Municipal securities |
| Equity | Corporate equity and FDI equity |
| Pensions | Life-insurance reserves and pension entitlements |
| Business | Miscellaneous other equity, whose household position is overwhelmingly noncorporate business equity |
| Wealth minus housing / broad financial assets | Three miscellaneous-claims instruments |
| Mutual funds | Split into equity, municipal, and taxable-bond components using the public FWTW mutual-fund sector's own asset composition in the same year |

Monetary gold/SDRs and a few residual fixed claims have no exact Table A1
counterpart and use the closest taxable-bond class. This is a declared
crosswalk approximation, not a hidden fallback.

Household liabilities follow Table A1 more tightly:

- home mortgages: public instrument 30651, allocated with owner-mortgage DINA
  shares;
- consumer credit, depository-institution loans, and other loans: instruments
  30660, 30680, and 30690, allocated with nonmortgage-debt shares; and
- deferred and unpaid life-insurance premiums: the household-issued identified
  miscellaneous Part 2 position, instrument 30900, which is held by life
  insurers and allocated with nonmortgage-debt shares.

## Full-Leontief transformation

For instrument $\ell$, issuer $i$, and holder $j$, let $X^\ell_{ij,t}$ denote
the published FWTW level. Household-holder cells are split across wealth groups
using the mapped DINA shares before instruments are summed. For intermediary
$i$, the direct ownership row is

$$
\bar M_{ij,t}=
\frac{\sum_\ell X^\ell_{ij,t}}
     {\sum_j\sum_\ell X^\ell_{ij,t}}.
$$

With owner columns first, write intermediary rows as $[B_t,Q_t]$. The full
unveiled ownership matrix is

$$
\Omega_t=(I-Q_t)^{-1}B_t.
$$

If $P^D_t$ gives intermediary direct holdings of household debt and
$\Lambda^D_t$ gives direct owner holdings, ultimate household-debt ownership
is

$$
A^D_t=D^{HH}_t\left(P^D_t\Omega_t+\Lambda^D_t\right).
$$

This is an infinite-chain solve. No finite-round truncation enters this
pipeline.

Because ultimate-owner rows are zero in the intermediation block, the
household augmentation changes the owner columns of the solve rather than
creating new intermediary rows. Household-issued debt is handled separately
in $P^D_t$ and $\Lambda^D_t$, so assets and liabilities can be checked against
the same aggregate household-debt stock. The full seven-owner asset allocation
sums to that stock; the four household wealth groups alone need not, because
government and rest-of-world owners can also hold household debt.

## Negative levels and discrepancy treatment

The Federal Reserve technical note explains that a negative FWTW level can be
interpreted as the economic direction being reversed. The primary pipeline
therefore swaps issuer and holder and takes the absolute level before the
household split. A separately generated sensitivity instead clips negative
levels to zero. The maximum headline difference between these treatments is
0.09 percentage points for the top 1% and 0.17 points for the bottom 99%.

The discrepancy pseudo-sector is excluded rather than treated as an ultimate
owner. Rows are then normalized over substantive economic holders, matching
the paper's owner/intermediary taxonomy. This preserves the ownership-share
invariant but means the public accounting discrepancy is outside the
estimand.

## Validation and observed result

- 54 annual observations, 1963--2016.
- 31 instruments and 25 substantive sectors in every year.
- 17--21 active intermediary sectors, reflecting sectors that do not yet exist
  or have no activity in early years.
- Maximum spectral radius of $Q_t$: 0.504.
- Maximum direct-row and unveiled-row closure errors: below
  $9\times10^{-16}$.
- Minimum unveiled and household-debt owner share after reorientation: zero
  and 0.0126, respectively.
- Full ultimate-owner household-debt asset shares sum to one, and the four
  household-group liabilities sum to aggregate household debt.
- Every displayed series is exactly zero in 1982.

Against the digitized paper series through 2016, the public reconstruction has
top-1 correlation 0.998 and mean absolute error 2.12 percentage points. The
old proxy has 0.993 and 2.41 points. For the bottom 99%, the new reconstruction
has correlation 0.995 and mean absolute error 1.98 points, while the old proxy
is closer in level with 1.38 points. The full operator improves the top-1
dimension most exposed to ultimate ownership, but the changed FWTW taxonomy
and vintage do not uniformly reduce numerical error.

## Generated outputs

| Output | Contents |
| --- | --- |
| `Data/processed/figure8_public_fwtw_full_leontief.csv` | Preferred annual four-group and bottom-99 asset, liability, net-debt, ratio, and 1982-relative series |
| `Data/processed/figure8_public_fwtw_clipped_sensitivity.csv` | Same schema under zero clipping of negative FWTW levels |
| `Data/interim/figure8_public_fwtw_network_diagnostics.csv` | Annual matrix dimensions, negative-level mass, spectral radius, closure errors, and mutual-fund split |
| `Data/processed/figure8_method_comparison.csv` | Aligned digitized paper and all three separately generated routes |
| `Data/processed/figure8_method_comparison_metrics.csv` | Correlation, MAE, and RMSE by route and group |
| `Results_Proposal/figures/figure8_public_fwtw_full_leontief.png` | Standalone newer-public-data robustness result |
| `Results_Proposal/figures/figure8_public_fwtw_sensitivity.png` | Negative-position treatment sensitivity |
| `Results_Proposal/figures/figure8_method_comparison.png` | Headline paper-versus-three-routes comparison |
| `Results_Proposal/figures/figure8_method_comparison_top1.png` | Top-1 paper-versus-three-routes comparison used in the focused deck |
| `Results_Proposal/figures/figure8_method_comparison_bottom99.png` | Bottom-99 paper-versus-three-routes comparison used in the focused deck |

Route producer: `Code/scripts/build_figure8_public_fwtw.py`. Reusable
implementation: `Code/unveiling/figure8_public_fwtw.py`. The comparison
outputs are produced separately by
`Code/scripts/build_figure8_method_comparison.py`.
