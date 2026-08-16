# Rich Saving Glut Replication

This workspace is for an independent, selective replication of the main results
in Mian, Straub, and Sufi's saving-glut project. The objective is not to rerun
every file in the authors' package. It is to understand the measurement,
accounting, and empirical steps well enough to reproduce a small set of central
results with transparent, documented code.

## Start here

1. Read [`AGENTS.md`](AGENTS.md) for the research objective, source hierarchy,
   project structure, and working rules.
2. Read [`docs/project/progress.md`](docs/project/progress.md) before starting
   substantial work. It is the only authoritative task dashboard.
3. Read the task record linked by the dashboard when a task spans multiple
   sessions or contains methodological decisions.
4. Read the compact
   [`author-kit quickstart`](docs/reference/author-kit-quickstart.md) before
   using the authors' package; consult the detailed
   [`author-kit map`](docs/reference/author-kit-map.md) only when a result needs
   a deeper code or data trace.

## Current state

The project has been initialized, the authors' package has been mapped, and the
Leontief unveiling operator has been implemented and tested. Figure 1 now has
a selective authors-data reconstruction plus a separate newer-public-data
robustness result; see `docs/project/progress.md` for the precise evidence
boundary. The authoritative target
paper is the 66-page July 25, 2025 draft
`MSS_SGR_July242025.pdf`. The paper states that it is a
heavily revised version of the earlier draft titled *The Saving Glut of the Rich
and the Rise in Household Debt*. `MSS2021Febreplicationkit/` corresponds to that
earlier version, so it is a valuable but non-identical implementation reference.
Figure numbers, dates, methodology, and results must be crosswalked rather than
assumed to match.

The compact replication submission artifacts are now available as the editable
17-slide `Presentation/5_replication_submission/presentation.pptx` and the
seven-page `Submission_Report/submission_report.pdf`, which combines the
referee report, compact replication summary, and extension proposal. The
longer `Report/report.tex` remains the detailed technical companion.

`NotebookLM-Present-Unveiling_the_Rich_Saving_Glut.pdf` is a
15-page, image-only NotebookLM synthesis of the newer paper. Use it for
orientation only.

The approved replication scope is Figures 1, 5, and 8, with Figure 9 as a
time-permitting extension. The project is explicitly learning-first: equations,
economic intuition, units, sign conventions, assumptions, and data lineage must
be explained in markdown and summarized in a consistent visual presentation as
the code is developed.

## Main folders

| Path | Purpose |
| --- | --- |
| `MSS_SGR_July242025.pdf` | Authoritative July 25, 2025 target paper. |
| `MSS2021Febreplicationkit/` | Authors' code, data, and outputs. Treat as read-only reference material. |
| `Code/` | This project's independent implementation, tests, and exploratory notebooks. |
| `Data/` | This project's data artifacts. See `docs/data/data-guide.md` before adding files. |
| `Results_Proposal/` | Candidate and selected replication targets, acceptance criteria, and result-level notes. |
| `Presentation/` | A concise, reproducible progress presentation for discussion and feedback. |
| `Report/` | The living LaTeX course report; include only documented and verified methods or results. |
| `Referee_Report/` | Editable referee-report source, reproducible build scripts, and local submission files. |
| `Submission_Report/` | Final combined LaTeX entry point and written-submission artifact. |
| `docs/` | Canonical project, data, and reference documentation. |

## Repository boundary

Git tracks the project's documentation, code, tests, and editable report and
presentation sources. It deliberately does not redistribute the authors'
45 GB replication package, external paper PDFs, large downloadable raw data,
copied or generated datasets, compiled documents, caches, or temporary render
output. These local inputs retain the paths used throughout the documentation:

- place the February 2021 author package at `MSS2021Febreplicationkit/`;
- place the authoritative target paper at `MSS_SGR_July242025.pdf`; and
- obtain the pinned public inputs described, with checksums, in
  [`Data/raw/README.md`](Data/raw/README.md).

This boundary keeps the Git history reviewable without weakening provenance:
source versions, retrieval dates, checksums, producing scripts, and generated
output paths remain documented in the tracked files.
