import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const root = process.env.MSS_PROJECT_ROOT;
const workspace = process.env.MSS_DECK_WORKSPACE;
const output = process.env.MSS_DECK_OUTPUT;
if (!root || !workspace || !output) throw new Error("Missing deck environment.");

const source = path.join(workspace, "template-starter.pptx");
const renderDir = path.join(workspace, "final-renders");
const layoutDir = path.join(workspace, "final-layout");
const presentation = await PresentationFile.importPptx(await FileBlob.load(source));

function slide(number) {
  return presentation.slides.items[number - 1];
}

function shape(number, name) {
  const item = slide(number).shapes.items.find((candidate) => candidate.name === name);
  if (!item) throw new Error(`Slide ${number}: missing inherited shape ${name}`);
  return item;
}

function setText(number, name, text) {
  shape(number, name).text = text;
}

function setNotes(number, text) {
  slide(number).speakerNotes.textFrame.setText(text);
}

async function imageBytes(relativePath) {
  const buffer = await fs.readFile(path.join(root, relativePath));
  return buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength);
}

async function replaceImage(number, index, relativePath, alt) {
  const item = slide(number).images.items[index];
  if (!item) throw new Error(`Slide ${number}: missing inherited image ${index}`);
  const frame = item.frame;
  const crop = item.crop;
  const fit = item.fit;
  const geometry = item.geometry;
  const borderRadius = item.borderRadius;
  const rotation = item.rotation;
  const flipHorizontal = item.flipHorizontal;
  const flipVertical = item.flipVertical;
  const lockAspectRatio = item.lockAspectRatio;
  await item.replace({
    blob: await imageBytes(relativePath),
    contentType: "image/png",
    alt,
    ...(fit ? { fit } : {}),
  });
  item.frame = frame;
  item.crop = crop;
  item.geometry = geometry;
  item.borderRadius = borderRadius;
  item.rotation = rotation;
  item.flipHorizontal = flipHorizontal;
  item.flipVertical = flipVertical;
  item.lockAspectRatio = lockAspectRatio;
}

// 1 — title.
setText(1, "eyebrow", "FIGURE 8 METHOD COMPARISON");
setText(1, "title", "Three routes to unveiled net household debt");
setText(1, "subtitle", "Separate the data vintage from the network operator");
setText(1, "legend-2021-text", "Full inverse: B · 2021 direct cells   C · public FWTW");
setText(1, "legend-2025-text", "Seven rounds: A · 2021 final-file benchmark");
setText(1, "date", "14 August 2026");
setNotes(1, "[Sources]\n- docs/project/tasks/figure8-replication.md\n- docs/data/figure8-2021-direct-data.md\n- docs/data/figure8-public-fwtw-data.md\n- Presentation/4_figure_comparison/presentation.pptx (visual source)");

// 2 — common target and three routes.
setText(2, "kicker", "COMMON TARGET");
setText(2, "title", "One estimand, three deliberately separate routes");
setText(2, "slide-number", "02");
setText(2, "question", "2025 Figure 8");
setText(2, "question-body", "ND(g,t) = household-debt assets − debt owed\nScale by national income; subtract 1982");
setText(2, "Strong precursor-label", "A · Old benchmark");
setText(2, "Strong precursor-body", "2021 final debt positions after the authors’ seven-round unveiling; revised display rule only.");
setText(2, "Partial match-label", "B · Primary test");
setText(2, "Partial match-body", "2021 direct/pre-unveiling cells, reconstructed network, and the 2025 full Leontief operator.");
setText(2, "Context only-label", "C · Public robustness");
setText(2, "Context only-body", "Current public FWTW bilateral levels plus 2021 DINA/NIPA and the same full operator.");
setText(2, "boundary-title", "Why three?");
setText(2, "boundary-body", "A→B changes the operator while holding the old vintage as close as saved inputs permit; C tests the method on an independent public network.");
setNotes(2, "[Sources]\n- MSS_SGR_July242025.pdf, Sections 4.1–4.2 and Figure 8\n- Code/unveiling/figure8_authors.py\n- Code/unveiling/figure8_2021_direct.py\n- Code/unveiling/figure8_public_fwtw.py");

