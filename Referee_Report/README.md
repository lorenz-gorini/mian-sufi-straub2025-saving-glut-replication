# Referee Report

`main.tex` is the standalone entry point for the two-page LaTeX referee
report. It imports the body-only `referee_report.tex`, whose second page
contains the two generated Figure 6 diagnostics.

Compile from this directory while preserving the existing semantic PDF name:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -jobname=referee_report main.tex
```

The Markdown/DOCX workflow remains separate. The same LaTeX body is imported
into the final combined report under
[`../Submission_Report/`](../Submission_Report/).
