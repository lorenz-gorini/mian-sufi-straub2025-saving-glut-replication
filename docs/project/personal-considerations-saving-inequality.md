# Personal Considerations on Saving, Wealth, and Debt

## Purpose and evidentiary status

This note records my interpretation of the distributional saving results and
the hypotheses I would like to test next. It deliberately separates:

1. what the July 2025 paper and our reconstruction measure;
2. what the available data already suggest; and
3. mechanisms that remain conjectures until we design a separate test.

The ideas about entrepreneurship, stock-backed borrowing, and tax incentives
are research hypotheses, not conclusions of the current replication.

## First clarification: Figure 5 versus Figure 6

My initial comment referred to Figure 5, but the graph of *saving rates across
wealth percentiles before and after 1982* is **Figure 6** of the 2025 paper.

- **Figure 5** plots each wealth group's total active-saving flow as a share of
  aggregate national income, using a trailing ten-year mean and subtracting
  the 1982 value.
- **Figure 6** plots cohort saving rates across the wealth distribution,
  comparing 1963--1982 with 1983--2019.

This distinction resolves part of my concern that the increase in the top
1 percent saving rate does not look very large. The paper reports an increase
from 43% to 54% of disposable income. Because the top 1 percent's income share
also increased, that rate applies to a much larger income base. In Figure 5,
the resulting annual top-1 saving flow rises by 2.9 percentage points of
aggregate national income after 1982, while bottom-99 saving falls by 6.7
percentage points. A moderate-looking rate change can therefore correspond to
a macroeconomically large flow change.

The paper's interpretation already includes two forces:

$$
S_{g t}=s_{g t}Z_{g t},
$$

where $S_{g t}$ is group $g$'s saving flow, $s_{g t}$ is its saving rate, and
$Z_{g t}$ is its disposable income. The saving glut can grow because the rich
receive more income, because they save a larger fraction of it, or both.

## My main hypothesis: ranks may conceal the role of wealth levels

My first conjecture is that a percentile graph may combine two different
changes:

1. the relationship between saving behavior and a household's real wealth;
2. the distribution of households and wealth across that relationship.

Perhaps households with similar real wealth save at similar rates in both
periods, while the post-1982 economy places much more wealth in the far upper
tail. In that case, rising inequality would work mainly through the changing
mass and scale of very wealthy households rather than through a large change
in behavior conditional on wealth.

The strongest version of this conjecture is:

$$
s_{t}(w) \approx s(w),
$$

where $s_t(w)$ is the saving rate at real wealth level $w$ in period $t$. A
pure composition story would imply a relatively stable $s(w)$ schedule and a
large change in the distribution of $w$.

## Exploratory wealth-level diagnostic

![Exploratory active-saving profiles by wealth level](../../Results_Proposal/figures/figure6_wealth_level_diagnostic.png)

The diagnostic keeps the 21 fine wealth-percentile cohorts supplied in the
2021 authors' kit but places each cohort at its **mean real net wealth per
adult**, rather than at its percentile rank. For cohort $c$ and period $P$,
the plotted rate is

$$
\widehat{s}_{cP}
=
\frac{\sum_{t\in P}\Theta_{ct}}
     {\sum_{t\in P}Y^{\mathrm{pretax}}_{ct}},
$$

where $\Theta_{ct}$ is active saving reconstructed with the 2025 valuation
identity and $Y^{\mathrm{pretax}}_{ct}$ is cohort pretax income from the
supplied DINA shares. The horizontal coordinate is mean cohort net wealth in
2018 dollars per adult. The ratio of period sums is used instead of averaging
annual ratios, which prevents a noisy year with small top-tail income from
dominating the result.

The accounting invariants still hold: the 21 cohorts sum to aggregate net
wealth, national income, and NIPA private saving in every year.

### What this diagnostic suggests

The result does **not** support the strongest, pure-composition version of my
hypothesis.

- In 1963--1982, the supplied 75--80% cohort has mean wealth of about
  \$124,000 and an estimated saving-to-pretax-income ratio of 14.5%. In
  1983--2016, the same rank has roughly \$256,000 of mean wealth but a rate of
  only 3.6%.
- Comparing nearby wealth levels rather than identical ranks gives the same
  message. The pre-1982 90--95% cohort averages about \$415,000 and saves
  29.0%; the post-1982 85--90% cohort averages about \$468,000 and saves
  10.4%.
- The post-1982 curve eventually crosses and exceeds the earlier curve, but
  only far into the upper tail. For the top 0.001%, the full-period proxy rises
  from about 19.3% to 53.0%, alongside a very large increase in mean wealth.
  Estimates for such tiny cohorts should be treated as especially sensitive.

Thus the data are more consistent with **both** a rightward expansion of the
wealth distribution and a change in the saving schedule: saving falls through
much of the middle and upper-middle distribution while it rises at the extreme
top. This is descriptive evidence, not a causal decomposition.

### Why this is not a Figure 6 replication

This plot cannot yet establish a stable or changing household-level $s(w)$
schedule.

- The DINA source is a repeated cross-section. A cohort in one year need not
  contain the same people in the next year, so entry, exit, and rank mobility
  remain mixed with saving.
- Each marker is a percentile cohort located at its mean wealth, not a fixed
  real-dollar wealth bin. Especially in the top tail, the mean represents a
  wide and skewed range.
- The denominator is supplied cohort **pretax income**. The 2025 Figure 6 rate
  uses disposable income and includes corporate disposable income attributable
  to shareholders. The plotted level is therefore a proxy.
