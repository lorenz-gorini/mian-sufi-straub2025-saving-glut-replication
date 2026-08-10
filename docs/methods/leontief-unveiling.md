# Leontief Unveiling of the Financial Network

## Replication target

This note implements and explains Sections 2.1--2.2 of Mian, Straub, and Sufi,
*The Saving Glut of the Rich* (July 25,
2025 draft). The authoritative passages are printed pages 5--9 (PDF pages
6--10), especially Equations (1)--(4).

The economic question is: **who ultimately owns a liability when its direct
holder is itself a financial intermediary?** Direct balance sheets stop at the
first holder. The unveiling calculation follows every possible chain of
cross-holdings until it reaches an ultimate owner.

This is the methodological core needed to interpret 2025 Figure 1 and, later,
to allocate household debt in Figure 8. The project reconstructs Figure 1 from
selected files in the authors' February 2021 snapshot and separately from a
June 2026 public FWTW release. The first is a closer old-vintage authors-data exercise; the
second is a later-vintage robustness check. Neither is the unavailable exact
2025 output.

## 1. Direct ownership

At date $t$, the paper has:

- $m=4$ ultimate owners: U.S. households, the federal government, state and
  local governments, and the rest of the world;
- $k=23$ intermediary sectors; and
- $m+k=27$ sectors in total, ordered with owners first.

Define

\[
s_t(i,j)
=
\frac{\text{dollar liabilities issued by }i\text{ and held directly by }j}
     {\text{total dollar liabilities issued by }i}.
\]

Rows therefore index **issuers/borrowers** and columns index
**holders/lenders**. Stacking the shares gives the direct ownership matrix

\[
\bar M_t=[s_t(i,j)]_{i,j=1}^{m+k},
\qquad
\bar M_t\mathbf 1=\mathbf 1.
\]

Every entry is a unit-free share in $[0,1]$. The row-sum identity says that all
liabilities issued by each sector are assigned to holders exactly once.

### Reading a row and a column

For a fixed issuer $i$, every entry $s_t(i,j)$ has the same denominator,
$L_{i,t}$. Outgoing arrows from $i$ therefore describe the composition of
that issuer's funding, and the row must sum to one. In the worked example,

\[
s(B,H)+s(B,F)+s(B,G)=0.20+0.70+0.10=1.
\]

The incoming arrow $F\rightarrow B$ has a different interpretation:
$s(F,B)=0.20$ says that the bank holds 20% of the fund's liabilities. Its
denominator is $L_F$, not the bank's total assets. It therefore does not mean
that 20% of bank lending goes to the fund. More generally, entries down column
$j$ use different issuer-liability denominators, so columns of $\bar M_t$ need
not sum to one. Dollar assets held by sector $j$ are instead

\[
\sum_i L_{i,t}s_t(i,j),
\]

which is the $j$th element of $L_t\bar M_t$ under the paper's row-vector
convention.

Intermediaries do own financial assets directly: a bank can hold fund
liabilities, mortgages, or government debt. They are called intermediaries
rather than ultimate owners because those asset holdings are financed by the
bank's own liabilities and equity, which must in turn be attributed to their
ultimate holders.

### Construction from the Financial Accounts

For instrument $h=1,\ldots,\ell$, let $M_{h,t}$ be a
$(m+k)\times(m+k)$ dollar matrix with the same issuer-row/holder-column
orientation. Let $L_t$ be the $1\times(m+k)$ vector of total liabilities in
dollars. Equation (4) is row scaling:

\[
\bar M_t
=
\left(\frac{1}{L_t}\right)^{\!\top}
\odot
\left(\sum_{h=1}^{\ell}M_{h,t}\right),
\qquad \ell=34.
\tag{4}
\]

Operationally: sum dollar holdings over the 34 instruments, then divide row
$i$ by $L_{i,t}$. Section 2.2 explains that the underlying FWTW data can have
unknown cells. Completing those cells under the paper's exact, proportionality,
and row-column-total rules is an **upstream data-construction task**. The
current Python constructor deliberately requires already-completed matrices.

### What Figure 1 measures before unveiling

Figure 1 measures the size of the balance-sheet layer that must be unveiled.
Let

\[
D_t(i,H)=\text{liabilities issued by sector }i
          \text{ and held directly by households}
\]

in current dollars, after summing instruments. If \(\mathcal F\) is the set of
financial-intermediary issuers, define

\[
V_t=\sum_{i\in\mathcal F}D_t(i,H).
\]

