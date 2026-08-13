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
setText(1, "title", "Two routes to unveiled net household debt");
setText(1, "subtitle", "Same 2025 estimand; different upstream data and network operators");
setText(1, "legend-2021-text", "Preferred: public FWTW + full Leontief reconstruction");
setText(1, "legend-2025-text", "Retained: 2021-kit + seven-round proxy");
setText(1, "date", "13 August 2026");
setNotes(1, "[Sources]\n- docs/project/tasks/figure8-replication.md\n- docs/data/figure8-public-fwtw-data.md\n- Presentation/4_figure_comparison/presentation.pptx (visual source)");

// 2 — common target and two routes.
setText(2, "kicker", "COMMON TARGET");
setText(2, "title", "Both routes estimate the same net-debt object");
setText(2, "slide-number", "02");
setText(2, "question", "2025 Figure 8");
setText(2, "question-body", "ND(g,t) = household-debt assets − debt owed\nScale by national income; subtract 1982");
setText(2, "Strong precursor-label", "Paper target");
setText(2, "Strong precursor-body", "Augment the household owner by wealth group, fully unveil the network, then isolate household debt.");
setText(2, "Partial match-label", "Preferred route");
setText(2, "Partial match-body", "Published FWTW bilateral levels + 2021 DINA/NIPA + full Leontief inverse.");
setText(2, "Context only-label", "Retained route");
setText(2, "Context only-body", "Authors’ final seven-round debt positions + the same group, sign, scale, and base rule.");
setText(2, "boundary-title", "Naming rule");
setText(2, "boundary-body", "Call the new result a public-FWTW full-Leontief reconstruction—not an exact reproduction of the unavailable authors’ 2025 vintage.");
setNotes(2, "[Sources]\n- MSS_SGR_July242025.pdf, Sections 4.1–4.2 and Figure 8\n- Code/unveiling/figure8_public_fwtw.py\n- Code/unveiling/figure8_authors.py");

// 3 — method crosswalk.
setText(3, "kicker", "TWO APPROACHES");
setText(3, "title", "Only the new route rebuilds the direct network");
setText(3, "slide-number", "03");
setText(3, "verdict-cell-0-0", "Object");
setText(3, "verdict-cell-0-1", "Input");
setText(3, "verdict-cell-0-2", "Operator");
setText(3, "verdict-cell-0-3", "Interpretation / boundary");
setText(3, "verdict-cell-1-0", "2025 target");
setText(3, "verdict-cell-1-1", "Custom 2019 vintage");
setText(3, "verdict-cell-1-2", "Full inverse");
setText(3, "verdict-cell-1-3", "34 instruments; 23 intermediaries + 4 owners; custom equity extension");
setText(3, "verdict-cell-2-0", "Old proxy");
setText(3, "verdict-cell-2-1", "2021 final file");
setText(3, "verdict-cell-2-2", "Seven rounds");
setText(3, "verdict-cell-2-3", "Starts after old unveiling; applies revised net-debt display rule");
setText(3, "verdict-cell-3-0", "New rebuild");
setText(3, "verdict-cell-3-1", "2026 public FWTW");
setText(3, "verdict-cell-3-2", "Full inverse");
setText(3, "verdict-cell-3-3", "31 instruments; 25 substantive sectors; 2021 DINA/NIPA to 2016");
setText(3, "verdict-cell-4-0", "Household split");
setText(3, "verdict-cell-4-1", "Fine DINA shares");
setText(3, "verdict-cell-4-2", "Before solve");
setText(3, "verdict-cell-4-3", "Asset-class shares split every direct household-holder cell by wealth group");
setText(3, "verdict-cell-5-0", "Debt owed");
setText(3, "verdict-cell-5-1", "Public FWTW totals");
setText(3, "verdict-cell-5-2", "DINA split");
setText(3, "verdict-cell-5-3", "Owner-mortgage shares + nonmortgage shares; five debt instruments");
setText(3, "verdict-cell-6-0", "Main test");
setText(3, "verdict-cell-6-1", "Both vs paper");
setText(3, "verdict-cell-6-2", "Diagnostic");
setText(3, "verdict-cell-6-3", "Operator and vintage change together; do not read the gap as causal");
setText(3, "takeaway-title", "Rule");
setText(3, "takeaway-body", "Use the new route for the final replication result; keep the old route as a transparent lineage benchmark.");
setNotes(3, "[Sources]\n- MSS_SGR_July242025.pdf, Sections 2.2 and 4.1; Table A1\n- Data/raw/fwtw/fwtw_data_2026-06-18.csv\n- docs/data/figure8-public-fwtw-data.md\n- docs/data/figure8-data.md");

