# Authors' Replication Kit Map

This is a navigation aid for `MSS2021Febreplicationkit/`. It does not replace
the authors' code or the paper.

For a shorter first read, use the
[`author-kit-quickstart.md`](author-kit-quickstart.md). It summarizes the
pipeline, preprocessing equations, prepared-file contracts, and which 2021
objects can and cannot be reused for the July 2025 methodology.

## Version relationship to the target paper

The target is `MSS_SGR_July242025.pdf`, dated July 25, 2025. Its title page says
that it is a heavily revised version of the earlier draft *The Saving Glut of
the Rich and the Rise in Household Debt*. The February 2021 package is the
replication kit for that earlier draft.

The exact accompanying paper revision is now stored as
`MSS_SGR_Feb2021.pdf`. The regenerated-output-to-paper-page mapping is in
[`author-output-crosswalk.md`](author-output-crosswalk.md).

Consequences:

- the target paper runs through 2019; the old kit generally runs through 2016;
- the target paper presents a matrix/Leontief unveiling methodology and
  incorporates Batty et al. (2023); the old kit explicitly unwinds successive
  intermediation rounds;
- 2025 Figures 1-13 do not share numbering with old Figures 1-12;
- the older state-level main section is no longer a main result in the target
  paper, which instead adds international and Norwegian evidence;
- some old outputs are close precursors to revised exhibits, but none should be
  declared an exact match without comparing definitions, periods, smoothing,
  group cutoffs, and underlying data.

Use this package to learn and benchmark the earlier implementation, then record
for each selected 2025 result which parts can be inherited, updated, or must be
rebuilt from a newer source.

## What the 2025 paper says each main dataset does

The searchable paper source is
/Users/lorenzogorini/Library/CloudStorage/OneDrive-UniversitàCommercialeLuigiBocconi/PhD/research-wiki/papers/inequality/mian-2025-saving-glut-rich/full.md.
Use it before reparsing the PDF. The quotations below are deliberately short;
the line number and printed page identify where to read the surrounding
argument.

The central data architecture is:

    Financial Accounts / FWTW
        -> instrument-by-issuer-by-holder dollar matrices
        -> direct ownership matrix -> unveiled ownership

    DINA asset-class shares + Financial Accounts household totals
        -> wealth by household cohort and asset class
        -> distributional saving and augmented household-owner columns

    NIPA + valuation inputs
        -> aggregate accounting closure and saving net of valuation

This corrects two common misunderstandings:

- the target paper has **23 intermediary sectors and 34 financial
  instruments**, not 23 instrument matrices; and
- DINA does not fill missing FWTW counterparty cells. Missing bilateral cells
  are completed within each instrument from Financial Accounts information,
  known margins, exclusions, proportionality, and balancing. DINA is merged
  later to split the aggregate household owner across wealth cohorts.

### Financial Accounts and FWTW: direct ownership

> “The U.S. Financial Accounts provide highly detailed data on assets and
> liabilities...”

Paper location: Section 2.2, printed p. 8, full.md:160. The rest of the
sentence says these data populate every cell of the direct ownership matrix.

> “the information here is broken down further by 34 instruments”

Paper location: Section 2.2, printed p. 9, full.md:167. Each instrument has a
dollar issuer-row/holder-column matrix. The matrices are summed, then each
issuer row is divided by that issuer's total liabilities.

> “fill the cells ... with exact values when they are known, and infer the
> unknown cells via a proportionality assumption”

Paper location: Section 2.2, printed p. 9, full.md:175. The same paragraph adds
a row-and-column-total balancing algorithm. A single unknown against a known
margin is a residual; several unknown cells generally are not identified by
subtraction alone.

Economic role:

- builds the 34 dollar matrices \(X_{h,t}(i,j)\);
- builds the aggregate direct ownership matrix \(\bar M_t\);
- identifies Figure 1's aggregate amount behind the veil;
- supplies B.101 household asset and liability totals; and
- supplies the primary-asset network needed for Figure 8.