// 3 — method crosswalk.
setText(3, "kicker", "METHOD CROSSWALK");
setText(3, "title", "Data and operator choices are now visible separately");
setText(3, "slide-number", "03");
setText(3, "verdict-cell-0-0", "Object");
setText(3, "verdict-cell-0-1", "Input");
setText(3, "verdict-cell-0-2", "Operator");
setText(3, "verdict-cell-0-3", "Interpretation / boundary");
setText(3, "verdict-cell-1-0", "2025 target");
setText(3, "verdict-cell-1-1", "Authors’ 2019 vintage");
setText(3, "verdict-cell-1-2", "Full inverse");
setText(3, "verdict-cell-1-3", "34 instruments; 23 intermediaries + 4 owners; custom equity extension");
setText(3, "verdict-cell-2-0", "A · Old benchmark");
setText(3, "verdict-cell-2-1", "2021 final file");
setText(3, "verdict-cell-2-2", "Seven rounds");
setText(3, "verdict-cell-2-3", "Starts after old unveiling; validates the older supplied pipeline");
setText(3, "verdict-cell-3-0", "B · Primary test");
setText(3, "verdict-cell-3-1", "2021 direct cells");
setText(3, "verdict-cell-3-2", "Full inverse");
setText(3, "verdict-cell-3-3", "351 saved direct fields; eight coarsened intermediary rows; no round fields read");
setText(3, "verdict-cell-4-0", "C · Robustness");
setText(3, "verdict-cell-4-1", "Public 2026 FWTW");
setText(3, "verdict-cell-4-2", "Full inverse");
setText(3, "verdict-cell-4-3", "31 instruments; 25 substantive sectors; independent current taxonomy");
setText(3, "verdict-cell-5-0", "Common layer");
setText(3, "verdict-cell-5-1", "2021 DINA/NIPA");
setText(3, "verdict-cell-5-2", "Through 2016");
setText(3, "verdict-cell-5-3", "Same groups, net-debt sign, national-income scale, and 1982 base");
setText(3, "verdict-cell-6-0", "Identification");
setText(3, "verdict-cell-6-1", "A versus B");
setText(3, "verdict-cell-6-2", "Closest operator test");
setText(3, "verdict-cell-6-3", "Not exact: the kit does not save the full 34×27 annual direct cube");
setText(3, "takeaway-title", "Hierarchy");
setText(3, "takeaway-body", "Lead with B; use A as the older-code benchmark and C as a public-data robustness check.");
setNotes(3, "[Sources]\n- MSS_SGR_July242025.pdf, Sections 2.2 and 4.1; Table A1\n- docs/data/figure8-data.md\n- docs/data/figure8-2021-direct-data.md\n- docs/data/figure8-public-fwtw-data.md");

// 4 — primary same-vintage pipeline.
setText(4, "kicker", "PRIMARY IMPLEMENTATION");
setText(4, "title", "Restart upstream, then replace seven rounds with the full inverse");
setText(4, "slide-number", "04");
setText(4, "question", "Question");
setText(4, "question-body", "Can the 2021 direct vintage support the 2025 operator without using any seven-round outputs?");
setText(4, "Strong precursor-label", "1 · Recover cells");
setText(4, "Strong precursor-body", "Read 351 pre-unveiling fields; rebuild mutual-fund allocation and eight intermediary rows.");
setText(4, "Partial match-label", "2 · Complete network");
setText(4, "Partial match-body", "Clip signed artifacts, balance to kit margins, split households by DINA, solve Ω = (I − Q)⁻¹B.");
setText(4, "Context only-label", "3 · Net debt");
setText(4, "Context only-body", "Trace household-debt assets to ultimate owners; subtract group mortgage and nonmortgage debt.");
setText(4, "boundary-title", "Verified boundary");
setText(4, "boundary-body", "Zero seven-round variables read; source debt margins close within \$2 million and unveiled ownership rows within 4.5×10⁻¹⁶.");
setNotes(4, "[Sources]\n- MSS_SGR_July242025.pdf, equations (1), (3), and (4); Sections 4.1–4.2\n- Code/unveiling/figure8_2021_direct.py\n- Data/interim/figure8_2021_direct_network_diagnostics.csv\n- Data/interim/figure8_2021_direct_component_diagnostics.csv");

