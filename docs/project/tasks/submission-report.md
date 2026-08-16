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

## Session record: 2026-08-16 report audit and code-package handoff

- Starting branch/commit: `main` at `5e42db5`; the worktree was clean.
- Goal: ensure the submitted report does not disclose AI or agent usage while
  making the accompanying code package directly reproducible.
- Audit: case-insensitive whole-word searches covered the combined entry point,
  every imported LaTeX body, and all extracted PDF text. Standard PDF metadata was
  also inspected. No reference to AI, agents, Codex, ChatGPT, OpenAI, LLMs, or
  AI assistance was present; the PDF author field is empty and its creator and
  producer identify only LaTeX/pdfTeX.
- Documentation: the root README now records the Python environment, non-Git
  input boundary, Figure 1 preserved-file setup, ordered build commands for
  Figures 1, 5, 6, and all three Figure 8 routes, headline outputs, full test
  command, and combined-submission rebuild.
- Evidence boundary: the README explicitly distinguishes old-input
  reconstructions, the Figure 1 and Figure 8 public-data robustness routes,
  the Figure 8 seven-round lineage benchmark, and the unavailable exact July
  2025 matrix inputs.
