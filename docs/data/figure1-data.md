# Figure 1 Data and Lineage

This is a selective, update-as-discovered inventory for Figure 1. It documents
only files that have proved useful for tracing or constructing the result. It
must be extended whenever later work discovers another relevant file, field,
revision, or limitation; future agents should not rescan the entire authors'
data directory merely to make this document look exhaustive.

## Economic object

Figure 1 asks how much of the U.S. household sector's financial assets sit
behind a financial intermediary and therefore need to be unveiled. With

\[
D_t(i,H)=\text{liabilities issued by sector }i
          \text{ and held by households},
\]

the amount behind the veil is

\[
V_t=\sum_{i\in\mathcal F}D_t(i,H),
\]

where \(\mathcal F\) contains financial-intermediary issuers. The two plotted
series are

\[
\frac{V_t}{\sum_{i\ne ROW}D_t(i,H)}
\quad\text{and}\quad
\frac{V_t}{NI_t}.
\]

Thus "owned indirectly" describes the household's observed claim on an
intermediary: it is a direct claim on the intermediary but an indirect claim on
the primary assets financed by that intermediary. It is not
\(\Omega_t-\bar M_t\). Equation (1) is used to trace where the amount behind
the veil ultimately leads.

The target paper combines **34 instruments** into bilateral positions among
four ultimate-owner sectors and 23 financial-intermediary sectors. Thus 23 is
the number of intermediaries, not the number of instruments.

## Authors-data reconstruction from the February 2021 snapshot

The downloaded February 2021 package now contains enough authors-supplied data
to reconstruct the stock behind the veil without rebuilding every Financial
Accounts table. It does not contain the 2025 paper's completed annual 27-by-27
matrices or all underlying FWTW text files, so it cannot deliver an exact
same-code reproduction of the revised paper.

| Dataset | Unit/key and coverage | Role in reconstruction |
| --- | --- | --- |
| `data/fof/LQpanel_2019Q1.dta` | quarter; unique `quarter`, 1945Q4--2019Q4 | Authors' prepared wide Financial Accounts panel; supplies Q4 household claims on named intermediary instruments and household financial-asset totals. |
| `data/finalfiles/Yunveilhhd.dta` | year; unique `year`, 1945--2019 | Authors' final old-method allocation file; supplies household financial-intermediary bond claims. |
| `data/crsp/msf.dta` | security-month, 1945--2018 | Authors' raw CRSP monthly stock file; supplies listed financial-intermediary market capitalization. |
| `data/finalfiles/YinequalityNIPAanalysis.dta` | year; unique `year`, 1913--2016 | Authors' annual national-income denominator. |

The common sample is 1963--2016 because the supplied national-income analysis
file ends in 2016. Starting from `LQpanel_2019Q1.dta` legitimately skips the
authors' upstream import, cleaning, and wide merge. The substantive aggregation
is retained explicitly:

\[
\begin{aligned}
V_t^{A}={}&\text{checkable deposits and currency}
 +\text{time and saving deposits}+\text{money-market-fund shares}\\
&+\text{GSE securities}+\text{mutual-fund shares}
 +\text{life-insurance reserves}+\text{funded pension entitlements}\\
&+\text{financial-intermediary bonds}
 +\text{listed financial-intermediary equity}.
\end{aligned}
\]

Funded pension entitlements equal total pension entitlements minus unfunded
claims. The bond term sums the four authors' allocated categories
`a_hh_absbnd`, `a_hh_fincbnd`, `a_hh_mreitbnd`, and `a_hh_pdibnd`.
Listed financial equity is rebuilt from the supplied CRSP records: retain each
December observation; apply the authors' share-code exclusion; classify SIC
6000--6399 and 6700--6799 as financial; compute market capitalization as
`abs(price) * shares_outstanding / 1000`; and multiply the aggregate by the
authors' household share of listed equity. This transparent extension is
broader than the three financial industries in the old support script and is
not claimed to be the unavailable 2025 equity extension.

Two share denominators are reported. The broad diagnostic is total household
financial assets less unfunded pensions. The paper-scope proxy additionally
removes private foreign deposits, residual miscellaneous assets, and old-kit
estimates of household claims on nonfinancial corporate bonds, equity, and
other loans. Neither is asserted to be the exact 2025 denominator because the
revised sector/instrument crosswalk is absent.

Generated outputs are:

| Output | Purpose |
| --- | --- |
| `Data/processed/figure1_authors_data.csv` | Annual authors-data reconstruction and components. |
| `Data/processed/figure1_paper_digitized.csv` | Approximate benchmark digitized from the paper's embedded Figure 1 raster. |
| `Data/processed/figure1_authors_comparison.csv` | Year-aligned reconstructed and digitized series. |
| `Results_Proposal/figures/figure1_authors_data_comparison.png` | Authors-data comparison used in the report and presentation. |

