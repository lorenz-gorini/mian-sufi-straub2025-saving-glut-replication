# Editable presentation source

This folder preserves the durable authoring inputs for the seven-slide Figure
Comparison deck. The final deliverable remains `../presentation.pptx`.

## Contents

- `build_presentation.mjs`: imports the prepared inherited slides, rewrites the
  comparison contract, inserts the Figure 8 full-inverse output, updates
  speaker notes, and exports QA renders;
- `template-starter.pptx`: frozen 18-slide visual source retained from the
  earlier comparison deck;
- `template-frame-map.json`: selects source slides 1, 2, 5, 10, 12, 17, and 18
  and declares every permitted edit;
- `template-audit.txt` and `deviation-log.txt`: template structure and
  intentional departures;
- `source-notes.txt`: comparison provenance; and
- `rebuild_presentation.zsh`: reproducible template-following entry point.

The reusable cropped Figure 6 paper exhibit remains in
`../assets/paper_figure6_no_caption.png`. Generated empirical charts must be
rebuilt by their Python producers before rebuilding this deck if results
change.

## Rebuild

Load `RUNTIME_NODE`, `RUNTIME_NODE_MODULES`, and `RUNTIME_BIN_DIR` from the
presentation runtime, then run from the project root:

```zsh
Presentation/4_figure_comparison/source/rebuild_presentation.zsh
```

The command inspects the frozen source, validates the frame map, creates a
seven-slide starter in `/private/tmp`, writes `../presentation.pptx`, and
retains renders, layout exports, and inspection files in the printed temporary
path. Pass an explicit output path as the first argument to test a build
without replacing the maintained deck.

If the installed presentation skill moves, set `PRESENTATIONS_SKILL_DIR` to its
current absolute directory. Do not commit generated renders, layouts,
inspection sidecars, runtime dependencies, or temporary QA caches.
