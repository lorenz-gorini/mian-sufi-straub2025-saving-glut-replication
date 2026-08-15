# T-007: Historical Benchmark, Selective Hydration, and New-Data Robustness

## Objective

Separate three forms of evidence that answer different questions:

1. **Historical benchmark:** do the authors' February 2021 final data and Stata
   analysis reproduce the February 2021 outputs?
2. **Independent reconstruction:** can the selected result be rebuilt from the
   earliest feasible authors' inputs in readable project-owned code?
3. **New-data robustness:** does the same economic pattern survive in a newer
   public data vintage?

The first two are the replication exercise. The third is useful robustness
evidence but cannot be presented as a substitute for same-input replication.

## Current evidence and storage decision

On 2026-08-08, a metadata-only audit found:

- about 45 GB apparent size in `MSS2021Febreplicationkit/data/`;
- about 37 GiB free on the internal disk;
- about 33 GB in `PSZusdina/`, 5.9 GB in `scf/`, 3.5 GB in
  `dinastate/`, and 1.5 GB in `census/`; and
- only about 311 MB in `finalfiles/`.

The full 45 GB vendor data tree was downloaded by the user by 2026-08-09. The
default policy is to treat it as read-only reference material. On 2026-08-09,
the user explicitly authorized one in-place full-pipeline test and accepted
that generated datasets and outputs would be replaced. The tree is therefore
no longer a pristine downloaded snapshot; this exception does not authorize
unrecorded future mutations. The deadline-first access policy still applies:

1. read only the folders and variables traced from a selected exhibit;
2. save compact annual/group-level outputs, not duplicate microdata; and
3. use an external SSD only if a full upstream rebuild would create large
   project-owned intermediates.

The detailed folder map and storage rules are in
[`../../data/author-kit-data-map.md`](../../data/author-kit-data-map.md).
`Data/raw/paper_originals/authors_data` is a convenience symlink to the
canonical vendor data and does not duplicate storage.

## Source-dictionary refinement

The folder map now distinguishes public upstream sources, author-modified
microfiles, author-prepared aggregate shares, licensed sources, and outputs
whose reconstruction requires restricted data. Every one of the 26 data
folders has a producer/source, supplied observation level, economic role, and
public methodology or data link where one could be identified safely.

The main conceptual clarification concerns DINA. `usdina19622016.dta` is a
weighted record-level distributional file, not merely a quantile table. The
authors collapse its income, wealth, asset, and liability amounts into annual
group shares such as `Yszshares.dta`, then apply those shares to Financial
Accounts category totals. This is a distributional allocation, not a
household-by-household match between DINA records and financial institutions.
The baseline allocation is sorted by wealth; `YszsharesIS.dta` is the
income-sorted alternative.

The dictionary deliberately leaves “MSV” unexpanded because the kit only
labels it “MSV 2017 deregulation” and does not supply enough evidence for a
safe citation. Similar unresolved provenance is marked explicitly rather than
inferred from filenames.

## Stata safety boundary and executed exception

By default, do not run
`MSS2021Febreplicationkit/mss_savingglut_master.do` in place because its scripts
use `replace` and write into vendor `data/`, `finalfiles/`, and `output/` paths.

For the first benchmark, use an isolated copy of the analysis code and redirect
outputs while reading the supplied final files. A full rebuild requires an
isolated writable data/interim tree and a record of the Stata and community
package versions.

The user overrode that default for the 2026-08-09 pipeline test: they asked for
the master to run in place, explicitly accepted overwritten outputs, and noted
that the original folder could be downloaded again. The resulting run is an
execution/reconstruction check, not a byte-for-byte comparison against the
now-overwritten downloaded outputs.

## 2026-08-09 full master execution

The entry point `mss_savingglut_master.do` completed in batch mode under
StataNow SE 19.5. The final uninterrupted log ends after `mss_analysis.do` with
both nested do-files closing normally and contains no uncaptured `r(...)`
return code. All four authored builders completed before the analysis stage:

1. NIPA saving data;
2. Financial Accounts and intermediary unveiling data;
3. wealth-saving data; and
4. state-level wealth data.

The final run regenerated 18 nonempty principal `.dta` files in
`data/finalfiles/`, `data/PSZusdina/`, and `data/dinastate/`, and produced 45
nonempty analysis artifacts in `output/`: 22 EPS figures and 23 TeX tables.
All 18 datasets were reopened successfully in a separate Stata audit using the
master's `set maxvar 32000` requirement; they range from 5 observations/71
variables (`YconsshareSCF.dta`) to 2,240,765 observations/228 variables
(`usdina19792008statessampled.dta`). The master log is
`MSS2021Febreplicationkit/mss_savingglut_master.log`.

### Portability and batch-mode changes

- The master root was set to this checkout and Windows path separators in
  executable Stata path globals were normalized to `/` in the master and the
  five referenced do-files. This changes file resolution only.
