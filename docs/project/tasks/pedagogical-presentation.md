# T-005: Final Pedagogical Presentation

## Objective

Use the verified topic-specific decks and the package-validation deck as source
modules for one concise final course presentation. It must explain the paper's
main methodological novelty, show exactly what the February 2021 package
reproduces, compare the selected July 2025 figures with our reconstructions,
and make remaining data/version limitations visually unmistakable.

Professional conference-level polish is not the objective. Clarity,
consistency, and instructional value are.

## Audience and rationale

The user has substantial technical experience in computer vision and PyTorch
but is learning the macroeconomics, national accounting, and financial-network
methodology. The presentation may assume comfort with matrices, code, and
statistical reasoning. It must not assume familiarity with Financial Accounts
terminology, distributional national accounts, saving-versus-valuation
decompositions, or sectoral balance-sheet conventions.

## Approved exhibit scope

| Order | Exhibit | Role in the teaching sequence |
| --- | --- | --- |
| 1 | Figure 1 | Explain why intermediation creates an ownership veil and how the matrix/unveiling method removes it. |
| 2 | Figure 5 | Explain how distributional saving is inferred from wealth changes net of valuation effects. |
| 3 | Figure 8 | Explain how unveiled debt assets and household liabilities determine net debt across wealth groups. |
| 4 | Figure 9 | Optional extension from debt stocks to financing flows if the three core figures are complete. |

## Content rules

For every core figure, include:

- the economic question and intuition;
- the relevant paper equation(s);
- definitions of symbols, units, signs, base periods, and smoothing;
- a source-to-variable-to-transformation diagram;
- at least one simple worked example for a non-obvious construction;
- the benchmark figure and the independently generated figure;
- a quantitative comparison and explanation of discrepancies;
- assumptions, data limitations, and what cannot be inferred.

Keep notation identical across markdown, code documentation, and slides. If a
short Python column name differs from paper notation, show the mapping once and
reuse it.

## Working method

1. Write the durable methodological explanation in the relevant result record.
2. Implement and verify the corresponding data/code stage.
3. Convert the explanation into a small number of visual slides.
4. Add generated outputs only; do not type estimates manually.
5. Rebuild and visually inspect the complete owning deck after material changes.
6. Never edit a presentation source owned by another concurrent chat; use the
   numbered topic subfolders documented in `Presentation/README.md`.

## Visual hierarchy contract

The project-wide standard is the PowerPoint grammar documented in
`Presentation/README.md`. Each content slide has one one-line declarative title,
one dominant visual or equation, a clearly separated implication band, and a
small source rail. Explanatory definitions are subordinate and separated from
the claim by whitespace. Diagram labels must visibly attach to their matrices,
nodes, or arrows; floating operators and overlapping elements are prohibited.

## Final synthesis plan

The final deck should be built only after the Figure 5 and 8 feasibility audit
settles which empirical comparisons are defensible. Its main sequence is:

1. research question and the 2021--2025 version boundary;
2. one intuitive flow diagram showing direct positions, intermediaries, and
   ultimate owners;
3. the Leontief-style unveiling novelty, with one small numerical example;
4. what the complete 2021 Stata run validated;
5. Figure 1, Figure 5, and Figure 8 comparison panels, each showing the 2021
   precursor, the 2025 target, and our result where feasible;
6. code/data changes that explain why our reconstruction can be closer to the
   2025 definition than the unchanged 2021 plotting code;
7. a compact evidence table distinguishing replicated, reconstructed, proxied,
   and unavailable results; and
8. limitations and one proposed extension.

`NotebookLM-Present-Unveiling_the_Rich_Saving_Glut.pdf` may guide visual pacing,
flow, and intuition. It is not an authoritative source and must not supply
empirical claims, definitions, or citations. Recreate useful diagrams in
editable TikZ/PowerPoint/Python form rather than copying the synthesis pages.

The old-package figures whose legends shrink the plotting region should be
regenerated from the underlying data or Stata graph definitions with the
legend moved outside the data panel, concise labels, consistent aspect ratios,
and readable fonts. Do not stretch or cosmetically crop the benchmark in a way
that could change the visual comparison.

## Initial outline

