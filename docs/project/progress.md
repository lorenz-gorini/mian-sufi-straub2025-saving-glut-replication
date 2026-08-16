# Project Progress and Task Dashboard

This is the only authoritative project-status document. It answers what is
active, what comes next, and what is complete. Detailed task records preserve
methodological decisions and evidence; stable data contracts live in
`docs/data/`.

## Active tasks

| ID | Task | Status | Priority | Category | Estimate | Objective | Progress and next action | Task record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-005 | Refresh the final pedagogical presentation | In progress | 1 | presentation |  | Replace the outdated Figure 8 proxy sequence while retaining the concise theory, data-lineage, and result-comparison narrative. | The source now defines an 18-slide deck with the focused three-route Figure 8 comparison and a project-built opening network visual; `node --check` passes. The verified 17-slide PowerPoint remains unchanged because the Artifact Tool runtime loader was unavailable. The superseded combined Beamer deck is now isolated under `Presentation/0_legacy_combined_deck/`. Next rebuild, render, and inspect all 18 slides when that dependency is restored. | [Presentation task](tasks/pedagogical-presentation.md); [submission deck](../../Presentation/5_replication_submission/README.md) |
| T-009 | Review and integrate the Figure 5, Figure 6, and Figure 8 comparisons | In progress | 1 | paper-review |  | Understand what the three figures measure, trace how our outputs were generated, evaluate the paper-versus-ours comparisons, and approve their presentation use. | Figure 8's primary 2021-direct/full-inverse route is now integrated into the compact report and pending presentation source. The old seven-round output remains lineage and current public FWTW remains robustness; next review the complete submission after the PowerPoint rebuild. | [Review task](tasks/figure5-figure8-review.md); [personal considerations](personal-considerations-saving-inequality.md); [Figure 5 replication](tasks/figure5-replication.md); [Figure 6 replication](tasks/figure6-replication.md); [Figure 8 replication](tasks/figure8-replication.md) |
| T-008 | Design a feasible extension proposal | In progress | 3 | research-design |  | Determine whether financial intermediation transformed rich saving into cheaper mortgage credit and extend nominal ownership unveiling to ultimate risk-bearing. | The verified debt decomposition now serves as motivating evidence that selects pre-2008 mortgages. The long design and two-page brief specify a pooling/agency model, a state-contingent loss operator, public-data sequence, identification threats, and an honest novelty boundary. Next close the exact Figure 6 group-income contribution and choose between conforming-loan eligibility and predetermined lender exposure for the first causal test. | [Extension proposal](tasks/extension-proposal.md); [submission brief](../../Extension_Proposal/extension_proposal.tex); [canonical financialization/risk design](../../Extension_Proposal/research_extension_idea_2.md); [extension data](../data/debt-composition-extension-data.md) |

## Immediate sequence: 2026-08-15

1. Use the verified seven-page combined submission report as the fixed written
   component. Rebuild and visually verify the prepared 18-slide presentation
   source when the required Artifact Tool runtime loader is available.
2. Treat the five-slide debt-composition evidence as mechanism-selection
   evidence: pre-2008 mortgages dominate, but ownership is not risk incidence
   and the current result is not an identified mortgage-credit effect.
3. Add the exact Figure 6 percentile/group-income saving-rate decomposition;
   revise the included financialization/risk-bearing proposal only if that new
   evidence changes its quantitative motivation.
4. Review the integrated Figure 8 result. Treat the 2021-direct/full-inverse
   route as the primary same-vintage test, the old seven-round result as its
   lineage benchmark, and the public-FWTW rerun as a robustness exercise.

## Completed tasks

