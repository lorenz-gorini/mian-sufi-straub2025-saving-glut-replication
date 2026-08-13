import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const requiredEnvironment = [
  "MSS_DECK_WORKSPACE",
  "MSS_PROJECT_ROOT",
  "MSS_DECK_SOURCE_DIR",
  "PRESENTATIONS_SKILL_DIR",
];
for (const variable of requiredEnvironment) {
  if (!process.env[variable]) throw new Error(`Missing required environment variable: ${variable}`);
}

const workspace = process.env.MSS_DECK_WORKSPACE;
const root = process.env.MSS_PROJECT_ROOT;
const sourceDir = process.env.MSS_DECK_SOURCE_DIR;
const skillDir = process.env.PRESENTATIONS_SKILL_DIR;
const output = process.env.MSS_DECK_OUTPUT
  ?? path.join(root, "Presentation/4_figure_comparison/presentation.pptx");
const source = path.join(sourceDir, "template-starter.pptx");
const renderDir = path.join(workspace, "final-renders");
const layoutDir = path.join(workspace, "final-layout");
const { saveBlobToFile } = await import(pathToFileURL(
  path.join(skillDir, "container_tools/artifact_tool_utils.mjs"),
).href);

const presentation = await PresentationFile.importPptx(await FileBlob.load(source));

function getSlide(slideNumber) {
  return presentation.slides.items[slideNumber - 1];
}

function setText(slideNumber, shapeName, value) {
  const shape = getSlide(slideNumber).shapes.items.find((item) => item.name === shapeName);
  if (!shape) throw new Error(`Slide ${slideNumber}: shape ${shapeName} not found.`);
  shape.text = value;
}

function setNotes(slideNumber, value) {
  getSlide(slideNumber).speakerNotes.textFrame.setText(value);
}

// Slide 1 — opening taxonomy.
setText(1, "title", "Four figures, one evidence hierarchy");
setText(1, "date", "12 August 2026");
setNotes(
  1,
  "[Sources]\n- docs/project/tasks/figure1-replication.md\n- docs/project/tasks/figure5-replication.md\n- docs/project/tasks/figure6-replication.md\n- docs/project/tasks/figure8-replication.md\n- Presentation/1_replication_package_validation/replication_package_validation.pptx (visual source)",
);

// Slide 2 — current evidence roles.
setText(2, "Context only-body", "Figures 1, 5, and 6: reconstructions. Figure 8: current proxy; full-method rerun planned.");
setNotes(
  2,
  "[Sources]\n- MSS_SGR_July242025.pdf, Figures 1, 5, 6, and 8\n- docs/project/tasks/result-selection.md\n- Results_Proposal/major_results.md, R-001 to R-003\n- docs/project/tasks/figure8-replication.md",
);

// Slide 3 — method crosswalk, with target and public dimensions kept distinct.
setText(3, "verdict-cell-1-3", "34 instruments; 23 intermediaries + 4 owners; matrix/Leontief method; exact code unavailable");
setText(3, "verdict-cell-3-3", "31 instruments; 25 substantive sectors; completed public FWTW; 1963–2019");
setNotes(
  3,
  "[Sources]\n- MSS_SGR_July242025.pdf, Sections 2.2 and 4.1\n- https://www.federalreserve.gov/releases/efa/fwtw.htm\n- Data/raw/fwtw/fwtw_data_2026-06-18.csv\n- docs/data/figure1-data.md",
);

// Slide 4 — concise exact-vintage versus method-replication boundary.
setText(4, "kicker", "FIGURE 8 RECONSTRUCTION BOUNDARY");
setText(4, "title", "Full-network rerun matches the method—not the vintage");
setText(4, "slide-number", "04");
setText(4, "question", "Figure 8 next step");
setText(4, "question-body", "Full Leontief rerun\nSame operation; different vintage");
setText(4, "Strong precursor-label", "2025 target");
setText(4, "Strong precursor-body", "Authors’ Batty-based matrices: 34 instruments, 27 sectors, custom equity treatment; to 2019.");
setText(4, "Partial match-label", "Feasible rerun");
setText(4, "Partial match-body", "Public completed FWTW: 31 instruments, 25 substantive sectors; 2021 DINA/NIPA to 2016.");
setText(4, "Context only-label", "Common method");
setText(4, "Context only-body", "Dollar matrices → direct shares → wealth-group columns → full Leontief inverse.");
setText(4, "boundary-title", "Status");
setText(4, "boundary-body", "Planned reconstruction. The Figure 8 graph later in this deck remains the seven-round proxy.");
setNotes(
  4,
  "[Sources]\n- MSS_SGR_July242025.pdf, Sections 2.2 and 4.1\n- https://www.federalreserve.gov/releases/efa/fwtw.htm\n- https://www.federalreserve.gov/releases/efa/fwtw_announcements.htm\n- Data/raw/fwtw/fwtw_data_2026-06-18.csv\n- docs/project/tasks/figure8-replication.md",
);