1. Research question, target paper, and version mismatch with the 2021 kit.
2. Approved scope and learning objectives.
3. Common balance-sheet and flow-of-funds vocabulary.
4. Figure 1 methodology and reconstruction.
5. Figure 5 methodology and reconstruction.
6. Figure 8 methodology and reconstruction.
7. Figure 9 extension, if reached.
8. Comparison summary, limitations, and lessons learned.
9. Appendix: schemas, merge diagnostics, accounting residuals, and robustness.

## Definition of done

- [x] The package-validation, data-map, and theoretical-methodology source
      modules exist and have been visually verified.
- [ ] The final synthesis deck has one 16:9 entry point that builds
      reproducibly.
- [ ] Figures 1, 5, and 8 each have a complete intuitive, mathematical, data,
      implementation, and result explanation.
- [ ] Every empirical value, figure, and table is generated by code.
- [ ] Notation, units, signs, group colors, and base periods are consistent.
- [ ] Benchmark and independent results are visually and quantitatively
      distinguished.
- [ ] Figure 9 is included only if the core scope is complete.
- [ ] Appendix diagnostics support rather than interrupt the main explanation.
- [ ] The rendered deck has been visually inspected for legibility.
- [ ] Benchmark legends and labels remain readable without materially shrinking
      the data panels.
- [ ] NotebookLM-inspired visuals are independently recreated and all factual
      content is checked against the 2025 paper or project evidence.

## Current module evidence

The first 14-slide module was added on 2026-08-02. Its worked-example slides
were redesigned and a one-bank row/column interpretation slide was added on
2026-08-03. Three Figure 1 slides were added on 2026-08-05. The authors-data
benchmark and evidence-hierarchy revision on 2026-08-09 brought the deck to 21
slides:

- entry point: `Presentation/presentation.tex`;
- rendered deck: `Presentation/presentation.pdf`;
- generated numerical inputs:
  `Presentation/generated/unveiling_values.tex` and
  `Presentation/generated/figure1_values.tex` and
  `Presentation/generated/figure1_authors_values.tex`;
- generated authors-data comparison chart:
  `Results_Proposal/figures/figure1_authors_data_comparison.png`;
- generating script: `Code/scripts/build_unveiling_teaching_assets.py`;
- Figure 1 scripts: `Code/scripts/build_figure1.py` and
  `Code/scripts/build_figure1_authors_data.py`;
- durable explanation: `docs/methods/leontief-unveiling.md`.

The data-architecture revision later on 2026-08-09 brings the deck to 24
slides. The module covers Sections 2.1--2.3, Equations (1)--(4), the paper's matrix
orientation, a worked example, code and invariants, and the comparison with the
authors' seven-round procedure. The revised example maps every nonzero
intermediary-row matrix entry to a directed edge, uses line width to encode the
direct share, and shows that 72.093% ultimate household ownership of the bank
equals 20% direct plus 52.093% through the fund. Exact numbers and paths are
generated by Python. The added one-bank slide
clarifies that outgoing shares have the bank-liability denominator and sum to
one, while an incoming fund-to-bank share has the fund-liability denominator
and is not a bank-portfolio share. The empirical slides distinguish 23 sectors
from 34 instruments; state which authors-prepared steps are reused; show the
explicit nine-group aggregation; compare the authors-data level with the
digitized paper; and keep the newer public result as robustness evidence. The
three new slides distinguish 34 instrument matrices from 23 intermediary
sectors, show when a missing cell is a residual versus a multi-cell balancing
problem, make the DINA cohort split explicit, and crosswalk the inputs and
equations for Figures 1, 5, and 8. The rebuilt 24-slide deck compiles without
layout warnings; the new slides were visually inspected at full resolution,
and the unchanged slides retain the earlier full-deck inspection. The legacy
combined artifact remains useful only for provenance; the verified Figure 5
and 8 results now live in the empirical-comparison PowerPoint.

The 24-slide root deck is now classified as a legacy combined artifact. The
current topic modules are the 12-slide
`Presentation/2_data-map/presentation.pptx` and the 16-slide
`Presentation/3_theoretical_methodology/presentation.pptx`, with the separate
seven-slide synthesis module
`Presentation/3_theoretical_methodology/presentation_short.pptx`. The earlier Beamer
sources and PDFs remain beside them for provenance but are not synchronized
with the revised layout. The theory PowerPoint covers only Sections 2.1--2.2:
direct ownership, block orientation, Equation (4), the path expansion, the
Leontief solve, convergence, the exact four-sector network, Equations (2)--(3),
the Python implementation, and the older seven-round comparison. Its network
slide reconciles 20% direct plus 52.093% through the fund to 72.093% ultimate
household ownership. All three current PowerPoints have passed full visual and
template-fidelity checks.

