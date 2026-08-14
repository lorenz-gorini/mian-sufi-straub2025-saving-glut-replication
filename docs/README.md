# Documentation

This folder contains durable project documentation. It is deliberately small:
code behavior belongs in code, task status belongs in one dashboard, and
generated numerical results belong in generated artifacts.

## Map

| Document | Purpose |
| --- | --- |
| [`../AGENTS.md`](../AGENTS.md) | Canonical research and engineering guidance for agents. |
| [`project/progress.md`](project/progress.md) | Sole authoritative task dashboard. Read before substantial work. |
| [`project/tasks/result-selection.md`](project/tasks/result-selection.md) | Current multi-session task record and definition of done. |
| [`project/tasks/pedagogical-presentation.md`](project/tasks/pedagogical-presentation.md) | Learning-first explanation and presentation contract. |
| [`project/tasks/final-report.md`](project/tasks/final-report.md) | Evidence standard, progress, and completion criteria for the LaTeX report. |
| [`project/tasks/author-data-benchmark.md`](project/tasks/author-data-benchmark.md) | Historical benchmark, authors-data reconstruction, storage, and new-data robustness boundary. |
| [`project/tasks/figure1-replication.md`](project/tasks/figure1-replication.md) | T-004 Figure 1 definition, data boundary, reconstruction equations, validation, and remaining exact-vintage gap. |
| [`project/tasks/figure5-replication.md`](project/tasks/figure5-replication.md) | T-004 Figure 5 saving identity, fine-share reconstruction, NIPA closure, and paper comparison. |
| [`project/tasks/figure6-replication.md`](project/tasks/figure6-replication.md) | T-010 exact-method Figure 6 reconstruction with older inputs, matched wealth-level and five-year evolution views, validation, and paper comparison. |
| [`project/tasks/figure8-replication.md`](project/tasks/figure8-replication.md) | T-004 Figure 8 old-pipeline benchmark, primary 2021-direct/full-Leontief reconstruction, public-FWTW robustness route, validation, and paper comparison. |
| [`project/tasks/extension-proposal.md`](project/tasks/extension-proposal.md) | T-008 selected debt-composition extension, implemented preliminary evidence, causal boundary, and next empirical stage. |
| [`project/personal-considerations-saving-inequality.md`](project/personal-considerations-saving-inequality.md) | Personal interpretation of Figures 5--6, exact-method, wealth-level, and time-evolution evidence, testable hypotheses, limitations, and proposed empirical sequence. |
| [`data/data-guide.md`](data/data-guide.md) | Data zones, schema contract, merge documentation, and descriptives checklist. |
| [`data/author-kit-data-map.md`](data/author-kit-data-map.md) | Selective folder dictionary and storage/access policy for the downloaded authors' tree. |
| [`data/figure1-data.md`](data/figure1-data.md) | Selective Figure 1 source inventory, schemas, transformations, provenance, and vintage boundary. |
| [`data/figure5-data.md`](data/figure5-data.md) | Figure 5 input fields, wealth groups, valuation rules, merge contracts, closure, and outputs. |
| [`data/figure6-data.md`](data/figure6-data.md) | Exact-method Figure 6 raw percentile construction, disposable-income denominator, valuation closure, five-year diagnostic, outputs, and comparison evidence. |
| [`data/figure6-wealth-level-diagnostic.md`](data/figure6-wealth-level-diagnostic.md) | Superseded Figure 6-motivated pretax-income diagnostic, retained for audit history. |
| [`data/figure8-data.md`](data/figure8-data.md) | Figure 8 fine debt-position fields, sign convention, proxy boundary, aggregation checks, and outputs. |
| [`data/figure8-2021-direct-data.md`](data/figure8-2021-direct-data.md) | Primary Figure 8 direct/pre-unveiling field reconstruction, coarsened network, full-Leontief operator, component diagnostics, and limits. |
| [`data/figure8-public-fwtw-data.md`](data/figure8-public-fwtw-data.md) | Figure 8 public-data robustness crosswalk, full-Leontief operator, signed-level treatment, invariants, and outputs. |
| [`data/debt-composition-extension-data.md`](data/debt-composition-extension-data.md) | Mortgage-versus-consumer-credit stocks, active-saving contributions, category-specific unveiling, outputs, diagnostics, and limitations. |
| [`methods/leontief-unveiling.md`](methods/leontief-unveiling.md) | Equations, orientation, worked example, code contract, invariants, and comparison with the 2021 unveiling procedure. |
| [`reference/author-kit-quickstart.md`](reference/author-kit-quickstart.md) | Compact 2021 pipeline, preprocessing summary, prepared-file contracts, and 2025 reuse decisions for future agents. |
| [`reference/author-kit-map.md`](reference/author-kit-map.md) | High-level map of the authors' package, final files, and exhibit outputs. |
| [`reference/author-output-crosswalk.md`](reference/author-output-crosswalk.md) | Regenerated 2021 outputs mapped to exact old-paper pages and their July 2025 relationships. |
| [`../Results_Proposal/major_results.md`](../Results_Proposal/major_results.md) | Candidate and eventually selected major results. |
| [`../Presentation/README.md`](../Presentation/README.md) | Progress-presentation workflow and visual conventions. |
| [`../Report/README.md`](../Report/README.md) | Final-report build workflow and generated-input contract. |

## Placement rules

- Add a task record only for multi-session work, methodological decisions,
  research findings, dependencies, or substantial refactors.
- Put stable dataset contracts in `data/`, not in task records.
- Put navigation aids for external/reference material in `reference/`.
- Link to generated tables and figures instead of copying their values.
- Archive superseded task records rather than leaving two active sources of
  truth.
