# Exploratory Figure 6 Wealth-Level Diagnostic: Data Contract

## Role and economic object

This is a **separate exploratory diagnostic**, not an exact replication of the
July 2025 paper's Figure 6. It asks whether the pre/post-1982 saving divergence
remains visible after replacing wealth-percentile rank on the horizontal axis
with each supplied cohort's mean real wealth per adult.

The numerator reuses the active-saving identity verified for Figure 5,

$$
\Theta_{cjt}=W_{cjt}-(1+\pi_{cjt})W_{cj,t-1},
\qquad
\Theta_{ct}=\sum_j\Theta_{cjt},
$$

but it keeps all 21 fine cohorts $c$. It therefore shares an upstream
calculation with the Figure 5 reconstruction while answering a different,
Figure 6-motivated question.

## Input inventory

All inputs are immutable files from the February 2021 authors' package.

| Dataset | Unit/key and coverage | Used fields | Role |
| --- | --- | --- | --- |
| `data/finalfiles/YwealthFOF.dta` | year; unique; usable 1962--2016 | `year`, `NatInc`, 29 `h...all` stocks | Aggregate balance-sheet levels and national income; millions of current dollars |
| `data/PSZusdina/Yszshares_fine.dta` | year; unique; 1962--2016 | 21 cohort shares for ten asset classes and pretax income | Allocates aggregate stocks and national income to fine cohorts |
| `data/finalfiles/Ywealthreturns.dta` | year; unique | housing and top-10/bottom-90 debt valuation factors | Known non-equity valuation adjustments |
| `data/finalfiles/YinequalityNIPAanalysis.dta` | year; unique; usable 1962--2016 | personal and business saving | Aggregate private-saving closure inherited from Figure 5 |
| `data/PSZusdina/parameters_mss.csv` | year; unique; usable 1962--2016 | `totadults20`, `nideflator` | Adults aged 20 or older, in thousands, and current-to-2018-dollar deflator |

All annual merges are one-to-one. The lag in active saving yields a 1963--2016
annual output.

## Wealth coordinate and saving-rate proxy

For cohort $c$, mean real net wealth per adult is

$$
\bar w_{ct}^{2018}
=
\frac{W_{ct}}
     {N_t p_c}
\times d_t,
$$

where $W_{ct}$ is net wealth, $N_t$ is the adult population, $p_c$ is the
cohort population share, and $d_t$ is the supplied 2018-dollar deflator. Since
$W$ is millions of dollars and $N$ is thousands of adults, the implementation
multiplies the quotient by 1,000 to obtain dollars per adult.

For period $P$, the plotted rate is

$$
\widehat s_{cP}
=
\frac{\sum_{t\in P}\Theta_{ct}}
     {\sum_{t\in P}NI_t\,s^{inc}_{ct}},
$$

where $s^{inc}_{ct}$ is the cohort pretax-income share. Using a ratio of period
sums rather than an unweighted mean of annual ratios prevents a noisy annual
top-tail denominator from dominating the result.

The figure reports both the paper-aligned windows 1963--1982 and 1983--2016,
and the endpoint decades 1973--1982 and 2007--2016.

## Identification boundary

The output must not be labelled as replicated Figure 6 because:

- the denominator is cohort pretax income, while the 2025 method uses personal
  plus attributable corporate disposable income;
- every x-coordinate is a percentile cohort's mean wealth, not a fixed
  real-dollar wealth bin; and
- the DINA source is a repeated cross-section, not a household panel.

The diagnostic can reject a simple descriptive claim that only percentile
labels changed. It cannot identify a household-level saving schedule $s(w)$ or
separate behavior, mobility, and cohort composition causally.

## Invariants and outputs

The implementation verifies annually that the 21 fine cohorts sum back to
supplied aggregate net wealth and national income, and that their active saving
preserves the NIPA private-saving closure used in Figure 5.

| Output | Contents | Producer |
| --- | --- | --- |
| `Data/processed/figure6_wealth_level_profiles.csv` | annual 21-cohort wealth, active saving, pretax income, and rate proxy; 1963--2016 | `Code/scripts/build_figure6_wealth_level_diagnostic.py` |
| `Data/processed/figure6_wealth_level_windows.csv` | paper-aligned pre/post and endpoint-decade summaries | same |
| `Results_Proposal/figures/figure6_wealth_level_diagnostic.png` | two-panel static diagnostic indexed by mean real wealth per adult | same |