The 12-slide `Presentation/4_figure_comparison/presentation.pptx` is now the
maintained empirical-comparison module. It distinguishes the 2025 target, the
authors-old Stata precursor, ours-public robustness, and ours-authors result,
then applies that hierarchy to Figures 1, 5, and 8. Figures 1 and 5 are labeled
reconstructions; Figure 8 is labeled a bounded proxy because the completed
2025 matrices are absent from the old package. Its main comparisons place each
paper graph beside our generated output and report common-sample fit. All 12
slides were rendered and inspected, contain source blocks in speaker notes,
and pass template-fidelity, overflow, unresolved-placeholder, and archive
checks.

## Decision log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-07-24 | Make the presentation a visual teaching companion, not a professional research talk. | The main purpose of the project is to learn the topic and methodology. |
| 2026-07-24 | Build the story around Figures 1, 5, and 8, with Figure 9 optional. | This mirrors the approved replication scope and avoids a disconnected presentation. |
| 2026-08-02 | Start the deck with a self-contained Leontief-unveiling module. | The matrix method is the prerequisite for interpreting Figures 1 and 8 and can be verified before the 2025 empirical matrices are reconstructed. |
| 2026-08-03 | Keep the reciprocal two-intermediary example and expose every edge and fixed-point contribution. | It is fully drawable but still contains an infinite ownership loop; adding sectors would make the example harder to audit without adding a new economic idea. |
| 2026-08-03 | Use ImageGen only for a conceptual companion and TikZ/Python for the exact diagram. | Generated raster art cannot reliably encode matrix labels or numerical edge weights. |
| 2026-08-03 | Add a one-bank slide before introducing the full network recursion. | The row denominator explains funding composition and the row-sum invariant; incoming column entries require different issuer denominators and cannot be read as the bank's portfolio shares. |
| 2026-08-05 | Add Figure 1 only as an explicitly later-vintage independent reconstruction. | The public series recovers the central rise, while the 21-versus-23 sector and data-vintage differences preclude an exact authors'-output label. |
| 2026-08-09 | Put the evidence hierarchy before the method and add an authors-data Figure 1 comparison before the newer public result. | The main replication exercise must be visually prior to robustness, and the deck must show which preparation was reused versus recomputed. |
| 2026-08-09 | Replace cloud-only conceptual raster dependencies with native TikZ schematics. | The exact diagrams are clearer, reproducible, and allow a warning-free build without changing empirical content. |
| 2026-08-09 | Separate FWTW cell completion, DINA cohort allocation, and NIPA/valuation closure in the visual architecture. | These sources identify different dimensions; treating DINA as the source of bilateral network residuals would misstate the paper's implementation. |
| 2026-08-09 | Keep package validation in a separate PowerPoint under `Presentation/1_replication_package_validation/`. | The user wants a direct old-package-versus-2025-paper audit, not additional slides inside the pedagogical Beamer deck. |
| 2026-08-09 | Replace the single combined-deck workflow with numbered topic-specific presentation folders. | Multiple chats edited the same root `presentation.tex`; separate ownership prevents accidental overwrites and keeps data architecture distinct from theoretical methodology. |
| 2026-08-09 | Use a planar square for the exact four-sector network. | It preserves all six directed edges while avoiding owner-link crossings; background-layer links and border-clipped arrowheads keep arrows out of node labels. |
| 2026-08-10 | Treat the three verified topic decks as source modules for a new final synthesis rather than merging their full contents. | The course presentation needs one short narrative; concatenating 39 slides would duplicate material and obscure the version/result comparison. |
| 2026-08-10 | Use the NotebookLM deck only as a visual-communication reference. | Its flow is useful, but it is a secondary synthesis and cannot establish the paper's definitions or empirical evidence. |
| 2026-08-10 | Regenerate benchmark figures when layout changes are needed. | Moving legends in the producing graph preserves data integrity and produces a fairer comparison than stretching or cropping rendered images. |
| 2026-08-10 | Use the package-validation PowerPoint as the presentation-wide visual grammar. | The previous Beamer theme had oversized wrapping titles, weak title/footer separation, and explanations that competed with the main claim. |
| 2026-08-10 | Enforce title → primary object → implication → source as the slide hierarchy. | Deliberate spacing and a single implication band make the main message immediately identifiable. |
| 2026-08-10 | Keep topic Beamer files as historical references and maintain the revised topic decks in PowerPoint. | The editable PowerPoint template produces the more professional hierarchy requested by the user without deleting earlier work. |
| 2026-08-10 | Render substantive PowerPoint equations from one shared LaTeX source. | Unicode approximations distorted sums, fractions, matrices, and subscripts; vector SVGs preserve the paper's notation and LaTeX geometry while remaining sharp at any slide size. |
| 2026-08-10 | Keep a separate seven-slide theory module instead of shortening the full teaching deck in place. | The full derivation remains available for study, while the condensed sequence can be combined with data and result modules without creating an excessively long final presentation. |
| 2026-08-10 | Put the four Figure 1 roles in a separate empirical-comparison deck. | The main replication test is ours-authors versus the 2025 target; separating the Stata precursor and public-data robustness prevents provenance, method, and vintage from being conflated. |
| 2026-08-10 | Extend the empirical-comparison deck with Figure 5 as a reconstruction and Figure 8 as a bounded proxy. | The old kit identifies the revised saving decomposition through 2016, but its seven-round unveiled debt assets are not the missing 2025 matrix inputs. The slide labels must preserve that difference in evidentiary strength. |

