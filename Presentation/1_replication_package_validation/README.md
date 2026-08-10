# Replication-package validation deck

`replication_package_validation.pptx` compares the outputs regenerated from
the authors' February 2021 Stata package with the closest exhibits in the July
2025 paper. It is separate from the other presentation modules in the parent
folder.

## Current presentation sequence

The ten-slide deck now has a deliberately short main sequence:

1. purpose and version boundary;
2. interpretation framework;
3. 2021 Figure 7 versus 2025 Figure 8: net household debt; and
4. 2021 Figure 9 versus 2025 Figure 10: safe-asset demand.

Slide 5 is an explicit appendix divider. The saving, debt-flow,
indirect-ownership, investment, and broad-summary slides are retained after it
for future use but are not part of the current presentation sequence.

The deck distinguishes three claims:

- **strong precursor:** the same economic object and a closely related
  graphical claim;
- **partial match:** the same accounting lineage with revised groups,
  smoothing, sample, or transformation; and
- **context only:** related motivation or input, but not the same 2025 outcome
  variable.

The final slide summarizes the broader crosswalk for 2025 Figures 1, 5, and
8--11. Every comparison slide identifies the old exhibit and the 2025 paper
figure and PDF page; detailed provenance is stored in PowerPoint speaker notes.

## Presentation-specific benchmark figures

`Code/stata/format_2021_benchmark_figures.do` reads the authors' regenerated
`YinequalityFAanalysis.dta` and exports presentation-specific versions of old
Figures 7 and 9 under `assets/`. The numerical series, observations, signs,
1982 normalization, national-income scaling, colors, line patterns, and
markers are unchanged from the relevant `mss_analysis.do` blocks. Only the
legend position, label sizing, white background, and 8:5 graph dimensions are
changed. The legends now sit inside the upper-left of each graph, so they no
longer compress the plotting region horizontally.

Run the formatting step from the project root:

```bash
/Applications/StataNow/StataSE.app/Contents/MacOS/stata-se -b do \
  Code/stata/format_2021_benchmark_figures.do
```

The Stata log is `logs/format_2021_benchmark_figures.log`. The revised
PowerPoint was rendered back to PNG and all ten slides were visually inspected
at 1280x720 on 2026-08-10.
