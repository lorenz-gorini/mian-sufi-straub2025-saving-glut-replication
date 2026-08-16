# T-012: Combined Written Submission

## Objective and status

Assemble the referee report, compact replication summary, and extension
proposal into one reproducible written submission while preserving each
component as an independently compilable document.

Status: **Complete**.

## Structure and source contract

The component files are body-only sources:

- `Referee_Report/referee_report.tex`;
- `Report/replication_summary.tex`; and
- `Extension_Proposal/extension_proposal.tex`.

Their local `main.tex` files own the standalone preambles, generated-value
inputs, document environments, and output names. `Submission_Report/main.tex`
owns the union preamble, loads both generated-value files, imports the three
bodies in the requested order, and inserts explicit page boundaries. This
keeps the prose, equations, tables, figures, and internal page breaks unchanged
while avoiding nested `\begin{document}` environments or duplicated command
definitions.

## Definition of done

- [x] Each component has a standalone `main.tex` entry point.
- [x] Each imported component source contains body content only.
- [x] The combined entry point imports referee, replication, and extension in
      that order.
- [x] All three standalone entry points compile to their original 2/3/2-page
      artifacts.
- [x] The combined entry point compiles without LaTeX, reference, or box
      warnings.
- [x] The seven-page PDF has continuous page numbering and all pages have been
      rendered and visually inspected.

## Session record: 2026-08-15

- Starting branch: `main`; the worktree was clean.
- Refactor: moved only the document class, packages, colors, generated inputs,
  macros, layout settings, and document environments into the four entry
  points. The substantive component bodies were not rewritten.
- Build command: `latexmk -pdf -interaction=nonstopmode -halt-on-error
  -jobname=submission_report main.tex` from `Submission_Report/`.
- Result: `Submission_Report/submission_report.pdf` contains two referee-report
  pages, three replication-summary pages, and two extension-proposal pages.
- Verification: the standalone and combined builds succeed; the combined log
  contains no layout or reference warnings; Poppler reports seven letter-sized
  pages; all pages were rendered at 144 dpi and inspected for clipping,
  overlap, table/figure legibility, section transitions, and pagination.
