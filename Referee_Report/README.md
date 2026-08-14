# Referee Report

`referee_report.md` is the editable source for the course referee report on the
July 25, 2025 draft of *The Saving Glut of the Rich*. It draws on the project's
version-aware replication evidence and includes the Figure 6 five-year
distributional heatmap as a clearly labelled referee diagnostic.

Build the submission files from the project root:

```bash
Referee_Report/source/rebuild_referee_report.zsh
```

The script writes:

- `Referee_Report/output/referee_report.docx`;
- `Referee_Report/output/referee_report.pdf`.

The DOCX uses a patched Pandoc reference document with the
`standard_business_brief` design tokens. The PDF is generated independently
from the same Markdown source with XeLaTeX. Temporary reference documents and
rendered QA pages remain under `tmp/referee_report/` and are not submission
artifacts. The current PDF is three pages: approximately 1.5 pages of referee
text and one page containing the two diagnostic figures.
