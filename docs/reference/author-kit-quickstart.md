# February 2021 Author Kit: Quickstart and 2025 Reuse Guide

## Purpose and evidence status

Use this note for a first, token-efficient read of
`MSS2021Febreplicationkit/`. It answers four questions:

1. what the old Stata pipeline computes;
2. how its principal datasets are prepared;
3. which transformations remain part of the July 2025 methodology; and
4. which old outputs are benchmarks or proxies rather than valid 2025 inputs.

The package accompanies the February 2021 revision of *The Saving Glut of the
Rich and the Rise in Household Debt*. It is an exact historical benchmark for
that revision, not an exact replication package for the heavily revised July
25, 2025 paper. The old sample generally ends in 2016; the target ends in 2019.

This is a routing document. Use the [full package map](author-kit-map.md) for
code spans and the complete folder inventory, the
[data dictionary](../data/author-kit-data-map.md) for source provenance, and
the [output crosswalk](author-output-crosswalk.md) for old paper exhibits.

The current folder was executed and its generated files replaced during the
user-authorized 2026-08-09 validation. Its master also contains portability
and dependency-bootstrap edits. Treat it as a now-frozen, validated working
copy rather than a pristine download; see the
[benchmark record](../project/tasks/author-data-benchmark.md). Do not run or
edit it further in place.

## Pipeline in one screen

```text
BEA NIPA + DINA income + SCF/PSID/CEX/Fisher robustness inputs
    -> build_nipa_saving_data.do
    -> NIPA.dta, YconsshareSCF.dta, YinequalityNIPAanalysis.dta

Financial Accounts + CRSP support
    -> seven-round household/government/mortgage-debt unveiling
    -> Yunveilhhd.dta, Yunveilgovd.dta, Yunveilmtgd.dta -> Yunveil.dta

DINA/DFA/SZZ household shares + Yunveil.dta + Financial Accounts
    -> remainder of build_fa_unveiling_data.do
    -> YinequalityFAanalysis.dta

YinequalityFAanalysis.dta + Ywealthreturns.dta + NIPA private saving
    -> build_wealth_saving_data.do
    -> YwealthFOF.dta -> Ysavingwealth.dta

Restricted/prepared state inputs + national outputs
    -> build_state_wealth_data.do
    -> SYsavingwealth.dta, SYcontrols.dta

final files -> mss_analysis.do -> output/*.eps and output/*.tex
```

The master runs those five scripts in that order. The state branch belongs to
the old paper and is not part of the selected 2025 Figures 1, 5, or 8.

## Prepared-file contracts

All listed files are wide Stata files with a unique annual `year` key. Dollar
balance-sheet quantities are current-dollar stocks unless a variable is
explicitly a flow, share, return, or ratio to national income.

| Prepared file | Coverage in the validated run | Economic object | Proper use |
| --- | --- | --- | --- |
| `data/PSZusdina/Yszshares.dta` | 1962-2016 | DINA wealth-cohort shares by asset/liability class | Reusable distributional shares over the common vintage, subject to group and mapping checks |
| `data/finalfiles/YinequalityNIPAanalysis.dta` | 1945-2016 | NIPA flows, national income, and income-minus-consumption alternatives | Aggregate denominators and closure; consumption measures are robustness, not the 2025 Figure 5 baseline |
| `data/finalfiles/Yunveil.dta` | 1945-2019 | Old seven-round allocations for household, government, and mortgage debt | Historical-method benchmark only; not a 2025 unveiled matrix |
| `data/finalfiles/YinequalityFAanalysis.dta` | 1960-2016 | Old unveiled debt and its allocation across household groups | Old Figure 7/Table 7 benchmark or explicitly labelled proxy |
| `data/finalfiles/Ywealthreturns.dta` | 1959-2019 | Housing, debt-write-down, and supporting valuation inputs | Supplied downstream input; not fully reconstructible from public files in the kit |
| `data/finalfiles/YwealthFOF.dta` | 1960-2016 | B.101 balance-sheet categories allocated to wealth cohorts | Strong intermediate for old-input reconstruction of 2025 Figure 5 |
| `data/finalfiles/Ysavingwealth.dta` | 1963-2016 | Active saving, wealth changes, and valuation effects by cohort and asset | Fast benchmark for the 2025 Figure 5 definition over the common sample |

