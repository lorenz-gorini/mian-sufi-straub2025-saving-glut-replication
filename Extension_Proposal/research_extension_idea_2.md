# Research Extension 2: From Unveiled Ownership to Unveiled Risk

## Purpose, status, and central decision

This is the canonical detailed note for the proposed extension of Mian,
Straub, and Sufi (MSS). The original debt-composition design produced useful
preliminary evidence, but **debt composition by wealth is not sufficiently
novel on its own**. It is therefore retained as the empirical foundation for a
sharper question:

> Did the expansion of financial intermediation transform the saving glut of
> the rich into cheaper and more abundant mortgage credit, thereby lowering
> middle-wealth households' measured saving, and who ultimately bore the
> resulting credit risk?

The proposed contribution moves from **unveiled ownership of nominal claims**
to **unveiled exposure to state-contingent losses**. It combines:

1. Figure 1's rise in indirect ownership and intermediation-chain length;
2. Figure 6's widening saving-rate gradient by wealth;
3. Figure 8's top-lender/middle-borrower split; and
4. a new model of pooling, screening, funding liquidity, capital absorption,
   guarantees, and loss pass-through.

The economic sequence to be tested is

$$
\text{top saving and demand for claims}
\longrightarrow
\text{financial intermediation and risk transformation}
\longrightarrow
\text{mortgage price and quantity}
\longrightarrow
\text{middle-household borrowing and saving}.
$$

This is a hypothesis, not a finding. Financialization may lower funding or
idiosyncratic-risk costs, but it may also weaken screening, hide aggregate
risk, or shift losses to intermediary capital and government guarantees. The
sign and quantitative importance of the mechanism must be estimated.

The broad mortgage-versus-consumer-credit decomposition is already implemented
and verified through 2016. It identifies the pre-2008 mortgage market as the
empirically relevant setting; it does not establish that financialization
caused the mortgage boom or the Figure 6 divergence.

## Why this question follows directly from MSS

MSS provide four motivating facts:

- **Saving-rate divergence.** Figure 6 shows that the top 1% saving rate rises
  from 43% to 54% between 1963--1982 and 1983--2019, while the rest falls from
  14% to 7%. The project's trailing-five-year heatmap adds timing and shows
  that the decline below the top is not a uniform secular shift.
- **Financialization.** Figure 1 shows the indirectly held share of household
  financial assets rising from about 45% in 1960 to about 70% in 2007, with
  longer intermediation chains.
- **Debt absorption.** Table A2 identifies additional borrowing as the largest
  accounting component of the saving decline below the top 1%.
- **Ultimate financing.** Figure 8 shows the top becoming a larger ultimate
  net lender to other households before 2008.

The paper's operator explains who ultimately owns a dollar claim, but it is
deliberately payoff-blind. It does not identify:

- how pooling changes idiosyncratic versus aggregate risk;
- whether securitization lowers funding costs or mortgage spreads;
- who screens the borrower and who retains first-loss exposure;
- how capital buffers, seniority, limited liability, and guarantees allocate
  losses; or
- whether intermediation caused the expansion of credit and the fall in
  middle-wealth saving.

This boundary is also the opening for the extension. MSS conclude that the
incentives and constraints directing excess saving toward household leverage
rather than productive investment are an important question for future
research. The proposed model makes that allocation choice explicit.

## Motivating evidence already established in this project

The current same-vintage implementation holds the February 2021 direct
ownership network fixed, separates home mortgages from broad consumer credit,
applies category- and group-specific write-down factors, and uses the full
Leontief inverse. It reads no old seven-round output field. Full provenance and
diagnostics are in the
[extension data contract](../docs/data/debt-composition-extension-data.md).

### Borrowing and active saving

From 1982 to 2007, mortgage liabilities rose by 23.63 percentage points of
aggregate national income for the next 40% and 13.85 points for the bottom 50%,
compared with consumer-credit increases of 2.92 and 4.04 points. During
1998--2007, mortgage borrowing contributed -3.09 and -2.28 percentage points of
national income per year to active saving for these groups; consumer credit
contributed -0.73 and -0.88 points.

These magnitudes use aggregate national income as the scale. They are not yet
the exact Figure 6 group saving-rate contributions, whose denominator is each
group's personal plus attributable corporate disposable income.

