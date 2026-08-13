# Project Progress and Task Dashboard

This is the only authoritative project-status document. It answers what is
active, what comes next, and what is complete. Detailed task records preserve
methodological decisions and evidence; stable data contracts live in
`docs/data/`.

## Active tasks

| ID | Task | Status | Priority | Category | Estimate | Objective | Progress and next action | Task record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-009 | Review and integrate the Figure 5, Figure 6, and Figure 8 comparisons | In progress | 1 | paper-review |  | Understand what the three figures measure, trace how our outputs were generated, evaluate the paper-versus-ours comparisons, and approve their presentation use. | The Figure 8 boundary is corrected: the plotted seven-round result remains a proxy, while current public completed FWTW plus 2021 DINA/NIPA make a labelled full-Leontief mixed-vintage reconstruction feasible. Next implement and validate that separate rerun before replacing the proxy as the main Figure 8 comparison. | [Review task](tasks/figure5-figure8-review.md); [personal considerations](personal-considerations-saving-inequality.md); [Figure 5 replication](tasks/figure5-replication.md); [Figure 6 replication](tasks/figure6-replication.md); [Figure 8 replication](tasks/figure8-replication.md) |
| T-005 | Build the final pedagogical presentation | In progress | 2 | presentation |  | Distill the methodology novelty, version audit, reconstructed results, and limitations into one visually coherent course presentation while retaining the topic decks as source modules. | The verified 18-slide empirical-comparison module covers Figures 1, 5, 6, and 8 and now separates the exact Figure 8 vintage gap from the feasible public-FWTW method rerun. Next carry only the approved panels into the short final synthesis rather than concatenating source decks. | [Presentation task](tasks/pedagogical-presentation.md); [comparison deck](../../Presentation/4_figure_comparison/README.md) |
| T-006 | Produce the compact final replication report | In progress | 2 | writing |  | Convert the technical evidence into an approximately two-page course-facing report: methodology novelty first, replication evidence and limitations second, with a concise extension proposal. | The report boundary now distinguishes the completed Figure 8 proxy from the feasible public-FWTW full-method reconstruction. Next add that distinction beside the Figure 5 evidence and avoid calling either mixed-vintage output an exact authors-vintage reproduction. | [Report task](tasks/final-report.md) |

## Immediate sequence: 2026-08-12

1. Build the public-FWTW Figure 8 reconstruction: 31 instruments and 25
   substantive sectors, mapped to 2021 DINA/NIPA through 2016, then augmented
   and unveiled with the full Leontief operator.
2. Validate issuer/holder margins, row normalization, ownership conservation,
   and the Figure 8 group/sign/scale/base transformation.
3. Compare that mixed-vintage method reconstruction with both the target-paper
   Figure 8 and the existing seven-round proxy; keep all three labels explicit.
4. Carry only the approved comparison panels into the final short presentation
   and compact report.
5. Finish the compact report and choose a feasible extension proposal. The AI
   circular-financing application is the leading candidate, not yet an
   approved or implemented extension.

## Completed tasks

| ID | Task | Status | Priority | Category | Estimate | Objective | Outcome | Task record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Crosswalk the selected 2025 results to usable 2021 inputs | Complete | 1 | paper-review | 60m | Determine, figure by figure, whether the supplied 2021 data can identify the July 2025 definition and isolate code, data-vintage, and unavailable-input gaps. | The source/code crosswalk is complete for Figures 1, 5, and 8. Figures 1 and 5 reconstruct through 2016; the current Figure 8 built from seven-round outputs remains a proxy. The exact authors-vintage matrices are unavailable, but current public completed FWTW enables a separate mixed-vintage full-method rerun. | [Result selection](tasks/result-selection.md); [quickstart](../reference/author-kit-quickstart.md) |
| T-002 | Inventory and document required data | Complete | 2 | data-lineage |  | Locate selected-exhibit inputs and document only the schemas, units, keys, vintage, and provenance actually used. | Figure-specific data contracts now identify the used files, columns, units, keys, coverage, source roles, and unavailable upstream objects for all three selected figures. | [Figure 1 data](../data/figure1-data.md); [Figure 5 data](../data/figure5-data.md); [Figure 8 data](../data/figure8-data.md) |
| T-003 | Reconstruct cleaning and merges | Complete | 2 | data-engineering |  | Reimplement the minimum required preparation with explicit transformations and merge contracts. | Python rebuilds the Figure 1 intermediary claims, Figure 5 fine wealth allocation and valuation closure, and Figure 8 fine-group aggregation with explicit contracts and aggregation/accounting checks. Authors' files remain read-only. | [Figure 1 replication](tasks/figure1-replication.md); [Figure 5 replication](tasks/figure5-replication.md); [Figure 8 replication](tasks/figure8-replication.md) |
| T-004 | Reproduce selected computations and exhibits | Complete | 1 | replication | 120m | Generate Figures 1, 5, and 8 as closely as the supplied inputs permit and compare each with declared benchmark evidence. | Figure 1 and Figure 5 are reconstructed from authors-kit inputs through 2016 and track the digitized 2025 targets closely. The delivered Figure 8 applies the revised group/sign/scale/base definition to the kit's seven-round positions and remains explicitly labelled a proxy; a separate public-FWTW full-method reconstruction is now the active follow-on. | [Figure 1 replication](tasks/figure1-replication.md); [Figure 5 replication](tasks/figure5-replication.md); [Figure 8 replication](tasks/figure8-replication.md); [major results](../../Results_Proposal/major_results.md) |
| T-007 | Validate the complete February 2021 replication package | Complete |  | replication-validation |  | Establish that the supplied Stata package can reproduce the paper version it accompanies and preserve a version-aware audit trail. | On 2026-08-09 the user-authorized StataNow 19.5 master run completed; all major outputs are mapped to the exact February 2021 revision, seven figures pass visual comparison, and Table 7 matches to three decimals. The verified nine-slide deck in `Presentation/1_replication_package_validation/` shows why this is a successful 2021 benchmark but not an exact 2025 replication. | [Benchmark and hydration](tasks/author-data-benchmark.md); [output crosswalk](../reference/author-output-crosswalk.md) |
| T-010 | Reconstruct Figure 6 with the 2025 method | Complete | 1 | replication |  | Apply the paper's percentile bins, active-saving numerator, and personal-plus-corporate disposable-income denominator to the 2021 authors-kit data, then construct directly comparable wealth-level and time-evolution views. | The raw DINA bins reaggregate to prepared author shares within $7.24\times10^{-8}$; annual wealth, saving, income, and equation (9c) close; audited paper correlations are 0.991 and 0.969. Percentile, wealth-level, comparison, digitization-audit, and five-year evolution figures cover the available 1963--2016 inputs. | [Figure 6 replication](tasks/figure6-replication.md); [Figure 6 data](../data/figure6-data.md); [personal considerations](personal-considerations-saving-inequality.md) |

## Planned tasks

| ID | Task | Status | Priority | Category | Estimate | Objective | Next action | Task record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-008 | Design a feasible extension proposal | Planned | 3 | research-design |  | Propose one economically meaningful extension without implying that it has been implemented; assess novelty, required data, identification, and feasibility. | Compare an AI circular-financing ownership/exposure network with one lower-data-cost extension using the supplied macro-financial data, then select the report proposal with the user. | [Extension proposal](tasks/extension-proposal.md) |

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