- Wealth-based saving is not simply income minus personal consumption. It also
  includes retained corporate earnings attributed to equity owners, and it
  separates active saving from valuation gains.

## Who owns the debt?

The relevant exhibit is Figure 8, not Figure 6. It measures each wealth
group's net household-debt position,

$$
ND_{g t}=A^D_{g t}-D_{g t},
$$

where $A^D_{g t}$ is household-debt claims ultimately held by group $g$ and
$D_{g t}$ is that group's own household-debt liability. The 2025 paper finds
that the top 1 percent accumulate substantial additional net claims after
1982, while middle-wealth households become net borrowers.

It would nevertheless be too strong to say that the top 1 percent “own all
the debt.” Figure 8 concerns **net household debt relative to 1982**, after
unveiling intermediaries. It does not say that every gross debt instrument is
owned by the top 1 percent, and it does not eliminate the roles of foreign
holders, other domestic sectors, or financial intermediaries.

## Mechanisms I would like to investigate

### Unequal income growth

I expect average U.S. income to have risen more than median income, with much
larger real gains at the top than for the bottom half. The relevant empirical
test should compare mean and median real income, not infer their behavior from
wealth percentiles. Aggregate fine-cohort income shares can recover group
means; medians require returning to the underlying DINA microdata.

The paper itself gives a useful benchmark: it reports that average post-tax
real income rose from \$418,000 to \$1.008 million for the top 1 percent between
1982 and 2016, compared with \$29,000 to \$46,000 for the bottom 90 percent.
That is consistent with strongly unequal income growth, but it does not by
itself explain the saving-rate change.

### Entrepreneurship and business-equity composition

My second hypothesis is that the modern upper tail contains more founders or
owner-managers whose wealth is concentrated in their own firms. Such owners
may retain shares and corporate earnings rather than realize personal income
or sell equity.

The kit can test a narrower, measurable statement: whether business and
corporate-equity wealth became a larger share of top-tail portfolios, and how
much reconstructed top saving comes from equity-like categories. It cannot
identify whether a shareholder is a founder, whether a board discouraged a
sale, or why the person retained the position.

This mechanism is particularly relevant because the paper intentionally counts
retained corporate earnings as saving on behalf of shareholders. Its residual
equity-valuation adjustment is designed to prevent those retained earnings
from being misclassified as pure capital gains.

### Borrowing against appreciated shares

My third hypothesis is that wealthy households increasingly borrow against
appreciated shares instead of selling them. That could provide liquidity while
deferring realization of taxable capital gains. The proceeds might finance
consumption, portfolio reallocation, or productive investment.

The replication kit can show whether top groups simultaneously hold more
equity and incur more debt. It cannot identify whether a loan is collateralized
by stock, what its proceeds finance, whether it is repaid from investment
returns, or whether tax deferral caused the transaction. Testing that mechanism
credibly would require loan-level collateral information or richer SCF and
administrative data, plus a design that separates tax incentives from wealth,
returns, and credit access.

## Proposed empirical sequence

The immediate follow-up work should proceed in this order:

1. **Reconstruct Figure 6's denominator as closely as the kit permits.** Add
   personal and attributable corporate disposable income, reproduce the
   paper's pre/post percentile profile through 2016, and quantify the remaining
   mismatch with the 2025 definition.
2. **Build fixed-real-wealth-bin profiles from the raw DINA extract.** Hold
   2018-dollar bin thresholds fixed across periods, document reweighting and
   sparse top-bin rules, and distinguish a shift in $s(w)$ from a change in the
   wealth distribution. Repeated-cross-section composition will remain a
   limitation.
3. **Decompose active saving by asset class.** Separate business/corporate
   equity, pensions, fixed income, housing, and debt to determine which
   balance-sheet categories generate the post-1982 divergence.
4. **Measure portfolio composition at the top.** Test whether business and
   corporate-equity shares rise for the top 1%, top 0.1%, and top 0.01%, while
   clearly labelling this as a proxy for entrepreneurship rather than founder
   status.
5. **Compare real income means and medians.** Use the raw DINA data for the
   bottom 50%, 51--90%, next 9%, and top 1%; report growth rates and the
   mean--median gap. Avoid treating wealth rank and income rank as equivalent.
6. **Assess the collateralized-borrowing hypothesis separately.** First map
   which SCF variables identify stock ownership, business ownership, secured
   borrowing, loan purpose, and tax-relevant realization. If collateral is not
   observed, report the mechanism as unidentifiable rather than inferring it
   from coincident equity and debt.

The first two tests address the central measurement question. The portfolio
and debt tests then assess mechanisms without conflating a descriptive
balance-sheet pattern with causal evidence about motives.

## Reproducibility links

- Producer: `Code/scripts/build_figure6_wealth_level_diagnostic.py`
- Reusable transformations:
  `Code/unveiling/figure6_wealth_level_diagnostic.py`
- Annual cohort data: `Data/processed/figure6_wealth_level_profiles.csv`
- Period summaries: `Data/processed/figure6_wealth_level_windows.csv`
- Figure: `Results_Proposal/figures/figure6_wealth_level_diagnostic.png`
- Tests: `Code/tests/test_figure6_wealth_level_diagnostic.py`
- Data and identification contract:
  [`figure6-wealth-level-diagnostic.md`](../data/figure6-wealth-level-diagnostic.md)
