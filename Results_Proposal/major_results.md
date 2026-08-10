# Major Results: Candidate and Selection Record

This is the result-level working document. The task dashboard tracks status;
this file records which economic claims and exhibits are candidates, selected,
or rejected.

## Source warning

`MSS_SGR_July242025.pdf` is the authoritative target paper. Its existing parsed
copy at
`/Users/lorenzogorini/Library/CloudStorage/OneDrive-UniversitàCommercialeLuigiBocconi/PhD/research-wiki/papers/inequality/mian-2025-saving-glut-rich/full.md`
should be used for text search and section reading; the PDF is needed only for
authoritative pagination, equations, figures, footnotes, and layout.
`Unveiling_the_Rich_Saving_Glut.pdf` is only a NotebookLM synthesis. The target
paper is a heavily revised version of the earlier draft represented by the
February 2021 kit: its horizon extends to 2019, its unveiling framework is
recast as a matrix/Leontief problem, and its exhibit numbering and empirical
scope changed. The old kit is useful only through an explicit version
crosswalk.

## Approved scope and deferred candidates

| ID | Status | Economic claim | 2025 exhibit | Old-kit precursor |
| --- | --- | --- | --- | --- |
| R-001 | Selected - core | Indirect household ownership rose materially, so aggregate direct holdings conceal the final use of saving. | Figure 1 | No exact equivalent; old Figure 6 is related. |
| R-002 | Selected - core | Top-1-percent saving diverged sharply from bottom-99-percent saving after 1982. | Figure 5 | Old Figures 1, 3, and 4. |
| R-003 | Selected - core | After unveiling intermediated ownership, the top group accumulates household-debt claims while the bottom 99 percent becomes a net debtor. | Figure 8 | Old Figure 7 and Table 7. |
| R-004 | Selected - extension if time permits | The bottom 99 percent increasingly finances expenditure with debt, much of it funded by the top 1 percent. | Figure 9 | Old Table 7 contains related flow components. |
| R-005 | Deferred | Top-1-percent demand for household and government debt is comparable to rest-of-world safe-asset accumulation. | Figure 10 | Old Figure 9. |
| R-006 | Deferred | Rising top-1-percent saving primarily financed consumption rather than additional net investment. | Figure 11 | Old Figures 2 and 4 are related but not equivalent. |
| R-007 | Out of initial scope | Similar patterns appear in international corporate/personal saving and Norwegian distributional saving. | Figures 12-13 | No direct old-kit counterpart. |

See [`docs/project/tasks/result-selection.md`](../docs/project/tasks/result-selection.md)
for selection criteria and feasibility notes.

## Selection decisions

| Date | Result ID | Decision | Rationale | Approved by |
| --- | --- | --- | --- | --- |
| 2026-07-24 | R-001 | Select as core. | Covers the central unveiling methodology and motivates all later allocation results. | User |
| 2026-07-24 | R-002 | Select as core. | Captures the paper's main saving-glut fact and its measurement. | User |
| 2026-07-24 | R-003 | Select as core. | Captures the main "who finances whom" application of unveiling. | User |
| 2026-07-24 | R-004 | Select only if time permits. | Reuses Figure 8 concepts and data while translating stocks into flows. | User |
| 2026-07-24 | R-005 to R-007 | Defer. | Methodological understanding and completion of the three core figures take priority over breadth. | User |

## Learning and explanation requirement

For each selected result, its replication record must explain:

- the economic question in plain language;
- every relevant equation and symbol;
- units, stock/flow status, signs, normalization, and smoothing;
- the data-to-equation-to-code mapping;
- the accounting or matrix invariant used for verification;
- what the figure establishes and what it does not establish.

These explanations are the source material for the visual teaching presentation.

## R-001: Indirect household ownership and the unveiling operator

**Paper reference**

- Exact paper version: July 25, 2025 draft, `MSS_SGR_July242025.pdf`.
- Method: Sections 2.1--2.2, printed pages 5--9 (PDF pages 6--10),
  Equations (1)--(4).
