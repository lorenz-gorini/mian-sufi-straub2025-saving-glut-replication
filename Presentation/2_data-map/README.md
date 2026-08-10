# Data-architecture presentation

This folder contains the standalone deck explaining how the main data
sources enter the Mian, Straub, and Sufi replication. It deliberately excludes
the detailed Leontief derivation and worked ownership-network example, which
belong in the separate theoretical-methodology presentation.

## Scope

The deck explains:

- what Financial Accounts/FWTW, DINA/DFA/SCF, NIPA, and valuation sources each
  identify;
- how the instrument-level dollar matrices are constructed and balanced;
- why DINA splits the household sector only after the direct network exists;
- which data branches feed target-paper Figures 1, 5, and 8;
- how the February 2021 builders map into the July 2025 methodology; and
- the benchmark, reconstruction, robustness, and storage workflow.

The canonical editable deliverable is `presentation.pptx`. Its 12 slides use
the project-wide PowerPoint hierarchy: a one-line takeaway title, two bounded
content zones, one `WHY IT MATTERS` band, and a separate source rail.
`presentation.pptx.inspect.ndjson` is the generated structural inspection
record.

`presentation.tex` and `presentation.pdf` are retained as historical Beamer
artifacts and are not visually synchronized with the PowerPoint.

## Historical Beamer build

From this folder, run:

    latexmk -pdf -interaction=nonstopmode -halt-on-error presentation.tex

Clean auxiliary files with:

    latexmk -c presentation.tex

## Maintenance

Keep this deck limited to data provenance, transformations, and figure
dependencies. Update it whenever a selected exhibit reveals a new source,
mapping, version discrepancy, or identifying limitation. Do not edit the
authors' replication kit or write generated outputs inside it.

All future changes must follow `../README.md`: keep the main message visually
dominant, place definitions and qualifications in subordinate text, maintain
deliberate whitespace between message layers, and render every slide before
delivery.