// 5 — public-data robustness and exact boundary.
setText(5, "kicker", "PUBLIC-DATA ROBUSTNESS");
setText(5, "title", "Public FWTW tests portability—not a same-vintage effect");
setText(5, "slide-number", "05");
setText(5, "question", "Classification");
setText(5, "question-body", "Same full operator\nDifferent completed direct matrix");
setText(5, "Strong precursor-label", "1 · Public FWTW");
setText(5, "Strong precursor-body", "June 2026 release: 31 instruments and 25 substantive sectors, already completed by the Fed.");
setText(5, "Partial match-label", "2 · Common layer");
setText(5, "Partial match-body", "Reuse 2021 DINA group shares and authors-kit national income; stop in 2016.");
setText(5, "Context only-label", "3 · Full solve");
setText(5, "Context only-body", "Split household holders, reorient negative positions, and apply the same Leontief operator.");
setText(5, "boundary-title", "Interpretation");
setText(5, "boundary-body", "Useful robustness, but operator, vintage, taxonomy, completion algorithm, and corporate-equity coverage differ from the paper.");
setNotes(5, "[Sources]\n- MSS_SGR_July242025.pdf, Section 2.2\n- https://www.federalreserve.gov/releases/efa/fwtw.htm\n- https://www.federalreserve.gov/releases/efa/fwtw_announcements.htm\n- Data/raw/README.md\n- docs/data/figure8-public-fwtw-data.md");

// 6 — paper plus three empirical routes.
setText(6, "kicker", "FIGURE 8 METHOD COMPARISON");
setText(6, "title", "All routes recover the split; level gaps remain");
setText(6, "slide-number", "06");
setText(6, "left-label", "Top 1% · paper plus three routes");
setText(6, "right-label", "Bottom 99% · paper plus three routes");
setText(6, "verdict", "TREND ROBUST");
setText(6, "assessment", "Top-1 MAE: 2.33 pp for 2021-direct/full vs 2.41 proxy; public/full is 2.12 pp.");
setText(6, "difference", "Bottom-99 MAE: 1.31 pp for 2021-direct/full vs 1.38 proxy; public/full is 1.98 pp.");
await replaceImage(6, 0, "Results_Proposal/figures/figure8_method_comparison_top1.png", "Top 1 percent Figure 8 method comparison");
await replaceImage(6, 1, "Results_Proposal/figures/figure8_method_comparison_bottom99.png", "Bottom 99 percent Figure 8 method comparison");
setNotes(6, "[Sources]\n- MSS_SGR_July242025.pdf, Figure 8, physical page 29; digitized benchmark\n- Results_Proposal/figures/figure8_method_comparison_top1.png\n- Results_Proposal/figures/figure8_method_comparison_bottom99.png\n- Data/processed/figure8_method_comparison_metrics.csv");

