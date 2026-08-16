# Extension Proposal

`main.tex` is the standalone entry point for the two-page extension proposal.
It imports the body-only `extension_proposal.tex` and produces
`extension_proposal.pdf` with the build command below.

The brief connects Figures 1, 6, and 8, reports the verified mortgage-versus-
consumer-credit evidence as motivation, and proposes a borrower--saver--
intermediary model that separates risk pooling from risk shifting. It extends
nominal ownership unveiling with a state-contingent loss-pass-through layer and
keeps the implemented descriptive accounting distinct from proposed causal
and structural work. The same body is imported into the final combined report
under [`../Submission_Report/`](../Submission_Report/).

Regenerate the displayed numerical values from the project root:

```bash
python Code/scripts/build_extension_proposal_assets.py
```

Then compile from this folder:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -jobname=extension_proposal main.tex
```

The numerical macros under `generated/` consume the verified processed tables
produced by `Code/scripts/build_debt_composition_extension.py`. Do not edit
their values by hand.
