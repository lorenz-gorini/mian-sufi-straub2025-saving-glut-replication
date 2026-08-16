# Reports

- `report.tex` is the longer, detailed methodological report.
- `main.tex` is the standalone entry point for the compact replication summary;
  it imports the body-only `replication_summary.tex` and produces
  `replication_summary.pdf` with the build command below.
- The compact summary contains one page of replication text followed by three
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
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -jobname=replication_summary main.tex
```

The compact report does not overwrite or replace the detailed version. The
referee report and extension proposal remain independently compilable under
[`../Referee_Report/`](../Referee_Report/) and
[`../Extension_Proposal/`](../Extension_Proposal/). The final combined entry
point lives under [`../Submission_Report/`](../Submission_Report/).