// 4 — preferred pipeline.
setText(4, "kicker", "PREFERRED IMPLEMENTATION");
setText(4, "title", "The public FWTW route follows the 2025 operator");
setText(4, "slide-number", "04");
setText(4, "question", "Question");
setText(4, "question-body", "Who ultimately owns household debt after every intermediary chain?");
setText(4, "Strong precursor-label", "1 · Expand");
setText(4, "Strong precursor-body", "Map each FWTW instrument to DINA; split the direct household holder into four wealth groups.");
setText(4, "Partial match-label", "2 · Unveil all chains");
setText(4, "Partial match-body", "Sum instruments, row-normalize, then solve Ω = (I − Q)⁻¹B.");
setText(4, "Context only-label", "3 · Form net debt");
setText(4, "Context only-body", "Allocate household-debt assets through Omega; subtract mortgage and nonmortgage liabilities.");
setText(4, "boundary-title", "Invariant");
setText(4, "boundary-body", "Every direct and unveiled row sums to one; all-owner debt assets and household-group liabilities each close to aggregate debt.");
setNotes(4, "[Sources]\n- MSS_SGR_July242025.pdf, equations (1), (3), and (4); Sections 4.1–4.2\n- Code/unveiling/figure8_public_fwtw.py\n- Data/interim/figure8_public_fwtw_network_diagnostics.csv");

// 5 — data boundary.
setText(5, "kicker", "DATA AND TAXONOMY BOUNDARY");
setText(5, "title", "The method is close; the exact 2025 vintage is unavailable");
setText(5, "slide-number", "05");
setText(5, "question", "Classification");
setText(5, "question-body", "Mixed-vintage method reconstruction\nNot an exact numerical reproduction");
setText(5, "Strong precursor-label", "1 · Public FWTW");
setText(5, "Strong precursor-body", "Completed bilateral estimates: 31 instruments, 25 substantive sectors, June 2026 vintage.");
setText(5, "Partial match-label", "2 · Distributional layer");
setText(5, "Partial match-body", "Fine DINA asset and liability shares plus authors-kit national income, 1963–2016.");
setText(5, "Context only-label", "3 · Signed levels");
setText(5, "Context only-body", "Negative positions reverse direction per the Fed note; zero clipping is a sensitivity.");
setText(5, "boundary-title", "Vintage gap");
setText(5, "boundary-body", "The paper’s 34-instrument, 27-sector matrices, exact crosswalk, and through-2019 extension were not recovered.");
setNotes(5, "[Sources]\n- MSS_SGR_July242025.pdf, Section 2.2\n- https://www.federalreserve.gov/releases/efa/fwtw.htm\n- https://www.federalreserve.gov/releases/efa/fwtw_announcements.htm\n- Data/raw/README.md\n- docs/data/figure8-public-fwtw-data.md");