- The interactive `browse` call at `code/mss_analysis.do:333` was changed to
  `capture noisily browse ...`. Stata batch mode has no Data Browser, so the
  command still reports `command browse is unrecognized` in the log but no
  longer aborts. It does not create, transform, estimate, or export anything.
- Messages of the form `(variable ... not found)` occur inside authored
  captured cleanup commands. They are nonfatal; there is no corresponding
  uncaptured Stata return code.

No statistical specification, sample restriction, variable construction,
weight, merge, sign convention, table statistic, or graph command was changed.

### Installed community commands

The commands below were installed from SSC. Versions were recorded from the
ado-file headers after the successful run:

| Package/command | Recorded version | Pipeline role |
| --- | --- | --- |
| `tabstatmat` | 1.4.4 (2011-02-25) | collect saved `tabstat` results into matrices |
| `egenmore` / `_gxtile` | 2.1 (2019-01-14) | grouped quantile construction |
| `gtools` / `gcollapse` | 1.3.1 (2021-11-03) | large weighted collapses |
| `missings` | 1.4.0 (2023-01-27) | state-data missing-observation cleanup |
| `ereplace` | 1.0.3 | grouped replacement |
| `labutil` / `labmask` | 1.0.0 (2002-08-20) | value labels from variables |
| `outreg` / `frmttable` | 1.32 (2015-09-18) | formatted TeX matrix tables |
| `ftools` | 2.50.0 (2026-01-09) | high-dimensional fixed-effect backend |
| `reghdfe` | 6.13.1 (2026-01-10) | fixed-effect regressions |
| `estout` / `esttab` | 2.1.4 (2026-04-13) | regression tables; also supplies `eststo` and `estadd` |
| `require` | 1.3.1 (2023-09-19) | dependency management required by current `reghdfe` |
| `ranktest` | 2.0.04 (2020-09-21) | IV rank diagnostics |
| `ivreg2` | 4.1.12 (2024-08-14) | IV estimator backend |
| `ivreghdfe` | 1.1.4 (2025-11-29) | IV regressions with absorbed fixed effects |

These are installation/environment changes. The newer package vintages are a
remaining historical-reproducibility qualification: successful execution does
not by itself establish numerical identity to the authors' original Stata and
ado environment.

The master now calls `code/mss_dependencies.do`. That bootstrap checks each
required command, installs its SSC package only when the command is absent,
then checks again and fails with a clear message if installation did not make
the command available. Existing installations are not upgraded. This is a
convenient clean-machine bootstrap, not exact version pinning: archival
replication would require vendoring the tested ado files and prepending that
directory to Stata's `adopath`.

## Manual exhibit benchmark

The exact February 2021 NBER revision is stored as `MSS_SGR_Feb2021.pdf` and
mapped to regenerated outputs in
[`../../reference/author-output-crosswalk.md`](../../reference/author-output-crosswalk.md).
Figures 1, 3, 4, 6, 7, 8, and 9 were rendered and checked visually against the
paper. Regenerated Table 7 matches all reported values to three decimals. The
crosswalk separately labels relationships to the July 2025 figures so an exact
old-draft benchmark is not mistaken for an exact revised-paper replication.

The nine-slide audit in
`Presentation/1_replication_package_validation/replication_package_validation.pptx`
is the presentation-facing completion evidence. It was rendered back to PNG,
inspected at full size, and archive-checked on 2026-08-09. This closes T-007:
the remaining July 2025 feasibility work belongs to T-001 through T-004 and is
not a reason to leave the historical benchmark open.

## Presentation requirement

The legacy combined deck states the evidence hierarchy before displaying
Figure 1. The two-frame insert
`Presentation/0_legacy_combined_deck/sections/replication_strategy.tex` is
included near the beginning of
`Presentation/0_legacy_combined_deck/presentation.tex`.

## Figure 1 authors-data reconstruction

The downloaded tree permits a meaningful intermediate benchmark without
rebuilding every source table. `Code/scripts/build_figure1_authors_data.py`
starts from the authors' prepared `LQpanel_2019Q1.dta`, reconstructs four bond
issuer-holder cells and the household equity share from its Q4 columns,
rebuilds listed financial equity from the raw CRSP monthly file, and normalizes
by the preserved national-income series. `Yunveilhhd.dta` is now a validation
target and approximate-denominator input, not a Figure 1 numerator input. The
code therefore skips mechanical imports and wide merges but explicitly retains
the central missing-cell allocation and instrument aggregation.

For 1963--2016, the reconstructed stock behind the veil divided by national
income has correlation 0.995 and mean absolute error 5.3 percentage points of
national income relative to the digitized 2025 Figure 1 curve. The ownership
share is less exact: the broad-denominator version has mean absolute error 3.2
percentage points. The missing completed 2025 matrices and revised denominator
crosswalk prevent an exact reproduction label.

Every reconstructed household bond cell matches the preserved Stata
intermediate within \$0.05 million; the maximum absolute discrepancy is
\$0.03615 million. This verifies the Python transcription of the old
proportional allocation rules without importing their downstream output into
the numerator.