The household directly owns each claim on an intermediary, but it owns the
primary assets financed by the intermediary only indirectly. The paper's two
Figure 1 series are therefore

\[
\frac{V_t}{\sum_{i\ne ROW}D_t(i,H)}
\qquad\text{and}\qquad
\frac{V_t}{NI_t},
\]

where \(NI_t\) is annual national income. The first denominator is the stock of
domestic household financial claims; the second is an annual current-dollar
flow. Figure 1's object is not the elementwise difference
\(\Omega_t-\bar M_t\), which is not even a conformable comparison in the block
implementation. The inverse is needed to say where \(V_t\) ultimately leads,
not to count how much sits behind the veil.

The precise public-data mapping, units, issuer exclusions, and vintage boundary
are documented in [`../data/figure1-data.md`](../data/figure1-data.md).

## 2. From direct to ultimate ownership

Set the first $m$ rows of $\bar M_t$ to zero to form $M_t$. The ownership
columns remain intact. Zeroing the owner rows stops a path once it has reached
an ultimate owner; it does not remove direct owner holdings.

One multiplication adds one layer of intermediation:

\[
(M_t^2)_{ij}
=
\sum_{\tilde j=m+1}^{m+k}
s_t(i,\tilde j)s_t(\tilde j,j).
\]

Thus $M_t$ records direct holdings, $M_t^2$ paths through one other
intermediary, $M_t^3$ paths through two other intermediaries, and so on. The
paper's Equation (1) sums every possible chain:

\[
\bar\Omega_t
=M_t+M_t^2+M_t^3+\cdots
=M_t(I-M_t)^{-1}.
\tag{1}
\]

The desired unveiled ownership matrix is the lower-left $k\times m$ block,
$\Omega_t$. Row $i$, column $j$ is the share of intermediary $i$ held
ultimately by owner $j$, directly or indirectly.

### The block form used in code

With owners first,

\[
M_t=
\begin{bmatrix}
0_{m\times m} & 0_{m\times k}\\
B_t           & Q_t
\end{bmatrix},
\]

where $B_t\in\mathbb R^{k\times m}$ contains intermediaries' direct owner
shares and $Q_t\in\mathbb R^{k\times k}$ contains intermediary
cross-holdings. Equation (1) then implies

\[
\Omega_t
=B_t+Q_tB_t+Q_t^2B_t+\cdots
=(I_k-Q_t)^{-1}B_t.
\tag{1a}
\]

The implementation solves

\[
(I_k-Q_t)\Omega_t=B_t
\]

with `numpy.linalg.solve`; it does not compute an explicit inverse. This is
algebraically identical to the paper but more direct and numerically preferable.

The maintained convergence condition is

\[
\rho(Q_t)<1,
\]

where $\rho(\cdot)$ is the spectral radius. Economically, no set of
intermediaries can own one another forever without some share eventually
reaching an ultimate owner.

## 3. Worked two-intermediary example

Order sectors as households $H$, government $G$, a bank $B$, and a fund $F$.
Consider

\[
\bar M=
\begin{bmatrix}
1&0&0&0\\
0&1&0&0\\
0.2&0.1&0&0.7\\
0.6&0.2&0.2&0
\end{bmatrix}.
\]

The bank's liabilities are held 20% by households, 10% by government, and 70%
by the fund. The fund's liabilities are held 60% by households, 20% by
government, and 20% by the bank. Therefore

\[
B=
\begin{bmatrix}
0.2&0.1\\
0.6&0.2
\end{bmatrix},
\qquad
Q=
\begin{bmatrix}
0&0.7\\
0.2&0
\end{bmatrix}.
\]

The first three contributions are

\[
B=
\begin{bmatrix}0.20&0.10\\0.60&0.20\end{bmatrix},\quad
QB=
\begin{bmatrix}0.42&0.14\\0.04&0.02\end{bmatrix},\quad
Q^2B=
\begin{bmatrix}0.028&0.014\\0.084&0.028\end{bmatrix}.
\]

Summing every round gives

\[
\Omega=(I-Q)^{-1}B
=
\begin{bmatrix}
0.72093&0.27907\\
0.74419&0.25581
\end{bmatrix}.
\]

Direct household ownership of the bank was only 20%, but ultimate household
ownership is 72.09% after tracing the fund-bank cross-holdings. Each row of
$\Omega$ sums to one, so every intermediary is fully assigned to owners.