### Ultimate positions

After unveiling, the 1982--2007 mortgage net-position change is +8.69 points
for the top 1%, -19.02 for the next 40%, and -13.73 for the bottom 50%. The top
1% was already a net mortgage lender in 1982; its position widened rather than
changing sign.

### A regime break

For the bottom 99%, the average mortgage contribution to active saving moves
from -6.36 points in 1998--2007 to -0.16 in 2008--2016, while broad consumer
credit moves only from -1.76 to -1.44. Mortgages therefore select the pre-2008
mechanism. The post-2008 consumer-credit residual is economically different
and should not be forced into the same model without a detailed category split.

### What this evidence does and does not show

The evidence establishes an accounting incidence:

$$
\text{rich ultimate mortgage claims rose while middle mortgage debt rose}.
$$

It does **not** establish the causal sequence

$$
\text{rich saving}
\Rightarrow
\text{financialization}
\Rightarrow
\text{cheaper credit}
\Rightarrow
\text{middle borrowing}.
$$

House prices, borrower demand, monetary policy, regulation, beliefs, and credit
supply are jointly determined. The implemented decomposition is motivating
evidence and a set of target moments for the proposed model.

## Core model

The minimum useful model has rich savers, middle-wealth potential borrowers,
financial intermediaries, and a government/guarantee sector. It needs to
separate **risk pooling** from **risk shifting**.

### Agents and timing

1. Rich households receive income and choose consumption and direct or
   intermediated claims. Their high saving supplies funds and creates demand
   for liquid or apparently safe assets.
2. Intermediaries choose funding, screening effort, retention/first-loss
   exposure, pool size, and security design. A financialization state
   $\phi_t$ summarizes the feasible intermediation technology.
3. Middle-wealth households choose housing, consumption, and mortgage debt
   given the loan rate and collateral constraint.
4. Aggregate and idiosyncratic mortgage shocks are realized. Losses are
   absorbed by borrower equity, intermediary capital, security holders, and
   explicit or implicit guarantees.

The scalar $\phi_t$ is a theoretical sufficient statistic, not a single
empirical series. It must be disciplined by separate observables: indirect
ownership, chain length, securitization share, pool/tranche structure,
originator retention, intermediary funding and capital, and government
guarantees.

### Mortgage risk and pooling

Let the per-dollar payoff on mortgage $i$ be

$$
R_{it}=\bar R_t-\eta_t-\varepsilon_{it},
$$

where $\eta_t$ is aggregate mortgage risk and $\varepsilon_{it}$ is an
idiosyncratic borrower shock, with

$$
\operatorname{Var}(\eta_t)=\sigma^2_{A,t},
\qquad
\operatorname{Var}(\varepsilon_{it})=\sigma^2_{I,t}.
$$

If financialization permits a pool of $N(\phi_t)$ conditionally independent
loans, its payoff variance is

$$
\operatorname{Var}(\bar R_{N,t})
=\sigma^2_{A,t}+\frac{\sigma^2_{I,t}}{N(\phi_t)}.
$$

Pooling diversifies idiosyncratic risk; it cannot eliminate the aggregate
housing/default shock. This invariant prevents the model from equating a
larger pool with a socially safer financial system.

### Loan pricing and the ambiguous effect of financialization

A reduced-form zero-profit loan spread consistent with the structural forces
is

$$
r^L_t-r^f_t
=c(\phi_t)
+\gamma_t\left(
\sigma^2_{A,t}+\frac{\sigma^2_{I,t}}{N(\phi_t)}
\right)
+\mu(\phi_t,e_t,k_t,g_t),
$$

where:

- $c(\phi_t)$ is the funding, origination, and intermediation cost;
- $\gamma_t$ prices retained risk;
- $e_t$ is screening effort;
- $k_t$ is intermediary loss-absorbing capital;
- $g_t$ is public or private guarantee protection; and
- $\mu(\cdot)$ is the agency, opacity, market-power, capital, and runnable-
  funding wedge.

Financialization lowers the spread if it reduces funding costs or
idiosyncratic risk enough. It can leave the spread unchanged, or increase
systemic fragility, if weak retention lowers screening, complexity raises
opacity, or capital migrates away from originators. The derivative
$\partial(r^L-r^f)/\partial\phi$ is therefore a model outcome rather than an
assumption.

