# T-004 Figure 1 Replication

## Objective and current classification

Reconstruct July 2025 Figure 1 from the earliest feasible inputs in the
February 2021 replication kit, implement the economically substantive steps in
Python, and compare the resulting annual series with the published figure.
The current output is an **old-input reconstruction of the 2025 Figure 1
definition through 2016**. It is neither the old paper's unveiled-debt figure
nor an exact same-vintage reproduction of the revised paper.

This record owns the Figure 1 part of T-004. T-004 remains active because
Figures 5 and 8 are still outstanding.

The earlier public-data implementation remains an intentional secondary
result. `Code/scripts/build_figure1.py` reads only the pinned June 2026 FWTW
release and BEA/FRED national income, covers 1963--2019, and writes only
`figure1_indirect_household_ownership.csv` and its matching figure. It is not
called by the primary authors-kit pipeline and is not superseded by it.

## Economic question and equation

Let

$$
D_t(i,H)=\text{year-end liabilities issued by sector }i
          \text{ and held directly by households},
$$

in millions of current dollars. If $\mathcal F$ is the set of financial
intermediary issuers, the balance-sheet layer behind the veil is

$$
V_t=\sum_{i\in\mathcal F}D_t(i,H).
$$

Figure 1 plots

$$
\frac{V_t}{\sum_{i\ne ROW}D_t(i,H)}
\qquad\text{and}\qquad
\frac{V_t}{NI_t},
$$

where $NI_t$ is annual national income in millions of current dollars.
The numerator is a Q4 stock; national income is an annual flow. The ratios are
therefore dimensionless, with the second interpreted as years of national
income.

The key methodological point is that Figure 1 is measured **before** solving
the Leontief system. A household claim on a bank, fund, insurer, or pension
fund is already behind the veil because the household directly owns the
intermediary liability but only indirectly owns the primary assets it
finances. Equation (1) of the paper subsequently identifies the ultimate
incidence of those claims; it does not create the Figure 1 numerator.

## Input boundary

| Input | Unit/key | Use | Classification |
| --- | --- | --- | --- |
| `MSS2021Febreplicationkit/data/fof/LQpanel_2019Q1.dta` | quarter; unique `quarter` | Q4 household instrument stocks, bond issuer/holder inputs, and direct-equity holder totals | Earliest feasible prepared boundary; it retains the relevant Financial Accounts cells but skips mechanical table imports and wide merges |
| `MSS2021Febreplicationkit/data/crsp/msf.dta` | security-month | December market capitalization of listed financial issuers | Raw licensed security input |
| `Data/processed/finalfiles/Yunveilhhd.dta` | year; unique `year` | Validate four reconstructed bond cells; supply three unavailable nonfinancial exclusions used only in the paper-scope share proxy | Preserved supplied final file, never a numerator input |
| `Data/processed/finalfiles/YinequalityNIPAanalysis.dta` | year; unique `year` | National-income denominator and 2016 common endpoint | Preserved supplied aggregate denominator |
| `MSS_SGR_July242025.pdf` | published figure | Digitized comparison curve only | Approximate benchmark, never a reconstruction input |

The kit does not supply the completed annual 34-instrument, 27-sector matrices
used in the revised paper. Starting from `LQpanel_2019Q1.dta` is therefore the
furthest meaningful upstream reconstruction available without inventing
missing bilateral cells. Starting from `Yunveilhhd.dta` for the numerator would
instead import the 2021 Stata allocations that this exercise is intended to
test.

## Python reconstruction

The numerator aggregates nine claim groups:

$$
\begin{aligned}
V_t^A={}&\text{checkable deposits and currency}
+\text{time and saving deposits}+\text{MMF shares}\\
&+\text{GSE securities}+\text{mutual-fund shares}
+\text{life-insurance reserves}\\
&+\text{funded pension entitlements}
+\text{financial-intermediary bonds}
+\text{listed financial equity}.
\end{aligned}
$$

Funded pension entitlements equal reported pension entitlements minus
unfunded claims. For ABS issuers, finance companies, mortgage REITs, and
private depository institutions, the old builder observes some issuer-holder
cells and allocates missing cells proportionally. In the generic residual
step, if $d_{s,t}^{net}$ is issuer $s$'s adjusted liability, $K_s$ is the
set of directly observed holders, and $b_{h,t}$ is holder $h$'s eligible
bond position, then