The same result can be read directly from the network. Let $\omega_{BH}$ be
the bank's ultimate household share and $\omega_{FH}$ the fund's ultimate
household share. The two intermediary rows imply

\[
\omega_{BH}=0.20+0.70\omega_{FH},
\qquad
\omega_{FH}=0.60+0.20\omega_{BH}.
\]

Substitution gives

\[
\omega_{BH}=0.62+0.14\omega_{BH}
\quad\Longrightarrow\quad
\omega_{BH}=\frac{0.62}{1-0.14}=0.72093.
\]

Equivalently, 20 percentage points come from the bank-to-household edge and
$0.70\times0.74419=0.52093$ comes through the fund, for a total of 72.093
percentage points. The 14% coefficient is the weight of one complete
bank-to-fund-to-bank loop. The Neumann expansion lists the corresponding
paths by length:

\[
0.20+0.42+0.028+0.0588+0.00392+0.008232+\cdots=0.72093.
\]

The exact network and this reconciliation are generated for the teaching deck
from `Code/scripts/build_unveiling_teaching_assets.py`; the supporting
ImageGen illustration is conceptual and is not used to encode any value.

## 4. Net worth and primary assets

Equation (2) maps the direct ownership matrix back to sector net worth. With
$L_t$ in dollars,

\[
W_t=L_t\bar M_t-L_t.
\tag{2}
\]

The closed-system balance-sheet invariant is

\[
\sum_{i=1}^{m+k}W_{i,t}=0.
\]

The paper then maps intermediated claims into $n=8$ primary assets. Let
$P_t\in\mathbb R^{n\times k}$ contain each primary asset's shares held
directly by intermediaries, and let
$\Lambda_t\in\mathbb R^{n\times m}$ contain direct owner shares. Equation (3)
is

\[
A_t=P_t\Omega_t+\Lambda_t.
\tag{3}
\]

All entries are shares. For each primary asset, the row sum across the columns
of $P_t$ and $\Lambda_t$ is one; the same must then be true of $A_t$.

## 5. Code contract and invariants

The implementation is in `Code/unveiling/network.py`.

| Paper object | Code object | Shape | Unit |
| --- | --- | --- | --- |
| $\{M_{h,t}\}_{h=1}^{\ell}$ | `instrument_holdings` | $(\ell,m+k,m+k)$ | dollars |
| $L_t$ | `total_liabilities` | $(m+k,)$ | dollars |
| $\bar M_t$ | `direct_ownership` | $(m+k,m+k)$ | share |
| $M_t$ | `intermediation_matrix()` | $(m+k,m+k)$ | share |
| $\Omega_t$ | `unveiled_ownership()` | $(k,m)$ | share |
| $W_t$ | `net_worth()` | $(m+k,)$ | dollars |
| $P_t,\Lambda_t$ | method inputs | $(n,k),(n,m)$ | share |
| $A_t$ | `primary_asset_ownership()` | $(n,m)$ | share |

Input, output, observation, keys, and invariant for this first task are:

- **input:** one completed cross-sector matrix per instrument and date, plus
  sector liabilities;
- **output:** direct and unveiled owner shares for the same date;
- **unit of observation:** issuer-holder-instrument-date before aggregation,
  then issuer-holder-date;
- **keys:** date, instrument, issuer sector, holder sector;
- **invariants:** rows of $\bar M_t$ sum to one; $\rho(Q_t)<1$; rows of
  $\Omega_t$ and $A_t$ sum to one; aggregate net worth sums to zero.

Validation occurs once at the class boundary. The central computation trusts
the validated representation.

## 6. Comparison with the February 2021 authors' code

The old package does **not** construct the 2025 $27\times27$ matrix or call a
matrix inverse. Its `build_fa_unveiling_data.do` implements an earlier,
asset-specific analogue by explicitly reallocating household debt, government
debt, and mortgage debt through seven named rounds.

| Dimension | 2025 paper and our Python | February 2021 Stata kit |
| --- | --- | --- |
| Core representation | One completed direct ownership matrix $\bar M_t$ | Many instrument- and sector-specific variables |
| Unwinding | Infinite path sum / Leontief solve | Seven explicit reallocation rounds |
| Scope | Full network, then eight primary assets | Household, government, and mortgage debt built separately |
| Missing cells | Batty et al. completion plus proportionality rules upstream | Hand-coded proportionality factors and net-issuance adjustments |
| Stopping rule | Exact closed form when $\rho(Q_t)<1$ | Economically chosen sequence ending in owners and residual buckets |
| Conservation check | Row sums of $\Omega_t$ and $A_t$ equal one | `test1`--`test7` compare round totals with the original debt stock |
| Main output | $\Omega_t$ and $A_t$ share matrices | Dollar totals such as `a_hh_hhd`, `a_gov_hhd`, `a_row_hhd`, and residuals |