Over 1963--2016, the national-income-normalized series has a mean absolute
error of 0.053 national-income units (5.3 percentage points of national
income) and correlation 0.995 relative to the digitized curve. It begins at
144.4% versus 148.5% and ends at 263.9% versus 269.0%. The broad-denominator
ownership share has a 3.2-percentage-point mean absolute error; the more
conceptually targeted paper-scope proxy has a 6.6-point error. The level result
is therefore a close old-vintage authors-data reconstruction, while the share comparison
remains denominator- and vintage-sensitive.

## New-data robustness inputs

| Dataset ID | Path | Role and provenance | Unit of observation and key | Coverage and shape | Unit |
| --- | --- | --- | --- | --- | --- |
| `fed_fwtw_2026q1` | `Data/raw/fwtw/fwtw_data_2026-06-18.csv` | Immutable current Federal Reserve EFA FWTW release, retrieved 2026-08-05 | instrument-holder-issuer-quarter; unique key `Instrument Code`, `Holder Code`, `Issuer Code`, `Date` | 1945Q4--2026Q1; 921,120 rows x 8 columns; 31 instruments, 27 holder codes including total/discrepancy, 26 issuer codes including total | Level stock, millions of current dollars |
| `bea_national_income_2026` | `Data/raw/national_income/A032RC1A027NBEA_2026-08-05.csv` | Immutable BEA series distributed by FRED, retrieved 2026-08-05 | year; `observation_date` is unique | 1929--2025; 97 rows x 2 columns | Annual flow, billions of current dollars; converted to millions |
| `figure1_series` | `Data/processed/figure1_indirect_household_ownership.csv` | Rebuildable output of `Code/scripts/build_figure1.py` | year; unique | 1963--2019; 57 rows x 6 columns | Current-dollar stocks plus fractions/ratios |

Raw-file checksums and retrieval URLs are recorded in `Data/raw/README.md`.
The FWTW release contains 26,834 negative long-form levels. The Federal
Reserve explicitly permits these for net positions and historical data
imperfections, so the loader preserves rather than silently truncates them.
Figure 1 aggregates the published values by issuer and does not require every
bilateral cell to be a nonnegative ownership share.

### Used FWTW columns

| Column | dtype after reading | Meaning | Missingness |
| --- | --- | --- | --- |
| `Instrument Name` | string | Financial Accounts instrument | none |
| `Instrument Code` | int32 | Five-digit instrument identifier | none |
| `Holder Name`, `Holder Code` | string, int16 | Direct holder/lender sector | none |
| `Issuer Name`, `Issuer Code` | string, int16 | Issuer/borrower sector | none |
| `Date` | string | Quarter in `YYYYQ#` form | none |
| `Level` | float64 | Bilateral stock | none |

We retain Q4 observations, use holder code 15 (households), and restrict the
generated result to 1963--2019. The domestic denominator excludes rest-of-
world issuer code 26 and aggregate/discrepancy codes 89 and 90. The numerator
also excludes the ultimate-owner issuers (15, 21, 26, 31) and nonfinancial
business issuers (10, 11); the remaining issuer codes are financial
intermediaries. Claims on nonfinancial businesses remain financial claims in
the denominator but are not themselves behind a financial intermediary.

### Output schema

| Column | Unit | Formula |
| --- | --- | --- |
| `year` | calendar year | Q4 balance-sheet date |
| `indirect_household_assets_millions` | millions of current dollars | \(V_t\) |
| `us_financial_assets_millions` | millions of current dollars | \(\sum_{i\ne ROW}D_t(i,H)\) |
| `national_income_millions` | millions of current dollars | BEA series multiplied by 1,000 |
| `indirect_share` | fraction | indirect amount / household U.S. financial assets |
| `indirect_assets_to_national_income` | ratio | indirect amount / national income |

The merge is one-to-one on year and must cover every year from 1963 through
2019. The accounting invariant is
\(0\le V_t\le\sum_{i\ne ROW}D_t(i,H)\).

## Minimal map of useful February 2021 files

The 2021 package is read-only and does not contain the completed annual FWTW
matrices or the exact 2025 Figure 1 series. These are the old-kit datasets
inspected closely enough to be relevant now.