// 7 — closest operator comparison and reconstruction boundary.
setText(7, "kicker", "SAME-VINTAGE OPERATOR TEST");
setText(7, "title", "The full inverse changes the old network only modestly");
setText(7, "slide-number", "07");
setText(7, "left-label", "B minus A · full inverse minus seven rounds");
setText(7, "right-label", "B · 2021 direct cells + full inverse");
setText(7, "verdict", "TRUNCATION IS NOT THE MAIN GAP");
setText(7, "assessment", "Mean |B−A|: 0.26 pp top 1% and 0.75 pp bottom 99%; 2007 differences are −0.56 and −2.15 pp.");
setText(7, "difference", "Caveat: signed-cell clipping absorbs 8.5–37.8% of gross debt-cell mass; 3.2–10.0% remains unassigned after coarsening.");
await replaceImage(7, 0, "Results_Proposal/figures/figure8_2021_operator_comparison.png", "Same-vintage Figure 8 full-Leontief minus seven-round comparison");
await replaceImage(7, 1, "Results_Proposal/figures/figure8_2021_direct_full_leontief.png", "2021 direct-cell full-Leontief Figure 8 reconstruction");
setNotes(7, "[Sources]\n- Results_Proposal/figures/figure8_2021_operator_comparison.png\n- Results_Proposal/figures/figure8_2021_direct_full_leontief.png\n- Data/processed/figure8_2021_operator_comparison_metrics.csv\n- Data/interim/figure8_2021_direct_network_diagnostics.csv");

// 8 — synthesis.
setText(8, "kicker", "REPLICATION SYNTHESIS");
setText(8, "title", "Lead with the same-vintage test; keep both comparators");
setText(8, "slide-number", "08");
setText(8, "question", "Submission choice");
setText(8, "question-body", "Primary: 2021 direct cells + full inverse.\nBenchmarks: old final file and public FWTW.");
setText(8, "Strong precursor-label", "Main result");
setText(8, "Strong precursor-body", "Route B restarts before unveiling and applies the 2025 operator to the old data vintage through 2016.");
setText(8, "Partial match-label", "Two distinct checks");
setText(8, "Partial match-body", "Route A validates the supplied older pipeline; Route C tests the method on current public bilateral data.");
setText(8, "Context only-label", "Economic conclusion");
setText(8, "Context only-body", "All three show rising top-1 net lending and increasingly negative bottom-99 net debt after 1982.");
setText(8, "boundary-title", "Report explicitly");
setText(8, "boundary-body", "The small A→B gap suggests seven-round truncation is not the main paper discrepancy; matrix coverage, completion, taxonomy, and wealth mapping remain.");
setNotes(8, "[Sources]\n- docs/project/tasks/figure8-replication.md\n- docs/data/figure8-2021-direct-data.md\n- docs/data/figure8-public-fwtw-data.md\n- Data/processed/figure8_method_comparison_metrics.csv\n- MSS_SGR_July242025.pdf, Figure 8");

await fs.mkdir(renderDir, { recursive: true });
await fs.mkdir(layoutDir, { recursive: true });
for (let index = 0; index < presentation.slides.items.length; index += 1) {
  const current = presentation.slides.items[index];
  const number = String(index + 1).padStart(2, "0");
  const png = await presentation.export({ slide: current, format: "png", scale: 1.5 });
  await fs.writeFile(path.join(renderDir, `slide-${number}.png`), new Uint8Array(await png.arrayBuffer()));
  const layout = await current.export({ format: "layout" });
  await fs.writeFile(path.join(layoutDir, `slide-${number}.layout.json`), await layout.text());
}
const montage = await presentation.export({ format: "webp", montage: true, scale: 1 });
await fs.writeFile(path.join(workspace, "final-montage.webp"), new Uint8Array(await montage.arrayBuffer()));
const inspect = await presentation.inspect({
  kind: "slide,textbox,shape,image,notes,layout",
  include: "id,slide,name,title,text,textPreview,textChars,textLines,bbox,bboxUnit,isPlaceholder,alt",
  maxChars: 240000,
});
await fs.writeFile(path.join(workspace, "final-inspect.ndjson"), `${inspect.ndjson}\n`, "utf8");
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(output);
await fs.rm(`${output}.inspect.ndjson`, { force: true });
console.log(output);