The user ran parts of the Stata package in the vendor tree before this audit,
so some vendor final-file hashes differ from the preserved downloaded copies.
For `Yunveilhhd.dta`, all numerical values and missing-value locations used by
this reconstruction are identical. The current and preserved national-income
files also agree exactly on the `NationalInc` series used here. This validates
the selected inputs but does not replace an isolated full historical run.

## Definition of done

- [x] Folder-level apparent sizes and roles are documented selectively.
- [x] Every data folder has an acronym/source, supplied granularity, economic
      role, public reference where available, and replication-status label.
- [x] The DINA microfile-to-group-share-to-Financial-Accounts bridge is
      documented explicitly.
- [x] The no-duplication convenience link is present and resolves correctly.
- [x] Historical benchmark, reconstruction, and robustness are conceptually
      separated.
- [x] The Stata in-place execution risk is explicit.
- [x] The two presentation frames are written and independently rendered.
- [x] Canonical Markdown and Beamer sources are locally readable again, and the
      dashboard links to this task record.
- [x] Remaining result-selection and presentation records cross-link the
      benchmark/reconstruction/robustness hierarchy.
- [x] The frames are included in the main deck and the complete PDF is visually
      verified.
- [x] An authors-data Figure 1 reconstruction from selected authors' inputs is
      generated, tested, and compared quantitatively with the paper curve.
- [x] The February 2021 full master pipeline is executed successfully under a
      recorded Stata/package environment, using the user-authorized in-place
      exception.
- [x] Major regenerated figures are visually matched to the exact February
      2021 revision, and regenerated Table 7 matches the published values to
      three decimals.

## Decision log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-08-08 | Same-input historical reproduction comes before new-data robustness in the evidence hierarchy. | It directly tests whether the supplied replication package reproduces the version it accompanies. |
| 2026-08-08 | Do not hydrate the full 45 GB tree on the internal disk. | Apparent source size exceeds the currently reported free space and most bytes are irrelevant to the selected exhibits. |
| 2026-08-08 | Use supplied final files for the first benchmark. | This is the fastest way to validate the old analysis stage while preserving a clear distinction from upstream reconstruction. |
| 2026-08-08 | Keep the vendor tree immutable and redirect all Stata writes. | The old scripts use `replace`; running them in place could overwrite author-supplied evidence. |
| 2026-08-08 | Treat DINA as a weighted distributional microfile whose group shares allocate macro totals, not as a quantile-only table or a person-to-bank linkage. | This matches the author read-me, the DINA construction, and the `Yszshares*.dta` build code. |
| 2026-08-08 | Mark unresolved acronym and vintage provenance instead of inferring it from folder names. | Folder labels such as `MSV` are insufficient evidence for an exact source citation. |
| 2026-08-09 | Retain selective access even after the full vendor tree became local. | Reading only exhibit-relevant files protects time and prevents unnecessary large processed copies. |
| 2026-08-09 | Start Figure 1 from the authors' prepared wide balance-sheet panel but rebuild the substantive intermediary-instrument aggregate. | Mechanical imports and merges add little learning value; the aggregation defining the object behind the veil is central to the paper and must remain visible. |
| 2026-08-09 | Treat the national-income-normalized result as a close old-vintage authors-data reconstruction, not an exact 2025 replication. | Its curve matches tightly, but the older kit lacks the revised completed matrices and exact ownership-share denominator. |
| 2026-08-09 | Honor the user's explicit request to run the full authors' master in place and replace generated outputs. | The purpose was to test the authors' actual upstream pipeline; the user accepted loss of the pristine generated files and can re-download the kit. The exception, package environment, code portability changes, and resulting artifacts are recorded above. |
| 2026-08-10 | Close T-007 and route all remaining July 2025 questions to the selected-result tasks. | The master run, exact 2021-paper output crosswalk, manual figure checks, Table 7 numerical match, and verified validation deck satisfy the historical benchmark definition of done. |
| 2026-08-10 | Replace the Figure 1 bond numerator input with a Python reconstruction from the Q4 panel. | The supplied Stata cells should validate the reconstruction, not predetermine it; all four categories now match within \$0.05 million. |

## Session record: 2026-08-10 closure review

- Starting version: the workspace is not recognized as a Git worktree, so no
  branch or commit identifier is available.
- Goal: decide whether yesterday's Stata work completed an existing task or
  merely advanced the July 2025 reconstruction.
- Evidence reviewed: successful full master log, regenerated-output inventory,
  February 2021 exhibit crosswalk, seven visual figure comparisons, Table 7
  three-decimal match, and the rendered validation deck.
- Result: T-007 is complete as a February 2021 historical benchmark. It does
  not claim that the July 2025 figures have been replicated.
- Next action: use the verified old outputs and supplied data as inputs to the
  T-001 Figure 5/8 feasibility audit.