| ID | Task | Status | Priority | Category | Estimate | Objective | Outcome | Task record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-006 | Produce the compact final replication report | Complete | 2 | writing |  | Preserve the detailed technical report while producing a short replication component that can be combined with the referee report and extension proposal. | The verified three-page brief contains one page of method, data, results, and limitations plus generated comparisons for Figures 1, 5, and 8. Figure 8 now leads with the same-vintage direct/full-inverse reconstruction, while lineage and public-data robustness remain explicit. The detailed report is preserved unchanged. | [Report task](tasks/final-report.md); [short report](../../Report/README.md) |
| T-001 | Crosswalk the selected 2025 results to usable 2021 inputs | Complete | 1 | paper-review | 60m | Determine, figure by figure, whether the supplied 2021 data can identify the July 2025 definition and isolate code, data-vintage, and unavailable-input gaps. | The source/code crosswalk is complete for Figures 1, 5, and 8. Figures 1 and 5 reconstruct through 2016. Figure 8 distinguishes the old downstream proxy, the earliest feasible 2021 direct-cell reconstruction, and the current public completed FWTW robustness route; the exact 2025 annual matrix cube remains unavailable. | [Result selection](tasks/result-selection.md); [quickstart](../reference/author-kit-quickstart.md) |
| T-002 | Inventory and document required data | Complete | 2 | data-lineage |  | Locate selected-exhibit inputs and document only the schemas, units, keys, vintage, and provenance actually used. | Figure-specific data contracts identify the used files, columns, units, keys, coverage, source roles, and unavailable upstream objects, including separate contracts for the Figure 8 proxy, 2021-direct reconstruction, and public-FWTW robustness route. | [Figure 1 data](../data/figure1-data.md); [Figure 5 data](../data/figure5-data.md); [Figure 8 proxy data](../data/figure8-data.md); [Figure 8 2021-direct data](../data/figure8-2021-direct-data.md); [Figure 8 public-FWTW data](../data/figure8-public-fwtw-data.md) |
| T-003 | Reconstruct cleaning and merges | Complete | 2 | data-engineering |  | Reimplement the minimum required preparation with explicit transformations and merge contracts. | Python rebuilds Figure 1 intermediary claims, Figure 5 fine wealth allocation and valuation closure, the retained Figure 8 fine-group aggregation, the 2021 direct-cell coarsened network, and the public-FWTW direct network with explicit accounting checks. Authors' files remain read-only. | [Figure 1 replication](tasks/figure1-replication.md); [Figure 5 replication](tasks/figure5-replication.md); [Figure 8 replication](tasks/figure8-replication.md) |
| T-004 | Reproduce selected computations and exhibits | Complete | 1 | replication | 120m | Generate Figures 1, 5, and 8 as closely as the supplied inputs permit and compare each with declared benchmark evidence. | Figure 1 and Figure 5 are reconstructed from authors-kit inputs through 2016. Figure 8 now has three separate results: old final-file/seven-round, 2021-direct/full-inverse, and public-FWTW/full-inverse; all are compared with the same digitized 2025 target. | [Figure 1 replication](tasks/figure1-replication.md); [Figure 5 replication](tasks/figure5-replication.md); [Figure 8 replication](tasks/figure8-replication.md); [major results](../../Results_Proposal/major_results.md) |
| T-007 | Validate the complete February 2021 replication package | Complete |  | replication-validation |  | Establish that the supplied Stata package can reproduce the paper version it accompanies and preserve a version-aware audit trail. | On 2026-08-09 the user-authorized StataNow 19.5 master run completed; all major outputs are mapped to the exact February 2021 revision, seven figures pass visual comparison, and Table 7 matches to three decimals. The verified ten-slide deck in `Presentation/1_replication_package_validation/` shows why this is a successful 2021 benchmark but not an exact 2025 replication. | [Benchmark and hydration](tasks/author-data-benchmark.md); [output crosswalk](../reference/author-output-crosswalk.md) |
| T-010 | Reconstruct Figure 6 with the 2025 method | Complete | 1 | replication |  | Apply the paper's percentile bins, active-saving numerator, and personal-plus-corporate disposable-income denominator to the 2021 authors-kit data, then construct directly comparable wealth-level and time-evolution views. | The raw DINA bins reaggregate to prepared author shares within $7.24\times10^{-8}$; annual wealth, saving, income, and equation (9c) close; audited paper correlations are 0.991 and 0.969. Percentile, wealth-level, comparison, digitization-audit, and five-year evolution figures cover the available 1963--2016 inputs. | [Figure 6 replication](tasks/figure6-replication.md); [Figure 6 data](../data/figure6-data.md); [personal considerations](personal-considerations-saving-inequality.md) |
| T-011 | Write the referee report | Complete | 1 | paper-review |  | Produce a constructive 1--1.5-page referee report, plus figures, that assesses the paper's contribution and turns the Figure 6 diagnostics into focused revision requests. | The report recommends revise and resubmit, foregrounds the paper's novelty, requests fixed real-wealth bins and time-resolved saving rates, corrects the heatmap scaling proposal for signed data, bounds the unveiling and valuation assumptions, and requests a version-matched 2025 package. The DOCX/PDF remain reproducibly built from Markdown, and a parallel LaTeX body now compiles through its standalone entry point and the combined submission. | [Referee-report task](tasks/referee-report.md); [LaTeX entry point](../../Referee_Report/main.tex); [Markdown source](../../Referee_Report/referee_report.md) |
| T-012 | Assemble the written submission | Complete | 1 | writing |  | Combine the referee report, replication summary, and extension proposal without duplicating document environments or preambles. | Each component has a standalone entry point and body-only source; the combined seven-page artifact passes visual inspection. Its source, rendered text, and metadata contain no AI- or agent-usage disclosure, while the root README now gives the reproducible Figure 1/5/6/8 and submission build sequence for the submitted code package. | [Submission-report task](tasks/submission-report.md); [combined entry point](../../Submission_Report/main.tex); [combined PDF](../../Submission_Report/submission_report.pdf) |

## Planned tasks

No task is merely planned: T-008 has begun as a research-design exercise, and
the core empirical implementation tasks are complete.

## Completed milestones

| ID | Milestone | Status | Outcome and evidence |
| --- | --- | --- | --- |
| M-001 | Project and agent-documentation foundation | Complete | Added the canonical agent brief, documentation index, task dashboard, data-documentation contract, author-kit map, result-selection record, and presentation conventions. |
| M-002 | Initial source and replication-kit audit | Complete | Confirmed the 66-page July 25, 2025 target paper and identified the attached second PDF as an image-only NotebookLM synthesis. Established that the February 2021 kit represents the paper's earlier draft, then mapped its master/build/analysis scripts, core final files, exhibit outputs, and unavailable inputs. See [the author-kit map](../reference/author-kit-map.md). |

## Status definitions

- **Proposed:** worth preserving but not accepted into the work plan.
- **Planned:** accepted and scoped, but implementation has not started.
- **In progress:** active work has evidence and a concrete next action.
- **Blocked:** cannot advance until a named dependency or decision is resolved.
- **Complete:** the definition of done is satisfied and evidence is linked.
- **Superseded:** replaced by another task or approach and retained for history.

## Maintenance rules

1. Read this dashboard before substantial work.
2. Update the owning row and task record in the same change as material
   progress.
3. Keep table cells concise; experiment history and rationale belong in task
   records.
4. Do not create a second TODO or completed-task list.
5. Mark a task complete only after checking its definition of done and linking
   inputs, code, outputs, and verification evidence.
