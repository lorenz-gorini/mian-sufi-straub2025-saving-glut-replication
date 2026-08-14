# T-009: Review and Integrate the Figure 5, Figure 6, and Figure 8 Comparisons

## Objective and status

Status: **In progress**.

Understand the economics and measurement behind the generated Figure 5,
Figure 6, and Figure 8 results before treating them as presentation evidence.
The task is complete only when the paper definitions, supplied inputs, Python
transformations, comparison metrics, and evidentiary labels can be explained
without relying on the code as a black box.

The maintained review output is a short interpretation and correction record
for `Presentation/4_figure_comparison/presentation.pptx` and the focused
`Presentation/6_figure8_method_comparison/presentation.pptx`. It must preserve
the distinction among an old-pipeline benchmark, an old-vintage
reconstruction, and a public-data robustness route.

The personal interpretation and hypotheses prompted by Figures 5--6 are
maintained separately in
[`personal-considerations-saving-inequality.md`](../personal-considerations-saving-inequality.md).
That note includes an exact-method Figure 6 reconstruction, a matched
wealth-level view, a trailing-five-year evolution diagnostic, and a prioritized
sequence for testing fixed-dollar wealth bins, income growth, portfolio
composition, and collateralized borrowing.

## Economic questions

### Figure 5: who actively saves?

For wealth group $g$ and balance-sheet category $j$, active saving is

$$
\Theta_{gjt}=W_{gjt}-(1+\pi_{gjt})W_{gj,t-1},
\qquad
\Theta_{gt}=\sum_j\Theta_{gjt}.
$$

$W_{gjt}$ is the end-of-year stock and $\pi_{gjt}$ is its valuation return.
The plotted series is the trailing ten-year mean of $\Theta_{gt}/NI_t$ minus
its 1982 value, in percentage points of aggregate national income. The review
must explain why an increase in wealth is not necessarily saving: capital
gains are removed before attributing the residual flow to active saving.

### Figure 6: how much of disposable income does each cohort save?

For wealth-percentile cohort $i$,

$$
s^N_{it}=\frac{\Theta_{it}}{Z^{d,p}_{it}+Z^{d,\pi}_{it}}.
$$

The numerator is active saving. The denominator combines personal disposable
income with corporate disposable income attributable through equity ownership.
The comparison averages annual rates over 1963--1982 and 1983--2016, while the
paper's later-data curve continues through 2019. The matched wealth-level panel
uses exactly the same rate and changes only the horizontal coordinate.

### Figure 8: who ultimately finances household debt?

For wealth group $g$,

$$
ND_{gt}=A^D_{gt}-D_{gt},
$$

where $A^D_{gt}$ is the household-debt asset ultimately held by the group and
$D_{gt}$ is its own household-debt liability. Both are stocks. The difference
is divided by aggregate national income and expressed relative to 1982.
Positive values mean net lending to other households; negative values mean net
borrowing.

## Required review sequence

1. Read the July 25, 2025 paper around Section 3.4 and Figures 5--6 (physical
   PDF pages 22 and 24), then Sections 4.1--4.2 and Figure 8 (physical PDF page
   29).
2. Compare those definitions with
   `docs/project/tasks/figure5-replication.md` and
   `docs/project/tasks/figure6-replication.md` and
   `docs/project/tasks/figure8-replication.md`.
3. Trace Figure 5 through `build_figure5_authors_data.py`,
   `figure5_authors.py`, the fine wealth-group shares, valuation adjustments,
   NIPA closure, ten-year trailing mean, and 1982 normalization.
4. Trace Figure 6 through `build_figure6_percentile_shares.py`,
   `build_figure6_authors_data.py`, raw DINA bin construction, personal and
   corporate disposable-income allocation, valuation closure, and period
   averaging.
5. Trace all three Figure 8 routes: the downstream seven-round benchmark,
   `build_figure8_2021_direct.py` and its 351-field/coarsened full-inverse
   reconstruction, and `build_figure8_public_fwtw.py` with the current public
   completed matrix. Then inspect the comparison-only build, $ND=A^D-D$,
   national-income scaling, and the 1982 base.
6. Inspect the paper-versus-ours panels and their common-sample metrics. Explain
   the remaining discrepancies using documented evidence rather than assigning
   them mechanically to either data or methodology.
