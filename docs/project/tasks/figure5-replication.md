# T-004 / R-002: Figure 5 Replication

## Objective and classification

Reconstruct the July 2025 Figure 5 procedure from the February 2021 authors'
data over the common sample. This is an **old-input reconstruction of the 2025
definition**, not a replot of `Ysavingwealth.dta` and not an extension to
2017--2019.

The economic question is whether the post-1982 saving divergence between the
top 1% and bottom 99% survives when the revised paper's group and display rules
are applied to the older supplied data.

## Target definition

Paper: July 25, 2025 draft, Section 3.4, Figure 5, physical PDF page 22. For
group $g$ and asset/liability $j$,

$$
\Theta_{gjt}=W_{gjt}-(1+\pi_{gjt})W_{gj,t-1}, \qquad
\Theta_{gt}=\sum_j\Theta_{gjt}.
$$

The chart plots the trailing ten-year mean of $\Theta_{gt}/NI_t$, relative to
its 1982 value. Groups are top 1%, next 9%, 51--90%, bottom 50%, and bottom
99%. Values are percentage points of aggregate national income; saving is a
flow inferred from stock changes net of valuation effects.

## Data and code lineage

- Aggregate wealth and national income:
  `MSS2021Febreplicationkit/data/finalfiles/YwealthFOF.dta`.
- Fine DINA shares:
  `MSS2021Febreplicationkit/data/PSZusdina/Yszshares_fine.dta`.
- Housing and debt valuation inputs:
  `MSS2021Febreplicationkit/data/finalfiles/Ywealthreturns.dta`.
- NIPA closure:
  `MSS2021Febreplicationkit/data/finalfiles/YinequalityNIPAanalysis.dta`.
- Older coarse validation series only:
  `MSS2021Febreplicationkit/data/finalfiles/Ysavingwealth.dta`.
- Old construction lineage:
  `MSS2021Febreplicationkit/code/build_wealth_saving_data.do`, especially the
  `DISTRIBUTE WEALTH FROM B101` and `WEALTH BASED APPROACH TO SAVING` blocks.
- Python transformation: `Code/unveiling/figure5_authors.py`.
- Reproducible entry point:
  `Code/scripts/build_figure5_authors_data.py`.
- Tests: `Code/tests/test_figure5_authors.py` and
  `Code/tests/test_wealth_groups.py`.
- Detailed field contract: `docs/data/figure5-data.md`.

The Python implementation reads the aggregate B.101-based wealth totals rather
than treating the final saving file as an empirical input. It allocates all 29
balance-sheet categories using the supplied fine shares, applies the asset
valuation rules, solves the residual equity return required by national
accounts, then performs the revised display transformation.

## Accounting interpretation

The residual equity return is identified by the national-accounts invariant

$$
\sum_g\Theta_{gt}=S_t^p+S_t^\pi,
$$

where $S_t^p$ is personal saving and $S_t^\pi$ is business saving accruing to
households. This prevents stock revaluations from being silently treated as
active saving. Liabilities retain their negative balance-sheet sign, so debt
accumulation lowers group saving.

## Verification and result

- Sample: annual saving 1963--2016; displayed trailing averages 1972--2016.
- NIPA closure: maximum residual below $10^{-10}$ of national income.
- Fine group partition: every supplied cohort appears exactly once.
- Old coarse Stata diagnostic: maximum annual difference 0.289 percentage
  points of national income; tolerance 0.3 points.
- Digitized-paper comparison, 1972--2016:
  - top-1 correlation 0.992; mean absolute error 0.40 percentage points;
  - bottom-99 correlation 0.997; mean absolute error 0.42 points.
- In 2016, our top-1 series is +3.25 points relative to 1982 versus +4.35 in
  the digitized paper; our bottom-99 series is -7.11 versus -8.46.

The match in timing, sign, and magnitude is strong. The remaining gap is
consistent with the older DINA/Financial Accounts vintage and the absence of
2017--2019, but it cannot be decomposed into a pure vintage effect without the
authors' revised inputs.

## Outputs

- `Data/processed/figure5_authors_annual.csv`
- `Data/processed/figure5_authors_data.csv`
- `Data/processed/figure5_saving_validation.csv`
- `Data/processed/figure5_paper_digitized.csv`
- `Data/processed/figure5_authors_comparison.csv`
- `Results_Proposal/figures/figure5_authors_data_reconstruction.png`
- `Results_Proposal/figures/figure5_authors_data_comparison.png`

## Definition of done

- [x] Target equation, groups, units, moving window, and base year documented.
- [x] Required-versus-available inputs mapped to supplied files.
- [x] Saving rebuilt upstream of `Ysavingwealth.dta` in Python.
- [x] Merge, partition, allocation, and NIPA invariants tested.
- [x] Paper curve digitized only as an external benchmark.
- [x] Common-sample comparison generated with declared metrics.
- [x] Data record, task record, and presentation-facing figures generated.
- [x] Remaining limitation documented: exact equality to the 2019 target is
      impossible without the revised DINA/Financial Accounts inputs and code.