| Dataset | Shape and key | What it contains | Figure 1 use |
| --- | --- | --- | --- |
| `data/fof/LQpanel_2019Q1.dta` | 297 x 1,111; unique quarter, 1945Q4--2019Q4 | Authors' prepared wide Financial Accounts panel | Primary authors-data balance-sheet input; avoids redoing mechanical table imports and supports the nine recoverable claim groups, but not the complete 34-matrix aggregation |
| `data/fof/LQpanel_2019Q1withgov.dta` | 294 x 1,049; unique quarter, 1945Q4--2019Q1 | Wide panel of Financial Accounts series assembled from sector/instrument tables | Upstream source for the old round-by-round debt unveiling; not a completed issuer-holder matrix |
| `data/finalfiles/Yunveilhhd.dta` | 75 x 2,117; unique year, 1945--2019 | Household-debt allocation, intermediate variables, and household/foreign contributions through rounds 1--7 | Supplies four authors-derived financial-intermediary bond allocations |
| `data/finalfiles/Yunveil.dta` | 75 x 2,170; unique year, 1945--2019 | Merge of old household-, government-, and mortgage-debt unveiling outputs; includes national income and the round variables | Closest final old unveiling file, but still debt-specific and not the 27-sector matrix |
| `data/crsp/msf.dta` | 4,346,059 x 8; security-month, 1945--2018 | Raw CRSP monthly security file supplied in the kit | Rebuilds listed financial-intermediary equity using the old code's December/share-code rules plus an explicit financial-SIC classification |
| `data/finalfiles/YinequalityNIPAanalysis.dta` | annual; unique year, 1913--2016 | Authors' national-income analysis file | Supplies the authors-data annual-flow denominator and fixes the common endpoint at 2016 |
| `data/finalfiles/YwealthFOF.dta` | 57 x 3,895; unique year, 1960--2016 | Wealth-group Financial Accounts asset/liability levels and shares; `NatInc` plus DINA/DFA variants | Downstream distributional wealth input, not the aggregate Figure 1 network |
| `data/fof/b101_09182019.dta` | 294 x 53; unique quarter, 1945Q4--2019Q1 | Table B.101 household balance-sheet series | Supplies household totals but not counterparty-complete FWTW cells |
| `data/fof/l125_09182019.dta` | 294 x 33; unique quarter, 1945Q4--2019Q1 | Table L.125 Government-Sponsored Enterprises | Useful for tracing GSE liabilities, but not sufficient to build the whole network |

Representative variables in `Yunveil.dta` are `a_hhd_tot` (total household
debt), `a_hh_hhd` (household-held household debt), `a_gov_hhd`, `a_row_hhd`,
`a_oth_hhd`, `a_hh_hhd1`--`a_hh_hhd7`, and `fa896140001a` (national income).
Most of the 2,170 columns are raw or intermediate Financial Accounts series;
they should not be documented unless a selected result actually uses them.

SHA-256 checksums pin the inspected vendor snapshot:

| File | SHA-256 |
| --- | --- |
| `LQpanel_2019Q1.dta` | `be73233df5310a3a87c6b85d4f778bb37ce7b0bb826b44e693510b342ea19bfa` |
| `LQpanel_2019Q1withgov.dta` | `95b15c997c1b7e1e6227961f51c4e4591a62fd6fa837a91cb7a7dc68698e7024` |
| `Yunveilhhd.dta` (current vendor tree, regenerated by Stata) | `fb2c0419e106357181314aac98227811856f58a012fc6a4016bc45f7634f6a6d` |
| `Yunveilhhd.dta` (preserved downloaded copy) | `d3b815def5593de2d239f4794f51924539ffa9535a47e2234e390e29c32bf30c` |
| `crsp/msf.dta` | `874a6e02f1dbdaaeb68896ecc33cc90dc21f1562b4f4d9a7b6ac7d8221ac7c5d` |
| `YinequalityNIPAanalysis.dta` (current vendor tree) | `c8d947a401a4ca26a3d1ff075dc2359a9f708c9511bb63645c5b10f0f267fe65` |
| `Yunveil.dta` | `d3e054df638b1397a39c501a75f5f635eb4f4f838f38d157919e69a2f5100b57` |
| `YwealthFOF.dta` | `9232c66b59a32b3541cecc3968aca0ab5c6a42e95d44b904203a6424376b6c41` |
| `b101_09182019.dta` | `f59341501e29186251b9542a862b51e0c4122e6396ab069f516e87046cc68914` |
| `l125_09182019.dta` | `a593651f23389414eb6d51f35dd44bf31fadac07088396cfcb068db3e5899c40` |

## Version boundary

There are now two complementary exercises. The authors-data result uses the
February 2021 snapshot and closely reconstructs the level series, but its old
sector taxonomy and missing completed 2025 matrices prevent an exact revised-
paper share. The current public FWTW result is a robustness exercise: it has 21
intermediary sectors after the four owners, whereas the paper uses 23, extends
the then-current Batty et al. matrices to corporate equity, and separately
identifies public and private corporations. It also embodies later Financial
Accounts revisions. Neither exercise should be labelled an exact 2025-vintage
reproduction.
