import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const requiredEnvironment = ["MSS_DECK_WORKSPACE", "MSS_PROJECT_ROOT"];
for (const variable of requiredEnvironment) {
  if (!process.env[variable]) {
    throw new Error(`Missing required environment variable: ${variable}`);
  }
}

const workspace = process.env.MSS_DECK_WORKSPACE;
const root = process.env.MSS_PROJECT_ROOT;
const output = process.env.MSS_DECK_OUTPUT
  ?? path.join(root, "Presentation/4_figure_comparison/presentation.pptx");
const source = path.join(workspace, "template-starter.pptx");
const renderDir = path.join(workspace, "final-renders");
const layoutDir = path.join(workspace, "final-layout");

const presentation = await PresentationFile.importPptx(await FileBlob.load(source));

function getSlide(slideNumber) {
  return presentation.slides.items[slideNumber - 1];
}

function getShape(slideNumber, shapeName) {
  const shape = getSlide(slideNumber).shapes.items.find(
    (item) => item.name === shapeName,
  );
  if (!shape) {
    throw new Error(`Slide ${slideNumber}: shape ${shapeName} not found.`);
  }
  return shape;
}

function setText(slideNumber, shapeName, value) {
  getShape(slideNumber, shapeName).text = value;
}

function setNotes(slideNumber, value) {
  getSlide(slideNumber).speakerNotes.textFrame.setText(value);
  getSlide(slideNumber).speakerNotes.setVisible(true);
}

async function readImage(relativePath) {
  const buffer = await fs.readFile(path.join(root, relativePath));
  return buffer.buffer.slice(
    buffer.byteOffset,
    buffer.byteOffset + buffer.byteLength,
  );
}

async function replaceImage(slideNumber, imageIndex, relativePath, alt) {
  const image = getSlide(slideNumber).images.items[imageIndex];
  if (!image) {
    throw new Error(`Slide ${slideNumber}: image ${imageIndex} not found.`);
  }
  const frame = image.frame;
  const crop = image.crop;
  const geometry = image.geometry;
  const borderRadius = image.borderRadius;
  const rotation = image.rotation;
  const flipHorizontal = image.flipHorizontal;
  const flipVertical = image.flipVertical;
  const lockAspectRatio = image.lockAspectRatio;
  await image.replace({
    blob: await readImage(relativePath),
    contentType: "image/png",
    alt,
    fit: "contain",
  });
  image.frame = frame;
  image.crop = crop;
  image.geometry = geometry;
  image.borderRadius = borderRadius;
  image.rotation = rotation;
  image.flipHorizontal = flipHorizontal;
  image.flipVertical = flipVertical;
  image.lockAspectRatio = lockAspectRatio;
}

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

// 1 — comparison-only opening.
setText(1, "eyebrow", "CORE FIGURE COMPARISON");
setText(1, "title", "Paper figures versus our implementations");
setText(1, "subtitle", "2025 target on the left; our common-sample reconstruction on the right");
setText(1, "legend-2021-text", "Figures 1, 5, and 6: 2025 definitions with 2021 authors-kit inputs");
setText(1, "legend-2025-text", "Figure 8: 2021 direct cells with the full Leontief inverse");
setText(1, "date", "16 August 2026");
setNotes(
  1,
  "[Sources]\n- MSS_SGR_July242025.pdf, Figures 1, 5, 6, and 8\n- docs/project/tasks/figure1-replication.md\n- docs/project/tasks/figure5-replication.md\n- docs/project/tasks/figure6-replication.md\n- docs/project/tasks/figure8-replication.md",
);

// 2 — comparison contract.
setText(2, "kicker", "COMPARISON CONTRACT");
setText(2, "title", "Each slide compares the paper directly with our implementation");
setText(2, "slide-number", "02");
setText(2, "question", "2025 targets");
setText(2, "question-body", "Figures 1, 5, 6, and 8\nRevised definitions through 2019");
setText(2, "Strong precursor-label", "Figures 1, 5, and 6");
setText(2, "Strong precursor-body", "Recompute the 2025 objects with February 2021 authors-kit inputs; the available series end in 2016.");
setText(2, "Partial match-label", "Figure 8");
setText(2, "Partial match-body", "Restart from saved direct cells and replace seven rounds with the full Leontief inverse.");
setText(2, "Context only-label", "Common comparison");
setText(2, "Context only-body", "Same target definition, common-period fit metrics, and an explicit vintage or matrix boundary.");
setText(2, "boundary-title", "Reading rule");
setText(2, "boundary-body", "The left panel is the paper target and the right panel is our implementation. Supporting diagnostics live in their method or extension decks.");
setNotes(
  2,
  "[Sources]\n- MSS_SGR_July242025.pdf, Figures 1, 5, 6, and 8\n- docs/project/tasks/result-selection.md\n- docs/project/tasks/figure8-replication.md",
);

