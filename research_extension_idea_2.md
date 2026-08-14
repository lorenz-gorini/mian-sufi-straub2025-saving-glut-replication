# Research Extension 2: Debt Composition, Saving, and Ultimate Financing

## Purpose and status

This is the canonical note for the most feasible empirical branch of
[`research_extension_idea_1.md`](research_extension_idea_1.md). It links three
questions that must remain empirically distinct:

1. **Saving decomposition:** which liability categories account for the
   post-1980 evolution of active saving and saving rates at each part of the
   wealth distribution?
2. **Ultimate financing:** after financial intermediaries are unveiled, which
   owners finance each category of household debt?
3. **Mechanism:** conditional on the dominant category, did borrowing expand
   because of collateral values, credit supply, expenditure costs, liquidity
   needs, or another category-specific force?

The research logic is therefore

$$
\text{documented fact}
\rightarrow
\text{accounting decomposition}
\rightarrow
\text{ultimate financing}
\rightarrow
\text{causal mechanism}.
$$

Stage 1 now has a **verified preliminary implementation** for the four broad
wealth groups: home mortgages and consumer credit are separated through 2016,
their write-down-adjusted active-saving contributions are measured, and their
ultimate owners are unveiled. The result is descriptive, not causal. The exact
Figure 6 percentile saving-rate decomposition remains a next step. More
detailed splits into credit-card, vehicle, student, medical, and other debt
require additional household surveys and have shorter or non-comparable time
coverage.

## Why this is a useful extension—and what it cannot answer alone

Mian, Straub, and Sufi show three facts that motivate this extension:

1. Figure 6 shows that saving rates fell across most of the distribution while
   rising for the top 1% after the early 1980s;
2. Section 3.5 and Table A2 identify increased borrowing as the largest
   component of the saving decline below the top 1%; and
3. Figure 8 shows that, after unveiling intermediaries, the top 1% hold
   substantial net claims on debt owed elsewhere in the wealth distribution.

The paper stops one level short of the proposed decomposition. Table A1 and
Appendix C.4 distinguish home mortgages from broad consumer/nonmortgage credit
for allocation and write-down adjustments, but Table A2 reports a single debt
contribution and Figure 8 reports aggregate household-debt positions. A
mortgage, a credit-card balance, a student loan, and an unpaid medical bill are
all liabilities, yet they finance different objects and imply different
welfare and policy conclusions.

The key novelty distinction is between

$$
\text{why household debt rose}
\quad\text{and}\quad
\text{which debt categories generated the fall in saving}.
$$

Mian and Sufi's mortgage-credit research already provides a rich account of
housing collateral, securitization, credit supply, home-equity extraction, and
defaults. The extension should not redescribe that literature as a new generic
"financialization caused leverage" result. It should first quantify which
liabilities account for the saving-rate divergence documented in Figure 6.
Only then should it select a category-specific mechanism.

This extension addresses the **borrower and absorption side** of the saving
glut. It does not, by itself, identify why the rich chose to save a larger share
of their income. The top-side mechanisms in Extension 1—income growth,
business-equity ownership, retained corporate earnings, taxation, and
entrepreneurial wealth—remain a necessary complement. Nor does observing that
the rich ultimately own a claim prove that their additional saving caused the
loan to be originated: credit supply, credit demand, collateral values, and
asset prices are jointly determined in equilibrium.

## Economic objects and accounting design

Let:

- $g$ index household wealth groups;
- $k$ index debt categories;
- $t$ index years;
- $L_{gkt}\geq 0$ be the liability owed by group $g$ in category $k$;
- $A_{gkt}\geq 0$ be claims on category-$k$ household debt ultimately owned by
  group $g$ after unveiling;
- $Z^d_{gt}$ be personal plus attributable corporate disposable income of
  group $g$; and
- $NI_t$ be aggregate national income.

The category-specific net household-debt position is

$$
ND_{gkt}=A_{gkt}-L_{gkt}.
$$

Positive $ND_{gkt}$ means that the group is a net lender to other households in
that debt category; negative $ND_{gkt}$ means that it is a net borrower. The
direct extension of Figure 8 is

$$
\widetilde{ND}_{gkt}
=
\frac{ND_{gkt}}{NI_t}
-
\frac{ND_{gk,1982}}{NI_{1982}}.
$$

If the categories exhaust household debt, they must add back to the original
estimand:

$$
\sum_k ND_{gkt}=ND_{gt}.
$$

### Extending the unveiling operator by debt category

Write the direct ownership matrix, with ultimate-owner columns first, as
$[H_t,Q_t]$. Here $H_t$ contains direct ownership by ultimate owners and $Q_t$
contains intermediary cross-holdings. The unveiled ownership shares are

$$
\Omega_t=(I-Q_t)^{-1}H_t.
$$

For debt category $k$, let $p_t^k$ be its direct intermediary-holder share
vector and $\lambda_t^k$ its direct ultimate-owner share vector. The final
owner shares of category $k$ are

$$
u_t^k=p_t^k\Omega_t+\lambda_t^k,
$$

and dollar ownership is aggregate category debt times $u_t^k$. The network
operator is unchanged; only the primary-asset vector is separated by debt
category.

The relevant invariants are:

$$
\sum_{o\in\mathcal O} A_{okt}=L_{kt},
\qquad
\sum_{g\in\mathcal H} L_{gkt}=L_{kt},
\qquad
\sum_k ND_{gkt}=ND_{gt},
$$

where $\mathcal O$ includes household groups, governments, and the rest of the
world, while $\mathcal H$ contains only household wealth groups. Consequently,
net positions need not sum to zero across U.S. household groups alone: part of
their debt can be owned by nonhousehold ultimate owners.

### Contribution of each debt category to active saving

Stocks alone do not say how much a category contributed to annual saving. Let
$WD_{gkt}$ be the write-down rate and retain positive liability notation. Net
active borrowing is

$$
F^L_{gkt}=L_{gkt}-(1-WD_{gkt})L_{gk,t-1},
$$

so the category's contribution to active saving is

$$
\Theta^L_{gkt}=-F^L_{gkt}.
$$

This correction matters because a debt write-down reduces the liability stock
without requiring the borrower to save. The paper already constructs separate
write-down factors for home mortgages and consumer credit for the top 10% and
bottom 90%. A category decomposition should preserve that adjustment rather
than treating every fall in debt as repayment.

Let $\Theta^{FA}_{gt}$ and $\Theta^{RE}_{gt}$ denote active saving through
financial assets and real estate. If the liability categories exhaust household
debt, total active saving is

$$
\Theta_{gt}
=
\Theta^{FA}_{gt}
+
\Theta^{RE}_{gt}
+
\sum_k \Theta^L_{gkt}.
$$

The exact Figure 6 net saving rate and each debt category's contribution are

$$
s^N_{gt}=\frac{\Theta_{gt}}{Z^d_{gt}},
\qquad
s^{L,k}_{gt}=\frac{\Theta^L_{gkt}}{Z^d_{gt}}.
$$

For a post-1982 versus pre-1982 comparison, linearity gives

$$
\Delta s^N_g
=
\Delta s^{FA}_g
+
\Delta s^{RE}_g
+
\sum_k \Delta s^{L,k}_g,
$$

where $\Delta$ is the difference between the post- and pre-period mean annual
rates, measured in percentage points. This is the direct bridge to Figure 6:
it converts the statement that debt reduced saving into a quantified answer to
"which debt?" The annual implementation must also preserve the paper's
income-weighted closure,

$$
\sum_g s^N_{gt}Z^d_{gt}=\sum_g\Theta_{gt},
$$

and category contributions must sum to the existing total debt contribution
before any economic interpretation is attempted.

## Testable hypotheses

The hypotheses should be stated before inspecting the category-specific
results.

### H1: mortgage debt explains most of the upper-middle decline

For the 51st–90th wealth percentiles, the leading hypothesis is

$$
|\Delta s^{L,\mathrm{mortgage}}_g|
>
|\Delta s^{L,\mathrm{nonmortgage}}_g|.
$$

This would support a housing-collateral channel consistent with the paper's
finding that households borrowed against rising asset valuations. It would
not yet establish whether house prices caused credit growth or credit growth
raised house prices.

### H2: the bottom group has a larger nonmortgage share, not necessarily more debt

The bottom 50% may devote a larger **share** of its liabilities to unsecured or
nonhousing debt while holding fewer dollars of debt in aggregate because many
households are credit constrained or do not own homes. The analysis must report
both