Starting from a final file reproduces or transforms an authors' prepared
object. It is not an independent upstream reconstruction. Move upstream only
when the selected result requires understanding or changing that preparation.

## What the code measures

### 1. National accounts and aggregate saving

The NIPA build imports and reshapes BEA tables, then constructs national income
as

\[
NI_t=GDP_t+ROW_t-\text{statistical discrepancy}_t-\delta_t,
\]

where $ROW_t$ is net income and transfers received from abroad and
$\delta_t$ is consumption of fixed capital. It also checks the expenditure-
and income-side representations of this identity. Aggregate private saving
used to close the wealth method is personal saving plus business saving.

`build_nipa_saving_data.do` also constructs several income-minus-consumption
measures using SCF, PSID, CEX, Fisher, CBO, and DINA inputs. Those series were
important robustness and presentation alternatives in the old paper. The July
2025 Figure 5 baseline is instead the wealth-based method below.

### 2. DINA shares allocate macro totals to wealth cohorts

The DINA microfile does not identify bilateral financial counterparties. For
asset class $j$, wealth group $g$, and year $t$, the code estimates

\[
\omega_{gjt}
=
\frac{\sum_i w_{it}\mathbf 1\{i\in g\}x_{ijt}}
     {\sum_i w_{it}x_{ijt}},
\qquad
W_{gjt}=\omega_{gjt}W^{FA}_{jt}.
\]

Here $x_{ijt}$ is a DINA asset or liability amount, $w_{it}$ is the tax
record weight, and $W^{FA}_{jt}$ is the corresponding Financial Accounts
aggregate. Thus DINA identifies the distribution and the Financial Accounts
identify the total.

The old baseline sorts on `wealth_ptile` and constructs top 1%, next 9%, and
bottom 90% groups. It adjusts debt signs before collapsing, calculates a
separate share for each asset class, and linearly interpolates the missing 1963
and 1965 shares from adjacent years. For every year and category, group shares
should sum to one. Bottom 99% is next 9% plus bottom 90%.

### 3. Wealth changes are split into saving and valuation

For group $g$, asset or liability $j$, and year $t$, both versions use
the accounting object

\[
\Theta_{gjt}=W_{gjt}-(1+\pi_{gjt})W_{gj,t-1},
\qquad
\Theta_{gt}=\sum_j\Theta_{gjt}.
\]

The old code implements the July 2025 paper's Appendix Table A1 mapping almost
line for line:

- B.101 totals are split with DINA asset-specific shares;
- owner-occupied housing inflation uses the JST repeat-sales index;
- fixed-income asset inflation is zero under the Financial Accounts convention;
- mortgage and consumer-credit write-downs enter as borrower valuation gains;
- equity-like categories receive one residual price-inflation factor; and
- that residual is chosen so total cohort saving equals personal plus business
  saving in NIPA.

The maintained invariants are

\[
\Delta W_{gjt}=\Theta_{gjt}+\pi_{gjt}W_{gj,t-1}
\quad\text{and}\quad
\sum_g\Theta_{gt}=S^p_t+S^\pi_t.
\]

This is the strongest old-to-new preprocessing continuity in the package. The
important limitations are the 2016 endpoint, revised source vintages, group
detail, and the fact that `Ywealthreturns.dta` contains prepared valuation
inputs whose private upstream sources are not all supplied.

### 4. The old unveiling is debt-specific and round based

