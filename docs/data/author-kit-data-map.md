# February 2021 Author-Kit Data Dictionary and Storage Policy

This is a selective navigation guide for `MSS2021Febreplicationkit/data/`.
It explains what the acronyms mean, who produced the underlying information,
the observation level actually supplied in the kit, and why each source enters
the authors' analysis. It is not an instruction to load every file. **Update
this document whenever work on a selected exhibit reveals another dependency,
variable definition, transformation, or limitation.**

The folder is the authors' February 2021 snapshot for an earlier version of the
paper. It must remain unchanged. Links below describe the source institution or
methodology; they do **not** imply that the current online release is identical
to the vintage saved in the kit. Same-input reproduction uses the supplied
files. A current online release belongs in a separately labelled robustness
exercise.

## The data architecture in one page

The folders make more sense when classified by the economic object they
identify:

| Layer | Economic question | Principal folders | Output used downstream |
| --- | --- | --- | --- |
| Macro totals and financial network | How much income, saving, debt, and each financial instrument exists in aggregate, and which sectors directly hold which sectors' liabilities? | `NIPA/`, `fof/` | National totals and the sector-by-sector direct ownership network. |
| Distribution across households | Which wealth or income group owns each asset category or owes each debt category? | `PSZusdina/`, `DFA/`, `scf/`, `SZZ2019/` | Annual group shares such as the top 1 percent's share of equity or the bottom 90 percent's share of mortgages. |
| Consumption, returns, and valuation adjustments | How much does each group consume, and how much of a wealth change is saving rather than a capital gain or write-down? | `PSID/`, `CEX/`, `Fisher/`, `crsp/`, `JST/`, `callreport/` | Consumption shares and asset-specific valuation/write-down adjustments. |
| Older state analysis and robustness | Do saving and wealth outcomes covary with state exposure and controls? | `dinastate/`, `Sirs/`, `WID/`, `census/`, `cps/`, `BEA/`, `MSV/`, `Zirs/` | State-by-year/group measures and controls. This is not currently one of the selected 2025-paper exhibits. |
| Authors' analysis layer | What files do the old plotting and regression routines read? | `finalfiles/` | Author-created benchmark files. These are downstream products, not raw data. |

This separation is fundamental. The Financial Accounts identify aggregate
stocks and inter-sector positions but do not identify rich and poor households.
DINA, DFA, or SCF supply distributional shares; they do not independently
identify every aggregate balance-sheet total.

## DINA: what it is and why it is here