## Session record: 2026-08-10 topic-deck visual redesign

- Starting version: the standalone data-map and theory modules were Beamer
  decks with oversized titles, weak footer separation, and several ambiguous or
  overlapping diagram annotations.
- Goal: establish one professional hierarchy that also governs every future
  deck revision.
- Outputs: `Presentation/2_data-map/presentation.pptx` (12 slides) and
  `Presentation/3_theoretical_methodology/presentation.pptx` (16 slides).
- Theory correction: the direct-ownership slide now attaches issuer rows,
  holder columns, owner/intermediary dimensions, and matrix blocks explicitly.
  The exact four-sector example then reconciles 20% direct plus 52.093%
  indirect ownership to the 72.093% unveiled household share without floating
  operators.
- Visual rule: every content slide has one one-line takeaway title, bounded
  primary content, a single `WHY IT MATTERS` band, and a source rail separated
  from the slide edge.
- Validation: both PowerPoints were rendered slide by slide and visually
  inspected; their template-fidelity checks passed with zero issues. The old
  Beamer sources and PDFs remain unchanged for provenance.

## Session record: 2026-08-10 equation and condensed-deck revision

- Starting issue: PowerPoint text approximations made summation limits,
  fractions, matrix notation, and subscripts look unlike the paper and unlike
  LaTeX; the four-sector edge shares were too small at normal viewing size.
- Mathematical correction: `Presentation/math-assets/equations.tex` is now the
  shared source for all substantive equations in the full theory and data-map
  PowerPoints. Equation (4) reproduces the paper's
  \((\mathbf 1/\mathbf L_t)^\top\odot\sum_h\mathbf M_{h,t}\) construction;
  the \((\mathbf I-\mathbf Q)^{-1}\mathbf B\) expression is labeled as the
  equivalent ultimate-owner block used by the Python implementation.
- Rendering correction: the LaTeX SVGs retain their native aspect ratios, so
  tall operators are not stretched and matrices are not clipped. The direct
  ownership graph uses enlarged node and edge-label text in both decks.
- New output: `Presentation/3_theoretical_methodology/presentation_short.pptx`
  is a seven-slide sequence covering the ownership veil, Equation (4), the
  Leontief inverse, the complete worked network, the 72.093% reconciliation,
  and the seven-round-versus-exact-solve comparison.
- Validation: the 16-slide full theory deck, 12-slide data-map deck, and
  seven-slide condensed theory deck were rendered and inspected slide by
  slide. Their titles remain one line, source-note blocks are complete, every
  element is on canvas, every PPTX archive validates, and all three
  template-fidelity checks pass with zero issues.

