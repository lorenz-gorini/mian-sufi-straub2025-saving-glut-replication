# Extension Proposal

`extension_proposal.tex` is the standalone two-page course-submission
component proposing a debt-composition and ultimate-financing extension of
Mian, Straub, and Sufi. `extension_proposal.pdf` is its compiled artifact.

The brief begins with Figure 6 and the project's time-resolved saving-rate
heatmap, reports the verified mortgage-versus-consumer-credit evidence, and
separates the implemented descriptive accounting from the proposed causal
research. It is designed to be combined later with the compact replication
summary and referee report without changing their source files.

Regenerate the displayed numerical values from the project root:

```bash
python Code/scripts/build_extension_proposal_assets.py
```

Then compile from this folder:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error extension_proposal.tex
```

The numerical macros under `generated/` consume the verified processed tables
produced by `Code/scripts/build_debt_composition_extension.py`. Do not edit
their values by hand.