Official reference: [Federal Reserve FWTW data and
documentation](https://www.federalreserve.gov/releases/efa/fwtw.htm).
Old-kit locations: data/fof/, code/build_fa_unveiling_data.do, and the prepared
data/fof/LQpanel_2019Q1.dta.

### DINA / PSZusdina: distribution across household groups

DINA means **Distributional National Accounts**. The supplied microfiles are
tax-record-based individual-level files with income components and imputed
wealth components. The project does not use raw individuals as ownership
matrix cells; it collapses them into group-by-asset-class shares.

> “estimate the share of aggregate wealth in asset class \(j\) held by group
> \(i\) in year \(t\)”

Paper location: Section 3.1, printed p. 15, full.md:297. The paper then
multiplies this share by the corresponding aggregate wealth total from
Financial Accounts Table B.101.

> “These financial instruments can in turn be mapped into DINA wealth
> categories”

Paper location: Section 4.1, printed p. 26, full.md:520. The mapping in
Appendix Table A1 lets the authors replace the one aggregate household-owner
column with wealth-cohort columns and repeat the unveiling.

Economic role:

- supplies \(\omega^a_{g,t}\), cohort \(g\)'s share of household asset or
  liability class \(a\);
- constructs \(W^a_{g,t}=\omega^a_{g,t}W^a_t\) for Figure 5;
- splits direct household positions by cohort for Figure 8; and
- supplies income, taxes, and transfers in the income-minus-consumption
  robustness exercise.

DINA is **not required for aggregate Figure 1** and is not a complete
(wealth group, intermediary, instrument) counterparty dataset.

Official/reference page: [U.S. Distributional National Accounts data,
microfiles, and code](https://gabriel-zucman.eu/usdina/). Old-kit locations:
data/PSZusdina/; DINA shares are built in
code/build_fa_unveiling_data.do:7259-7510 and used in
code/build_wealth_saving_data.do.

### NIPA: aggregate flows, denominators, and closure

NIPA means **National Income and Product Accounts**. It records aggregate
flows, not bilateral ownership positions.

> “map unveiled wealth to saving using the national income and product
> accounts (NIPA) accounting identities”

Paper location: Section 2.4, printed p. 13, full.md:258.

> “aggregate private saving from the wealth-based approach matches the
> aggregate private saving in NIPA”

Paper location: Section 3.1, printed p. 17, full.md:329. The remaining equity
price-inflation term is chosen to impose this national-accounts consistency.

Economic role:

- provides national income \(NI_t\), Figure 1's stock-to-income denominator;
- provides disposable-income, consumption, personal-saving, and
  corporate-saving aggregates;
- closes Figure 5 so cohort saving sums to total private saving; and
- normalizes Figure 8 debt stocks by national income.

Official reference: [BEA National Income and Product
Accounts](https://www.bea.gov/products/national-income-and-product-accounts).
Old-kit locations: data/NIPA/, code/build_nipa_saving_data.do, and
data/finalfiles/YinequalityNIPAanalysis.dta.

### Valuation inputs: separating saving from capital gains

> “The results shown in this paper use the
> Jorda-Schularick-Taylor Macrohistory Database for the house price index
> because of its longer coverage.”

Paper location: Section 3.1, printed p. 16, full.md:310.

Economic role:

- JST identifies repeat-sales housing price inflation;
- fixed-income price inflation is set to zero under the Financial Accounts
  reporting convention;
- debt write-down inputs prevent defaults from being misclassified as active
  borrower saving; and
- equity price inflation is the residual that makes wealth-based saving match
  NIPA, rather than the full equity capital gain.

Reference page: [Jorda-Schularick-Taylor Macrohistory
Database](https://www.macrohistory.net/database/). Old-kit locations:
data/JST/, data/callreport/, data/finalfiles/Ywealthreturns.dta, and
code/build_wealth_saving_data.do.

### DFA and SCF: distributional validation

> “cross-checks our results using wealth shares in the Distributional
> Financial Accounts”

Paper location: Section 3.6, printed p. 25, full.md:507.

The DFA combines Financial Accounts aggregate household balance sheets with
SCF distributional information. In this project it is an alternative to DINA
for wealth shares from 1989 onward, not a source of the FWTW network.

> “using an individual-level panel data for the years 1983 and 1989 available
> from the Survey of Consumer Finances”

Paper location: Section 3.3, printed p. 19, full.md:399. This panel checks
whether DINA's repeated-cross-section saving rates are distorted by entry and
exit from wealth groups.

Official references: [Federal Reserve Distributional Financial
Accounts](https://www.federalreserve.gov/releases/z1/dataviz/dfa/) and
[Survey of Consumer Finances](https://www.federalreserve.gov/econres/aboutscf.htm).
Old-kit locations: data/DFA/, data/scf/, and the group-share sections of
code/build_fa_unveiling_data.do.

### SCF consumption, CEX, and PSID: a robustness route

The 2025 Figure 5 baseline is wealth-based saving:
\(\Theta_{g,t}=\Delta W_{g,t}-\text{valuation}_{g,t}\). Income minus
consumption is Appendix C.1 robustness, not the baseline.

> “CEX and the Panel Study of Income Dynamics (PSID), do not measure the
> consumption of the highest-income households ... accurately”

Paper location: Appendix C.1, printed p. 52, full.md:1030.

The 2025 paper therefore uses SCF-based consumption shares following Fisher et
al. (2018), while CEX checks whether the subset of spending categories observed
in the SCF has a stable share of total expenditure (full.md:1032-1045).
The older 2021 kit contains additional PSID, CEX, and Fisher alternatives, so
they are more prominent in build_nipa_saving_data.do than in the revised
paper's baseline.

Official references: [BLS Consumer Expenditure
Surveys](https://www.bls.gov/cex/) and [Panel Study of Income
Dynamics](https://psidonline.isr.umich.edu/). Old-kit locations:
data/CEX/, data/PSID/, data/Fisher/, and
code/build_nipa_saving_data.do:452-700.

## Rules for agents

1. Treat the entire folder as an immutable vendor snapshot. Reading and
   checksumming are allowed; editing, renaming, and writing generated files
   inside it are not.
2. Do not begin by scanning or loading every dataset. The downloaded data tree
   occupies about 45 GB, and individual DINA files have sizes of several
   gigabytes. Trace a selected exhibit backward and inspect only its dependency
   chain.
3. Never run the master or build scripts in place. They write with `replace`
   into `data/finalfiles/`, `data/fof/`, `data/DFA/`, `data/PSZusdina/`, and
   `output/`.
4. Do not infer the economic meaning of a cryptic Financial Accounts or DINA
   variable from its name. Check Stata labels, source dictionaries, code
   formulas, and the paper.
5. Treat supplied final files as benchmarks. Record explicitly when our
   reconstruction begins from a final file because unavailable inputs prevent a
   deeper reconstruction.
6. Preserve the distinction between an annual aggregate (`Y...`), a
   state/group/year file (`SY...`), and quarterly Financial Accounts inputs.
   Prefixes are useful navigation hints, not validated schema contracts.
7. Use project-relative paths in our code. Do not reproduce the authors'
   machine-specific global root or Windows separators.

## Top-level structure

```text
MSS2021Febreplicationkit/
├── readme.pdf                    # package scope and unavailable-data notes
├── mss_savingglut_master.do      # global paths and pipeline orchestration
├── code/                         # four data builders plus paper analysis
├── data/                         # source, intermediate, and supplied final data
└── output/                       # authors' generated EPS figures and TeX tables
```

The package mixes raw sources, author-created intermediate files, and final
analysis files under `data/`. Folder placement alone does not establish
provenance. T-002 must classify each file actually used.

## Entry points

| Path | Role |
| --- | --- |
| `MSS2021Febreplicationkit/readme.pdf` | Authors' one-page package description and data-availability caveats. |
| `MSS2021Febreplicationkit/mss_savingglut_master.do` | Sets paths and runs the four build/analysis stages. The root path must be edited in an isolated copy before use. |
| `MSS2021Febreplicationkit/code/build_nipa_saving_data.do` | Builds income-minus-consumption saving measures and `finalfiles/YinequalityNIPAanalysis.dta`. |
| `MSS2021Febreplicationkit/code/build_fa_unveiling_data.do` | Builds the Financial Accounts ownership/unveiling data and `finalfiles/YinequalityFAanalysis.dta`. |
| `MSS2021Febreplicationkit/code/build_wealth_saving_data.do` | Builds wealth returns and wealth-based saving, including `Ywealthreturns.dta`, `YwealthFOF.dta`, and `Ysavingwealth.dta`. |
| `MSS2021Febreplicationkit/code/build_state_wealth_data.do` | Builds state-level wealth/saving inputs and controls. |
| `MSS2021Febreplicationkit/code/mss_analysis.do` | Produces paper tables, figures, and text calculations from final files. This is the first place to map an exhibit backward. |

The master execution order is:

```text
build_nipa_saving_data.do
    -> build_fa_unveiling_data.do
    -> build_wealth_saving_data.do
    -> build_state_wealth_data.do
    -> mss_analysis.do
```

Later stages depend on final files from earlier stages. The scripts use global
paths, Windows-style separators in many places, community Stata commands, and
`replace` extensively. Never run the master script inside the reference package.

## Code folder: inputs, transformations, and outputs

### `build_nipa_saving_data.do`

Purpose: construct annual saving measures using income less consumption and
assemble national accounting series.

Main steps visible in the script:

- import and transpose six updated BEA NIPA CSV tables;
- merge GDP, personal income, government, foreign transactions, saving and
  investment, and consumption-detail series;
- construct SCF consumption shares from repeated cross-sections;
- add PSID, DINA/PSZ, CBO, CEX, and Fisher consumption/income alternatives;
- construct multiple consumption-to-income assumptions and wealth/income-group
  saving measures;
- save `NIPA.dta`, `YconsshareSCF.dta`, and
  `YinequalityNIPAanalysis.dta`.

Important inputs:

- `data/NIPA/`
- `data/scf/`
- `data/PSID/small_sample_post1999.dta`
- `data/PSZusdina/usdina19622016.dta` and `parameters_mss.csv`
- `data/CBO/55413-CBO-supplemental-data.xlsx`
- `data/CEX/`
- `data/Fisher/`

### `build_fa_unveiling_data.do`

Purpose: trace household and government debt through layers of financial
intermediation and distribute ultimate holdings across wealth groups.

Main steps visible in the script:

- start from the quarterly Financial Accounts panel and CRSP-based intermediary
  equity support;
- unveil household debt through seven explicit intermediation rounds;
- repeat the process for government debt and mortgage debt;
- check that unveiled components add to the relevant aggregates;
- construct ownership shares from DFA, DINA, Smith-Zidar-Zwick, and alternative
  demographic/income groupings;
- merge annual ownership and Financial Accounts components into
  `YinequalityFAanalysis.dta`.

The script is about 8,900 lines. Navigate by its section comments rather than
reading it linearly. Its core inputs are:

- `data/fof/LQpanel_2019Q1.dta`
- `data/crsp/fof_equity_support.dta`
- `data/DFA/`
- `data/PSZusdina/`
- `data/SZZ2019/`

It writes not only to `data/finalfiles/` but also intermediate annual share files
under `data/fof/`, `data/DFA/`, `data/PSZusdina/`, and `data/SZZ2019/`.

#### Exact trace of the older unveiling procedure

The script does not form the 2025 paper's $27\times27$ direct ownership
matrix or calculate a Leontief inverse. It implements the earlier method as
three long, parallel dollar-allocation pipelines:

| Object unveiled | Main code span | Seven-round output |
| --- | --- | --- |
| Household debt | lines 9--2405 | `data/finalfiles/Yunveilhhd.dta` |
| Government debt | lines 2444--4713 | `data/finalfiles/Yunveilgovd.dta` |
| Household mortgage debt | lines 4754--7158 | `data/finalfiles/Yunveilmtgd.dta` |

For household debt, round 1 assigns home mortgages and consumer credit to
their direct holders (lines 31--171). Later rounds successively pass embedded
household debt through GSE/ABS/finance-company/REIT securities, monetary and
fund sectors, deposit institutions, non-financial corporations, and
non-corporate businesses. The round aggregation markers are at lines 131, 724,
1066, 1259, 1740, 2138, and 2316. Variables `test1`--`test7` conserve the debt
stock across reallocations. Lines 2385--2388 aggregate final holdings into U.S.
households, government, rest of world, and residual/other categories.

The three outputs are merged into `Yunveil.dta` at lines 7163--7171. Section 5
then merges these unveiled amounts with DFA, DINA, and SZZ ownership shares
(starting at line 7681) and saves `YinequalityFAanalysis.dta` at line 8904.
The old paper's Figure 6 reads that final file at
`code/mss_analysis.do:587`; Figures 7--8 do so at lines 775 and 804.

The economic recursion is a precursor to the 2025 matrix method, but it is not
a literal seven-term power series of one fixed matrix: the script uses
instrument-specific proportionality factors, net-issuance adjustments,
special sector treatments, and explicit residual buckets. See
[`../methods/leontief-unveiling.md`](../methods/leontief-unveiling.md) for the
equation-level comparison and our Python implementation contract. The
submission-facing discussion and the common-input comparison protocol are in
[`../../Report/report.tex`](../../Report/report.tex); future agents should not
claim numerical equality across paper versions before that protocol is run.

### `build_wealth_saving_data.do`

Purpose: distribute aggregate balance-sheet wealth across groups and compute
wealth-based active saving by separating wealth changes from valuation changes.

Main steps visible in the script:

- optionally build asset-return inputs from CoreLogic, JST Macrohistory, and
  private debt write-down data;
- allocate B.101 balance-sheet assets and liabilities using group ownership
  shares from `YinequalityFAanalysis.dta`;
- calculate asset-specific valuation changes and active saving;
- merge national-account aggregates to close the saving measure;
- save `YwealthFOF.dta` and `Ysavingwealth.dta`.

The block that creates `Ywealthreturns.dta` is commented because CoreLogic is
not supplied. The included `Ywealthreturns.dta` is therefore a required
benchmark input unless a public replacement is explicitly designed.

### `build_state_wealth_data.do`

Purpose: construct state-income-group wealth, saving, and state controls for the
cross-state validation.

Main steps visible in the script:

- sample tax filers above an AGI threshold using IRS state tables and Pareto
  parameters;
- combine state identifiers with DINA tax-unit data;
- build state/group/year wealth and rescale it to aggregate totals;
- merge Financial Accounts ownership and unveiled-debt inputs;
- combine state house-price changes with aggregate wealth returns;
- compute state saving and assemble migration, banking deregulation, industry,
  education, and demographic controls;
- save `SYsavingwealth.dta` and `SYcontrols.dta`.

The CoreLogic-dependent block cannot be reconstructed from this package. The
authors include its final state-saving output.

### `mss_analysis.do`

Purpose: generate the paper's main and appendix exhibits plus numbers quoted in
the text.

The file is organized by paper section and exhibit marker. It is the preferred
starting point for every selected result. It consumes final annual and
state-level files rather than recreating their inputs.

## Data folder inventory

### Core national and distributional sources

| Folder | Contents | Main use |
| --- | --- | --- |
| `NIPA/` | Six BEA NIPA source tables, original and updated CSV variants, plus `YPersConsExUpdate.dta` | Aggregate income, consumption, saving, investment, government, and foreign-sector accounting. |
| `PSZusdina/` | DINA microfiles for 1962-2016, an alternative PSZ file, state DINA data, capitalization parameters, yields, and generated group-share files | Income/wealth distributions, capitalization, group shares, and state analysis. The largest files have multi-GB logical sizes; never load them blindly. |
| `scf/` | Survey of Consumer Finances extracts for 1989-2019, combined files, updated public extracts, and two supporting do-files | Consumption shares, wealth-share checks, pension and interest-income calculations. |
| `PSID/` | `small_sample_post1999.dta` | Alternative household consumption-share estimates. |
| `CBO/` | CBO reports and underlying/supplemental workbooks | Alternative household-income shares and average household income. |
| `CEX/` | Precomputed expenditure shares and an Aguiar-Bils table | Consumption-expenditure distribution by income group. |
| `Fisher/` | Three prepared Fisher-series Stata files | Alternative consumption inequality/share series. |
| `IRS/` | Federal tax and income share workbooks | Supporting tax-distribution sources; verify the exact active code path before use. |

### Financial Accounts and portfolio-allocation sources

| Folder | Contents | Main use |
| --- | --- | --- |
| `fof/` | Financial Accounts tables, annual/quarterly Z.1 CSVs and dictionaries, converted Stata tables, an assembled quarterly panel, intermediary data, and `fofcreate.do` | Core stocks/flows and intermediation network. `raw/z1_csv_files/data_dictionary/` maps Financial Accounts table codes. |
| `crsp/` | CRSP market data, balance-sheet support, and `fof_equity_support.do/.dta` | Market-value equity adjustments for financial intermediaries. |
| `DFA/` | Distributional Financial Accounts CSV/XLSX inputs and prepared group-share files | Allocation of asset holdings across net-worth and demographic groups. |
| `SZZ2019/` | Smith-Zidar-Zwick workbooks and prepared shares | Alternative wealth-group allocation. |
| `JST/` | JST Macrohistory Stata file | Housing, equity, and bond return/valuation series. |
| `callreport/` | Debt write-down code and prepared quarterly/annual files | Mortgage and consumer-credit write-down adjustments; underlying Equifax data are private. |

### State-level and validation sources

| Folder | Contents | Main use |
| --- | --- | --- |
| `Sirs/` | State tax tables for 1979-2016, an imputed high-income variant, and state codes | State-income-group counts and AGI totals. |
| `dinastate/` | Sampled tax-unit state DINA and prepared state/group/year wealth | State wealth construction; multi-GB files. |
| `BEA/` | State industry-employment CSVs for 1969-2000 and 2001-2017 with metadata, plus a few aggregate series | State industry controls and supporting macro series. |
| `census/` | Large prepared population and education/skill files | State population weights and skilled-labor controls. |
| `cps/` | Prepared migration file | State migration control. |
| `MSV/` | Banking deregulation/cross-state control file | State regression controls. |
| `WID/` | WID state top-income-share data and metadata | State top-income-share changes in Figure 10 and later analysis. |

### Supporting, comparison, or non-core folders

| Folder | Contents | Guidance |
| --- | --- | --- |
| `socsec/` | Annual Social Security series | Used for a text calculation in `mss_analysis.do`. |
| `Kuhnetal/` | Kuhn-Schularick-Steins workbook and prepared Stata file | Not referenced by the five main top-level scripts in a static path search; treat as supporting/legacy until traced. |
| `autensplinter/` | Auten-Splinter workbook and prepared Stata file | Not referenced by the five main top-level scripts in a static path search; likely a comparison series. |
| `Zirs/` | Prepared IRS/ZIP-related file | Used by the private-data debt-write-down workflow, not by the default master path directly. |

Do not equate "not referenced by the five top-level scripts" with irrelevant:
some files may document robustness, supply prebuilt results, or support
subfolder do-files. Trace before deleting or ignoring.

## Core supplied final files

| File under `data/finalfiles/` | Main role in analysis |
| --- | --- |
| `NIPA.dta` | National Income and Product Accounts building blocks. |
| `YinequalityNIPAanalysis.dta` | Annual income-minus-consumption measures, aggregates, and accounting series. |
| `YinequalityFAanalysis.dta` | Annual unveiled Financial Accounts ownership/debt measures. |
| `Ywealthreturns.dta` | Asset-return/valuation inputs used by the wealth-based approach. |
| `YwealthFOF.dta` | Wealth levels constructed from Financial Accounts inputs. |
| `Ysavingwealth.dta` | Annual wealth-based saving and valuation measures by wealth group. |
| `Yunveil.dta`, `Yunveilhhd.dta`, `Yunveilgovd.dta`, `Yunveilmtgd.dta` | Unveiled ownership allocations for debt categories. |
| `SYsavingwealth.dta` | Supplied state-income-group saving measures. |
| `SYcontrols.dta` | State-level controls. |

T-002 has begun documenting schema, keys, coverage, and producer/consumer
relationships selectively. Extend the inventory only as a chosen result makes
another file relevant.

### Selective Figure 1 data findings

The exact 2025 Figure 1 completed matrices and plotted series are not present
in the old kit. The downloaded tree nevertheless supports an authors-data
reconstruction of the stock behind the veil from these boundary files:

| File | Observed schema | What it establishes |
| --- | --- | --- |
| `data/fof/LQpanel_2019Q1.dta` | 297 x 1,111; unique quarter, 1945Q4--2019Q4 | Authors' prepared wide balance-sheet panel; supplies Q4 household holdings across named intermediary instruments and the household financial-asset total. |
| `data/fof/LQpanel_2019Q1withgov.dta` | 294 x 1,049; unique quarter, 1945Q4--2019Q1 | Wide raw Financial Accounts panel used upstream by the older allocation code; not a completed issuer-holder matrix. |
| `data/finalfiles/Yunveilhhd.dta` | 75 x 2,117; unique year, 1945--2019 | Household-debt-specific output through seven named rounds; its preserved project copy validates four Python-reconstructed bond cells and supplies three nonfinancial exclusions only for the approximate share denominator. |
| `data/crsp/msf.dta` | 4,346,059 x 8; security-month, 1945--2018 | Raw monthly security observations used to rebuild listed financial-intermediary equity with explicit December, share-code, and SIC rules. |
| `data/finalfiles/YinequalityNIPAanalysis.dta` | annual, unique year, 1913--2016 | Supplies national income and sets the common authors-data endpoint at 2016. |
| `data/finalfiles/Yunveil.dta` | 75 x 2,170; unique year, 1945--2019 | Merge of household, government, and mortgage debt allocations; closest old unveiling output but not Figure 1. |
| `data/finalfiles/YwealthFOF.dta` | 57 x 3,895; unique year, 1960--2016 | Downstream wealth-group Financial Accounts data, not the aggregate network. |
| `data/fof/b101_09182019.dta` | 294 x 53; unique quarter, 1945Q4--2019Q1 | Household balance-sheet totals without complete bilateral counterparties. |
| `data/fof/l125_09182019.dta` | 294 x 33; unique quarter, 1945Q4--2019Q1 | GSE balance-sheet table, useful for one sector but insufficient for the full network. |

Starting from `LQpanel_2019Q1.dta` skips only upstream imports, cleaning, and
wide merges. `Code/unveiling/figure1_authors.py` still combines the economically
central intermediary instruments, adjusts funded pensions, reconstructs the
four bond cells and household equity share from the Q4 panel, and reconstructs
listed financial equity from raw CRSP records. The target paper
uses 23 intermediary sectors and 34 instruments; 23 is not an instrument
count. The resulting 1963--2016 stock-to-national-income curve has correlation
0.995 with the digitized paper curve. Every reconstructed bond cell matches the
supplied Stata intermediate within \$0.05 million. The ownership-share match is
weaker because the kit omits the revised denominator crosswalk and completed
matrix.

Detailed used-column meanings, representative `Yunveil.dta` variables, current
public FWTW inputs, and source-file checksums are maintained in
[`../data/figure1-data.md`](../data/figure1-data.md). That note is explicitly
update-as-discovered; future agents should not reload all 45 GB merely to make
the inventory exhaustive.

## Output folder

`output/` contains the authors' already-generated artifacts:

- 22 EPS figure files;
- 25 TeX table fragments;
- one PDF flow diagram.

These artifacts are comparison targets, not destinations for our code. Our
implementation must write elsewhere. Some paper exhibits combine multiple
output files, such as the three panels of Figure 3 or the household,
government, and combined-debt panels of Figure 8.

## Older-paper exhibit outputs

| Earlier-paper exhibit | Authors' output | Broad content |
| --- | --- | --- |
| Figure 1 | `output/fig_glut.eps` | Top-1-percent saving across wealth-based, DINA, and CBO approaches. |
| Table 1 | `output/tab_glut.tex` | Period means and changes for the Figure 1 measures. |
| Figure 2 | `output/fig_trad.eps` | Net domestic investment, current account, and government borrowing relative to the 1978-1982 base. |
| Table 2 | `output/tab_trad.tex` | Period decomposition corresponding to Figure 2. |
| Figure 3 | `output/fig_hh_a.eps`, `fig_hh_b.eps`, `fig_hh_c.eps` | Saving changes for the bottom 90 percent, next 9 percent, and top 1 percent. |
| Figure 4 | `output/fig_bottomline.eps` | Distributional saving and macroeconomic absorption/accounting decomposition. |
| Figure 6 | `output/fig_owndet.eps` | Direct household asset ownership composition before unveiling. |
| Table 6 | `output/tab_unveil1.tex`, `tab_unveil9.tex`, `tab_unveil90.tex` | Saving and debt-absorption decomposition by wealth group. |
| Figure 7 | `output/fig_nhhd.eps` | Net household-debt positions across wealth groups. |
| Table 7 | `output/tab_nhhd_.tex` | Household-debt saving/holding decomposition by period and wealth group. |
| Figure 8 | `output/fig_hhddebt.eps`, `fig_govddebt.eps`, `fig_demddebt.eps` | Ownership of household debt, government debt, and their sum. |
| Figure 9 | `output/fig_safe.eps` | Top-1-percent versus rest-of-world accumulation of household and government debt. |
| Figures 10-12 | `output/fig_Dtop1state.eps`, `fig_statesavingt6.eps`, `fig_statesaving.eps`, `fig_statewealth.eps` | State-level income-share, saving, and wealth relationships. |
| Tables 8-9 | `output/tab_statesaving.tex`, `tab_statewealth.tex` | State-level fixed-effects and long-difference regressions. |

Figure 5 and Appendix Table A2 are explicitly marked "not created in code" in
`mss_analysis.do`.

## Efficient trace recipe for a selected result

Use this sequence instead of reading the package broadly:

1. Find the `** Figure N` or `** Table N` marker in `mss_analysis.do`.
2. Record every `use`, `merge`, sample restriction, transformation, weighting
   rule, statistic/regression, and export command in that block.
3. Inspect the labels and schema of only the referenced final files.
4. Find the `save` command that produces each final file in the build scripts.
5. Trace only the variables used by the exhibit back through that build script.
6. Stop when reaching a supplied raw source, a clearly author-created prepared
   file, or an unavailable input. Record that boundary explicitly.
7. Reproduce the exhibit first from the final file as a benchmark, then replace
   final-file columns with reconstructed columns one dependency block at a
   time.

For very large `.dta` files, inspect metadata and selected columns before any
full read. Never ask pandas or Stata to load a 12-16 GB microfile merely to list
its variables.

## Known availability constraints

The package read-me identifies two relevant exceptions:

1. `data/callreport/debtwritedown.dta` uses Equifax ZIP-code debt data that are
   not public. The producing do-file is not run by default.
2. CoreLogic house-price files used in the state-level saving construction are
   not included. The relevant code is retained but commented, and
   `data/finalfiles/SYsavingwealth.dta` is supplied.

These constraints affect how independently the state analysis and some debt
write-down adjustments can be reconstructed. Document the boundary rather than
silently substituting the authors' final file.

## Likely Stata requirements for an original-code benchmark

`mss_analysis.do` calls community commands including `labmask`, `frmttable`,
`tabstatmat`, `reghdfe`, `eststo`/`esttab`, and `ereplace`. Record the Stata
version and installed package versions if the original analysis is benchmarked.
The independent Python implementation must not depend on these commands.