`build_fa_unveiling_data.do` separately passes household debt, government debt,
and mortgage debt through seven named layers of intermediation. Each layer
uses instrument-specific proportionality factors, net-issuance adjustments,
special sector rules, and residual buckets. `test1` through `test7` check that
the debt stock is conserved as it is reallocated.

After aggregate household debt has been unveiled into the asset vehicles held
by households, the code assigns each vehicle to DINA groups using the matching
asset-class share. It separately allocates debt owed by each group using DINA
debt shares. In the old files, `a_hh1_hhdSZ` is household debt held as an asset
by the top 1% under DINA shares, while `d_hh1_hhdSZ` is debt owed by that group.

The economic net-debt position is

\[
ND_{g,t}=A^D_{g,t}-D_{g,t},
\]

positive for a net lender and negative for a net borrower. The old Stata file
stores debt liabilities with a negative sign in parts of the build, so
`mss_analysis.do` reverses the sign before constructing the plotted stock.

The July 2025 paper instead constructs one 27-sector direct-ownership matrix
from 34 instrument matrices, completes missing cells using known margins and
balancing rules, applies a Leontief-style infinite-path solve, maps the result
to eight primary assets, and repeats the solve after splitting the household
owner by wealth cohort. See the
[method note](../methods/leontief-unveiling.md) for the equations and exact
comparison. `Yunveil.dta` is therefore not a drop-in input for the 2025
operator.

## Reuse decisions for a 2025 reconstruction

| Layer | Relationship to July 2025 | Reuse decision |
| --- | --- | --- |
| NIPA definitions and private-saving closure | Same national-account logic; older data vintage | Reuse over 1963-2016, then update source tables for 2017-2019 and test identities again |
| Adjusted DINA wealth shares | Same broad DINA bridge, pension correction, and top-end fixed-income-return concern | Reuse prepared shares for the old-vintage benchmark; recollapse microdata when different percentile groups are required |
| B.101-to-DINA asset mapping | Old formulas match the 2025 Appendix Table A1 closely | Reuse for Figure 5, with explicit variable mapping and unit/sign tests |
| Housing, fixed-income, debt, and residual-equity valuation logic | Same core accounting method | Reuse conceptually; treat supplied private-source components as benchmark inputs, not independently rebuilt data |
| Wide Financial Accounts panel | Contains many required old-vintage series but not the completed 34 instrument matrices | Reuse selected source series only; reconstruct matrices rather than inferring them from old unveiled outputs |
| Seven-round unveiled debt outputs | Conceptual precursor with different empirical rules and scope | Do not use as the 2025 Ω or primary-asset matrix; use only as a historical benchmark or labelled proxy |
| DINA allocation of unveiled debt | Same distributional idea, applied at a different stage of the operator | Reuse the group shares, not the already allocated debt result, for a genuine 2025-method build |
| Old plots and tables | Different figures, smoothing, groups, and endpoints | Use only for exact February 2021 validation and version-aware comparison |

## Selected-figure implications

These are feasibility classifications, not claims that the corresponding
reconstructions have already been completed and verified.

| July 2025 target | What is usable from the old kit | First unsupported or changed step | Correct label |
| --- | --- | --- | --- |
| Figure 1: assets behind the intermediation veil | `fof/LQpanel_2019Q1.dta`, raw CRSP support, preserved national income; old final cells only for validation/denominator proxy | Completed 27-sector/34-instrument matrices, revised corporate-equity extension, and exact denominator are absent | Verified old-input reconstruction through 2016; bond cells rebuilt from the Q4 panel; not exact 2025 |
| Figure 5: top 1% versus bottom 99% saving | `YwealthFOF.dta`, `Ywealthreturns.dta`, `Ysavingwealth.dta`, and NIPA closure | Extend to 2019; rebuild next-40/bottom-50 detail; apply trailing 10-year mean and subtract the 1982 level | High-feasibility old-input reconstruction through 2016, still to be validated |
| Figure 8: net household-debt stock by wealth group | DINA shares, group liabilities, and old `a_hh*_hhdSZ`/`d_hh*_hhdSZ` series | The full augmented 2025 matrix and primary-asset solve cannot be recovered from the lossy old unveiled totals | Exact old Figure 7 benchmark or 2021-method proxy under 2025 plotting conventions |
| Figure 9: net household financing flows | Annual changes in the Figure 8 proxy components | Inherits the Figure 8 operator gap; 10-year moving-average flow and 2019 extension must be rebuilt | Extension proxy unless the Figure 8 matrix gap is resolved |

