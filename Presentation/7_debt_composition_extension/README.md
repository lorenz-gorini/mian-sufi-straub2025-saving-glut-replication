# Debt-Composition Extension Deck

This seven-slide PowerPoint presents the implemented Stage 1 evidence for the
selected research extension. It remains separate from the replication
comparison deck: the evidence uses validated 2021-direct/full-Leontief results
and exact-method Figure 6 diagnostics, but the interpretation is a new,
preliminary extension.

The deck shows:

1. the mortgage-channel thesis and evidence boundary;
2. mortgage and consumer-credit liability changes by wealth group;
3. category-specific, write-down-adjusted contributions to active saving;
4. mortgage and consumer-credit net positions after full unveiling;
5. Figure 6 saving rates indexed by mean real wealth;
6. trailing-five-year Figure 6 rates across wealth percentiles; and
7. the causal question and additional data needed for the next stage.

The two Figure 6 slides were moved here from the direct-comparison deck because
they interpret the saving mechanism rather than compare a paper exhibit with
our implementation. The mean-wealth view shows that similarly wealthy bins
save much less after 1982; the heat map shows a persistent upper-middle decline
alongside volatile top-1 saving.

All empirical values are read from generated CSVs. Every slide contains a
`[Sources]` block in speaker notes, and the deck labels the evidence as
descriptive rather than causal.

## Build

First build and test the empirical extension and Figure 6 outputs from the
project root. Then load `RUNTIME_NODE`, `RUNTIME_NODE_MODULES`, and
`RUNTIME_BIN_DIR` from the presentation runtime and run:

```zsh
Presentation/7_debt_composition_extension/source/rebuild_presentation.zsh
```

The durable source follows a frozen seven-slide template starter and validated
frame map. It reuses the chart-plus-callout structure for the two Figure 6
diagnostics and writes QA renders and layouts to an isolated `/private/tmp`
workspace.

All seven slides were rendered and inspected individually on 2026-08-16. The
deck passes template-plan, template-fidelity, overflow, unresolved-placeholder,
speaker-note source, and PowerPoint-archive checks.

## Evidence boundary

- Sample: 1963--2016; highlighted pre-crisis changes use 1982--2007.
- Mortgage and consumer-credit stocks come from the February 2021 authors-kit
  direct-cell vintage and DINA wealth shares.
- The saving-flow chart applies the paper's category-specific debt write-down
  factors to signed Figure 5 liability levels.
- Figure 6 applies the 2025 net-saving-rate definition to 2021-kit inputs; the
  wealth view uses cohort means, not fixed-dollar bins.
- Consumer credit is an aggregate category. Credit cards, vehicles, student
  loans, and medical debt are not separately identified.
- The network has eight coarsened intermediary rows and an explicit unassigned
  owner, so this is not the unavailable 2025 34-instrument, 27-sector matrix.
