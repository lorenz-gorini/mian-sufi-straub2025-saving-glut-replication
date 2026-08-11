# Data Guide

This document defines how data must be organized and documented. It will become
the canonical inventory during T-002.

The selected-result inventories are [`figure1-data.md`](figure1-data.md),
[`figure5-data.md`](figure5-data.md), and [`figure8-data.md`](figure8-data.md).
They document only the files and columns used by the selected exhibits rather
than reproducing the entire old-package schema.

## Data zones

| Location | Role | Mutation policy |
| --- | --- | --- |
| `MSS2021Febreplicationkit/data/` | Authors' supplied raw, intermediate, and final data | Read-only. Never overwrite, rename, or clean in place. |
| `Data/raw/` | Frozen copies of additional source data needed by this replication | Immutable after acquisition; include source and retrieval metadata. |
| `Data/interim/` | Rebuildable intermediate data | Written only by code; never hand-edited. |
| `Data/processed/` | Validated analysis-ready data | Written only by code from documented inputs. |

Create a zone only when it receives its first real artifact. Do not copy the
entire authors' package into `Data/`; refer to it in place and record checksums
for the files actually used.

## Required inventory

Maintain one row per relevant dataset once T-002 begins:

| Field | Required content |
| --- | --- |
| Dataset ID | Stable, descriptive identifier used in documentation. |
| Path | Project-relative path; identify whether it belongs to the authors or us. |
| Provenance | Publisher/author source, retrieval date or package version, and immutable-file checksum. |
| Format | `.dta`, `.csv`, `.xlsx`, etc., including format/version when relevant. |
| Role | Raw source, intermediate, final authors' file, or our processed file. |
| Unit of observation | For example year, year-percentile, state-year, or instrument-sector-year. |
| Primary key | Columns that uniquely identify a row; uniqueness must be tested. |
| Coverage | Years, groups, geography, and known exclusions. |
| Shape | Rows and columns after reading. |
| Producer/consumer | Script that creates it and selected results that use it. |

## Required schema documentation

For every analysis dataset, document each used column:

| Column | dtype | Unit | Meaning | Source or formula | Missingness | Valid range/categories |
| --- | --- | --- | --- | --- | --- | --- |

Do not document hundreds of unused columns merely because they exist. First
record the full machine-generated schema, then curate the subset needed for
selected results and all merge/key columns.

## Reading and validation contract

At the first boundary:

1. assert that the file exists and has the expected format;
2. select columns explicitly where practical;
3. assert required columns and dtypes/coercions;
4. assert key uniqueness and non-missingness;
5. validate year/group ranges and categorical domains;
6. preserve labels or construct a separate label dictionary for Stata files;
7. fail with a specific error when a structural contract is violated.

Validate once, then pass a trusted representation downstream. Do not scatter the
same checks across transformations and plotting functions.

## Merge documentation

Before each merge, state:

- economic purpose;
- left and right units of observation;
- join keys and expected cardinality (`1:1`, `m:1`, etc.);
- expected coverage and allowed unmatched observations;
- treatment of duplicates and missing keys;
- columns introduced and name-collision policy.

After each merge, report row counts and match categories. Raise an error if
cardinality or allowed unmatched shares are violated.

## Descriptive checklist

For each selected-result dataset, report:

- shape, key uniqueness, time and group coverage;
- missing counts/shares for used columns;
- numeric quantiles, mean, standard deviation, minimum, and maximum;
- counts for categorical variables;
- units and whether variables are levels, flows, stocks, shares of national
  income, or changes relative to a base period;
- economically important identities and their numerical residuals;
- a small, deterministic sample for human inspection.

Descriptives are evidence, not silent cleaning instructions. Do not drop,
impute, winsorize, or recode observations without an explicit rule justified by
the paper or source data.
