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
| [`data/data-guide.md`](data/data-guide.md) | Data zones, schema contract, merge documentation, and descriptives checklist. |
| [`data/author-kit-data-map.md`](data/author-kit-data-map.md) | Selective folder dictionary and storage/access policy for the downloaded authors' tree. |
| [`data/figure1-data.md`](data/figure1-data.md) | Selective Figure 1 source inventory, schemas, transformations, provenance, and vintage boundary. |
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