7. Review the comparison deck slide titles, role labels, legends, source notes,
   and implication bands. Record any changes required before the panels enter
   the final synthesis presentation.

## Evidence boundary and invariants

- **Figure 5 is an old-input reconstruction.** The supplied wealth, fine-share,
  valuation, and NIPA inputs identify the revised transformation through 2016.
  The accounting check is
  $\sum_g\Theta_{gt}=S_t^p+S_t^\pi$.
- **Figure 6 is an exact-method, old-input reconstruction.** The supplied raw
  DINA, disposable-income, valuation, and NIPA inputs identify the revised rate
  through 2016. It verifies
  $\sum_i s^N_{it}Z^d_{it}=S_t^p+S_t^\pi$.
- **Figure 8 has three explicitly separated routes.** Route A reads
  fine-group debt assets after the older seven-round unveiling. Route B reads
  no round outputs, reconstructs eight coarsened intermediary rows from 351
  saved direct fields, and applies the full inverse; it is the primary
  same-vintage operator test. Route C applies the full inverse to current
  public completed FWTW and is a robustness route. All must equal zero in 1982
  and satisfy their documented matrix and allocation closures.
- High correlation with a digitized paper curve supports similarity in timing
  and shape; it does not identify whether a residual gap comes from data
  vintage, classifications, or the unveiling method.

## Definition of done

- [ ] The relevant paper passages have been read and summarized in economic
      language.
- [ ] Every symbol, unit, group, sign, window, and normalization in Figures 5,
      6, and 8 can be explained.
- [ ] The input-to-output lineage of all three Python builds has been reviewed.
- [ ] The Figure 5 saving closure, Figure 6 income-weighted closure, and Figure
      8 aggregation/base-year checks have been inspected.
- [ ] The reconstruction-versus-proxy distinction and remaining discrepancies
      are understood.
- [ ] The comparison slides have been reviewed and required corrections have
      been recorded or implemented.
- [ ] The approved panels and explanations have been added to the final short
      presentation without duplicating the full comparison module.

## Decision log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-08-11 | Create a human-review task separate from completed empirical implementation T-004. | The code and comparison deck are verified artifacts, but the learning-first project contract also requires Lorenzo to understand and approve the economics, construction, and evidentiary boundary before final synthesis. |
| 2026-08-11 | Treat the saving-rate discussion as Figure 6 interpretation and the new wealth-level plot as an exploratory diagnostic. | Figure 5 reports aggregate saving flows by broad group, while Figure 6 reports saving rates by percentile. The new plot retains fine percentile cohorts but changes their horizontal coordinate and uses a pretax-income proxy, so it must not inherit the Figure 6 replication label. |
| 2026-08-11 | Supersede the pretax-income diagnostic with an exact-method Figure 6 reconstruction and a matched wealth-level view. | Both new panels use personal plus attributable corporate disposable income; only the horizontal coordinate changes, so their comparison is interpretable. |
| 2026-08-11 | Treat the five-year evolution as a diagnostic rather than a new replication target. | It holds the 2025 annual saving-rate definition fixed and reveals timing, but overlapping windows do not constitute a formal structural-break test. |
| 2026-08-12 | Separate the exact 2025 data-vintage gap from methodological feasibility. | The 2021 kit alone lacks the Batty-completed target matrices, but the current public FWTW release supplies completed bilateral estimates that can be combined with 2021 DINA/NIPA for a labelled mixed-vintage full-Leontief rerun. |
| 2026-08-13 | Use the public-FWTW full-Leontief build as the preferred Figure 8 result and retain the old proxy as lineage. | The full operator is now implemented and closes exactly; it improves top-1 fit but not every level, while the public vintage and taxonomy remain different from the authors' unavailable target matrices. |
| 2026-08-14 | Supersede the public route as the primary test: lead with 2021 direct cells plus the full inverse, retain the old proxy as the same-vintage benchmark, and relabel public FWTW as robustness. | Moving upstream within the old kit separates the operator from data vintage as far as the saved fields permit. The comparison remains closest-feasible rather than exact because the old general matrix cube was not saved. |

## Session record: 2026-08-14 same-vintage Figure 8 reconstruction