// Slides 5–15 preserve the verified empirical content; update inherited numbering.
for (let slideNumber = 5; slideNumber <= 15; slideNumber += 1) {
  setText(slideNumber, "slide-number", String(slideNumber).padStart(2, "0"));
}
setText(8, "cell-1-2", "21 intermediaries");

// Slide 16 — exact-vintage gap is narrower than a methodological impossibility.
setText(16, "title", "The exact 2025 vintage is missing—not the method");
setText(16, "slide-number", "16");
setText(16, "Strong precursor-label", "1 · Exact-vintage gap");
setText(16, "Strong precursor-body", "Authors’ completed matrices, equity split, and exact crosswalk are not in the 2021 kit.");
setText(16, "Partial match-label", "2 · Available now");
setText(16, "Partial match-body", "Public completed FWTW plus 2021 DINA/NIPA support a full-Leontief mixed-vintage rerun.");
setText(16, "Context only-label", "3 · Current graph");
setText(16, "Context only-body", "Still uses seven-round debt assets with the 2025 group, sign, scale, and base.");
setText(16, "boundary-body", "Current plotted result: proxy. Planned public-FWTW rerun: method reconstruction with explicit vintage/taxonomy caveats.");
setNotes(
  16,
  "[Sources]\n- MSS_SGR_July242025.pdf, Sections 4.1–4.2 and Figure 8\n- https://www.federalreserve.gov/releases/efa/fwtw.htm\n- docs/project/tasks/figure8-replication.md\n- docs/data/figure8-data.md",
);

// Slide 17 — preserve the existing proxy comparison and its label.
setText(17, "slide-number", "17");
setText(17, "difference", "Correlations: 0.993 / 0.995 (top 1% / bottom 99%). Exact-vintage inputs are missing; public FWTW supports a separate method rerun.");

// Slide 18 — synthesis with an explicit next full-method path.
setText(18, "title", "Figure 8 has a proxy today—and a full-method rerun path");
setText(18, "slide-number", "18");
setText(18, "Context only-body", "Current proxy matches direction; public FWTW enables the next full-Leontief, mixed-vintage reconstruction.");
setText(18, "boundary-body", "The 2021 inputs establish old-vintage evidence. For Figure 8, current public FWTW can test the 2025 operator, but not reproduce the authors’ exact vintage.");
setNotes(
  18,
  "[Sources]\n- Results_Proposal/major_results.md, R-001 to R-003\n- docs/project/tasks/figure1-replication.md\n- docs/project/tasks/figure5-replication.md\n- docs/project/tasks/figure6-replication.md\n- docs/project/tasks/figure8-replication.md\n- https://www.federalreserve.gov/releases/efa/fwtw.htm",
);

await fs.mkdir(renderDir, { recursive: true });
await fs.mkdir(layoutDir, { recursive: true });
for (let index = 0; index < presentation.slides.items.length; index += 1) {
  const slide = presentation.slides.items[index];
  const number = String(index + 1).padStart(2, "0");
  const png = await presentation.export({ slide, format: "png", scale: 1.5 });
  await saveBlobToFile(png, path.join(renderDir, `slide-${number}.png`));
  const layout = await presentation.export({ slide, format: "layout" });
  await saveBlobToFile(layout, path.join(layoutDir, `slide-${number}.layout.json`));
}

const snapshot = await presentation.inspect({
  kind: "slide,textbox,shape,image,notes,layout",
  include: "id,slide,name,title,text,textPreview,textChars,textLines,bbox,bboxUnit,isPlaceholder,alt",
  maxChars: 300000,
});
await fs.writeFile(path.join(workspace, "final-inspect.ndjson"), `${snapshot.ndjson}\n`, "utf8");

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(output);
try {
  await fs.rename(`${output}.inspect.ndjson`, path.join(workspace, "final-pptx.inspect.ndjson"));
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
}
console.log(output);