For Figure 5, the 2025 display transformation is not the old five-year-bin
graph. Construct annual top-1 and bottom-99 saving divided by contemporaneous
national income, take the trailing 10-year average (so the first point is 1972
for 1963-1972), and subtract each series' 1982 value. For Figure 8, normalize
the net-debt stock by national income and subtract its 1982 level.

## Variable-name decoder

The names are terse but systematic enough for navigation:

- `a_..._hhd` / `a_..._govd`: household or government debt held as an asset;
- `d_..._hhd`: household debt owed; check the sign before using it;
- `SZ`: DINA/PSZ distributional allocation in the Financial Accounts build;
- no `SZ` on old group debt variables: commonly the DFA allocation;
- group suffix `1`, `9`, `90`, or `10`: top 1%, next 9%, bottom 90%, or top 10%;
- `ha...`, `hl...`, `hnetworth...`: cohort asset, liability, and net-worth levels;
- `saving_...2NI`: active saving divided by national income;
- `D...2NI` and `V...2NI`: wealth change and valuation component divided by
  national income;
- `DFA`, `PSZ`, and `c11`-`c20`: alternative distribution/capitalization
  variants rather than baseline variables.

Variable names are navigation hints, not definitions. Confirm labels and the
generating expression before using a series.

## Efficient lookup protocol for future agents

1. Start here and identify the paper version and economic object.
2. For an old exhibit, use the [output crosswalk](author-output-crosswalk.md),
   then jump to its marker in `code/mss_analysis.do`.
3. Record the final file and variables read by that block.
4. Search backward for the exact `save` and generating expressions in only the
   responsible builder. Do not read the 8,900-line Financial Accounts build
   linearly.
5. Inspect only required columns and metadata. The data tree is about 45 GB;
   the large DINA files should not be loaded merely to answer a figure question.
6. Before reusing an old object for 2025, check period, group, unit, sign,
   normalization, smoothing, matrix stage, and source vintage.
7. Classify the result as an exact 2021 benchmark, an old-input reconstruction
   of a 2025 definition, a proxy, or infeasible with supplied data.

Useful routes:

- dataset provenance and acronyms: [author-kit data map](../data/author-kit-data-map.md);
- code spans and final-file roles: [full author-kit map](author-kit-map.md);
- 2021 output-to-paper pages: [author output crosswalk](author-output-crosswalk.md);
- 2025 network equations and invariants: [Leontief method note](../methods/leontief-unveiling.md);
- selected-result status: [result-selection task](../project/tasks/result-selection.md) and
  [major results](../../Results_Proposal/major_results.md).

## Non-public and unavailable boundaries

- ZIP-level Equifax data used to build distributional debt write-downs are not
  public; only the prepared `debtwritedown.dta` is supplied.
- CoreLogic files used in the original return/state work are absent; the
  relevant build blocks are commented and downstream files are supplied.
- State identifiers and some state-level inputs are restricted or
  author-prepared; `SYsavingwealth.dta` is supplied instead.
- CRSP is licensed rather than an unrestricted public input.
- The completed July 2025 instrument matrices, corporate-equity extension, and
  exact plotted annual series are not in the February 2021 kit.

These gaps do not invalidate the historical benchmark. They determine how far
upstream an independent reconstruction can honestly begin.
