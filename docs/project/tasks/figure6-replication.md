# T-010: Reconstruct Figure 6 with the 2025 Method

## Objective and status

Status: **Complete**.

Reproduce the July 2025 Figure 6 saving-rate method using the February 2021
authors-kit data, then place the exact same cohort rates against mean real
wealth so that the percentile and wealth-level descriptions are economically
comparable.

This task is separate from Figure 5. Figure 5 reports broad-group active-saving
flows relative to aggregate national income over time. Figure 6 reports
cohort-specific net saving divided by personal plus attributable corporate
disposable income across the wealth distribution.

## Target and method

- Target: July 2025 paper, Figure 6, physical PDF page 24.
- Paper bins: bottom 40%, then every one-percentile bin through the top 1%.
- Paper periods: 1963--1982 and 1983--2019.
- Available reconstruction periods: 1963--1982 and 1983--2016.
- Rate:

$$
s^N_{it}
=\frac{\Theta_{it}}{Z^{d,p}_{it}+Z^{d,\pi}_{it}}.
$$

The numerator uses the same 2025 active-saving identity already understood for
Figure 5, but it is rebuilt on the exact Figure 6 percentile allocation. The
denominator allocates supplied personal disposable income by `ponog` shares and
NIPA business saving by corporate-equity shares.

## Reconstruction boundary

The raw 16 GB DINA file is processed in bounded chunks to reconstruct the exact
percentile bins. This is preferable to forcing the authors' prepared 21
cohorts into one-percentile bins. The prepared file is used only as a coarser
aggregation check, with a maximum absolute discrepancy of
$7.24\times10^{-8}$.

All source files remain read-only. Generated intermediate data live under
`Data/interim/`; analysis tables live under `Data/processed/`; figures live
under `Results_Proposal/figures/`.

## Results

The reconstructed curves closely match the digitized paper shape:

| Window | Correlation | MAE |
| --- | ---: | ---: |
| 1963--1982 | 0.991 | 1.46 percentage points |
| 1983--2016 versus paper 1983--2019 | 0.969 | 1.22 percentage points |

The middle and upper-middle wealth distribution saves substantially less after
1982 in both the paper and reconstruction. For example, the 80th-percentile
bin falls from 18.1% to 7.4%, and the 90th-percentile bin falls from 31.5% to
15.2%. The reconstructed top 1% rises from 28.8% to 36.2%, in the same
direction as the paper's approximately 43% to 54% but at lower levels.

The matched wealth-level view confirms that this is not just a relabelling
artifact. The pre-1982 90th-percentile bin has mean real wealth near
\$303,000 and a 31.5% rate; the post-1982 80th-percentile bin has a similar
mean real wealth near \$286,000 but only a 7.4% rate. This remains descriptive
because the source is a repeated cross-section and the points are cohort means,
not fixed-dollar bins.

The trailing-five-year diagnostic rejects an overly simple interpretation of
1982 as one permanent common break. The 80th-percentile rate is about 20.1% in
the five years ending in 1982, briefly rises to 21.8% by 1987, then falls to
4.1% by 2002 and ends at 6.1% in 2016. The 90th percentile also trends down,
from 24.5% in 1982 to 17.8% in 2016, with reversals. The top 1% is far more
volatile: it peaks at 68.5% in the five-year window ending in 2008 and returns
to 24.1% by 2016. The supported claim is therefore heterogeneous persistence,
not a smooth monotone change at every percentile.

## Verification

- All asset, income, and population shares sum to one annually.
- Raw shares reaggregate to the authors' prepared shares within $10^{-6}$.
- Percentile wealth sums to aggregate net wealth annually.
- Personal and corporate disposable-income allocations close to their supplied
  aggregates annually.
- Active saving and the income-weighted rates close to NIPA personal plus
  business saving, including the paper's equation (9c).
- Targeted tests cover raw bin construction and the saving/income closure.
- The digitization audit recovers exact-color pixels for all 61 percentile
  samples on both paper curves; zero Figure 6 points require interpolation.
- The paper-raster overlay confirms that the recovered solid centerlines sit on
  the original dashed curves. One vertical pixel is 0.129 percentage points.
- All eight generated static plots were visually inspected after regeneration.

## Definition of done

- [x] Paper equation, bins, periods, units, and averaging convention recorded.
- [x] Required personal and corporate disposable-income inputs traced.
- [x] Exact percentile shares reconstructed from the raw DINA source.
- [x] Raw reconstruction validated against prepared author shares.
- [x] Annual active saving and disposable-income rates constructed in Python.
- [x] Accounting identities and equation (9c) tested.
- [x] Percentile, matched wealth-level, and paper-comparison figures generated.
- [x] Trailing-five-year percentile evolution generated without changing the
      paper's annual rate definition.
- [x] Digitized paper coordinates overlaid on the original embedded raster and
      direct pixel-match counts recorded.
- [x] Remaining data-vintage and identification boundaries documented.

## Reproducibility

Run once to rebuild the heavy raw-data intermediate:

```bash
PYTHONPATH=Code python Code/scripts/build_figure6_percentile_shares.py
```

Then rebuild all analysis outputs and plots:

```bash
PYTHONPATH=Code python Code/scripts/build_figure6_authors_data.py
```

The stable schema and complete output list are in
[`figure6-data.md`](../../data/figure6-data.md).

## Decision log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-08-11 | Preserve the earlier pretax-income wealth-level diagnostic but supersede it for substantive interpretation. | It was useful for hypothesis formation, but changing both the denominator and horizontal representation prevented a clean comparison with the paper. |
| 2026-08-11 | Use personal plus attributable corporate disposable income in both new panels. | Holding the numerator and denominator fixed isolates the effect of changing the horizontal coordinate from percentile rank to mean wealth. |
| 2026-08-11 | Recompute residual equity valuation on the exact percentile allocation. | Reusing the broad Figure 5 allocation left a small NIPA closure residual; solving on the Figure 6 bins restores the required invariant exactly. |
| 2026-08-11 | Add trailing-five-year means as a diagnostic, not a new target definition. | The paper's two-window comparison cannot distinguish a gradual shift from oscillation. Holding the annual rate fixed shows a persistent upper-middle decline but strong top-1 volatility. |
| 2026-08-11 | Audit digitization against the original embedded paper raster. | The overlay makes the approximate benchmark construction inspectable and confirms that no Figure 6 percentile sample depends on interpolation. |

## Session record: 2026-08-11 implementation

- Starting branch/commit: `main` at `91ab323`; unrelated worktree changes were
  preserved.
- Inputs: raw DINA microdata, authors' aggregate wealth and returns, NIPA
  saving, disposable-income aggregate, demographics, and the target PDF.
- Implementation: added chunked raw preprocessing, exact-method annual and
  period calculations, prepared-share validation, paper digitization,
  comparison metrics, tests, and static plots.
- Result: the method and most of the paper's cross-sectional shape reproduce
  closely through 2016; the top-1 level remains materially below the 2025
  curve.
- Follow-up: a trailing-five-year diagnostic shows a persistent but nonmonotone
  decline around the 80th--90th percentiles and a highly volatile top 1%.
- Next action: construct fixed-2018-dollar wealth bins if the project pursues a
  genuine descriptive estimate of $s(w)$ rather than cohort means.