// 3–5 — inherited Figure 1, Figure 5, and Figure 6 direct comparisons.
setText(3, "slide-number", "03");
setText(4, "slide-number", "04");
setText(5, "slide-number", "05");

// 6 — primary Figure 8 full-inverse reconstruction.
setText(6, "title", "The full inverse recovers the lender–borrower split");
setText(6, "slide-number", "06");
setText(6, "right-label", "Our implementation · 2021 direct cells + full Leontief");
setText(6, "verdict", "FULL-INVERSE MATCH");
setText(6, "assessment", "Correlations: 0.994 / 0.995 (top 1% / bottom 99%); MAE: 2.33 / 1.31 pp.");
setText(6, "difference", "2007: top 1% +11.47 pp versus +18.02 paper; bottom 99% −41.03 pp versus −38.76 paper. Eight coarsened intermediary blocks; ends 2016.");
await replaceImage(
  6,
  1,
  "Results_Proposal/figures/figure8_2021_direct_full_leontief.png",
  "Figure 8 reconstruction from 2021 direct cells using the full Leontief inverse",
);
setNotes(
  6,
  "[Sources]\n- MSS_SGR_July242025.pdf, Figure 8, physical PDF page 29\n- Results_Proposal/figures/figure8_2021_direct_full_leontief.png\n- Data/processed/figure8_method_comparison.csv\n- Data/processed/figure8_method_comparison_metrics.csv\n- docs/project/tasks/figure8-replication.md\n- Code/scripts/build_figure8_2021_direct.py\n- Code/scripts/build_figure8_method_comparison.py",
);

// 7 — synthesis.
setText(7, "title", "All four comparisons recover the paper’s central patterns");
setText(7, "slide-number", "07");
setText(7, "question-body", "What survives independent implementation?");
setText(7, "Strong precursor-body", "Indirect household ownership rises strongly; the reconstructed level tracks the target through 2016.");
setText(7, "Partial match-body", "Saving-flow divergence and the cross-sectional saving-rate profile reproduce closely.");
setText(7, "Context only-body", "The full-inverse result recovers the lender–borrower split; the top-1 level remains understated.");
setText(7, "boundary-body", "The 2021 inputs support high-fidelity reconstructions of the paper’s mechanisms. Remaining gaps concentrate in data vintage and financial-network detail.");
setNotes(
  7,
  "[Sources]\n- Results_Proposal/major_results.md, R-001 to R-003\n- docs/project/tasks/figure1-replication.md\n- docs/project/tasks/figure5-replication.md\n- docs/project/tasks/figure6-replication.md\n- docs/project/tasks/figure8-replication.md",
);

await fs.mkdir(renderDir, { recursive: true });
await fs.mkdir(layoutDir, { recursive: true });
for (let index = 0; index < presentation.slides.items.length; index += 1) {
  const slide = presentation.slides.items[index];
  const number = String(index + 1).padStart(2, "0");
  await writeBlob(
    path.join(renderDir, `slide-${number}.png`),
    await presentation.export({ slide, format: "png", scale: 2 }),
  );
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(
    path.join(layoutDir, `slide-${number}.layout.json`),
    await layout.text(),
  );
}

await writeBlob(
  path.join(workspace, "final-montage.webp"),
  await presentation.export({ format: "webp", montage: true, scale: 1 }),
);

const snapshot = await presentation.inspect({
  kind: "slide,textbox,shape,image,notes,layout",
  include: "id,slide,name,title,text,textPreview,textChars,textLines,bbox,bboxUnit,isPlaceholder,alt",
  maxChars: 180000,
});
await fs.writeFile(
  path.join(workspace, "final-inspect.ndjson"),
  `${snapshot.ndjson}\n`,
  "utf8",
);

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(output);
try {
  await fs.rename(
    `${output}.inspect.ndjson`,
    path.join(workspace, "final-pptx.inspect.ndjson"),
  );
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
}
console.log(output);