$$
c_{gkt}=\frac{L_{gkt}}{\sum_j L_{gjt}}
\quad\text{and}\quad
q_{gkt}=\frac{L_{gkt}}{\sum_h L_{hkt}},
$$

where $c_{gkt}$ is category composition within a group and $q_{gkt}$ is the
group's share of all debt in that category. These answer different questions.

### H3: student debt is a life-cycle and education mechanism

Low net worth does not imply low education. Young households can have little
financial wealth and substantial student debt precisely because they attended
college and expect higher future income. Student debt should therefore be
analyzed within age or birth-cohort groups and by completed education. It
should not be interpreted as ordinary consumption debt. Existing
[CBO tabulations](https://www.cbo.gov/publication/60807) sharpen this point: in
2022, student loans were 64% of nonmortgage debt for the bottom wealth quarter,
but mortgages remained that group's largest total debt category; CBO explicitly
links the student-debt concentration to the group's younger average age. This
supports the age hypothesis, not the assumption that low-wealth households are
necessarily less educated.

### H4: medical debt is concentrated differently and is a recent-data question

Unpaid medical bills are plausibly more concentrated among low-wealth and
uninsured households, but they are not separately identified in our DINA or
FWTW files. They may also enter macro balance sheets differently from bank
credit. Medical debt should be treated as a separate recent household-welfare
exercise unless it can be reconciled to an explicit Financial Accounts
instrument and creditor sector.

### H5: ultimate financing differs across debt categories

Mortgages, student loans, and consumer credit pass through different
intermediaries and involve different government roles. The top 1% may
ultimately finance a larger share of some private-credit categories, while the
federal government may be especially important for student debt. This is the
part of the project for which the unveiling methodology creates the clearest
increment beyond a standard SCF debt-composition exercise.

## What our existing project data can identify

### 1. Authors-kit DINA and Financial Accounts: feasible now

The supplied fine DINA shares contain separate distributions for
owner-occupied mortgage debt and nonmortgage debt. The old direct-cell file
also preserves household home-mortgage and consumer-credit positions before
the authors' seven-round unveiling. Therefore, using the existing 1963–2016
pipeline, we can construct:

- mortgage-versus-nonmortgage active-borrowing and saving-rate contributions on
  the exact Figure 6 percentile bins;
- liabilities and active-borrowing contributions for the four Table A2 groups:
  top 1%, next 9%, next 40%, and bottom 50%;
- category-specific ultimate ownership for home mortgages and the broad
  consumer/nonmortgage block; and
- category-specific net positions whose sum reproduces total Figure 8.

The implemented extension now preserves those categories before returning the
aggregate Figure 8 result. It reuses the validated direct matrix, wealth-group
shares, Leontief solve, national-income denominator, and accounting tests in
[`docs/data/figure8-2021-direct-data.md`](docs/data/figure8-2021-direct-data.md).

This layer **cannot** distinguish credit-card, vehicle, student, medical, or
other personal debt within the nonmortgage block.

### 2. Public FWTW pipeline: category-specific creditor paths are feasible

The pinned public FWTW file distinguishes home mortgages, consumer credit,
depository-institution loans, other loans, and identified miscellaneous
claims. It can therefore reveal direct and unveiled owner paths for broad debt
instruments. The existing contract is
[`docs/data/figure8-public-fwtw-data.md`](docs/data/figure8-public-fwtw-data.md).

There is an important limitation: all nonmortgage liabilities are currently
allocated across wealth groups with the same DINA nonmortgage shares.
Separating public FWTW instruments without importing richer borrower-side
microdata would produce mechanically identical wealth distributions within
the nonmortgage block. That would be accounting, not new evidence about which
groups use credit cards, student loans, or vehicle loans.

### 3. Distributional Financial Accounts: a useful macro benchmark

The Federal Reserve's Distributional Financial Accounts (DFA) allocate
Financial Accounts totals using SCF distributional information and provide
quarterly wealth-group estimates beginning in 1989. They should be used as an
external benchmark for mortgage and consumer-credit liabilities, not silently
mixed into the 1963–2016 authors-vintage series. The DFA uses five wealth groups
and a different data vintage, so any comparison needs an explicit crosswalk.

## Additional microdata needed for the detailed composition

| Source | Useful coverage and categories | Best role | Main limitation |
| --- | --- | --- | --- |
| Survey of Consumer Finances (SCF) | Standardized public series from 1989–2022; net worth, mortgages/HELOCs, other residential debt, credit-card balances, education loans, vehicle loans, other installment loans, and other debt | Primary detailed wealth-by-debt composition and top-tail measurement | Triennial repeated cross-sections; public geography is insufficient for many causal designs; requires five implicates and replicate weights |
| Panel Study of Income Dynamics (PSID) | Wealth components since 1984 and active-saving questions in selected waves; true household panel | Life-cycle transitions, within-household leverage changes, and saving flows | Early nonmortgage debt bundles credit cards, student loans, medical bills, and personal loans; weak coverage of the extreme upper tail |
| Survey of Income and Program Participation (SIPP) | Modern public files identify housing, vehicle, credit-card, education, medical, and other debt alongside assets and demographics | Recent medical-debt and unsecured-debt heterogeneity | Modern redesign offers only a short window for the post-1980 question; comparability with older panels must be audited |
| Financial Accounts Z.1 and G.19 | Aggregate mortgage and consumer-credit stocks; memo categories include revolving, vehicle, student, and other consumer credit | Macro totals and reconciliation targets | The detailed borrower purpose is generally not cross-classified with both wealth group and ultimate holder; student-loan memo series begins only in 2006 |
| Consumer Credit Panel or administrative credit data | Mortgage, HELOC, auto, student, and credit-card balances with geography and delinquency | Credit-supply shocks, defaults, and local exposure | No direct wealth measure; access and disclosure restrictions may bind |

The official SCF balance-sheet definitions use `MRTHEL`, `RESDBT`, `CCBAL`,
`EDN_INST`, `VEH_INST`, `OTH_INST`, `ODEBT`, `DEBT`, and `NETWORTH`. The
analysis must respect the SCF's multiple imputations, sample weights, and
replicate weights. The SIPP's public variables include household amounts for
credit-card (`THDEBT_CC`), education (`THDEBT_ED`), home (`THDEBT_HOME`),
vehicle, other, and total secured/unsecured debt, while medical bills enter
the unsecured-debt construction through `TMED_AMT`.

## Required measurement safeguards

### Debt mechanically affects wealth rank

Because net worth equals assets minus debt, additional borrowing can move a
household down the wealth distribution mechanically. A regression of debt on
current net-wealth rank can therefore partly sort on the outcome. Every result
should show at least three classifications:

1. the paper's current net-wealth rank, for comparability;
2. gross-asset rank or net worth excluding the focal debt category, to reduce
   mechanical sorting; and
3. age-specific or birth-cohort wealth rank, to separate life-cycle position
   from persistent low wealth.

Where panel data permit it, lagged wealth rank is preferable.

### Do not divide by near-zero net worth

Debt-to-net-worth ratios explode or change sign for households close to zero or
with negative net worth. Report category shares, dollars per household,
debt-to-income, and debt-to-gross-assets. Use debt-to-net-worth only for groups
whose denominator is economically meaningful, and report the share with
nonpositive net worth separately.

### Separate stocks, flows, participation, and intensity

For every debt category report:

- the fraction of households holding the debt;
- the mean and median conditional balance;
- the unconditional mean balance;
- the group's share of the aggregate category stock; and
- the write-down-adjusted change in debt contributing to active saving.

This separates an extensive-margin expansion in access from larger balances
among existing borrowers.

### Separate the debt instrument from the expenditure it financed

- A mortgage or HELOC is an instrument; it may finance a house purchase,
  renovation, consumption, education, or another use through equity extraction.
- Vehicle debt finances a durable good.
- Student debt finances human capital, although completion risk matters.
- Credit-card balances can finance consumption, medical bills, or short-term
  liquidity.
- Medical debt may be involuntary and may initially be an unpaid bill rather
  than a conventional loan; it can later migrate to collections, a card, or a
  personal loan.

Combining them under the label "consumption debt" would erase the mechanism the
extension is intended to identify. Stage 1 identifies broad balance-sheet
**instruments**, not their ultimate expenditure purposes. Purpose requires
richer transaction, survey, or loan-origination data and should be presented as
a second research layer.

## Proposed empirical sequence

### Stage 1: two-category accounting extension using existing files — broad-group evidence implemented

1. Hold both validated baselines fixed: the exact-method Figure 6 active-saving
   pipeline and the 2021-direct/full-Leontief Figure 8 route.
2. Preserve separate home-mortgage and consumer/nonmortgage liabilities on the
   exact Figure 6 percentile bins and the four broad wealth groups.
3. Apply the paper's category- and group-specific write-down adjustments and
   construct $\Theta^L_{gkt}$ and $s^{L,k}_{gt}$.
4. Decompose the pre/post Figure 6 saving-rate change and the Table A2 debt
   contribution into mortgage and nonmortgage components, then trace the
   annual or trailing-five-year contribution of each category through 2016.
5. Return separate mortgage and consumer/nonmortgage primary-asset vectors
   before Figure 8 aggregation, unveil each vector, and construct $A_{gkt}$,
   $L_{gkt}$, $ND_{gkt}$, and the 1982-relative national-income ratios.
6. Verify annual asset, income, debt-stock, saving-flow, and category-to-total
   closure before comparing the component sums with the existing Figure 6,
   Table A2, and Figure 8 outputs.

**First deliverables:** one Figure 6 debt-contribution time-evolution panel,
one stacked Figure 8 decomposition, one period table extending Table A2, and
one accounting-diagnostics file. This is the minimum credible course extension
and has the lowest data cost.

#### Preliminary broad-group findings

From 1982 to 2007, home-mortgage liabilities increased by 23.63 percentage
points of national income for the next 40% and 13.85 points for the bottom
50%, compared with 4.50 points for the top 1%. Consumer-credit increases were
2.92, 4.04, and 0.00 points, respectively. During 1998--2007, mortgage
borrowing contributed -3.09 percentage points per year to active saving for
the next 40% and -2.28 points for the bottom 50%, compared with -0.43 points
for the top 1%.

After intermediaries are unveiled, the 1982--2007 mortgage net-position change
is +8.69 points for the top 1%, -19.02 points for the next 40%, and -13.73
points for the bottom 50%. Mortgage plus consumer-credit assets, liabilities,
and net positions reproduce the existing aggregate route with a maximum
additivity error of $9.31\times10^{-10}$ million.

These findings support H1 and motivate the mortgage branch of Stage 4. They do
not show that rich saving caused mortgage origination, that credit caused house
prices, or that the borrowing was welfare-reducing. The remaining Stage 1 task
is the exact Figure 6 percentile saving-rate decomposition and time-evolution
panel.

Generated evidence and its schema are documented in
[`docs/data/debt-composition-extension-data.md`](docs/data/debt-composition-extension-data.md).
The compact editable deck is documented in
[`Presentation/7_debt_composition_extension/README.md`](Presentation/7_debt_composition_extension/README.md).

### Stage 2: detailed borrower-side composition with the SCF

1. Harmonize 1989–2022 SCF summary variables in constant dollars.
2. Reproduce the paper's wealth groups and add bottom-quartile detail where
   sample sizes permit.
3. Estimate mortgage, HELOC, credit-card, student, vehicle, installment, and
   other-debt profiles by wealth group.
4. Repeat the profiles within age groups and using gross-asset or
   focal-debt-excluded ranks.
5. Decompose changes into participation and conditional balances.
6. Reconcile weighted category totals to Financial Accounts totals and explain
   residual concept differences.

This stage provides the detailed facts, but by itself remains descriptive.

### Stage 3: join borrower detail to ultimate financing

Use the SCF or DFA to estimate borrower shares for categories that the DINA
files aggregate, and use Financial Accounts/FWTW information to estimate
direct holders. Three cases must be labelled separately:

1. **identified:** a category-specific direct holder matrix and borrower split
   are both observed;
2. **calibrated:** an aggregate FWTW instrument is split using external
   category totals or survey shares; and
3. **bounded:** holder-by-category cells are unavailable, so report ranges
   under transparent allocation scenarios rather than a false point estimate.

The resulting output would answer not only who owes each debt, but who
ultimately owns it through deposits, funds, pensions, insurers, banks, and
government entities.

### Stage 4: choose one causal mechanism

The descriptive result should determine the causal branch:

- If mortgages dominate, study collateral and credit supply using a credible
  geographic or policy shock. Candidate designs include banking-deregulation
  timing, exposure to securitization, or mortgage-market eligibility rules,
  but each requires data and exclusion assumptions not available in the
  current public SCF files.
- If student debt dominates a relevant cohort, use policy-induced changes in
  federal loan eligibility or limits and follow education, debt, and saving by
  cohort.
- If medical debt matters, use insurance-coverage or medical-billing reforms
  in SIPP-style data; this would explain a recent low-wealth channel rather
  than the full post-1980 break.
- If revolving credit matters, investigate credit-card supply or usury/banking
  reforms with administrative balances and delinquency outcomes.

Do not impose a universal mechanism in which financialization raises credit
and therefore raises housing, education, and medical prices in the same way.
Housing collateral, federal student lending, revolving credit, and medical
billing have different institutions and supply elasticities. The decomposition
determines which mechanism deserves a separate identification design.

Do not estimate a single aggregate time-series regression of saving on credit
and call it causal. Common trends in inequality, interest rates, demographics,
house prices, and regulation would make that coefficient uninterpretable.

## Novelty boundary

Debt composition by wealth is not itself a new fact. The
[CBO](https://www.cbo.gov/publication/60807) already reports detailed SCF-based
debt composition by wealth group for 1989–2022, and
[Bartscher, Kuhn, Schularick, and Steins (2025)](https://doi.org/10.1016/j.red.2025.101288)
use SCF+ and PSID data to study the distribution of U.S. household debt since
1950, emphasizing mortgage debt and home-equity extraction.

Nor would a finding that mortgage borrowing rose among middle-wealth
households be novel on its own. Existing work by Mian and Sufi studies mortgage
credit expansion, securitization, housing speculation, home-equity extraction,
and the resulting defaults and spending dynamics. The proposed analysis uses
that literature to interpret a mortgage result; it does not claim to discover
the housing-credit channel.

The potential contribution is narrower and more closely tied to Mian, Straub,
and Sufi:

> connect debt-instrument-specific borrower incidence to the Figure 6 saving-
> rate divergence and the Figure 8 unveiling network, thereby measuring each
> category's active-saving contribution and ultimate financing across wealth
> groups.

That intersection appears more distinctive than another descriptive chart of
debt composition, but a systematic literature review is still required before
claiming novelty.

## Policy interpretation

The policy conclusion depends on the category and causal mechanism.

| Dominant channel | Relevant policy margin | Why the sign is ambiguous |
| --- | --- | --- |
| Mortgage/collateral | Loan-to-value and debt-to-income rules, securitization, mortgage subsidies, housing supply | Credit can expand homeownership and consumption smoothing, but can also capitalize into house prices and increase fragility |
| Credit cards/unsecured credit | Underwriting, disclosure, fees, interest-rate rules, bankruptcy and collections | Liquidity can insure shocks, but expensive revolving balances can amplify distress |
| Student loans | Tuition and grant policy, loan limits, income-contingent repayment, completion support | Debt can finance productive human capital, but weak completion or high tuition can leave borrowers with low wealth and repayment burdens |
| Medical debt | Insurance coverage, cost sharing, billing and collection rules | It may reflect uninsured health shocks rather than voluntary intertemporal substitution |

No form of debt should be treated as intrinsically harmful. Welfare analysis
requires the marginal use of funds, borrowing terms, repayment risk, price
effects in inelastic-supply markets, and the counterfactual without credit.

## Relation to the other extension directions

- This note operationalizes **Priority 1** and empirical steps 2–4 in
  [`research_extension_idea_1.md`](research_extension_idea_1.md):
  financialization, credit supply, and the fall in middle-class saving.
- The **business ownership and corporate saving** branch in Extension 1 is the
  complementary supply-side project explaining why saving may originate at
  the top.
- The **risk-pooling** branch becomes testable only after category-specific
  holder paths are measured and combined with spreads, defaults, or loss data.
  Ownership unveiling alone does not show that intermediation reduced risk.
- The AI circular-financing proposal in
  [`docs/project/tasks/extension-proposal.md`](docs/project/tasks/extension-proposal.md)
  is a more novel transplant of the operator, but its contract-level data are
  much less available. The household-debt extension is the lower-data-cost and
  more directly paper-linked candidate.
- The measurement cautions about wealth levels, age, and repeated
  cross-sections build directly on
  [`docs/project/personal-considerations-saving-inequality.md`](docs/project/personal-considerations-saving-inequality.md).

## Feasibility verdict

| Claim | Feasibility | Honest label |
| --- | --- | --- |
| Mortgage versus nonmortgage liabilities by wealth group, 1963–2016 | High with current files | Implementable long-run accounting extension |
| Mortgage versus broad consumer-debt ultimate ownership by wealth group | High with a modest extension of the validated network code | Implementable category-specific unveiling |
| Credit-card, vehicle, and student debt by wealth group, 1989–2022 | High after adding public SCF | Descriptive microdata extension |
| Medical debt by wealth group | Moderate using recent SIPP | Recent-period auxiliary analysis |
| Category-specific ultimate owners for every detailed loan purpose | Partial | Identified, calibrated, or bounded category by category |
| Financial innovation caused rich saving or middle-class borrowing | Low with current files | Requires a separate causal design |

The recommended first proposal is therefore:

> Decompose the debt contribution to Figure 6 and Table A2 into mortgages and
> nonmortgage credit, showing which category accounts for the change in saving
> rates across the wealth distribution and how its importance evolves over
> time. Extend Figure 8 by tracing the ultimate owners of each broad claim class
> through the financial network. Then use the SCF to determine whether the
> nonmortgage component reflects credit-card, vehicle, student, or other debt
> and to separate age and education composition. Treat medical debt as a recent
> SIPP extension and reserve causal claims for a second stage tailored to the
> dominant debt category.

## Source and implementation map

### Project sources

- Target paper: [`MSS_SGR_July242025.pdf`](MSS_SGR_July242025.pdf), especially
  Sections 3.1, 3.4–3.5, and 4.1–4.2; Figures 6 and 8; Table A1; Table A2;
  and Appendix C.4.
- Figure 6 research record:
  [`docs/project/tasks/figure6-replication.md`](docs/project/tasks/figure6-replication.md).
- Figure 8 research record:
  [`docs/project/tasks/figure8-replication.md`](docs/project/tasks/figure8-replication.md).
- Old-vintage direct-cell contract:
  [`docs/data/figure8-2021-direct-data.md`](docs/data/figure8-2021-direct-data.md).
- Public-FWTW contract:
  [`docs/data/figure8-public-fwtw-data.md`](docs/data/figure8-public-fwtw-data.md).
- Existing baselines: `Code/unveiling/figure6_authors.py`,
  `Code/unveiling/figure8_2021_direct.py`, and
  `Code/unveiling/figure8_public_fwtw.py`.

### External data and literature

- [Federal Reserve SCF data and historical surveys](https://www.federalreserve.gov/econres/scfindex.htm)
- [SCF asset and debt variable map](https://www.federalreserve.gov/econres/files/Networth%20Flowchart.pdf)
- [Federal Reserve Distributional Financial Accounts](https://www.federalreserve.gov/releases/z1/dataviz/dfa/index.html)
- [Federal Reserve FWTW methodology](https://www.federalreserve.gov/econres/notes/feds-notes/from-whom-to-whom-relationships-in-the-financial-accounts-of-the-united-states-20230324.html)
- [Financial Accounts consumer-credit definitions and memo items](https://www.federalreserve.gov/releases/z1/current/html/F4_3_s.htm)
- [Census SIPP datasets](https://www.census.gov/programs-surveys/sipp/data/datasets.html)
- [SIPP public variable dictionary](https://api.census.gov/data/2022/sipp/variables.html)
- [PSID assessment of asset and liability data](https://psidonline.isr.umich.edu/Guide/Quality/AssessingAssetData.pdf)
- [CBO, *Trends in the Distribution of Family Wealth, 1989 to 2022*](https://www.cbo.gov/publication/60807)
- [Bartscher et al. (2025), *The Distribution of Household Debt in the United States, 1950–2022*](https://doi.org/10.1016/j.red.2025.101288)
- [Mian and Sufi, *The Consequences of Mortgage Credit Expansion*](https://www.nber.org/papers/w13936)
- [Mian and Sufi, *House Prices, Home Equity-Based Borrowing, and the U.S. Household Leverage Crisis*](https://www.nber.org/papers/w15283)
- [Mian, Straub, and Sufi, *Indebted Demand*](https://www.nber.org/papers/w26940)
- [Black et al., *Taking It to the Limit: Effects of Increased Student Loan Availability*](https://www.nber.org/papers/w27658)
- [CFPB, *Medical Debt Burden in the United States*](https://files.consumerfinance.gov/f/documents/cfpb_medical-debt-burden-in-the-united-states_report_2022-03.pdf)
