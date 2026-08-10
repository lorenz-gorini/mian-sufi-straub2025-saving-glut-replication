# February 2021 Author-Output Crosswalk

## Purpose and benchmark source

This note maps the regenerated Stata outputs to the exhibits in the exact paper
revision accompanied by the authors' February 2021 replication kit. It then
states whether each output is an exact historical benchmark or only a precursor
to the heavily revised July 2025 target paper.

The exact historical benchmark is `MSS_SGR_Feb2021.pdf`, the February 2021
revision of NBER Working Paper 26941. It has 69 PDF pages, was created in
February 2021, and has SHA-256
`1a16181d35a280da6f19ee1ddf9c9f5215ff528972d95001ff27499d1355f2f6`.
Source URL:
`https://www.nber.org/system/files/working_papers/w26941/revisions/w26941.rev1.pdf`.

The July 2025 target paper is a heavily revised version. Exhibit numbers,
periods, group definitions, smoothing, and the unveiling implementation can
differ. An exact match below therefore means exact correspondence to the
February 2021 paper, not automatic equality to the July 2025 paper.

## Highest-value manual checks

| February 2021 exhibit | Regenerated output | Analysis code | PDF page (printed page) | Economic evidence | July 2025 relationship |
| --- | --- | --- | --- | --- | --- |
| Figure 1 | `output/fig_glut.eps` | `mss_analysis.do:153` | 16 (14) | Top-1-percent saving from wealth-based, DINA income-less-consumption, and CBO income-less-consumption methods; five-year bins relative to 1978-1982. | Strong precursor to 2025 Figure 5, but the revised figure uses 10-year moving averages, bottom 99%, data through 2019, and a 1982 normalization. |
| Figure 3 | `output/fig_hh_a.eps`, `fig_hh_b.eps`, `fig_hh_c.eps` | `mss_analysis.do:282` | 20 (18) | Saving of top 1%, next 9%, and bottom 90% under three measurement approaches. | Strong precursor to the group breakdown in 2025 Figure 5; groups and smoothing are revised. |
| Figure 4 | `output/fig_bottomline.eps` | `mss_analysis.do:400` | 22 (20) | Accumulated accounting absorption of top-1-percent saving by the bottom 99%, government, investment, foreign flows, and discrepancy. Bars sum to zero by construction. | Related to 2025 Figures 5 and 11, but not an exact counterpart. |
| Figure 6 | `output/fig_owndet.eps` | `mss_analysis.do:587` | 31 (29) | Asset classes through which households increased ultimate holdings of household and government debt. | Contextual precursor to 2025 Figure 1's motivation for unveiling; it is not the revised indirect-ownership figure. |
| Table 7 | `output/tab_nhhd_.tex` | `mss_analysis.do:745` | 34 (32) | Household-debt borrowing, unveiled debt-asset accumulation, and net household-debt accumulation by group and period. | Strong flow/decomposition precursor to 2025 Figures 8 and 9. |
| Figure 7 | `output/fig_nhhd.eps` | `mss_analysis.do:774` | 35 (33) | Net household-debt stocks for top 1%, next 9%, and bottom 90%, scaled by national income and relative to 1982. | Closest old-kit precursor to 2025 Figure 8. |
| Figure 8 | `output/fig_demddebt.eps` | `mss_analysis.do:803` | 36 (34) | Sources financing the post-1982 rise in combined government and household debt. The code also exports household-only `fig_hhddebt.eps` and government-only `fig_govddebt.eps` diagnostics. | Related to the revised debt-financing results, especially 2025 Figure 10, but the exhibit is redefined. |
| Figure 9 | `output/fig_safe.eps` | `mss_analysis.do:865` | 37 (35) | Unveiled U.S. household and government debt held by the rest of the world and top 1%, scaled by national income. | Strong precursor to 2025 Figure 10. |

The regenerated Table 7 values match the February 2021 PDF to three decimals.
The regenerated versions of Figures 1, 3, 4, 6, 7, 8, and 9 were rendered and
visually checked against the listed PDF pages; series, labels, group ordering,
normalizations, and plotted magnitudes agree. This is a visual benchmark, not a
pixel-hash comparison.

## Supporting tables worth checking

| February 2021 table | Regenerated output | What it checks |
| --- | --- | --- |
| Table 1 | `output/tab_glut.tex` | Period means and changes for top-1-percent saving across the three methods. |
| Table 3 | `output/tab_bot90.tex`, `tab_nex9.tex` | Period means for dissaving by the bottom 90% and next 9%. |
| Table 4 | `output/tab_bot90val.tex`, `tab_nex9val.tex`, `tab_top1val.tex` | Decomposition of net-worth changes into active saving and valuation effects. |
| Table 5 | `output/tab_top1dec2.tex`, `tab_nex9dec2.tex`, `tab_bot90dec2.tex` | Active saving split into financial assets, real estate, and debt. |
| Table 6 | `output/tab_unveil1.tex`, `tab_unveil9.tex`, `tab_unveil90.tex` | Financial-asset accumulation that ultimately finances household and government debt. |

## Lower-priority historical-only outputs

The state-level figures and regression tables (`fig_Dtop1state.eps`,
`fig_statesaving*.eps`, `fig_statewealth.eps`, and `tab_state*.tex`) are exact
outputs for the February 2021 state analysis. The July 2025 paper drops that
main state-analysis section and adds different international evidence, so these
are useful for testing the old package but not for checking the selected 2025
Figures 1, 5, 8, or 9.
