# Asset provenance

## `leontief-network-cover.png`

- Purpose: conceptual 16:9 background for the title slide only.
- Generator: OpenAI ImageGen, built-in generation mode.
- Generated: 2026-08-09.
- Quantitative role: none. Exact shares, arrows, matrices, and equations are
  drawn in TikZ/LaTeX elsewhere in the deck.
- Original generated path:
  `/Users/lorenzogorini/.codex/generated_images/019fe2f2-22bc-7322-80dc-684d55a3e88d/exec-86ed13a9-f49c-4b6f-8229-674965a49d1a.png`

Prompt used:

> Use case: scientific-educational. Asset type: 16:9 title-slide background for
> an economics PhD presentation. Create an elegant conceptual illustration of
> financial-network unveiling and a Leontief-style resolution of intermediation
> chains. Use a clean warm-white to pale blue-gray background, an orderly web
> of abstract intermediary nodes on the right, and a restrained burnt-orange
> path resolving toward terminal owners. Preserve generous negative space on
> the left. Use a sophisticated flat editorial style with deep navy, slate,
> warm white, and burnt orange. No text, numbers, equations, bank buildings,
> currency symbols, people, logos, or watermarks; keep links behind nodes and
> avoid misleading quantitative encoding, neon colors, glossy 3D, clutter, and
> stock-photo styling.

This image remains part of the historical Beamer deck. The current PowerPoint
uses a text-led cover and does not depend on it.

## `pptx-veil-chain.dot`

- Purpose: exact conceptual chain from a primary asset through a bank and fund
  to an ultimate owner.
- Generator: Graphviz `dot`.
- Quantitative role: none; arrows encode direction only.
- Embedded output: full theoretical-methodology PowerPoint slide 2 and
  condensed PowerPoint slide 2.

## `pptx-four-sector.dot`

- Purpose: exact four-sector direct-ownership network used in the worked
  Leontief example.
- Generator: Graphviz `neato` using fixed node positions.
- Quantitative role: edge labels reproduce all six nonzero direct ownership
  shares: bank to household/government/fund and fund to
  household/government/bank.
- Legibility rule: node text and edge-share labels are deliberately enlarged
  for normal slide viewing; do not reduce them to diagram-caption size.
- Embedded output: full theoretical-methodology PowerPoint slide 9 and
  condensed PowerPoint slide 5.
