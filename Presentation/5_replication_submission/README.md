# Replication submission presentation

`presentation.pptx` is the previously verified 17-slide submission deck.
`source/build_presentation.mjs` now defines the pending 18-slide refresh,
which combines three parts:

1. the theoretical unveiling method;
2. the data lineage and the 2021/2025 version boundary; and
3. comparisons for Figures 1, 5, and 8.

The refreshed deck distinguishes a historical benchmark, an upstream reconstruction,
and a robustness exercise. Figures 1 and 5 are reconstructed from February
2021 authors' inputs. Figure 8 is condensed from
`../6_figure8_method_comparison/`: the primary route reconstructs a coarsened
network from saved 2021 direct/pre-round fields and applies the full inverse;
the old seven-round output is its lineage benchmark; and the public-FWTW route
is a separate mixed-vintage robustness check.

The refreshed opening network visual and theory pacing are inspired by the initial
NotebookLM synthesis slides, but all equations, definitions, and empirical
claims are checked against the July 2025 paper and project evidence.

The revised source has passed `node --check`, but the PowerPoint has not yet
been exported because the required presentation runtime dependency loader was
unavailable in the authoring session. Until it is rebuilt and visually
verified, `presentation.pptx` remains the older 17-slide artifact.

## Build

The source script imports the verified slides from the three component decks,
preserves their editable native elements and speaker-note source blocks, and
relinks embedded images whose PowerPoint asset identifiers collide across the
source files.

Run `source/build_presentation.mjs` in an environment containing
`@oai/artifact-tool` with these variables:

- `MSS_PROJECT_ROOT`: repository root;
- `MSS_DECK_WORKSPACE`: temporary render and audit directory.

The default output is `Presentation/5_replication_submission/presentation.pptx`.