The old household-debt trace begins at lines 9--171, constructs round 2 at
724--803, then rounds 3--7 at 1066--1131, 1259--1287, 1740--1790,
2138--2180, and 2316--2353. Final owner and residual totals are assembled at
2385--2405. Government debt repeats the logic at 2444--4713; mortgage debt at
4754--7158; the three files are merged into `Yunveil.dta` at 7163--7171.

The two approaches share the economic proportionality assumption: an
intermediary's embedded assets are attributed in line with the ownership of its
liabilities. A finite round-by-round sum converges to the Leontief result when
the same stationary $B_t,Q_t$ matrices are used and enough rounds are taken.
The old Stata code is not literally a seven-term truncation of one common
matrix, however: it changes instruments and sector treatments across named
rounds, makes bespoke net-issuance adjustments, and creates residual buckets.
Therefore conceptual consistency is strong, but numerical identity cannot be
claimed without reconstructing both approaches from a common completed input
matrix.

### What is, and is not, established

Three comparisons must remain separate:

1. **Algebraic equivalence on a common stationary network is established.**
   If an explicit round algorithm uses the same fixed $B_t,Q_t$ in every
   round, then after $R$ rounds
   $\Omega_t^{(R)}=\sum_{r=0}^{R-1}Q_t^rB_t$ and
   $\Omega_t^{(R)}\to(I-Q_t)^{-1}B_t$ when $\rho(Q_t)<1$.
2. **Conceptual consistency with the 2021 code is established.** Both methods
   recursively allocate embedded assets according to the liability ownership
   of the current intermediary and both preserve the relevant debt total.
3. **Numerical equality between the actual 2021 Stata output and the 2025
   matrix implementation is not established.** The empirical inputs,
   instrument coverage, residual definitions, sector aggregation, and even the
   paper version differ. The old seven rounds are not seven powers of one fixed
   $Q_t$.

This evidence does not support a claim that the paper is wrong or that the
Python implementation is economically superior. The Python solve is a concise
and exact implementation of the stationary operator stated in the 2025 paper;
the Stata code is a detailed implementation of the earlier paper's empirical
allocation rules. A numerical comparison becomes meaningful only after both
algorithms are applied to the same completed dollar matrices and aggregated to
the same owner and asset definitions. The report discussion and proposed
comparison protocol are maintained in `Report/report.tex`.

## 7. Current replication boundary

Completed here:

- Equations (1)--(4) implemented with the paper's orientation and dimensions;
- a deterministic worked example;
- tests of the closed form against the paper's formula and an 80-round sum;
- accounting, ownership, and convergence invariants;
- a code-level crosswalk to the old authors' procedure;
- a 1963--2016 authors-data Figure 1 reconstruction from the authors' prepared
  balance-sheet panel, raw CRSP file, and national income, with the four bond
  cells and household equity share rebuilt in Python from Q4 panel inputs;
- validation of every reconstructed bond cell against the supplied Stata
  intermediate within \$0.05 million; the maximum error is \$0.03615 million;
- a comparison with a digitized paper benchmark: correlation 0.995 and mean
  absolute error 5.3 percentage points of national income for the level series;
- an independent 1963--2019 robustness series from pinned June 2026 FWTW and
  BEA/FRED national-income inputs; and
- data-boundary, raw-cell reconstruction, and network-algebra tests.

Still required for an exact-vintage Figure 1 replication:

- obtain the authors' July 2025 matrices or plotted annual values;
- match their 23 intermediary sectors, corporate-equity extension, and
  public/private corporation split; and
- compare the complete annual series under a tolerance declared before that
  exact benchmark is evaluated.

The authors-data reconstruction closely matches the paper's normalized stock
but does not exactly match the ownership share: the broad-denominator version
has mean absolute error 3.2 percentage points, and the conceptually narrower
proxy has 6.6 points. The public-data robustness result yields an indirect
share of 47.5% in 1963, 66.3% in 2007, a 70.1% peak in 2009, and 66.2% in 2019.
These differences are consistent with the missing 2025 denominator crosswalk,
sector definitions, and data vintage; they are not evidence against the target
paper.
