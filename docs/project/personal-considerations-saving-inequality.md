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

## Exact-method Figure 6 and the matched wealth-level view

![Figure 6 percentile and matched wealth-level views](../../Results_Proposal/figures/figure6_percentile_vs_wealth_level.png)

The new reconstruction uses the 2025 Figure 6 rate in both panels:

$$
s^N_{it}
=
\frac{\Theta_{it}}
     {Z^{d,p}_{it}+Z^{d,\pi}_{it}},
$$

where $\Theta_{it}$ is active saving, $Z^{d,p}_{it}$ is personal disposable
income, and $Z^{d,\pi}_{it}$ is corporate disposable income attributable to
the cohort through its corporate-equity ownership. The paper-style point for
period $P$ is the simple mean of the annual rates:

$$
\bar s^N_{iP}=\frac{1}{|P|}\sum_{t\in P}s^N_{it}.
$$

The left panel places the bottom 40% and each subsequent one-percentile cohort
at its wealth rank. The right panel places the **same observations with the
same numerator and denominator** at the cohort's mean real net wealth per adult
in 2018 dollars. This makes the two panels comparable. The authors-kit input
vintage limits the second period to 1983--2016 rather than the paper's
1983--2019.

The implementation reconstructs the percentile shares from the 16 GB raw DINA
file. Personal disposable income is allocated with the supplied `ponog`
concept, and NIPA business saving is attributed with corporate-equity shares.
The resulting rates satisfy the paper's accounting identity

$$
\sum_i s^N_{it}Z^d_{it}=S^p_t+S^\pi_t.
$$

### What the comparable views suggest

The exact-method result again rejects the strongest pure-composition version
of my hypothesis descriptively.

- At the 80th-percentile bin, the mean saving rate falls from 18.1% in
  1963--1982 to 7.4% in 1983--2016, while mean real wealth rises from about
  \$141,000 to \$286,000.
- Comparing nearby wealth levels rather than identical ranks strengthens the
  point. The pre-1982 90th-percentile bin has mean wealth near \$303,000 and a
  31.5% rate; the post-1982 80th-percentile bin has mean wealth near \$286,000
  but only a 7.4% rate.
- The reconstructed top 1% moves in the opposite direction: mean wealth rises
  from about \$3.0 million to \$6.9 million and its saving rate rises from
  28.8% to 36.2%.

Thus the available old-vintage data show both a rightward expansion of wealth
and a change in the cross-sectional saving-rate profile: rates decline through
much of the middle and upper-middle distribution but increase at the top 1%.
This is descriptive evidence, not a causal decomposition.

### Did the change occur once or evolve gradually?

![Trailing five-year Figure 6 evolution](../../Results_Proposal/figures/figure6_rolling5_evolution.png)

To avoid imposing the paper's pre/post split on the interpretation, I also
compute the trailing five-year mean of the same annual rate:

$$
\bar s^N_{i,t;5}=\frac{1}{5}\sum_{\tau=t-4}^{t}s^N_{i\tau}.
$$

This does not change the numerator or denominator; it only exposes when the
cross-sectional profile moved.

- The upper-middle decline is persistent but not perfectly monotone. At the
  80th percentile, the five-year rate is 20.1% in 1982, 21.8% in 1987, 4.1%
  in 2002, and 6.1% in 2016. At the 90th percentile, the corresponding values
  are 24.5%, 21.5%, 11.4%, and 17.8%.
- The top 1% does not follow a smooth rising trend. Its rate oscillates strongly
  and reaches 68.5% in the five-year window ending in 2008 before falling to
  24.1% in 2016.
- Therefore the data are inconsistent with both extreme stories: neither a
  one-time common break in 1982 nor a uniform monotone trend describes the
  whole distribution. A more defensible reading is a persistent downward
  shift through the upper middle combined with much stronger top-tail
  volatility.

The smoothing is descriptive. Overlapping five-year windows induce serial
dependence, and the exercise is not a formal break or trend test.

### What is replicated and what remains limited

The 2025 rate definition, percentile bins, valuation logic, and period
averaging are now reconstructed. The main numerical boundary is the older
input vintage. The reconstructed top-1 rates are also materially below the
paper's approximately 43% and 54%, even though the rest of the curves are
close: the paper-versus-ours correlations are 0.991 before 1982 and 0.969
after 1982.

The wealth-level panel still cannot establish a household-level $s(w)$
schedule:

- the DINA source is a repeated cross-section, so entry, exit, and rank
  mobility remain mixed with saving;
- each point is a percentile cohort located at its mean wealth, not a fixed
  real-dollar wealth bin; and
- especially in the top tail, a cohort mean represents a wide, skewed range.

The earlier pretax-income diagnostic is retained for audit history, but it is
superseded because it changed both the denominator and the horizontal
representation at once.

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

The follow-up work should proceed in this order:

1. **Completed: reconstruct Figure 6's denominator and percentile profile.**
   Personal and attributable corporate disposable income now enter both the
   percentile and matched wealth-level views, and the remaining paper mismatch
   is quantified.
2. **Next: build fixed-real-wealth-bin profiles from the raw DINA extract.** Hold
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

- Raw percentile producer:
  `Code/scripts/build_figure6_percentile_shares.py`
- Figure producer: `Code/scripts/build_figure6_authors_data.py`
- Reusable transformations: `Code/unveiling/figure6_authors.py`
- Annual data: `Data/processed/figure6_authors_annual.csv`
- Period summaries: `Data/processed/figure6_authors_data.csv`
- Matched figure:
  `Results_Proposal/figures/figure6_percentile_vs_wealth_level.png`
- Paper comparison:
  `Results_Proposal/figures/figure6_authors_data_comparison.png`
- Five-year evolution:
  `Results_Proposal/figures/figure6_rolling5_evolution.png`
- Rolling data: `Data/processed/figure6_authors_rolling5.csv`
- Tests: `Code/tests/test_figure6_authors.py`
- Task record: [`figure6-replication.md`](tasks/figure6-replication.md)
- Data and identification contract: [`figure6-data.md`](../data/figure6-data.md)

The superseded pretax-income files and producer remain documented in
[`figure6-wealth-level-diagnostic.md`](../data/figure6-wealth-level-diagnostic.md).
