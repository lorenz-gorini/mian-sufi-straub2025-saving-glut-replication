# T-004 / R-003: Figure 8 Replication

## Objective and classification

Apply the July 2025 Figure 8 net-debt definition to the finest debt positions
available in the February 2021 package and compare the result with the target.
The completed 2025 matrices are absent, so the result is classified as a
**close old-unveiling proxy**, not an independent rerun of the 2025 augmented
Leontief methodology.

## Target definition

Paper: July 25, 2025 draft, Sections 4.1--4.2, Figure 8, physical PDF page 29.

$$
ND_{gt}=A^D_{gt}-D_{gt}.
$$

$A^D_{gt}$ is household debt held as an asset by group $g$ after the financial
system is unveiled; $D_{gt}$ is the group's own household debt liability.
Stocks are divided by aggregate national income and expressed relative to
1982. Positive values mean net lending to other households; negative values
mean net borrowing.

## Required-versus-available crosswalk

| 2025 requirement | February 2021 availability | Decision |
| --- | --- | --- |
| Completed annual instrument-by-sector direct matrices | Not supplied | Cannot rerun the revised matrix construction |
| Augmented household wealth-group columns | No upstream matrices | Cannot perform the revised Leontief solve |
| Fine-cohort unveiled household-debt assets | Supplied downstream in `YinequalityFAanalysis.dta` | Reuse with an explicit old-seven-round label |
| Fine-cohort debt liabilities | Supplied in the same file | Subtract as positive liability stocks |
| National income and 1982 base | Supplied in the same file | Apply the 2025 scale and display rule |

The precise stopping boundary is therefore before construction of the revised
augmented matrix. Reprocessing raw 2021 files cannot recover cells that the
package does not contain.

## Data and code lineage

- Input:
  `MSS2021Febreplicationkit/data/finalfiles/YinequalityFAanalysis.dta`.
- Old unveiling builder:
  `MSS2021Febreplicationkit/code/build_fa_unveiling_data.do`.
- Old analysis precursor:
  `MSS2021Febreplicationkit/code/mss_analysis.do`, Figure 7 and Table 7 blocks.
- Python transformation: `Code/unveiling/figure8_authors.py`.
- Reproducible entry point:
  `Code/scripts/build_figure8_authors_data.py`.
- Tests: `Code/tests/test_figure8_authors.py` and
  `Code/tests/test_wealth_groups.py`.
- Detailed field contract: `docs/data/figure8-data.md`.

The unit of observation is year. The 21 fine cohorts partition top 1%, next
9%, next 40%, and bottom 50%; bottom 99% is their lower-three-group sum.

## Verification and result

- Sample: 1963--2016, 54 annual observations.
- Fine-to-coarse validation: maximum absolute error $1 million; maximum
  relative error $3.18\times10^{-7}$ across assets and liabilities.
- All five displayed series equal zero in 1982.
- Digitized-paper comparison:
  - top-1 correlation 0.993; mean absolute error 2.41 percentage points;
  - bottom-99 correlation 0.995; mean absolute error 1.38 points.
- 2007 levels relative to 1982:
  - top 1%: proxy +12.03 points; paper +18.02;
  - bottom 99%: proxy -38.88 points; paper -38.76.
- 2016 levels relative to 1982:
  - top 1%: proxy +13.00 points; paper +17.80;
  - bottom 99%: proxy -33.36 points; paper -34.80.

The old-vintage result strongly reproduces the direction, timing, and
bottom-99 magnitude. Its top-1 asset position is systematically smaller. That
is exactly the dimension most exposed to the revised financial-network and
wealth-group allocation; the gap is therefore informative but cannot be
called a causal code-only effect.

## Outputs

- `Data/processed/figure8_authors_proxy.csv`
- `Data/processed/figure8_aggregation_validation.csv`
- `Data/processed/figure8_paper_digitized.csv`
- `Data/processed/figure8_authors_proxy_comparison.csv`
- `Results_Proposal/figures/figure8_authors_proxy.png`
- `Results_Proposal/figures/figure8_authors_proxy_comparison.png`

## Definition of done

- [x] Target equation, units, sign, groups, and base year documented.
- [x] Exact missing-input boundary identified before implementation.
- [x] Best-feasible fine-cohort proxy implemented and labelled in code/output.
- [x] Fine-to-coarse aggregation and accounting signs tested.
- [x] Paper curve digitized only as an external benchmark.
- [x] Common-sample comparison generated with declared metrics.
- [x] Remaining limitation documented: exact 2025-method replication is
      infeasible without the revised completed matrices or an equivalent
      raw-data completion procedure.