// 6 — three-way empirical comparison.
setText(6, "kicker", "FIGURE 8 METHOD COMPARISON");
setText(6, "title", "Full unveiling improves top-1 fit, not every level");
setText(6, "slide-number", "06");
setText(6, "left-label", "Top 1% · 2025 paper vs both implementations");
setText(6, "right-label", "Bottom 99% · 2025 paper vs both implementations");
setText(6, "verdict", "MIXED IMPROVEMENT");
setText(6, "assessment", "Top-1 MAE: 2.12 pp new vs 2.41 proxy. Bottom-99 MAE: 1.98 pp new vs 1.38 proxy.");
setText(6, "difference", "Top-1 correlation rises to 0.998. The 2007 new result is +12.28 / −44.31 pp versus paper +18.02 / −38.76 pp.");
await replaceImage(6, 0, "Results_Proposal/figures/figure8_method_comparison_top1.png", "Top 1 percent Figure 8 method comparison");
await replaceImage(6, 1, "Results_Proposal/figures/figure8_method_comparison_bottom99.png", "Bottom 99 percent Figure 8 method comparison");
setNotes(6, "[Sources]\n- MSS_SGR_July242025.pdf, Figure 8, physical page 29; digitized benchmark\n- Results_Proposal/figures/figure8_method_comparison_top1.png\n- Results_Proposal/figures/figure8_method_comparison_bottom99.png\n- Data/processed/figure8_method_comparison_metrics.csv");

// 7 — result and robustness.
setText(7, "kicker", "VALIDATION AND SENSITIVITY");
setText(7, "title", "The preferred result is stable to negative-cell treatment");
setText(7, "slide-number", "07");
setText(7, "left-label", "Preferred reconstruction · five wealth groups");
setText(7, "right-label", "Reorient negative positions vs clip to zero");
setText(7, "verdict", "ACCOUNTING CLOSES");
setText(7, "assessment", "Max spectral radius 0.504; direct, unveiled, and primary-asset closure errors below 9×10⁻¹⁶.");
setText(7, "difference", "Reorientation vs clipping changes top 1% by at most 0.09 pp and bottom 99% by at most 0.17 pp.");
await replaceImage(7, 0, "Results_Proposal/figures/figure8_public_fwtw_full_leontief.png", "Public FWTW full Leontief Figure 8 reconstruction");
await replaceImage(7, 1, "Results_Proposal/figures/figure8_public_fwtw_sensitivity.png", "Figure 8 negative-position treatment sensitivity");
setNotes(7, "[Sources]\n- Results_Proposal/figures/figure8_public_fwtw_full_leontief.png\n- Results_Proposal/figures/figure8_public_fwtw_sensitivity.png\n- Data/interim/figure8_public_fwtw_network_diagnostics.csv\n- https://www.federalreserve.gov/releases/efa/fwtw.htm");

// 8 — synthesis.
setText(8, "kicker", "REPLICATION SYNTHESIS");
setText(8, "title", "Use the full-Leontief result; retain the proxy as lineage");
setText(8, "slide-number", "08");
setText(8, "question", "Submission choice");
setText(8, "question-body", "Lead with the new method reconstruction; show the old proxy as an audit.");
setText(8, "Strong precursor-label", "Preferred result");
setText(8, "Strong precursor-body", "Public completed FWTW + DINA/NIPA + full 2025 Leontief operator, 1963–2016.");
setText(8, "Partial match-label", "Supporting result");
setText(8, "Partial match-body", "2021-kit seven-round proxy preserves the older authors’ pipeline and downstream benchmark.");
setText(8, "Context only-label", "Interpretation");
setText(8, "Context only-body", "Both reproduce the central split: rising top-1 lending and bottom-99 borrowing after 1982.");
setText(8, "boundary-title", "Report explicitly");
setText(8, "boundary-body", "Operator, public vintage, taxonomy, and sample endpoint change together; the remaining paper gap is not a pure code effect.");
setNotes(8, "[Sources]\n- docs/project/tasks/figure8-replication.md\n- docs/data/figure8-public-fwtw-data.md\n- Data/processed/figure8_method_comparison_metrics.csv\n- MSS_SGR_July242025.pdf, Figure 8");

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