## Session record: 2026-08-10 final-deliverable refresh

- Starting version: the workspace is not recognized as a Git worktree, so no
  branch or commit identifier is available.
- Goal: connect yesterday's verified package-validation output with today's
  final presentation requirements.
- Result: T-005 now owns one final synthesis deck, readable regenerated
  benchmark figures, a three-layer 2021/2025/ours comparison, and an explicit
  rule for using the NotebookLM presentation only as visual inspiration.
- Next action: complete the Figure 5 and 8 feasibility classifications before
  fixing the comparison-panel layouts and assembling the final narrative.

## Session record: 2026-08-10 Figures 5 and 8 comparison module

- Goal: implement the two remaining core exhibits with the 2025 definitions
  wherever the February 2021 inputs permit, then add defensible paper-versus-
  ours comparisons to the empirical deck.
- Figure 5: reconstruct fine wealth by group, remove valuation changes using
  the paper's saving identity and NIPA equity closure, aggregate to the revised
  wealth groups, apply the trailing ten-year mean, and subtract the 1982
  value. The top-1/bottom-99 correlations with the digitized paper curves are
  0.992/0.997, with mean absolute errors 0.40/0.42 percentage points.
- Figure 8: aggregate the package's fine seven-round debt-asset positions and
  liabilities, apply $ND=A^D-D$, divide by national income, and subtract
  1982. This is a proxy rather than a reconstruction because the completed
  revised instrument-by-sector matrices are unavailable.
- Output: the comparison PowerPoint now has 12 slides and includes the paper
  graphs without their printed captions, two method-boundary slides, two
  primary comparison slides, and a cross-figure synthesis.
- Validation: all slides were rendered and inspected at full size. The deck
  passes template-fidelity, overflow, unresolved-placeholder, source-note, and
  archive-integrity checks.
- Next action: assemble the final short course presentation from the verified
  topic modules and carry the same reconstruction/proxy distinction into the
  compact report.

## Session record: 2026-08-11 substantive-review handoff

- Starting branch/commit: `main` at `880b14b`; the worktree already contained
  the verified 12-slide comparison module and other presentation changes.
- Goal: make Lorenzo's substantive review of the new Figure 5 and Figure 8
  results a prerequisite for their use in the final short presentation.
- Changed files: this task record, `docs/project/progress.md`, and the new
  T-009 review record.
- Result: T-009 now owns paper reading, economic interpretation, code tracing,
  metric review, and slide corrections. T-005 will integrate only the approved
  comparison panels and explanations.
- Next action: complete the Figure 5/8 review checklist, then assemble the final
  synthesis without duplicating the full empirical-comparison deck.

## Session record: 2026-08-10 focused package-validation sequence

- Goal: retain the successful two-figure comparison grammar while removing
  weaker old-to-new mappings from the current presentation sequence.
- Main sequence: after the purpose and version-boundary slides, show only old
  Figure 7 versus 2025 Figure 8 and old Figure 9 versus 2025 Figure 10.
- Appendix: saving, debt-flow, indirect-ownership, investment, and the broad
  crosswalk are preserved after a visible appendix divider.
- Benchmark formatting: `Code/stata/format_2021_benchmark_figures.do` regenerates
  the two old figures from `YinequalityFAanalysis.dta`, with the same numerical
  series and graph semantics but inside legends, smaller labels, a white
  background, and an 8:5 aspect ratio. No authors-package file is overwritten.
- Validation: StataNow SE 19.5 completed the formatting script; the exact 2007
  Figure 7 values were 0.1203363, 0.0003915, and -0.3891515 for the top 1%,
  next 9%, and bottom 90%. The final ten-slide PowerPoint was rendered back to
  PNG and inspected slide by slide.
- Next action: add a third panel for our reconstruction and document each code
  change that moves the 2021 definition toward the 2025 target.

## Session record: 2026-08-09 replication-package validation deck

- Goal: compare the regenerated February 2021 authors-package outputs with the
  closest exhibits in the July 2025 paper and state how much validation each
  comparison supports.
- Output:
  `Presentation/1_replication_package_validation/replication_package_validation.pptx`.
- Coverage: old Figures 1, 4, 6, 7, and 9 and old Table 7 against 2025 Figures
  1, 5, and 8--11.
