# Submission Report

`main.tex` is the final written-submission entry point. It defines the common
LaTeX preamble and imports the three body-only components in submission order:

1. `../Referee_Report/referee_report.tex`;
2. `../Report/replication_summary.tex`; and
3. `../Extension_Proposal/extension_proposal.tex`.

Each component still has its own standalone `main.tex`. Keep document classes,
packages, generated-value inputs, command definitions, and
`\begin{document}`/`\end{document}` in the entry points rather than the body
files.

Compile from this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -jobname=submission_report main.tex
```

The result is `submission_report.pdf`: two referee-report pages, three
replication-summary pages, and two extension-proposal pages, with continuous
page numbering.
