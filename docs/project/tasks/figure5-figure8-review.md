# T-009: Review and Integrate the Figure 5 and Figure 8 Comparisons

## Objective and status

Status: **In progress**.

Understand the economics and measurement behind the newly generated Figure 5
and Figure 8 results before treating them as presentation evidence. The task is
complete only when the paper definitions, supplied inputs, Python
transformations, comparison metrics, and evidentiary labels can be explained
without relying on the code as a black box.

The maintained review output is a short interpretation and correction record
for `Presentation/4_figure_comparison/presentation.pptx`. It must preserve the
distinction between a reconstruction and a proxy.

The personal interpretation and hypotheses prompted by Figures 5--6 are
maintained separately in
[`personal-considerations-saving-inequality.md`](../personal-considerations-saving-inequality.md).
That note includes a generated wealth-level diagnostic and a prioritized
sequence for testing income growth, fixed-dollar wealth bins, portfolio
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

1. Read the July 25, 2025 paper around Section 3.4 and Figure 5 (physical PDF
   page 22), then Sections 4.1--4.2 and Figure 8 (physical PDF page 29).
2. Compare those definitions with
   `docs/project/tasks/figure5-replication.md` and
   `docs/project/tasks/figure8-replication.md`.
3. Trace Figure 5 through `build_figure5_authors_data.py`,
   `figure5_authors.py`, the fine wealth-group shares, valuation adjustments,
   NIPA closure, ten-year trailing mean, and 1982 normalization.
4. Trace Figure 8 through `build_figure8_authors_data.py`,
   `figure8_authors.py`, fine-group aggregation, the old seven-round unveiled
   asset positions, $ND=A^D-D$, national-income scaling, and the 1982 base.
5. Inspect the paper-versus-ours panels and their common-sample metrics. Explain
   the remaining discrepancies using documented evidence rather than assigning
   them mechanically to either data or methodology.
6. Review the comparison deck slide titles, role labels, legends, source notes,
   and implication bands. Record any changes required before the panels enter
   the final synthesis presentation.

## Evidence boundary and invariants

- **Figure 5 is an old-input reconstruction.** The supplied wealth, fine-share,
  valuation, and NIPA inputs identify the revised transformation through 2016.
  The accounting check is
  $\sum_g\Theta_{gt}=S_t^p+S_t^\pi$.
- **Figure 8 is a bounded proxy.** Its fine-group debt assets come from the
  older seven-round unveiling because the completed 2025 direct matrices are
  absent. Every series must equal zero in 1982, and the group assets and
  liabilities must aggregate back to the supplied totals.
- High correlation with a digitized paper curve supports similarity in timing
  and shape; it does not identify whether a residual gap comes from data
  vintage, classifications, or the unveiling method.

## Definition of done

- [ ] The relevant paper passages have been read and summarized in economic
      language.
- [ ] Every symbol, unit, group, sign, window, and normalization in Figures 5
      and 8 can be explained.
- [ ] The input-to-output lineage of both Python builds has been reviewed.
- [ ] The Figure 5 saving closure and Figure 8 aggregation/base-year checks have
      been inspected.
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

## Session record: 2026-08-11 task creation

- Starting branch/commit: `main` at `880b14b`; the worktree already contained
  the Figure 5/8 implementation and presentation changes.
- Goal: turn the requested reading, interpretation, code tracing, comparison,
  and presentation review into one auditable task without reopening completed
  implementation T-004.
- Changed files: this task record and `docs/project/progress.md`.
- Result: T-009 owns the substantive review and final-presentation approval of
  the Figure 5 reconstruction and Figure 8 proxy.
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