- Added the 2021-direct/full-inverse route without changing either existing
  route. It reads 351 direct/pre-unveiling fields and zero round-output fields.
- Added route-specific network and component diagnostics, a comparison-only
  build, same-vintage operator metrics, and a revised eight-slide three-route
  deck.
- The full inverse changes the old seven-round series modestly: mean absolute
  differences are 0.26 percentage points for the top 1% and 0.75 for the
  bottom 99%. Signed-cell clipping and the explicit unassigned owner remain
  material limitations, so this is not an exact code-only experiment.

## Session record: 2026-08-13 preferred Figure 8 reconstruction

- Implemented the public-FWTW direct-network build in a separate module and
  entry point; the old seven-round proxy is unchanged.
- Added the explicit public-instrument-to-DINA crosswalk, annual full inverse,
  household-debt allocation, negative-position sensitivity, tests, processed
  outputs, and diagnostics.
- Added the first version of the separate eight-slide comparison deck. The
  2026-08-14 revision supersedes its two-route hierarchy while retaining the
  public-FWTW implementation as Route C.

## Session record: 2026-08-11 task creation

- Starting branch/commit: `main` at `880b14b`; the worktree already contained
  the Figure 5/8 implementation and presentation changes.
- Goal: turn the requested reading, interpretation, code tracing, comparison,
  and presentation review into one auditable task without reopening completed
  implementation T-004.
- Changed files: this task record and `docs/project/progress.md`.
- Result: T-009 owns the substantive review and final-presentation approval of
  the Figure 5 reconstruction and all three explicitly separated Figure 8
  routes.
- Next action: read the two target-paper passages, then walk through Figure 5's
  saving identity before reviewing the generated comparison panel.

## Session record: 2026-08-11 personal hypotheses and wealth levels

- Economic question: can the post-1982 divergence be explained only by a
  rightward shift in wealth, or did saving behavior also change conditional on
  wealth?
- Implementation: retained the 21 supplied fine cohorts, reconstructed their
  active saving with the verified Figure 5 valuation identity, located each at
  mean net wealth per adult in 2018 dollars, and pooled saving relative to
  supplied pretax income over pre/post and endpoint-decade windows.
- Invariants: fine-cohort wealth and income aggregate to their supplied totals,
  and active saving retains the annual NIPA private-saving closure.
- Finding: a pure composition explanation is insufficient descriptively. The
  post-1982 saving profile lies substantially below the earlier profile at
  middle and upper-middle wealth levels, then rises above it only in the far
  upper tail.
- Boundary: repeated cross-sections, percentile-cohort means, and a pretax-
  income denominator do not identify a household-level fixed-wealth schedule
  or reproduce the paper's disposable-income Figure 6 rate.
- Next action: reconstruct the Figure 6 disposable-income denominator as far as
  the kit permits, then create fixed-2018-dollar wealth bins from the raw DINA
  extract before testing portfolio-composition and collateral hypotheses.

## Session record: 2026-08-11 exact-method Figure 6

- Economic object: annual active saving divided by personal plus attributable
  corporate disposable income for the bottom 40% and each later wealth
  percentile.
- Implementation: rebuilt the bins from raw DINA data, allocated the two
  denominator components, solved valuation closure on the exact bins, and
  averaged annual rates over the paper-aligned periods available through 2016.
- Validation: raw shares match the authors' prepared aggregates within
  $7.24\times10^{-8}$; equation (9c) closes; paper correlations are 0.991 and
  0.969 with MAEs of 1.46 and 1.22 percentage points.
- Finding: the post-1982 profile is lower through most of the middle and upper
  middle but higher at the top 1%; the old-input top-1 levels remain below the
  2025 curve.
- Next action: decide whether fixed-real-dollar bins are worth the additional
  raw-data transformation.

## Session record: 2026-08-11 Figure 6 evolution and presentation

- Added trailing-five-year means for every wealth-percentile bin while keeping
  the exact Figure 6 numerator and denominator unchanged.
- Result: the 80th--90th percentile decline is persistent but nonmonotone; the
  top 1% oscillates sharply and peaks in the five-year window ending in 2008.
- Integrated Figure 5 and Figure 6 method, paper-comparison, wealth-level, and
  evolution evidence into the verified fourth presentation.