- Interpretation: the saving, net-debt, and safe-asset exhibits are strong
  precursors; the debt-flow and investment exercises retain accounting lineage
  but use revised transformations; the old ownership-detail chart is only
  contextual for 2025 Figure 1.
- Validation: the exported nine-slide PowerPoint was rendered back to PNG;
  every slide was inspected at full size, the saved archive passed an integrity
  test, and no overflow or overlap warning appeared in the generated inspection
  records.
- Boundary: the deck does not call the old package an exact 2025 replication
  because the revised paper changes the sample endpoint, groups, smoothing, and
  matrix/unveiling implementation.

## Session record: 2026-08-09 data architecture

- Starting version: the workspace was not recognized as a Git worktree, so no
  branch or commit identifier was available.
- Goal: explain which datasets construct the ownership network and which split
  it across household groups, then connect those layers to Figures 1, 5, and 8.
- Changed files: Presentation/presentation.tex, Presentation/presentation.pdf,
  Presentation/README.md, and this task record.
- Reasoning: the Financial Accounts/FWTW identify bilateral sector positions;
  DINA supplies mapped cohort shares; NIPA and valuation inputs identify
  saving. CEX and PSID are not the 2025 Figure 5 baseline.
- Validation: the 24-slide deck was built twice in an isolated temporary
  directory because OneDrive log placeholders were not writable. The final log
  has no layout warnings; slides 8, 9, and 19 were inspected at full
  resolution.
- Result: the deck now prevents the 23-sector/34-instrument and
  FWTW/DINA-residual confusions before presenting the empirical figures.
- Next action: trace and implement the exact Figure 5 baseline variables and
  replace the architecture preview with generated benchmark/result slides.

## Session record: 2026-08-09 standalone data-map deck

- Starting version: the workspace was not recognized as a Git worktree, so no
  branch or commit identifier was available.
- Goal: recover the overwritten data-architecture presentation as a standalone
  artifact while leaving the root combined deck and other agents' presentation
  folders untouched.
- Changed files: `Presentation/2_data-map/presentation.tex`,
  `Presentation/2_data-map/presentation.pdf`,
  `Presentation/2_data-map/README.md`, `Presentation/README.md`,
  `docs/project/progress.md`, and this task record.
- Scope: dataset identification, instrument-level dollar matrices, missing
  FWTW cells, row normalization, DINA cohort shares, household-column
  augmentation, NIPA/valuation closure, Figure 1/5/8 branches, old-kit builders,
  and replication storage architecture.
- Boundary: detailed Leontief recursion, worked network examples, Python
  implementation, and empirical Figure 1 results are excluded because they
  belong in other decks.
- Validation: `latexmk` produced a 12-page 16:9 PDF with no warning, overfull,
  underfull, undefined-reference, or error lines; all 12 pages were rendered to
  PNG and visually inspected.
- Result: `Presentation/2_data-map/` is now the canonical editable data-map
  deck. The root 24-slide deck is preserved as a legacy combined artifact.

## Session record: 2026-08-09 standalone theory deck

- Starting version: the root `Presentation/presentation.tex` was a 24-slide
  combined progress deck and had been edited by multiple chats.
- Goal: recreate only the paper's theoretical methodology in an isolated
  `Presentation/3_theoretical_methodology/` deck.
- Changed files: the new folder's `presentation.tex`, `presentation.pdf`,
  README, local generated-value input, cover asset and asset README;
  `Presentation/README.md`; this task record; and the project dashboard.
- Scope: Sections 2.1--2.2 and Equations (1)--(4), including implementation and
  old/new recursion comparison; no data map and no empirical result slides.
- Visual decision: use a conceptual ImageGen cover only. The exact four-sector
  network is a planar TikZ square so owner links do not cross, arrows terminate
  visibly at node borders, and the unveiled household share is reconciled to
  the original direct network.
- Validation: `latexmk` produced an 18-page 16:9 PDF with no LaTeX layout
  warnings. All 18 slides were rendered with Poppler and inspected; crowded
  frames and diagram crossings were corrected before the final build.
- Result: theory, data architecture, and package validation now have separate
  editable entry points; the legacy root deck is retained only for provenance.
- Next action: keep empirical reconstruction slides in their own result-owned
  presentation rather than adding them to the theory deck.
