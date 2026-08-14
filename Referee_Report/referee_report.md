---
title: "Referee Report"
subtitle: "The Saving Glut of the Rich"
date: "Review of the July 25, 2025 draft"
papersize: letter
geometry: margin=1in
fontsize: 11pt
mainfont: "Times New Roman"
mathfont: "STIX Two Math"
colorlinks: true
linkcolor: "1F4D78"
urlcolor: "1F4D78"
header-includes:
  - |
    \usepackage{microtype}
    \usepackage{setspace}
    \setstretch{1.04}
    \usepackage{titling}
    \setlength{\droptitle}{-4em}
    \pretitle{\begin{center}\LARGE\bfseries}
    \posttitle{\par\end{center}\vskip 0.15em}
    \preauthor{}
    \postauthor{}
    \predate{\begin{center}\small}
    \postdate{\par\end{center}\vskip 0.5em}
    \usepackage{caption}
    \captionsetup{font=small,labelfont=bf}
    \usepackage{float}
    \floatplacement{figure}{H}
    \usepackage{xcolor}
    \definecolor{headingblue}{HTML}{1F4D78}
    \usepackage{titlesec}
    \titleformat{\section}{\large\bfseries\color{headingblue}}{}{0pt}{}
    \titleformat{\subsection}{\normalsize\bfseries\color{headingblue}}{}{0pt}{}
    \titlespacing*{\section}{0pt}{1.25em}{0.55em}
    \titlespacing*{\subsection}{0pt}{1em}{0.4em}
    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \fancyhf{}
    \fancyhead[L]{\small Referee Report}
    \fancyhead[R]{\small July 25, 2025 draft}
    \fancyfoot[C]{\small \thepage}
    \renewcommand{\headrulewidth}{0pt}
---

**Recommendation: Revise and resubmit.** This is an ambitious, original, and
highly relevant paper. Its central innovation is to combine Financial Accounts
data with a Leontief-style operator that traces claims through intermediary
cross-holdings to their ultimate owners and uses. This makes visible a major
within-household shift that aggregate national accounts conceal: the rise in
top-1-percent saving and its counterpart in household and government debt.
The treatment of valuation changes, retained corporate earnings, and
national-accounts closure is particularly valuable. Our reconstruction using
the older supplied inputs reproduces the main patterns closely, which increases
my confidence that the paper captures a real and economically important fact.
I recommend publication after a focused revision addressing the following
measurement and interpretation issues.

# Main comments

## 1. Show saving rates over time and by inflation-adjusted wealth levels

Figure 6 compares two long-period averages by wealth percentile. This is a
useful summary, but percentile rank is not the only relevant horizontal axis.
If households become richer over time and consumption rises less than
proportionally with wealth, an increasing saving rate at high ranks could
partly reflect movement along a stable, non-homothetic saving schedule rather
than a change in behavior conditional on resources. The paper should therefore
show the same saving-rate definition against inflation-adjusted wealth levels,
ideally using fixed real-wealth bins in addition to percentile bins.

Our diagnostic re-plots the same percentile-cohort saving rates at their mean
net wealth per adult in 2018 dollars (Referee Figure 1). The result does **not**
make the post-1982 divergence disappear. For example, the pre-1982 90th-percentile
cohort has mean wealth of about \$303,000 and a 31.5 percent saving rate, while
the post-1982 80th-percentile cohort has similar mean wealth of about \$286,000
but saves only 7.4 percent. The top 1 percent moves from about \$3.0 million to
\$6.9 million in mean wealth while its saving rate rises from 28.8 to 36.2
percent. These comparisons suggest both a rightward shift in wealth and a
change in the saving-rate profile. They remain descriptive because cohort means
are not fixed-dollar bins and the data are repeated cross-sections; this is
precisely why the authors should perform the fixed-real-wealth-bin exercise on
their exact 1963--2019 microdata.

The two-period average also hides considerable time variation (Referee Figure
2). In our older-input reconstruction, the five-year top-1 rate is 35.6 percent
in the window ending in 1982, peaks at 68.5 percent in the window ending in
2008, and falls to 24.1 percent by 2016. The bottom-40 rate moves from -3.3 to
-15.3 and back to -3.2 percent over the same windows. This is consistent with
strong crisis-era movement at both ends, in opposite directions, but it is not
a causal Great Recession estimate: overlapping windows blur timing and the
2008 window contains four pre-crisis years. The paper should add annual or
non-overlapping windows, recession shading, and a decomposition into financial
assets, housing, debt write-downs, and the equity-valuation residual.

A standard logarithmic color scale is invalid because saving rates can be zero
or negative. I suggest a linear, zero-centered main heatmap and a clearly
labelled symmetric-logarithmic or inverse-hyperbolic-sine diagnostic, accompanied
by selected-percentile lines. If the intended object is *change*, the heatmap
should plot deviations from each percentile's pre-1982 mean rather than levels.

## 2. Bound what the unveiling and saving assumptions identify

The proportional allocation rule is transparent, but claims issued by an
intermediary differ in seniority, maturity, collateral, guarantees, and risk.
The operator therefore identifies proportional ultimate claim ownership, not
necessarily loss incidence, control, or causation. The paper should report the
observed, balanced, and imputed shares of the direct matrix; the residual share;
and sensitivity of Figures 8--10 to perturbations of the largest imputed links
and alternative instrument-specific allocations.

Likewise, NIPA closure is an essential accounting check but does not identify
how the residual equity valuation term is distributed. Because equity ownership
is concentrated, plausible alternatives for equity inflation, corporate saving,
housing returns, and debt write-downs should be propagated into uncertainty or
sensitivity bands for Figures 5 and 6. These diagnostics are especially
important around 2008. Finally, causal verbs such as "fueled" or "drove" should
be reserved for identified mechanisms; the baseline establishes that saving is
ultimately *absorbed by* or *held against* particular debt claims.

## 3. Provide a version-matched replication package

The February 2021 package reproduces its own paper version, but it generally
ends in 2016 and uses the earlier round-by-round unveiling. The revised paper
should archive the exact 2025 inputs, completed annual matrices, crosswalks,
valuation construction, and figure scripts behind the 2019 results. This is
particularly important for a paper whose methodology is itself a major
contribution.

Overall, these requests would sharpen the interpretation rather than overturn
the main finding. The paper offers a genuinely useful framework and compelling
evidence that rising inequality has changed both the composition and ultimate
use of saving.

```{=latex}
\newpage
```

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Referee diagnostics

![Referee Figure 1. The same net-saving rates are plotted by percentile rank and by cohort mean net wealth per adult in 2018 dollars. This is an older-input reconstruction through 2016, not a fixed-real-wealth-bin estimate and not the authors' 2025 series.](../Results_Proposal/figures/figure6_percentile_vs_wealth_level.png){width=90%}

![Referee Figure 2. Trailing five-year net saving rates across the wealth distribution. The figure uses the February 2021 input vintage through 2016 and is diagnostic evidence, not the authors' July 2025 series.](../Results_Proposal/figures/figure6_rolling5_heatmap.png){width=90%}
