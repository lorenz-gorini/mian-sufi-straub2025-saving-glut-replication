# Data

This folder is reserved for this project's immutable raw additions and
rebuildable interim/processed artifacts. The authors' data remain in
`../MSS2021Febreplicationkit/data/` and must not be copied wholesale or edited.

Read [`../docs/data/data-guide.md`](../docs/data/data-guide.md) before adding
data. The selective Figure 1 inventory and current raw-source provenance are in
[`../docs/data/figure1-data.md`](../docs/data/figure1-data.md) and
[`raw/README.md`](raw/README.md). Ensure every later processed file has
documented inputs, keys, units, and a producing script.

## Figure 1 processed outputs

The two approaches are intentionally parallel and must not be treated as one
pipeline:

| Approach | Processed output | Producing script |
| --- | --- | --- |
| Primary authors-kit reconstruction | `processed/figure1_authors_data.csv`, `processed/figure1_authors_comparison.csv`, and `processed/figure1_bond_validation.csv` | `../Code/scripts/build_figure1_authors_data.py` |
| Secondary newer-public-data robustness | `processed/figure1_indirect_household_ownership.csv` | `../Code/scripts/build_figure1.py` |

The first uses authors-supplied older inputs through 2016. The second uses a
later public FWTW/BEA vintage through 2019. Their rows should be compared as
separately labelled results, never concatenated as if they came from one data
vintage.