**DINA means Distributional National Accounts.** The national accounts tell us
the total amount of national income, but not how that total is distributed.
The DINA project combines tax records, surveys, and national accounts so that
income assigned across the distribution adds back to the macroeconomic total.
The original U.S. method is described by
[Piketty, Saez, and Zucman](https://www.nber.org/papers/w22945); the archived
microfiles and code are linked from
[Gabriel Zucman's U.S. DINA page](https://gabriel-zucman.eu/usdina/), and the
broader accounting conventions are in the
[WID DINA methodology](https://wid.world/methodology/).

### Is DINA just a table of quantiles?

No. The large files in `PSZusdina/` are **weighted statistical microfiles**:
they contain record-level amounts, weights, and ranks, not only a row for the
top 1 percent and a row for the bottom 90 percent. They are constructed from
tax microdata plus imputed non-filers and income components that are not
observed directly on tax returns. They are therefore not a conventional survey
of identifiable households, and they are not a panel in which this project
follows the same named person over time.

The exact population unit must be taken from the codebook for the relevant
vintage rather than guessed from the folder name. In particular, the authors'
read-me explicitly says that `usdina19792008states.dta` is at the **tax-unit**
level; it does not say that every DINA variant in the folder has the same unit
convention. Before using a large file directly, we must record whether its
record represents a tax unit, an adult/equal-split unit, or another constructed
unit.

The three large variants have different roles:

| File | What the authors' read-me says | Replication interpretation |
| --- | --- | --- |
| `usdina19622016psz.dta` | Joined PSZ DINA files, retaining variables that PSZ dropped and adding annual percentiles. | Closest old-package bridge to the original PSZ construction. |
| `usdina19622016.dta` | The Mian-Straub-Sufi main DINA version; differences from PSZ are described in the old paper. | Main microfile used to build the package's national income, wealth, asset, and debt shares. It is author-modified, not an untouched PSZ download. |
| `usdina19792008states.dta` | Tax-unit file with state identifiers from NBER tax-record files, limited to years in which state identifiers exist. | Upstream input for the old state exercise; its restricted-data lineage prevents a fully public from-scratch reconstruction. |

### How DINA connects income, wealth, and ownership

The answer to “do we use DINA to relate household income to ownership?” is
**yes, but not through a household-by-household match to the Financial
Accounts**.

For each year, the authors use DINA ranks such as `wealth_ptile` or
`poinc_ptile`, a record weight (`dweght`), and components including equity,
housing, business wealth, pensions, fixed income, mortgages, other debt, and
pre- or post-tax income. The baseline wealth allocation ranks records by
`wealth_ptile`; `YszsharesIS.dta` is the alternative sorted by post-tax income.
For an asset or liability category `j`, group `g`, and year `t`, the
essential aggregation is:

$$
s_{gjt}
=
\frac{\sum_i w_{it}\,\mathbf{1}\{i\in g\}\,x_{ijt}}
     {\sum_i w_{it}\,x_{ijt}},
\qquad
H_{gjt}=s_{gjt}H_{jt}^{FA}.
$$

Here $x_{ijt}$ is the DINA value for record $i$, $w_{it}$ is its weight,
$s_{gjt}$ is group $g$'s share of category $j$, and $H_{jt}^{FA}$ is the
aggregate Financial Accounts amount. Thus the code says, for example, “DINA
estimates that the top 1 percent owns this fraction of total equity; allocate
that fraction of the aggregate equity total to the top 1 percent.” It does not
say “this specific DINA household owns this specific bank claim.”

The old Stata build collapses `usdina19622016.dta` into annual files such as
`Yszshares.dta`. That file includes shares of wealth, equity, housing, pensions,
business wealth, fixed income, mortgages, non-mortgage debt, and income for the
top 1 percent, next 9 percent, and bottom 90 percent. Those small prepared files
are quantile tables; the upstream DINA microfile is not.

### DINA, SCF, and DFA are complements, not synonyms

| Source | Unit and frequency | Main strength | Role in this package |
| --- | --- | --- | --- |
| DINA | Annual constructed, weighted micro-records; unit convention depends on the file/vintage. | National-account-consistent income distribution and a long annual series; also contains constructed wealth and portfolio components. | Baseline annual group shares and income-sorted/demographic alternatives. |
| SCF | Triennial cross-section of U.S. families, with a wealthy oversample and five multiple-imputation implicates. | Detailed observed family balance sheets, income, pensions, and demographics. | Portfolio and consumption-share checks; an alternative distributional source. See the [Federal Reserve SCF documentation](https://www.federalreserve.gov/econres/scfindex.htm). |
| DFA | Quarterly group-level estimates since 1989, constructed by reconciling SCF concepts with Financial Accounts totals. | A ready-made bridge from detailed SCF distributional shares to macro balance-sheet totals. | Alternative asset/liability shares by net worth, income, age, and generation. See the [Federal Reserve DFA](https://www.federalreserve.gov/releases/z1/dataviz/dfa/) and its [construction paper](https://www.federalreserve.gov/econres/feds/files/2019017pap.pdf). |

## Dataset dictionary

The “unit in the kit” column describes the supplied file, which may already be
far downstream from the producer's raw data. “Author-prepared” means that the
folder is not a reproducible copy of the public source by itself.

### Core national and distributional inputs

| Folder (size) | Acronym, producer, and source | Unit and contents in this kit | Why the authors use it / replication status |
| --- | --- | --- | --- |
| `fof/` (37 MB) | **FOF** = Flow of Funds, now published as the Federal Reserve's **Financial Accounts of the United States (Z.1)**. [Financial Accounts guide](https://www.federalreserve.gov/apps/fof/About.htm); current [issuer-to-holder/FWTW data](https://www.federalreserve.gov/releases/efa/fwtw.htm). | Hundreds of quarterly sector-by-instrument tables, dictionaries, converted Stata tables, and author-built `LQpanel*.dta` panels. | Core aggregate balance sheets and direct sector ownership positions for the old unveiling. Public upstream plus extensive author preparation. Current FWTW data are useful for a new-data robustness exercise, not a drop-in replacement for the 2021 vintage. |
| `NIPA/` (390 KB) | **NIPA** = National Income and Product Accounts, produced by the U.S. Bureau of Economic Analysis (BEA). [NIPA Handbook](https://www.bea.gov/resources/methodologies/nipa-handbook). | Annual BEA tables for GDP, personal income and its disposition, consumption, government, foreign transactions, and saving/investment; one converted consumption file. | Supplies aggregate national income, consumption, saving, investment, and government/foreign-sector terms. Public source snapshot. |
| `PSZusdina/` (33 GB) | **PSZ** = Thomas Piketty, Emmanuel Saez, and Gabriel Zucman; **U.S. DINA** = U.S. Distributional National Accounts. [Paper and description](https://www.nber.org/papers/w22945); [archived data/code](https://gabriel-zucman.eu/usdina/). | Three very large weighted microfiles, parameters, capitalization factors and yields, plus small author-created annual share files (`Yszshares*.dta`). | Main bridge from aggregate income/wealth to top 1, next 9, and bottom 90 groups. Both the Mian-Straub-Sufi main microfile and the prepared share files are author-modified/derived. |
| `DFA/` (1.7 MB) | **DFA** = Distributional Financial Accounts, Federal Reserve Board. [Overview and downloads](https://www.federalreserve.gov/releases/z1/dataviz/dfa/). | A 2019-vintage set of quarterly group-level CSVs by net worth, income, age, education, race, and generation, plus authors' annual share files. It is not household microdata. | Alternative distributional allocation of Financial Accounts assets and liabilities and a consistency comparison with DINA. Public source plus author aggregation. |
| `scf/` (5.9 GB) | **SCF** = Survey of Consumer Finances, Federal Reserve Board. [Survey and historical downloads](https://www.federalreserve.gov/econres/scfindex.htm). | Repeated family-level cross-sections, 1989–2019 files, five implicates for survey years, combined extracts, and helper Stata code. | Detailed portfolio, income, and imputed-consumption checks. Survey microdata; the combined package files are author-prepared. |
| `SZZ2019/` (133 KB) | **SZZ** = Matthew Smith, Owen Zidar, and Eric Zwick. Their method capitalizes administrative income while allowing heterogeneous returns. [Project description](https://economics.princeton.edu/working-papers/top-wealth-in-america-new-estimates-under-heterogenous-returns/); [authors' materials](https://www.ericzwick.com/). | Two source workbooks from an early paper vintage and `Yszzshares.dta`, an author-prepared annual table for P0–90, P90–99, and P99–100 wealth shares. | Alternative top-wealth distribution, used to test sensitivity to capitalization assumptions. Prepared comparison series, not the confidential tax microdata. |
| `crsp/` (366 MB) | **CRSP** = Center for Research in Security Prices, a licensed securities database. [U.S. stock database description](https://indexes.morningstar.com/research-data-products/crsp-us-stock-databases). | Monthly security file (`msf.dta`), balance-sheet/OTC-GSE support workbooks, and `fof_equity_support.do/.dta`. | Constructs market-value equity support for depository institutions, GSEs, and life insurers in the old Financial Accounts build. Licensed upstream; author-prepared intermediary. |
| `JST/` (872 KB) | **JST** = Òscar Jordà, Moritz Schularick, and Alan Taylor, Macrohistory Database. [Database and documentation](https://www.macrohistory.net/database/). | One annual country-year macro-financial file. | Supplies long-run U.S. house-price and asset-return/valuation series used to separate saving from capital gains. Public research database snapshot. |
| `finalfiles/` (311 MB) | No external acronym: these are Mian-Straub-Sufi outputs. | Thirteen analysis-ready annual and state files, including NIPA analysis, Financial Accounts analysis, unveiled debt, wealth/saving, returns, and controls. | Fastest route to the historical benchmark. Fully downstream author products: reproducing a figure from them validates the analysis stage, not the upstream reconstruction. |

### Income and consumption alternatives

| Folder (size) | Acronym, producer, and source | Unit and contents in this kit | Why the authors use it / replication status |
| --- | --- | --- | --- |
| `PSID/` (29 MB) | **PSID** = Panel Study of Income Dynamics, University of Michigan. [PSID documentation](https://psidonline.isr.umich.edu/Guide/default.aspx). | One author-provided post-1999 family/person panel extract (`small_sample_post1999.dta`) with income and consumption variables; the code calls it the “Ludwig JMP PSID file.” | Alternative consumption shares for income or wealth groups, mainly 1999–2013. Prepared extract; its upstream extraction recipe is not included here. |
| `CEX/` (31 KB) | **CEX/CE** = Consumer Expenditure Surveys, U.S. Bureau of Labor Statistics. [BLS CE program](https://www.bls.gov/cex/). The folder also contains a table from [Aguiar and Bils (2015)](https://www.aeaweb.org/articles?id=10.1257%2Faer.20120599). | Annual aggregate-expenditure shares by decile/quintile and one published comparison table. These are small tables, not raw consumer-unit microdata. | Alternative distribution of consumption and a measurement-error robustness check. Author-prepared/publication-derived. |
| `Fisher/` (10 KB) | Jonathan Fisher and coauthors' income-consumption-wealth work. [Inequality in 3-D project page](https://equitablegrowth.org/working-papers/inequality-3d-income-consumption-wealth/). | Three small annual tables. `Yfisher.dta` contains consumption shares for the top 5 percent and selected quintiles; `Yfisherfinal.dta` maps them to top 1/next 9/bottom 90. | Alternative consumption-distribution calibration. Prepared comparison series, not underlying microdata. |
| `CBO/` (4.2 MB) | **CBO** = Congressional Budget Office. [The Distribution of Household Income, 2016](https://www.cbo.gov/publication/55413). | 2019 report PDFs and supplemental/underlying Excel tables with household income before and after taxes and transfers, 1979–2016. | Alternative income-group shares and income-definition robustness. Public report tables. |
| `IRS/` (150 KB) | **IRS SOI** = Internal Revenue Service, Statistics of Income. [SOI individual-income statistics](https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304). | Two federal tax/income-share workbooks. The filenames alone do not prove that both are untouched IRS releases. | Supporting comparison with tax-return income shares. Treat as prepared workbooks until their exact provenance and vintage are traced. |
| `autensplinter/` (3.1 MB) | Gerald Auten and David Splinter, alternative national-income distribution estimates. [Paper and methodology](https://www.davidsplinter.com/AutenSplinter-Tax_Data_and_Inequality.pdf); [author data site](https://www.davidsplinter.com/). | One source workbook and `Yautensplinter.dta`, with annual pre- and after-tax top 10, top 5, and top 1 percent shares. | Alternative income-distribution benchmark to PSZ/DINA. Publication-derived series. |
| `Kuhnetal/` (15 KB) | Moritz Kuhn, Moritz Schularick, and Ulrike Steins. [Income and Wealth Inequality in America, 1949–2016](https://www.journals.uchicago.edu/doi/10.1086/708815). | Source workbook and `kuhnetaldata.dta`, an annual table of SCF+-based top 5/top 10 income and wealth shares. | Long-run alternative inequality series based on historical SCF waves. Publication-derived series. |

### Older state analysis and restricted/supporting inputs

| Folder (size) | Acronym, producer, and source | Unit and contents in this kit | Why the authors use it / replication status |
| --- | --- | --- | --- |
| `dinastate/` (3.5 GB) | Author-created state DINA derivatives; parent methodology is PSZ DINA. | A sampled state DINA microfile and `SYdinawealth.dta`, a state-year-by-group table of income, wealth, portfolio, tax, and debt components. | Core distributional input for the old state exercise. Derived from restricted state identifiers; not reproducible from public DINA alone. |
| `Sirs/` (7.4 MB) | “S” denotes the authors' state layer; **IRS SOI** is the source. [IRS Historic Table 2](https://www.irs.gov/statistics/soi-tax-stats-historic-table-2). | State-year-by-AGI-bracket returns, AGI, wages, dividends, interest, pensions, and related items for 1979–2016, plus a high-income imputation and state codes. | Constructs state income/asset capitalization inputs. The kit read-me says 1996 onward comes from Historic Table 2 and earlier years were digitized from IRS PDFs. Author-assembled. |
| `WID/` (181 KB) | **WID** = World Inequality Database. [Methodology and downloads](https://wid.world/methodology/). | WID extract/metadata plus `WIDstates20190904.dta`, with state code, percentile, year, and income-share value (for example, P99–100). | State top-income-share comparison in the older analysis. Public-series extract plus author reshape. |
| `census/` (1.5 GB) | U.S. Census population estimates and an **IPUMS USA** harmonized census extract. [Census population estimates](https://www.census.gov/programs-surveys/popest.html); [IPUMS USA](https://usa.ipums.org/usa/). | `censuspop_aggregated.dta` is county-year population/migration data; `census_score.dta` is person-level census microdata with weights, age, education, employment, industry, and occupation. | Population weights, dependency ratios, and skill/education controls for the state analysis. Prepared extracts, not raw Census releases. |
| `cps/` (290 MB) | **CPS ASEC** = Current Population Survey, Annual Social and Economic Supplement; the labels indicate an **IPUMS CPS** extract. [Census CPS overview](https://www.census.gov/programs-surveys/cps/about.html); [IPUMS CPS](https://cps.ipums.org/cps/). | Person-level annual file with weights, state, total income, prior-state/migration status, 1979 onward. | The old code identifies high-income interstate movers and collapses them into a state “rich in-migration” control. Prepared microdata extract. |
| `BEA/` (86 MB) | **BEA** = U.S. Bureau of Economic Analysis, Regional Economic Accounts. [Regional accounts](https://www.bea.gov/data/economic-accounts/regional). | Mainly state industry-employment files and metadata under old SIC and newer NAICS classifications, plus a few macro series. | State employment-composition controls. Public source snapshot. |
| `MSV/` (2.7 MB) | The replication kit does not safely expand “MSV.” Its code comments only say “MSV 2017 deregulation”; this should not be turned into an author citation without further evidence. | One very wide state file. The old code keeps `statecode` and `pc1`; its label is “Dereg. measure,” and the file also contains interstate/intrastate deregulation dates. | Banking-deregulation control in the old state regressions. Exact upstream paper and construction remain to be documented. |
| `Zirs/` (17 MB) | In the authors' naming, “Z” denotes ZIP-code data and “irs” denotes IRS-derived information; it is not a standard agency acronym. Parent source: [IRS SOI geographic data](https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-state-data). | `ZYirsclean.dta`: ZIP-year AGI, wages, number of returns, interest, dividends, pensions, and related tax items. | Ranks ZIP codes into top 10/bottom 90 income groups for the debt-write-down workflow. Author-prepared; exact raw ZIP release/vintage still needs tracing. |
| `callreport/` (37 KB) | Bank **Call Reports** plus restricted Equifax credit data. [FDIC Call Report documentation and data links](https://www.fdic.gov/resources/bankers/bank-financial-reports/). | `Qwritedowns.dta` contains quarterly/monthly mortgage and consumer-credit loan/write-down aggregates; `debtwritedown.dta` is a group-level output; the included code references private ZIP-level Equifax files that are absent. | Allocates consumer and mortgage write-down rates to top 10/bottom 90. Only the supplied output can be benchmarked publicly; the full build cannot be reproduced from this kit. |
| `socsec/` (4 KB) | **SSA/OASDI** = Social Security Administration / Old-Age, Survivors, and Disability Insurance. [Annual Statistical Supplement](https://www.ssa.gov/policy/docs/statcomps/supplement/). | `Ysocsec.dta`, an annual table with Social Security income and cost variables beginning in 1938. | A supporting calculation cited in the old text, not a core Figure 1 input. Prepared table. |

## Storage snapshot: updated 2026-08-09

The sizes in the dictionary come from filesystem metadata, not from scanning all
observations. The data tree has about **45 GB local size** after the user
downloaded the full folder. The three largest `PSZusdina/` files alone are
approximately 17.1 GB, 13.0 GB, and 5.3 GB. Local availability does not justify
scanning all files or duplicating them into project-owned storage.

The selective inspection used for this dictionary read folder/file metadata,
the author-kit read-me, relevant Stata passages, and headers/small samples of a
few compact prepared files. It did not scan every observation in the large
microfiles. Apparent sizes and counts can change if the OneDrive or vendor
snapshot changes.

## Recommended access order

### Tier 1 - historical benchmark

Read only:

- `MSS2021Febreplicationkit/code/`;
- `MSS2021Febreplicationkit/data/finalfiles/`;
- `MSS2021Febreplicationkit/output/`; and
- the package read-me and master file.

This is well below 1 GB and is enough to determine whether the supplied final
files reproduce the February 2021 exhibits. It does **not** constitute an
independent reconstruction.

### Tier 2 - selected upstream reconstruction

Read only the dependency chain of the selected exhibit. For Figure 1 this is
currently `fof/LQpanel_2019Q1.dta`, four bond allocations from
`finalfiles/Yunveilhhd.dta`, `crsp/msf.dta`, and the `NationalInc` series in
`finalfiles/YinequalityNIPAanalysis.dta`. Use selected columns and annual
aggregation as early as economically valid. Do not scan `PSZusdina/`, `scf/`,
or state folders until a traced variable requires them.

### Tier 3 - full historical rebuild

A full master-script rebuild should use an external SSD even though the source
tree is now local. The immutable source tree is about 45 GB, and a safe working
copy plus intermediates requires materially more than that. Reserve at least
100 GB of free SSD space, preferably more, before attempting it.

## What to save in this project

- Keep the vendor tree as the single copy of the authors' files.
- Store only compact, analysis-ready outputs under `Data/processed/`.
- Use `Data/interim/` only for rebuildable caches that prevent repeated scans
  of a large source. Prefer column-pruned, compressed Parquet files.
- Aggregate to the selected result's observation unit as early as the paper's
  method allows, while preserving the required accounting identities.
- Record source path, checksum, producing script, selected columns, filters,
  keys, units, and row counts for every saved artifact.
- Delete or regenerate interim caches rather than preserving several nearly
  identical versions. Never delete vendor inputs.

An external SSD is useful for Tier 3 scratch data and large Parquet extracts.
It is not needed for Tier 1 or either annual Figure 1 result. Canonical
code, documentation, aggregate outputs, and comparison tables should remain in
the project so the replication does not depend on one machine-specific mount.

## Stata safety

Do not run `mss_savingglut_master.do` in the vendor directory. The old scripts
use `replace` and write into `data/`, `finalfiles/`, and `output/`. A safe
benchmark has two modes:

1. **Analysis-only benchmark:** copy the Stata code and output directory to a
   project-owned sandbox, point reads to the immutable supplied `finalfiles/`,
   and redirect every export to the sandbox.
2. **Full rebuild:** use an isolated writable data/interim tree, preferably on
   an external SSD, and record Stata plus community-package versions.

Never interpret successful reproduction of a February 2021 figure as automatic
replication of the revised July 2025 figure. Preserve the paper-version label on
every output.

## Convenience path

`Data/raw/paper_originals/` is a navigation aid only. Its `authors_data`
symlink points to the canonical vendor data tree and consumes no duplicate
storage. Code and provenance records should continue to name
`MSS2021Febreplicationkit/data/` as the authoritative source, and no process may
write through the symlink.
