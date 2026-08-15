# Extension Proposal

`extension_proposal.tex` is the standalone two-page course-submission
component proposing a financialization and ultimate-risk-bearing extension of
Mian, Straub, and Sufi. `extension_proposal.pdf` is its compiled artifact.

The brief connects Figures 1, 6, and 8, reports the verified mortgage-versus-
consumer-credit evidence as motivation, and proposes a borrower--saver--
intermediary model that separates risk pooling from risk shifting. It extends
nominal ownership unveiling with a state-contingent loss-pass-through layer and
keeps the implemented descriptive accounting distinct from proposed causal
and structural work. It is designed to be combined later with the compact
replication summary and referee report without changing their source files.

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
