# Debt-Composition Extension Data Contract

## Economic object and status

This contract documents the implemented Stage 1 extension proposed in
[`research_extension_idea_2.md`](../../research_extension_idea_2.md). It holds
the validated 2021-direct/full-Leontief Figure 8 network fixed and separates
its primary household-debt vector into:

- `home_mortgage`: owner-occupied home-mortgage debt; and
- `consumer_credit`: the authors-kit aggregate consumer-credit block.

For wealth group $g$, category $k$, and year $t$, the stock estimand is

$$
ND_{gkt}=A_{gkt}-L_{gkt},
$$

where $A_{gkt}$ is the category's debt ultimately owned after unveiling and
$L_{gkt}\geq 0$ is the liability owed. Stocks are millions of current dollars.
Ratios are fractions of current national income, and the presentation reports
percentage-point changes relative to 1982.

The matching active-saving contribution uses the Figure 5 negative-liability
sign. For $W_{gkt}=-L_{gkt}$ and valuation factor $\pi_{gkt}$,

$$
S^L_{gkt}=W_{gkt}-(1+\pi_{gkt})W_{gk,t-1}.
$$

Additional borrowing is therefore a negative saving contribution. The
write-down adjustment prevents debt forgiveness from being misclassified as
active repayment.

## Inputs and merge contracts

| Input | Unit/key and coverage | Used fields | Role |
| --- | --- | --- | --- |
| `MSS2021Febreplicationkit/data/finalfiles/Yunveilhhd.dta` | Year; unique; 1963--2016 | Direct mortgage and consumer-credit holder cells, category margins, and the 351-field direct-network contract | Category-specific primary asset vectors and fixed coarsened network |
| `MSS2021Febreplicationkit/data/PSZusdina/Yszshares_fine.dta` | Year; unique; 1962--2016 | Owner-mortgage, nonmortgage, and asset-class wealth shares | Four-group borrower liabilities and household-holder allocation |
| `MSS2021Febreplicationkit/data/finalfiles/YwealthFOF.dta` | Year; unique; 1962--2016 | Aggregate balance-sheet categories and `NatInc` | Figure 5 signed debt levels and national-income denominator |
| `MSS2021Febreplicationkit/data/finalfiles/Ywealthreturns.dta` | Year; unique | `ZIP_mdebt_wd10`, `ZIP_mdebt_wd90`, `ZIP_cdebt_wd10`, `ZIP_cdebt_wd90` | Top-10/bottom-90 mortgage and consumer-debt write-down factors |

All joins are annual one-to-one joins. The boundary validation requires unique,
contiguous years and complete 1963--2016 coverage. Authors-kit files remain
read only.

## Processed outputs

### `Data/processed/debt_composition_2021_direct.csv`

Unit of observation and primary key: `(year, category, group)`. Shape: 540
rows = 54 years $\times$ 2 categories $\times$ 5 displayed groups. `bottom_99`
is the exact sum of `next_9`, `next_40`, and `bottom_50`.

| Column | Unit | Meaning |
| --- | --- | --- |
| `year` | calendar year | 1963--2016 |
| `category` | category | `home_mortgage` or `consumer_credit` |
| `group` | wealth group | `top_1`, `next_9`, `next_40`, `bottom_50`, or `bottom_99` |
| `debt_assets_millions` | current-dollar millions | Category claims ultimately owned by the group |
| `debt_liabilities_millions` | current-dollar millions | Positive category liabilities owed by the group |
| `net_debt_millions` | current-dollar millions | Assets minus liabilities |
| `*_to_national_income` | fraction | Stock divided by current national income |
| `*_relative_to_1982` | fraction | National-income ratio minus its 1982 value |

### `Data/processed/debt_composition_saving_contributions.csv`

Unit/key: `(year, category, group)`; 540 rows. It reports positive liability
stocks, signed active-saving contributions, their sign-reversed active-
borrowing flows, national income, and corresponding national-income ratios.

### `Data/processed/debt_composition_period_summary.csv`

Unit/key: `(period, category, group)`; 40 rows. Periods are 1963--1982,
1983--1997, 1998--2007, and 2008--2016. The two `*_pp_national_income`
columns are mean annual percentage-point contributions.

