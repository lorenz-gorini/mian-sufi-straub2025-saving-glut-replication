# Editable presentation source

This folder contains the durable Artifact Tool inputs for the focused Figure 8
method-comparison deck. The final deliverable is `../presentation.pptx`.

- `build_presentation.mjs` edits only mapped, inherited elements and replaces
  four inherited chart frames with the generated three-route comparison and
  same-vintage operator outputs.
- `template-starter.pptx` and `template-frame-map.json` preserve the visual
  structure inherited from the broader comparison deck.
- `template-audit.txt`, `deviation-log.txt`, and `source-notes.txt` document
  the visual and evidentiary boundary.
- `rebuild_presentation.zsh` creates an isolated temporary workspace, builds
  the deck, and retains QA intermediates at the printed path.

The rebuild requires `RUNTIME_NODE`, `RUNTIME_NODE_MODULES`, and
`RUNTIME_BIN_DIR` from the presentation runtime dependency loader. It does not
install dependencies into the repository.
