# T-011: Referee Report

## Objective and status

Write a constructive referee report on the July 25, 2025 draft of *The Saving
Glut of the Rich*. The submission should appreciate the contribution and
methodology, identify focused revisions, and remain within 1--1.5 pages of
prose plus any figures.

Status: **Complete**.

## Deliverables

- Editable source: `Referee_Report/referee_report.md`.
- Matching LaTeX source: `Report/referee_report.tex`.
- Reproducible build: `Referee_Report/source/rebuild_referee_report.zsh` and
  `Referee_Report/source/style_docx.py`.
- Local submission artifacts: `Referee_Report/output/referee_report.docx` and
  `Referee_Report/output/referee_report.pdf`, plus the LaTeX-built
  `Report/referee_report.pdf`.
- Diagnostics: `Results_Proposal/figures/figure6_percentile_vs_wealth_level.png`
  and `Results_Proposal/figures/figure6_rolling5_heatmap.png`.

## Main assessment

The report recommends revise and resubmit. It treats the Leontief-style
unveiling of intermediary claims, the valuation adjustment, and the connection
between top saving and ultimate debt uses as novel and relevant contributions.
The requested revisions sharpen interpretation rather than overturn the main
finding:

1. supplement wealth-percentile comparisons with fixed inflation-adjusted
   wealth bins and time-resolved saving rates;
2. show crisis-era variation and decompose the saving measure around 2008;
3. use a zero-centered linear heatmap as the main display and a sign-preserving
   symmetric-logarithmic or inverse-hyperbolic-sine robustness display, because
   an ordinary logarithm is undefined for zero and negative saving rates;
4. report sensitivity to proportional claim allocation and valuation-residual
   assumptions, while separating accounting incidence from causal mechanisms;
   and
5. archive a replication package matched to the July 2025 revision.

## Evidence boundary

The wealth-level diagnostic re-plots the same percentile-cohort saving rates at
cohort mean net wealth per adult in 2018 dollars. It shows that the post-1982
divergence does not disappear at comparable wealth levels, but it is not a
fixed-real-wealth-bin estimate. The five-year heatmap uses the February 2021
input vintage through 2016. Its window ending in 2008 includes 2004--2008 and
therefore supports a crisis-era descriptive statement, not a causal Great
Recession estimate. Both limitations are stated in the report and captions.

## Verification

- The PDF has three pages: roughly 1.5 pages of prose followed by one page with
  both diagnostics.
- All three PDF pages were rendered to PNG and visually inspected for clipping,
  overflow, figure readability, captions, headers, and page numbering.
- The DOCX ZIP package passes `unzip -t`; Pandoc re-extraction recovers the full
  report text and both captions. The document includes the intended styles,
  numbering, images, header, and footer.
- Exact Word-to-PDF automation was attempted, but Microsoft Word blocked on its
  save dialog. The independently generated PDF from the same Markdown source is
  therefore the visual-layout reference for this session.

## Session record: 2026-08-12

- Starting branch/commit: `main` at `eb31ee5`; unrelated worktree changes were
  preserved.
- Definition of done: satisfied. The requested length, positive assessment,
  wealth-level argument, heatmap discussion, further methodological comments,
  figures, editable format, and reproducible build are all present.

## Session record: 2026-08-15 LaTeX alignment

- Goal: create a LaTeX version that can later be merged with the compact
  replication summary submitted to the professor.
- Decision: keep `Report/referee_report.tex` as a separate standalone entry
  point and match `Report/replication_summary.tex` exactly on document class,
  margins, Latin Modern typography, colors, title hierarchy, paragraph spacing,
  and figure-note conventions.
- Verification: `latexmk -pdf -interaction=nonstopmode -halt-on-error
  referee_report.tex` succeeds without layout warnings. The two-page result has
  one complete text page and one figure page; both pages were rendered at 150
  dpi and visually inspected for overflow, clipping, and legibility.
- Existing Markdown, DOCX, PDF, detailed report, and compact replication
  summary were preserved unchanged.