- Result: Section 2.3 and Figure 1, printed pages 9--10 (PDF pages 10--11).
- Claim: the share of U.S. household financial assets held indirectly rises
  from about 45% in 1960 to about 70% in 2007, then falls toward 60%; the
  indirectly held amount rises from about 150% to over 250% of national income.

**Authors' implementation and version boundary**

- No exact 2025 analysis code or completed annual matrix is present in the
  February 2021 kit.
- The old methodological precursor is
  `MSS2021Febreplicationkit/code/build_fa_unveiling_data.do`: household debt at
  lines 9--2405, government debt at 2444--4713, mortgage debt at 4754--7158,
  and the merged `Yunveil.dta` at 7163--7171.
- The old Figure 6 block at `code/mss_analysis.do:587--678` reads
  `YinequalityFAanalysis.dta` and exports `output/fig_owndet.eps`. It is related
  direct-ownership composition, not an exact precursor of 2025 Figure 1.
- The detailed package navigation record is
  `docs/reference/author-kit-map.md`; the equation/code comparison is
  `docs/methods/leontief-unveiling.md`.

**Empirical definition**

- Let $D_t(i,H)$ be liabilities issued by sector $i$ and held directly by the
  household sector, summed across Financial Accounts instruments. If
  $\mathcal F$ is the financial-intermediary issuer set, the stock behind the
  veil is $V_t=\sum_{i\in\mathcal F}D_t(i,H)$.
- Figure 1 plots $V_t/\sum_{i\ne ROW}D_t(i,H)$ and $V_t/NI_t$, where $NI_t$
  is annual national income. The numerator is a Q4 stock in current dollars;
  national income is a current-dollar annual flow.
- A household claim on an intermediary is direct with respect to that
  intermediary but indirect with respect to the primary assets it finances.
  Therefore Figure 1's numerator is not $\Omega_t-\bar M_t$. The Leontief
  operator identifies where $V_t$ ultimately goes; it is not required merely
  to measure how much is behind the veil.
- The target network has 4 ultimate owners, 23 intermediaries, and 34
  instruments. Our public-data reconstruction has 21 intermediary issuer
  sectors after excluding the four owners because it uses a later FWTW
  vintage and aggregation.

**Our implementation**

- Code: `Code/unveiling/network.py`.
- Authors-data reconstruction: `Code/unveiling/figure1_authors.py`.
- Authors-data entry point: `Code/scripts/build_figure1_authors_data.py`.
- New-public-data robustness code: `Code/unveiling/figure1.py` and
  `Code/scripts/build_figure1.py`.
- Tests: `Code/tests/test_network.py`.
- Figure 1 tests: `Code/tests/test_figure1_authors.py` and
  `Code/tests/test_figure1.py`.
- Worked example: `Code/examples/leontief_unveiling.py`.
- Teaching-output generator:
  `Code/scripts/build_unveiling_teaching_assets.py`.
- Explanation: `docs/methods/leontief-unveiling.md`.
- Method presentation:
  `Presentation/3_theoretical_methodology/presentation.pptx` and
  `Presentation/3_theoretical_methodology/presentation_short.pptx`.
- Report discussion: `Report/report.tex`, Sections 2--3.
- Authors-data outputs: `Data/processed/figure1_authors_data.csv`,
  `Data/processed/figure1_bond_validation.csv`,
  `Data/processed/figure1_paper_digitized.csv`, and
  `Data/processed/figure1_authors_comparison.csv`.
- Authors-data comparison figure:
  `Results_Proposal/figures/figure1_authors_data_comparison.png`.
- New-data robustness series and figure:
  `Data/processed/figure1_indirect_household_ownership.csv` and
  `Results_Proposal/figures/figure1_indirect_household_ownership.png`.
- Data contract and provenance: `docs/data/figure1-data.md` and
  `Data/raw/README.md`.
