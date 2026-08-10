# Project Progress and Task Dashboard

This is the only authoritative project-status document. It answers what is
active, what comes next, and what is complete. Detailed task records preserve
methodological decisions and evidence; stable data contracts live in
`docs/data/`.

## Active tasks

| ID | Task | Status | Priority | Category | Estimate | Objective | Progress and next action | Task record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Crosswalk the selected 2025 results to usable 2021 inputs | In progress | 1 | paper-review | 60m | Determine, figure by figure, whether the supplied 2021 data can identify the July 2025 definition and isolate code, data-vintage, and unavailable-input gaps. | The compact author-kit quickstart now records the pipeline and preliminary reuse boundary: Figure 5 preprocessing is closely aligned, while Figure 8's old unveiled totals are not a 2025 matrix input. Next complete the variable-level Figure 5 and 8 inventories and validate those classifications computationally. | [Result selection](tasks/result-selection.md); [quickstart](../reference/author-kit-quickstart.md) |
| T-002 | Inventory and document required data | In progress | 2 | data-lineage |  | Locate selected-exhibit inputs and document only the schemas, units, keys, vintage, and provenance actually used. | The Figure 1 inputs and cross-package data architecture are documented. Next add exact used-column schemas, merge contracts, and required-versus-available rows for Figures 5 and 8 rather than broadening the folder inventory. | [Figure 1 data](../data/figure1-data.md); [quickstart](../reference/author-kit-quickstart.md); [author-kit map](../reference/author-kit-map.md) |
| T-003 | Reconstruct cleaning and merges | In progress | 2 | data-engineering |  | Reimplement the minimum required preparation with explicit transformations and merge contracts. | The authors-data Figure 1 preparation is implemented and tested. After reviewing it, reconstruct the earliest feasible Figure 5 pipeline, then reuse its verified group and wealth inputs for Figure 8 where possible. | [Figure 1 data](../data/figure1-data.md) |
| T-004 | Reproduce selected computations and exhibits | In progress | 1 | replication | 120m | Generate Figures 1, 5, and 8 as closely as the supplied inputs permit and compare each with declared benchmark evidence. | Figure 1's 1963--2016 level closely matches the digitized 2025 curve (correlation 0.995; MAE 5.3 pp of NI), while its share remains denominator-sensitive. Today confirm that implementation, then run bounded Figure 5 and 8 feasibility builds and report exact failure boundaries rather than forcing false matches. | [Major results](../../Results_Proposal/major_results.md) |
| T-005 | Build the final pedagogical presentation | In progress | 2 | presentation |  | Distill the methodology novelty, version audit, reconstructed results, and limitations into one visually coherent course presentation while retaining the topic decks as source modules. | The 16-slide theory and 12-slide data modules now use paper-exact LaTeX vector equations; the ownership labels are enlarged, and a verified seven-slide theory module is ready for synthesis. Next add our 2025-definition reconstructions and an explicit code-change comparison to the final course deck. | [Presentation task](tasks/pedagogical-presentation.md) |
| T-006 | Produce the compact final replication report | In progress | 2 | writing |  | Convert the technical evidence into an approximately two-page course-facing report: methodology novelty first, replication evidence and limitations second, with a concise extension proposal. | The current ten-page report is a verified technical evidence base, not yet the requested short deliverable. Next incorporate the Figure 5/8 feasibility results, explain why our transformations differ from the 2021 code, and compress only after the empirical boundary is settled. | [Report task](tasks/final-report.md) |

## Immediate sequence: 2026-08-10

1. Review the existing Figure 1 reconstruction equation by equation and confirm
   which inputs and transformations come from the 2021 package.
2. For Figure 5 and then Figure 8, write the target definition, map every
   required object to the supplied files, and decide whether the 2016 endpoint
   can be computed under the 2025 definition. Missing 2017--2019 observations
   alone do not invalidate a 1963--2016 partial reconstruction.
3. Implement only the transformations supported by that inventory. Label each
   output as a historical benchmark, old-input reconstruction of a 2025
   definition, or infeasible with the supplied data.
4. Regenerate presentation-facing figures with readable legends and consistent
   axes, then synthesize the 2021 benchmark, 2025 published result, and our
   result without conflating them.
5. Finish the compact report and choose a feasible extension proposal. The AI
   circular-financing application is the leading candidate, not yet an
   approved or implemented extension.

## Completed tasks

| ID | Task | Status | Priority | Category | Estimate | Objective | Outcome | Task record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-007 | Validate the complete February 2021 replication package | Complete |  | replication-validation |  | Establish that the supplied Stata package can reproduce the paper version it accompanies and preserve a version-aware audit trail. | On 2026-08-09 the user-authorized StataNow 19.5 master run completed; all major outputs are mapped to the exact February 2021 revision, seven figures pass visual comparison, and Table 7 matches to three decimals. The verified nine-slide deck in `Presentation/1_replication_package_validation/` shows why this is a successful 2021 benchmark but not an exact 2025 replication. | [Benchmark and hydration](tasks/author-data-benchmark.md); [output crosswalk](../reference/author-output-crosswalk.md) |

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