$$
r_{s,t}=d_{s,t}^{net}-\sum_{h\in K_s}a_{h,s,t},
\qquad
a_{h,s,t}=\frac{b_{h,t}}{\sum_{g\in R_s}b_{g,t}}r_{s,t},
\quad h\in R_s.
$$

`Code/unveiling/figure1_authors.py` implements the issuer-specific eligible
sets and adjustments from
`MSS2021Febreplicationkit/code/build_fa_unveiling_data.do`. It also rebuilds
the household share of corporate equity from the raw Q4 holder cells, then
applies that share to December CRSP capitalization for SIC 6000--6399 and
6700--6799 after the authors' share-code exclusion.

Every annual input is validated once at its boundary. Merges are one-to-one on
`year`, must retain all 54 observations from 1963 through 2016, and fail on
missing or duplicate keys. Stocks are millions of current dollars. ABS,
finance-company, and mortgage-REIT allocations must close to adjusted issuer
liabilities within relative tolerance $10^{-6}$.

## Evidence

- Entry point: `Code/scripts/build_figure1_authors_data.py`.
- Unit and integration tests: `Code/tests/test_figure1_authors.py`.
- Annual reconstruction: `Data/processed/figure1_authors_data.csv`.
- Python-versus-Stata cell audit:
  `Data/processed/figure1_bond_validation.csv`.
- Digitized benchmark and aligned comparison:
  `Data/processed/figure1_paper_digitized.csv` and
  `Data/processed/figure1_authors_comparison.csv`.
- Generated exhibit:
  `Results_Proposal/figures/figure1_authors_data_comparison.png`.

The four reconstructed household bond cells match the supplied Stata
intermediates in every year within the declared \$0.05 million tolerance. The
largest absolute discrepancy is \$0.03615 million for the 2009 ABS cell,
consistent with Stata single-precision rounding.

Against the digitized 2025 curve over 1963--2016, the national-income-normalized
series has correlation 0.9949 and mean absolute error 5.33 percentage points of
national income. It begins at 144.4% rather than 148.5% and ends at 263.9%
rather than 269.0%. The broad ownership-share denominator has MAE 3.23
percentage points; the narrower old-kit proxy has MAE 6.61 points.

## What this identifies

The tight level match shows that the older stock inputs recover most of the
scale and time variation in the revised paper. It does not isolate a pure
"method effect" from a pure "data effect": the exact 2025 completed matrices,
23-intermediary crosswalk, public/private corporation split, corporate-equity
extension, and domestic-asset denominator are absent. The share comparison is
especially sensitive to that missing denominator.

The authors' 2021 seven-round debt procedure also cannot be treated as
$\sum_{r=0}^{7}Q_t^rB_t$. Its instruments, net-issuance adjustments, and
residual allocation rules vary across stages. It shares proportional
allocation logic with the revised method, but numerical equivalence would
require both procedures to start from the same completed direct matrix.

## Presentation correction

`Presentation/3_theoretical_methodology/presentation.pptx` and its condensed
companion now state both boundaries explicitly: Figure 1 stops after building
direct claims, and the 2021 pipeline is stage-specific rather than a fixed-Q
truncation. The historical Beamer source is retained for provenance and is not
the maintained delivery target.

## Remaining exact-vintage work

- obtain the July 2025 completed matrices or plotted annual series;
- reproduce the revised 23-intermediary and 34-instrument crosswalk;
- implement the paper's exact equity extension and denominator; and
- rerun both algorithms on the same direct-dollar matrices before attributing
  any residual difference to methodology.

## Decision log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-08-10 | Treat Figure 1 as a pre-unveiling stock measurement. | This follows the July 2025 text and equations: the solve identifies ultimate incidence, while Figure 1 measures the direct intermediary claims that require unveiling. |
| 2026-08-10 | Start the numerator from `LQpanel_2019Q1.dta`, not `Yunveilhhd.dta`. | The wide panel is the earliest feasible supplied boundary and permits an independent Python reconstruction of the substantive missing-cell allocation. |
| 2026-08-10 | Use preserved final files only for validation and unavailable denominator objects. | This prevents the old seven-round output from entering the numerator while retaining reproducible checks and the authors' supplied national-income series. |
| 2026-08-10 | Label the result an old-input reconstruction of the 2025 definition. | Missing revised matrices and crosswalks rule out an exact 2025-vintage claim even though the level curve matches closely. |
| 2026-08-10 | Retain the newer-public-data result as a separate secondary pipeline. | Its later endpoint and easy reproducibility are valuable robustness evidence, but mixing it with the authors-kit build would obscure changes in vintage, sectors, equity treatment, and denominators. |