- Environment: Python 3.13.2, NumPy 2.1.3, pytest 8.4.2; recorded in
  `Code/README.md`.

**Verification**

- The block solve equals the paper's full $M_t(I-M_t)^{-1}$ expression.
- The closed form equals an 80-round Neumann sum in the deterministic example.
- Rows of unveiled and final primary-asset ownership sum to one.
- Equation (2) satisfies aggregate net worth equal to zero.
- A closed intermediary cycle fails with a clear convergence error.
- The authors-data tests verify the named-component aggregation, funded-pension
  adjustment, raw-panel bond reconstruction, household equity-share
  construction, CRSP December/SIC construction, merge contract, and failure on
  duplicate annual keys.

The raw-panel Python reconstruction of household bond claims on ABS issuers,
finance companies, mortgage REITs, and private depository institutions matches
the supplied Stata intermediates in every year within the declared \$0.05
million tolerance. The maximum absolute cell error is \$0.03615 million.

The worked example provides an edge-level verification. Its fixed
point satisfies $\Omega=B+Q\Omega$, and the bank's 72.093% ultimate household
share is reconciled as 20% direct plus 52.093% through the fund. The report
separates this proved common-matrix equivalence from the untested empirical
comparison with the actual 2021 Stata pipeline.

The old-vintage authors-data reconstruction has 54 annual Q4 observations from
1963 through 2016. Relative to the digitized paper curve, its
national-income-normalized
level has correlation 0.995 and mean absolute error 5.3 percentage points of
national income. It begins at 144.4% rather than 148.5% and ends at 263.9%
rather than 269.0%. The broad-denominator ownership share has mean absolute
error 3.2 percentage points; the more conceptually targeted paper-scope proxy
has 6.6 points of error. This is strong evidence that the supplied stock inputs
recover the scale and time pattern, but it does not establish exact equality of
the revised paper's denominator or classification.

The independent June 2026-vintage robustness reconstruction has 57 annual Q4
observations from 1963 through 2019. Its indirect share is 47.5% in 1963, 66.3%
in 2007, peaks at 70.1% in 2009, and is 66.2% in 2019. The corresponding stock
is 157.2% of national income initially, 277.6% in 2007, and 325.6% in 2019.

**Remaining exact-vintage verification**

- Obtain the authors' July 2025 FWTW vintage or plotted series.
- Match the target's 23 intermediary definitions, corporate-equity extension,
  and separate public/private corporations.
- Recompute both ratios from the completed 34-instrument, 27-sector matrices
  and compare the full annual series under a declared numerical tolerance.

**Interpretation and limitation**

The method removes the intermediation veil by allocating every intermediary to
its ultimate owners under the proportionality assumption. Figure 1 itself is
the direct intermediary-claim stock measured before that solve. Our
equation-level implementation matches the target algebra; the authors-data
reconstruction closely matches Figure 1's normalized stock; and the newer
public data provide a separate robustness check. The remaining share discrepancy is not evidence
that the paper is wrong because the February 2021 package lacks the revised
matrix, denominator crosswalk, and complete equity extension needed for that
claim.

## Replication record template

Copy this section once for each selected result.

### R-XXX: Short claim

**Paper reference**

- Exact paper version:
- Section/page:
- Figure/table:
- Caption and claim:

**Authors' implementation**

- Analysis-code lines:
- Output file:
- Final analysis inputs:
- Upstream build scripts and source files:

**Empirical definition**

- Unit of observation:
- Sample and period:
- Population/wealth groups:
- Variables and formulas:
- Units and normalization:
- Weights:
- Statistical model or accounting identity:

**Our implementation**

- Input dataset:
- Producing code:
- Generated table/figure:
- Environment/configuration:

**Verification**

- Benchmark statistic or series:
- Comparison metric:
- Predeclared tolerance:
- Result:
- Explained discrepancy:
- Unresolved discrepancy:

**Interpretation**

- Economic conclusion:
- Assumptions required:
- Limitations:
