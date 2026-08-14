# Reports

- `report.tex` is the longer, detailed methodological report.
- `replication_summary.tex` and `replication_summary.pdf` are the separate
  compact submission version: one page of replication text followed by three
  generated comparison figures. Its Figure 8 panel uses the primary
  same-vintage reconstruction from saved 2021 direct/pre-round fields with
  the full inverse; it retains the old seven-round output as a lineage
  benchmark and the current-public-FWTW rerun as robustness.

Regenerate the compact report metrics from the processed comparison tables:

```bash
python Code/scripts/build_replication_summary_assets.py
```

Then compile from this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error replication_summary.tex
```

The report does not overwrite or replace the detailed version.
