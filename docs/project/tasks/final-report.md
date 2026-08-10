# T-006: Final Replication Report

## Objective

Produce an approximately two-page course-facing replication report. The first
page should explain the paper's main methodological novelty and the data objects
it requires. The second should summarize the February 2021 benchmark, what can
and cannot be reconstructed for July 2025 from the supplied inputs, why our
code differs from the old plotting code, and one clearly labelled extension
proposal.

The existing ten-page `Report/report.tex` is a verified technical evidence
base. Preserve it while the empirical audit is active; compress or refactor it
only after the Figure 5 and 8 feasibility boundaries are established.

## Evidence standard

For every method or exhibit, the report must separately state:

1. algebraic consistency with the target paper;
2. conceptual or code-lineage consistency with the February 2021 package;
3. whether both implementations have been run on a common input;
4. the benchmark, comparison metric, tolerance, and numerical result; and
5. which assumptions or data choices explain any remaining discrepancy.

Do not infer that the paper is wrong from a mismatch with the older package.
Such a claim would require a reproducible violation of the target paper's own
equations or accounting identities on its intended inputs.

## Compact report contract

The final main text should contain four tightly linked components:

1. **Novelty:** why direct balance sheets obscure ultimate financing and how
   \(\Omega_t=(I-Q_t)^{-1}B_t\) unveils intermediary chains under proportional
   allocation.
2. **Evidence hierarchy:** successful full reproduction of the February 2021
   package; old-input reconstructions of July 2025 definitions where possible;
   and explicit gaps where the revised data or construction are unavailable.
3. **Core figures:** a concise Figure 1/5/8 result table or panel with period,
   definition, comparison metric, and status. Any claim that our result is
   closer to 2025 must name the transformation responsible and show the
   numerical comparison.
4. **Extension:** one paragraph describing the selected research proposal,
   its required data, and its binding limitation. AI circular financing is a
   candidate, not yet the selected or implemented extension.

Detailed equations, schemas, diagnostics, and code-line crosswalks may remain
in a technical companion or appendix if course rules allow, but they should
not crowd the two-page main argument.

## Current evidence

The initial `Report/report.tex` section was drafted on 2026-08-03, extended
with the public Figure 1 robustness result on 2026-08-05, and revised with the
authors-data comparison on 2026-08-09. It contains:

- the direct matrix, block form, convergence condition, and linear solve;
- the issuer-row denominator, the absence of a column-sum restriction, and the
  distinction between direct intermediary assets and terminal ownership;
- the complete bank--fund worked example and path reconciliation;
- a proof that stationary rounds converge to the Leontief solution;
- an exact truncation-error formula and generated seven-round toy diagnostic;
- a code-level comparison with the 2021 Stata procedure; and
- a common-input protocol required before claiming empirical equality;
- the correct Figure 1 stock and share definitions, including why the plotted
  numerator is not `Omega - M_bar`;
- the authors-data inputs, skipped mechanical preparation, retained nine-group
  aggregation, equity extension, units, and merge contract;
- a generated 1963--2016 comparison against the digitized paper curve;
- a quantitative result: correlation 0.995 and 5.3-percentage-point national-
  income MAE for the level, versus a denominator-sensitive ownership share;
- the separate 1963--2019 public-data robustness result; and
- a data-architecture section distinguishing the 34 FWTW instrument matrices,
  DINA cohort shares, NIPA closure, valuation terms, and consumption
  robustness;
- equations for instrument margins, the DINA-to-B.101 allocation, the
  augmented household column, Figure 5 saving, and Figure 8 net debt; and
- a bounded conclusion that distinguishes close level reproduction, share
  uncertainty, and new-data robustness.

Numerical example values are imported from
`Presentation/generated/unveiling_values.tex`; empirical values are imported
from `Presentation/generated/figure1_values.tex` and
`Presentation/generated/figure1_authors_values.tex`. They are produced by
`Code/scripts/build_unveiling_teaching_assets.py` and
the two Figure 1 build scripts. The current ten-page PDF compiles without
layout warnings. The new and reflowed pages were inspected at full size on
2026-08-09; the unchanged pages retain the earlier inspection.

## Definition of done