### Borrower choice and the mapping to Figure 6

A middle household chooses consumption, housing, and debt:

$$
\max_{c_{0},c_{1},h,b}\;
u(c_0,h)+\beta\mathbb E[u(c_1)]
$$

subject to

$$
c_0+q_t h=y_0+b,
\qquad
c_1+(1+r^L_t)b=y_1+q_{t+1}h,
\qquad
b\leq\lambda(\phi_t,e_t)q_t h.
$$

Financialization can affect borrowing through both the price $r^L_t$ and the
approval/collateral limit $\lambda$. For group $g$, the measured mortgage
contribution to active saving is

$$
s^{L,m}_{gt}
=-
\frac{L^m_{gt}-(1-WD^m_{gt})L^m_{g,t-1}}
{Z^d_{gt}},
$$

where $WD^m_{gt}$ is the write-down rate and $Z^d_{gt}$ is personal plus
attributable corporate disposable income. This is the exact bridge from the
model's debt choice to MSS Figure 6.

### Saver choice and market clearing

Rich household $r$ allocates saving across direct primary assets and claims on
intermediaries. The portfolio problem can be represented as

$$
\max_{a^D_r,a^I_r}\;
\mathbb E[V(W'_r)]
-\frac{\gamma_r}{2}\operatorname{Var}(W'_r)
$$

subject to $a^D_r+a^I_r=S_r$ and the available security menu generated by
$\phi_t$. Loan-market clearing requires the mortgage liabilities originated to
equal the direct and intermediated claims held by all terminal sectors, net of
intermediary equity and retained exposure. This connects the quantity of rich
saving to loan prices only in equilibrium; an ownership identity alone is not
a supply equation.

## Extending MSS from claim ownership to loss incidence

Write the MSS direct ownership matrix as $[H_t,Q_t]$, where $H_t$ contains
direct terminal-owner shares and $Q_t$ intermediary cross-holdings. The
unveiled ownership operator is

$$
\Omega_t=(I-Q_t)^{-1}H_t.
$$

$\Omega_t$ allocates the **face value of claims**. Proportional claim ownership
does not imply proportional exposure to losses because capital buffers,
seniority, guarantees, and limited liability intervene between the primary
loan and the terminal owner.

Define, for state $\omega$:

- $\ell^0_t(\omega)$: a row vector of primary mortgage losses entering
  intermediary nodes;
- $P_t(\omega)$: a matrix whose $(i,j)$ entry is the share of a marginal loss
  at intermediary $i$ passed to intermediary $j$;
- $C_t(\omega)$: a matrix of direct marginal-loss shares passed from
  intermediaries to terminal owners, including government when guarantees are
  honored; and
- $a_t(\omega)$: the share absorbed by intermediary capital or other explicit
  buffers.

For a locally linear loss waterfall,

$$
\ell^O_t(\omega)
=\ell^0_t(\omega)
(I-P_t(\omega))^{-1}C_t(\omega)
$$

allocates total losses to terminal sectors. Row-level conservation requires

$$
P_t(\omega)\mathbf 1
+C_t(\omega)\mathbf 1
+a_t(\omega)=\mathbf 1.
$$

This is a separate operator, not a reinterpretation of $\Omega_t$. For large
shocks the waterfall is nonlinear because buffers are exhausted and seniority
switches which claim is marginal. The inverse is therefore a piecewise-linear
or local approximation; a full quantitative model must simulate the waterfall
state by state.

Three outputs should be kept distinct:

1. **nominal ownership:** who owns the face value, from $\Omega_t$;
2. **expected risk:** who bears ex ante variance or expected loss; and
3. **realized loss incidence:** who loses in a particular state, from the
   waterfall and guarantees.

## Model predictions and falsification

The model should generate predictions that distinguish mechanisms.

1. **Funding-liquidity channel.** When securitization is easier, mortgage
   approval and quantity should become less sensitive to originator deposit or
   capital conditions. If sensitivity does not change, the funding channel is
   weak.
2. **Risk-pooling channel.** Larger pools should reduce the price of
   idiosyncratic risk but not exposure to common house-price shocks. If spreads
   decline only when guarantees rise, pooling is not the sole mechanism.
3. **Agency channel.** Lower retention or longer chains should predict weaker
   screening and worse ex post performance conditional on observable borrower
   risk. If loan quality does not deteriorate, the moral-hazard wedge is less
   important.
4. **Distributional quantity channel.** Exposure to the intermediation shock
   should increase mortgage originations and make the mortgage contribution to
   middle-wealth saving more negative. A rise in balances without new
   originations or approvals would point instead to house-price or refinancing
   dynamics.
5. **Ownership-versus-risk wedge.** The top's ultimate mortgage claims may rise
   even if losses are initially absorbed by intermediary equity or government
   guarantees. If nominal and loss shares coincide, the extra risk operator
   adds little empirically.
6. **Regime dependence.** The mechanism should be strongest before 2008. A
   model that predicts the same mortgage-saving channel after 2008 conflicts
   with the implemented decomposition.

## Empirical and quantitative sequence

### Stage 0: finish the accounting bridge

1. Re-express mortgage and consumer-credit active-saving contributions using
   the exact Figure 6 group disposable-income denominator.
2. Retain the paper's percentile bins and verify that debt categories sum to
   total debt saving and that all asset classes recover the complete Figure 6
   rate.
3. Preserve the four-group full-inverse ownership decomposition as the
   same-vintage benchmark.

This stage measures the target moment; it does not identify the mechanism.

### Stage 1: measure financialization as a vector of mechanisms

Construct annual or loan-market measures of:

- MSS indirect ownership and intermediation-chain length;
- mortgage securitization and loan-sale shares;
- GSE versus private-label securitization;
- originator funding structure, liquidity, and capital;
- screening proxies, originator retention, and tranche subordination; and
- guarantee coverage and realized loss allocation.

Do not collapse these variables into one index before testing which channel
each one represents.

### Stage 2: estimate the credit-supply pass-through

The leading empirical design should exploit mortgage-market eligibility or
originator exposure rather than an aggregate time-series correlation. Two
candidate designs are:

1. **Conforming-loan eligibility.** Compare loans around the time-varying GSE
   conforming-loan limit and interact eligibility with originator funding
   constraints. Outcomes are approval, rate, loan amount, sale/securitization,
   and ex post performance. Manipulation of loan amount around the cutoff and
   nonrandom borrower sorting must be tested explicitly.
2. **Predetermined lender exposure.** Use lender exposure to the expansion of
   private-label securitization or secondary-market access, matched to local
   mortgage applications. The exclusion restriction is that pre-exposure
   affects borrower outcomes only through the credit-supply channel; lender
   specialization and local housing expectations are the main threats.

The reduced-form estimand is the effect of an intermediation-driven shift in
loan terms on mortgage borrowing. It is not automatically the effect of rich
saving.

### Stage 3: estimate and validate the structural model

Estimate or calibrate the model to jointly match:

- Figures 1, 6, and 8;
- the implemented mortgage liability, saving, and net-position moments;
- mortgage spreads, approvals, originations, and securitization shares;
- borrower defaults and loss severities; and
- intermediary funding, capital, charge-offs, and guarantee recoveries.

The quasi-experimental estimates discipline the elasticities of loan price and
quantity with respect to intermediation. Cross-sectional and time-series
moments discipline equilibrium quantities and the distribution of risk.

### Stage 4: unveil risk and run counterfactuals

For each historical network and simulated mortgage shock:

1. compute nominal ultimate ownership with $\Omega_t$;
2. allocate losses through capital, seniority, and guarantees;
3. report losses by wealth group, intermediary capital, government, and rest
   of world; and
4. verify state-by-state loss conservation.

The headline counterfactual holds 2007 household incomes, collateral, and
borrower fundamentals fixed but replaces the 2007 intermediation technology
and risk-bearing structure with its 1982 counterpart. It asks how much smaller
middle-wealth mortgage borrowing and the Figure 6 saving-rate decline would
have been. A fuller decomposition varies, in turn:

- the distribution of income and top saving;
- intermediation, pooling, and funding technology;
- house prices and collateral constraints; and
- screening, capital, and guarantees.

Because these forces interact, the final attribution should use a transparent
Shapley or all-order counterfactual decomposition rather than depend on one
arbitrary sequence of shocks.

## Dataset map

The project should start with public data and label any restricted-data stage
separately.

| Source | Unit, key, and useful coverage | Model object | Main limitation |
| --- | --- | --- | --- |
| MSS authors-kit DINA, Financial Accounts, and 2021 direct cells | Year; 1963--2016 in the available vintage | Figure 6 saving, Figure 8 ownership, mortgage and consumer-credit stocks/write-downs | Four broad wealth groups for the implemented extension; exact 2025 matrix cube unavailable |
| Public Financial Accounts/FWTW and DFA | Sector-instrument-year or wealth-group-quarter | Ownership network, intermediary balance sheets, macro wealth benchmark | Nominal claims do not identify contractual loss waterfalls |
| HMDA loan-level applications/originations | Application or loan, lender, geography, year; historical coverage must be harmonized | Approval, amount, borrower income, lender, purchaser/loan sale | No direct household wealth; fields and coverage change over time; public data are privacy-modified |
| Bank Call Reports | Bank-quarter | Funding mix, capital, liquidity, mortgage holdings, charge-offs | Limited view of nonbanks and off-balance-sheet exposures |
| FHFA conforming-loan limits and GSE activity | County-year or national year | Eligibility shock, guarantee/securitization regime | Loan amount can bunch endogenously around the threshold |
| Fannie Mae and Freddie Mac loan-performance data | Loan-month from roughly 1999/2000 onward, depending on dataset | Defaults, prepayments, recoveries, loss severity | Covers GSE-acquired/guaranteed loans, not the private-label universe; registration/terms apply |
| SCF and DFA | Household or wealth-group wave/quarter | Borrower wealth rank, debt composition, portfolio holdings | SCF is triennial and repeated cross-sectional; cannot directly link households to HMDA loans |
| FHFA/local house prices and housing-supply measures | Geography-quarter/year | Collateral, aggregate housing risk, local amplification | House prices are endogenous to credit supply |
| Agency and private-label MBS disclosures | Loan/pool/tranche-month where available | Pool size, subordination, retention, security cash flows | Historical private-label terms and owner identities may require commercial data |
| Consumer Credit Panel or servicing data | Consumer-loan-month | Balances, transitions, delinquency, default | Restricted access and no direct top-tail wealth measure |

The public minimum viable version combines the existing MSS/FWTW/DINA
pipeline with HMDA, Call Reports, conforming-loan limits, GSE performance data,
SCF/DFA, and house prices. Security-level private-label data improve the loss
waterfall but should not be assumed available in the course implementation.

## Data and accounting invariants

The implementation must verify:

1. **Ownership closure:** every direct ownership row sums to one before
   unveiling, subject only to explicitly reported unassigned shares.
2. **Category additivity:** mortgage plus consumer-credit stocks and flows
   recover the corresponding total household-debt object.
3. **Figure 6 closure:** income-weighted group saving equals aggregate national-
   account saving, and debt categories plus other assets recover total saving.
4. **Loan-market clearing:** funded mortgage claims equal mortgage liabilities
   after explicitly accounting for intermediary equity, retained claims, and
   unassigned sectors.
5. **Loss conservation:** in every simulated state, primary mortgage losses
   equal terminal-holder losses plus intermediary-capital absorption and
   government-guarantee transfers.
6. **Aggregate-risk preservation:** pooling may reduce idiosyncratic variance
   but cannot remove the common shock.
7. **Vintage separation:** 2021 authors-kit results, public current FWTW
   results, and the unavailable 2025 matrix are never silently combined.

## Identification and measurement safeguards

### Financialization is endogenous

More securitization may follow lower mortgage rates, safer borrowers, or
expected house-price growth rather than cause them. Figure 1 co-movement is
not an instrument. A credible design needs policy eligibility, predetermined
lender exposure, or another shock with explicit exclusion restrictions.

### Ex ante risk differs from ex post loss

Realized 2008 losses do not reveal agents' pre-crisis beliefs. The model should
use both ex ante pricing/ratings/retention moments and ex post default and loss
moments. Welfare conclusions depend on information available when contracts
were chosen.

### Wealth rank is partly an outcome of debt

Because net worth equals assets minus liabilities, current wealth rank can
mechanically sort high-debt households downward. Borrower results should be
reported using the paper's current net-wealth rank, gross-asset or focal-debt-
excluded rank, and age-specific or lagged wealth rank where possible.

### The debt instrument is not the expenditure purpose

A mortgage can finance a purchase, renovation, refinancing, or equity
extraction. The current macro decomposition identifies the balance-sheet
instrument, not the final use of funds. Loan purpose and cash-out refinancing
require richer loan-level or survey information.

### Stocks, flows, access, and intensity are different

Report participation/approval, conditional loan amount, aggregate stock,
write-down-adjusted active borrowing, defaults, and loss severity separately.
This distinguishes expanded access from larger balances among existing
borrowers.

## Novelty and relationship to the literature

### What is already well studied

The proposal should not claim the following as new:

- debt composition by wealth;
- the pre-2008 mortgage boom and home-equity extraction;
- securitization's effect on the sensitivity of lending to bank funding;
- mortgage-credit supply and housing amplification; or
- agency problems in originate-to-distribute chains.

[CBO's wealth report](https://www.cbo.gov/publication/60807) and
[Bartscher et al. (2025)](https://doi.org/10.1016/j.red.2025.101288) already
document distributional debt composition. Loutskina and Strahan show that
securitization weakened the link between bank financial condition and mortgage
supply. Justiniano, Primiceri, and Tambalotti model credit supply in the
housing boom. Mian and Sufi, and Mian, Sufi, and Matvos, connect disintermediation
and private-label securitization to mortgage expansion, default, and housing
speculation.

Nor is it safe to assume that securitization mechanically lowers mortgage
rates. Heuson, Passmore, and Sparks give conditions under which the observed
negative correlation runs from low rates to securitization. Segura and
Villacorta show theoretically that demand for safe assets can expand
securitization while increasing underlying loan risk through capital
reallocation and moral hazard.

### Candidate contribution

The more distinctive contribution is the intersection:

> integrate distributional saving rates, ultimate claim ownership, and
> state-contingent mortgage-loss incidence in one quantitative framework, then
> ask how the intermediation technology maps the saving glut of the rich into
> middle-wealth credit and who actually bears the risk.

This is closely tied to MSS but not already delivered by their accounting
operator. It also extends *Indebted Demand*: that paper models how inequality
and financial liberalization produce household debt and low natural rates,
whereas this proposal opens the intermediation block and disciplines it with
claim-network, loan-level, and loss-incidence data.

The novelty claim remains provisional until a systematic literature review
checks papers combining distributional saving, securitization networks, and
wealth-group loss incidence. The generic phrase “financialization caused more
debt” is too broad and too crowded to be the contribution.

### Closest references

- [Mian, Straub, and Sufi, *The Saving Glut of the Rich*](https://straub.scholars.harvard.edu/sites/g/files/omnuum7751/files/2025-07/MSS_SGR_July242025.pdf)
- [Mian, Straub, and Sufi, *Indebted Demand*](https://www.nber.org/papers/w26940)
- [Loutskina and Strahan, *Securitization and the Declining Impact of Bank Finance on Loan Supply*](https://www.nber.org/papers/w11983)
- [Justiniano, Primiceri, and Tambalotti, *Credit Supply and the Housing Boom*](https://www.nber.org/papers/w20874)
- [Mian and Sufi, *The Consequences of Mortgage Credit Expansion*](https://www.nber.org/papers/w13936)
- [Mian, Sufi, and Matvos, *Credit Supply and Housing Speculation*](https://www.nber.org/papers/w24823)
- [Heuson, Passmore, and Sparks, *Credit Scoring and Mortgage Securitization*](https://www.federalreserve.gov/econres/feds/credit-scoring-and-mortgage-securitization-do-they-lower-mortgage-rates.htm)
- [Segura and Villacorta, *The Paradox of Safe Asset Creation*](https://doi.org/10.1016/j.jet.2023.105640)
- [Gorton and Souleles, *Special Purpose Vehicles and Securitization*](https://www.nber.org/papers/w11190)

## Feasibility and fallback designs

| Claim or output | Feasibility | Honest label |
| --- | --- | --- |
| Mortgage versus consumer-credit accounting by four wealth groups, 1963--2016 | Implemented and verified | Motivating same-vintage evidence |
| Exact Figure 6 mortgage contribution using group income | High with current project files | Remaining measurement closure |
| Financialization moments from MSS/FWTW, HMDA, Call Reports, and GSE data | Moderate to high | Public-data empirical extension |
| Causal credit-supply effect using conforming eligibility or lender exposure | Moderate | Design requires manipulation/balance/exclusion tests |
| Structural counterfactual for middle borrowing and saving | Moderate | Quantitative mechanism, conditional on model |
| Complete state-contingent loss unveiling for agency and private-label MBS | Low to moderate | Likely requires security-level or commercial data |
| Welfare effect of financialization | Low in the course version | Requires beliefs, utility, housing supply, and policy incidence |

If detailed private-label waterfalls are unavailable, the minimum credible
extension is still sharper than debt composition alone: estimate how
securitization/funding access shifts mortgage approval and borrowing, calibrate
the pooling-versus-agency model, and bound ultimate losses under transparent
capital and guarantee scenarios.

## Relation to the other extension directions

- The broad menu remains in
  [`research_extension_idea_1.md`](research_extension_idea_1.md). Its business-
  ownership/retained-earnings branch is the strongest alternative for
  explaining the **origin** of top saving, but it uses the unveiling network
  less directly.
- The earlier detailed debt-composition design is now the empirical foundation
  inside this note, not the final novelty claim.
- The AI circular-financing idea in the
  [extension task record](../docs/project/tasks/extension-proposal.md) is more
  novel as an application but much less feasible because contract-level data
  are sparse and private.
- The wealth-rank and time-evolution cautions in
  [personal considerations](../docs/project/personal-considerations-saving-inequality.md)
  remain part of the empirical design.

## Source and implementation map

### Project evidence

- Authoritative target: [`MSS_SGR_July242025.pdf`](../MSS_SGR_July242025.pdf),
  especially Sections 2--4, Figures 1, 6, and 8, Table A2, Appendix C.4, and
  the conclusion.
- Figure 6 record:
  [`figure6-replication.md`](../docs/project/tasks/figure6-replication.md).
- Figure 8 record:
  [`figure8-replication.md`](../docs/project/tasks/figure8-replication.md).
- Implemented extension contract:
  [`debt-composition-extension-data.md`](../docs/data/debt-composition-extension-data.md).
- Existing implementation:
  [`build_debt_composition_extension.py`](../Code/scripts/build_debt_composition_extension.py),
  [`debt_composition_extension.py`](../Code/unveiling/debt_composition_extension.py),
  and [`figure8_2021_direct.py`](../Code/unveiling/figure8_2021_direct.py).
- Preliminary evidence deck:
  [`Presentation/7_debt_composition_extension`](../Presentation/7_debt_composition_extension/README.md).

### Public data documentation

- [CFPB/FFIEC HMDA data](https://www.consumerfinance.gov/data-research/hmda/)
- [Historical HMDA downloads](https://www.consumerfinance.gov/data-research/hmda/historic-data/)
- [FHFA conforming-loan limits](https://www.fhfa.gov/data/conforming-loan-limit)
- [Freddie Mac single-family loan-level dataset](https://www.freddiemac.com/research/datasets/sf-loanlevel-dataset)
- [Fannie Mae Data Dynamics and loan-performance data](https://capitalmarkets.fanniemae.com/tools-applications/data-dynamics)
- [Federal Reserve SCF](https://www.federalreserve.gov/econres/scfindex.htm)
- [Federal Reserve DFA](https://www.federalreserve.gov/releases/z1/dataviz/dfa/index.html)
- [Federal Reserve FWTW methodology](https://www.federalreserve.gov/econres/notes/feds-notes/from-whom-to-whom-relationships-in-the-financial-accounts-of-the-united-states-20230324.html)

## Recommended course-facing formulation

The concise proposal should make one claim and one boundary clear:

> **Claim to investigate:** financialization may have converted the rise in
> rich households' demand for financial claims into a larger and cheaper
> supply of mortgages, contributing to the pre-2008 fall in middle-wealth
> saving rates.
>
> **Boundary:** the current project establishes mortgage accounting incidence
> and ultimate nominal ownership, not causal credit supply or ultimate risk
> incidence. The extension proposes a model, new data, and a loss-unveiling
> operator to identify and quantify those missing links.