### Presentation and diagnostic layers

| Output | Role |
| --- | --- |
| `Data/processed/debt_composition_presentation_metrics.csv` | Generated 1982--2007/2016 stock changes and 1998--2007 saving-flow values used by the short deck |
| `Data/interim/debt_composition_accounting_diagnostics.csv` | Annual category closure, convergence, and unassigned-owner diagnostics |
| `Results_Proposal/figures/debt_composition_liability_stocks.png` | Time paths of gross category liabilities by group |
| `Results_Proposal/figures/debt_composition_unveiled_net_positions.png` | Category-specific unveiled net positions |
| `Results_Proposal/figures/debt_composition_saving_contributions.png` | 1998--2007 active-saving contributions |

Producer: `Code/scripts/build_debt_composition_extension.py`. Reusable logic:
`Code/unveiling/figure8_2021_direct.py` and
`Code/unveiling/debt_composition_extension.py`.

## Accounting validation

The extension must satisfy, for every year and wealth group,

$$
X_{gt}^{\mathrm{mortgage}}+X_{gt}^{\mathrm{consumer\ credit}}
=X_{gt}^{\mathrm{total}},
\qquad X\in\{A,L,ND\}.
$$

Observed validation on 2026-08-14:

- 54 annual observations and zero seven-round output fields read;
- maximum spectral radius: 0.180;
- maximum category primary-asset closure error: $4.17\times10^{-16}$;
- maximum category liability closure error: $1.86\times10^{-9}$ million;
- maximum category-to-total additivity error: $9.31\times10^{-10}$ million;
- mortgage unassigned ultimate-owner share: 1.65%--9.63%; and
- consumer-credit unassigned share: 5.41%--11.36%.

## Verified descriptive findings and limits

From 1982 to 2007, mortgage liabilities rose by 23.63 percentage points of
national income for the next 40% and 13.85 points for the bottom 50%, compared
with 4.50 points for the top 1%. Consumer-credit increases were 2.92, 4.04,
and 0.00 points, respectively. During 1998--2007, mortgage borrowing
contributed -3.09 percentage points per year to active saving for the next 40%
and -2.28 points for the bottom 50%, compared with -0.43 points for the top 1%.

After unveiling, the 1982--2007 mortgage net-position change is +8.69 points
for the top 1%, -19.02 points for the next 40%, and -13.73 points for the
bottom 50%. These are descriptive accounting results. They do not identify a
credit-supply effect, a house-price response, or household welfare.

The period evidence also reveals a break after the housing boom. For the
bottom 99%, the average mortgage contribution to active saving changes from
-6.36 percentage points of national income per year in 1998--2007 to -0.16 in
2008--2016, while the consumer-credit contribution remains negative at -1.44
points. For the bottom 50%, the mortgage contribution turns positive at +0.42
points after 2008, consistent with net active mortgage repayment after the
crisis. Correspondingly, the bottom 50%'s mortgage-liability increase relative
to 1982 falls from 13.85 points in 2007 to 1.81 points in 2016, while its
consumer-credit increase rises from 4.04 to 4.82 points.

The unveiled positions evolve differently across groups. By 2016, the top
1%'s mortgage net position is 9.33 points above its 1982 value and the next
40% remains 15.99 points below, whereas the bottom 50% has recovered from
-13.73 points in 2007 to -2.32 points in 2016. Consumer-credit net positions
continue to widen through 2016: +3.61 points for the top 1%, -5.45 for the
next 40%, and -5.19 for the bottom 50%.

This time pattern supports a two-regime interpretation: mortgage expansion is
the main debt-related saving drag during the pre-2008 boom, while the residual
post-2008 borrowing of the lower wealth groups is relatively more
consumer-credit intensive. It does not establish that either debt category
caused the total Figure 6 saving-rate movement, because the present flow metric
is scaled by aggregate national income rather than each group's disposable
income and the analysis contains no exogenous credit-supply variation.

`consumer_credit` does not distinguish credit cards, vehicles, student loans,
or medical debt. The network remains the same eight-row coarsening described
in [`figure8-2021-direct-data.md`](figure8-2021-direct-data.md), not the
unavailable 2025 34-instrument, 27-sector matrix.