- [x] A single `Report/report.tex` entry point compiles independently.
- [x] The initial method section states a bounded comparison with the old kit.
- [ ] Figures 1, 5, and 8 each have a verified result section.
- [ ] Every empirical table and figure is generated by code.
- [ ] Every result states its benchmark, tolerance, and discrepancy.
- [ ] Sources, periods, units, assumptions, and version boundaries are explicit.
- [ ] The complete rendered report has been visually inspected.
- [ ] The course-facing main text is approximately two pages and preserves the
      evidence hierarchy of the technical draft.
- [ ] The report explains any claimed improvement over the 2021 code with a
      reproducible transformation and quantitative comparison.
- [ ] The extension is labelled as proposed, partially illustrated, or
      implemented and states its required data.

## Decision log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-08-03 | Separate algebraic equivalence, conceptual consistency, and empirical equality throughout the report. | Conflating them would either overstate the replication or invite an unsupported claim that the revised paper is wrong. |
| 2026-08-03 | Treat Python and Stata as implementations of different paper versions until a common-input experiment is available. | The 2021 rounds include instrument-specific rules and residuals that are not seven powers of the 2025 stationary matrix. |
| 2026-08-03 | State the denominator attached to every arrow interpretation. | Outgoing entries in one issuer row share a liability denominator and sum to one; incoming entries come from different issuer rows and cannot be read as shares of the holder's asset portfolio. |
| 2026-08-05 | Label Figure 1 as a public-data reconstruction rather than an exact replication. | The later FWTW vintage recovers the economic trend but differs from the target in revisions, sector aggregation, and corporate-equity treatment. |
| 2026-08-09 | Call the authors-data level a close reproduction but keep the share explicitly provisional. | The level tracks the digitized paper tightly, while the completed 2025 matrix and exact denominator crosswalk are absent. |
| 2026-08-09 | Document skipped preparation and retained aggregation separately. | Beginning from an authors-prepared panel is acceptable only if the report makes clear that the central instrument grouping and equity construction are recomputed. |
| 2026-08-09 | Treat Financial Accounts, DINA, NIPA, valuation inputs, and consumption surveys as separate identification layers. | The paper does not use DINA to infer missing bilateral FWTW cells, and its Figure 5 baseline is wealth-based rather than income minus consumption. |
| 2026-08-10 | Treat the ten-page report as a technical evidence base and target an approximately two-page final main text. | The user wants a compact course report centered on the methodology novelty and the replication verdict, while the existing detail remains useful for auditing claims. |
| 2026-08-10 | Delay compression until the Figure 5 and 8 feasibility audit is complete. | Writing a polished conclusion before identifying the available 2021 inputs would risk overstating or misclassifying the July 2025 replication evidence. |

## Session record: 2026-08-10 final-deliverable refresh

- Starting version: the workspace is not recognized as a Git worktree, so no
  branch or commit identifier is available.
- Goal: align the report task with the requested short final deliverable and
  yesterday's completed historical benchmark.
- Result: the report now has a two-page synthesis contract, retains the
  ten-page technical draft as its evidence base, and requires a reproducible
  explanation for any claim that our code is closer to the 2025 result.
- Next action: finish the Figure 5 and 8 feasibility audit, then populate the
  compact comparison table before editing the prose to length.

## Session record: 2026-08-09 data architecture

- Starting version: the workspace was not recognized as a Git worktree, so no
  branch or commit identifier was available.
- Goal: add a defensible source-to-object-to-equation account for the main
  datasets and selected figures.
- Changed files: Report/report.tex, Report/report.pdf,
  docs/reference/author-kit-map.md, docs/project/progress.md, and this task
  record.
- Reasoning: aggregate network construction, distribution across cohorts, and
  saving/valuation closure are different empirical steps and must not be
  described as one residual operation.
- Validation: the ten-page report was built in an isolated temporary directory;
  the final log contains no warnings, and the new/reflowed pages 2--5 were
  rendered and visually inspected.
- Result: the report now states exactly when subtraction identifies one missing
  FWTW cell, why multiple unknowns need the Batty balancing procedure, why DINA
  enters later, and why CEX/PSID are robustness inputs.
- Next action: inventory and implement the Figure 5 baseline from the earliest
  feasible supplied files, then add a generated benchmark comparison.
