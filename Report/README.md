# Reports

- `report.tex` is the longer, detailed methodological report.
- `replication_summary.tex` and `replication_summary.pdf` are the separate
  compact submission version: one page of replication text followed by three
  generated comparison figures. Its Figure 8 panel uses the primary
  same-vintage reconstruction from saved 2021 direct/pre-round fields with
  the full inverse; it retains the old seven-round output as a lineage
  benchmark and the current-public-FWTW rerun as robustness.
- `referee_report.tex` and `referee_report.pdf` are the matching compact
  referee-report component: approximately 1--1.5 pages of text followed by one
  page with the two Figure 6 diagnostics. It uses the same typography, colors,
  margins, and heading system as `replication_summary.tex` so the two can be
  merged into one submission later.
Regenerate the compact report metrics from the processed comparison tables:

```bash
python Code/scripts/build_replication_summary_assets.py
```

Then compile from this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error replication_summary.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error referee_report.tex
```

The report does not overwrite or replace the detailed version. The separate
research-extension component and its build instructions live under
[`../Extension_Proposal/`](../Extension_Proposal/).
