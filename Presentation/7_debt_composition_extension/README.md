# Debt-Composition Extension Deck

This five-slide PowerPoint presents the implemented Stage 1 evidence for the
selected research extension. It is intentionally separate from the replication
submission deck: the evidence uses the validated 2021-direct/full-Leontief
route, but the economic interpretation is a new, preliminary extension.

The deck shows:

1. mortgage and consumer-credit liability changes by wealth group;
2. category-specific, write-down-adjusted contributions to active saving;
3. mortgage and consumer-credit net positions after full unveiling; and
4. the causal question and additional data needed for the next research stage.

All empirical values are read from generated CSVs. No number is hand-entered
into the deck builder. Every slide contains a `[Sources]` block in its speaker
notes. The deck labels the evidence as descriptive rather than causal.

## Build

First build and test the empirical extension from the project root:

```bash
python Code/scripts/build_debt_composition_extension.py
python -m pytest -q Code/tests/test_debt_composition_extension.py \
  Code/tests/test_figure8_2021_direct.py
```

Then set `RUNTIME_NODE`, `RUNTIME_NODE_MODULES`, and `RUNTIME_BIN_DIR` from the
presentation runtime dependency loader and run:

```bash
Presentation/7_debt_composition_extension/source/rebuild_presentation.zsh
```

The editable output is `presentation.pptx`. On 2026-08-14, all five exported
slides were inspected at full resolution; the deck passed the automated
overflow test and the PowerPoint archive check.

## Evidence boundary

- Sample: 1963--2016; highlighted pre-crisis changes use 1982--2007.
- Mortgage and consumer-credit stocks come from the February 2021 authors-kit
  direct-cell vintage and DINA wealth shares.
- The saving-flow chart applies the paper's category-specific debt write-down
  factors to signed Figure 5 liability levels.
- Consumer credit is an aggregate category. Credit cards, vehicles, student
  loans, and medical debt are not separately identified.
- The network has eight coarsened intermediary rows and an explicit unassigned
  owner, so this is not the unavailable 2025 34-instrument, 27-sector matrix.
