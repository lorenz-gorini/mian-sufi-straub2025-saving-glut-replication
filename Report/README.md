# Replication Report

`report.tex` is the single LaTeX entry point for the course report. It is a
living artifact: add a section only after the corresponding method or result is
documented and verified elsewhere in the repository.

The report records the Leontief operator, the complete four-sector worked
example, the carefully bounded comparison between the 2025 matrix method and
the February 2021 Stata procedure, an authors-data reconstruction of Figure 1,
and a separate newer-data robustness exercise. Generated values are imported from
`Presentation/generated/unveiling_values.tex` and
`Presentation/generated/figure1_values.tex` and
`Presentation/generated/figure1_authors_values.tex`; do not copy or hand-edit
them in the report.

From the project root, regenerate the numerical inputs:

After the editable installation documented in `Code/README.md`, run:

```bash
python Code/scripts/build_unveiling_teaching_assets.py
python Code/scripts/build_figure1.py
python Code/scripts/build_figure1_authors_data.py
```

Compile from `Report/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error report.tex
```

The rendered output is `Report/report.pdf`. The final report must distinguish
proved algebraic equivalence, conceptual consistency, and empirical equality;
these are not interchangeable claims.
