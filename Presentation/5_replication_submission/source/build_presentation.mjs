import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const requiredEnvironment = [
  "MSS_DECK_WORKSPACE",
  "MSS_PROJECT_ROOT",
];
for (const variable of requiredEnvironment) {
  if (!process.env[variable]) {
    throw new Error(`Missing required environment variable: ${variable}`);
  }
}

const workspace = process.env.MSS_DECK_WORKSPACE;
const root = process.env.MSS_PROJECT_ROOT;
const output = process.env.MSS_DECK_OUTPUT
  ?? path.join(root, "Presentation/5_replication_submission/presentation.pptx");
const renderDir = path.join(workspace, "final-renders");
const layoutDir = path.join(workspace, "final-layout");
const montagePath = path.join(workspace, "final-montage.webp");

async function saveBlobToFile(blob, outputPath) {
  if (blob && typeof blob.arrayBuffer === "function") {
    await fs.writeFile(outputPath, Buffer.from(await blob.arrayBuffer()));
    return;
  }
  if (blob instanceof Uint8Array || Buffer.isBuffer(blob)) {
    await fs.writeFile(outputPath, blob);
    return;
  }
  if (typeof blob === "string") {
    await fs.writeFile(outputPath, blob, "utf8");
    return;
  }
  throw new Error(`Unsupported export payload for ${outputPath}.`);
}

const sourcePaths = {
  theory: path.join(root, "Presentation/3_theoretical_methodology/presentation_short.pptx"),
  data: path.join(root, "Presentation/2_data-map/presentation.pptx"),
  results: path.join(root, "Presentation/4_figure_comparison/presentation.pptx"),
  figure8: path.join(root, "Presentation/6_figure8_method_comparison/presentation.pptx"),
};

const presentations = {};
for (const [key, sourcePath] of Object.entries(sourcePaths)) {
  presentations[key] = await PresentationFile.importPptx(await FileBlob.load(sourcePath));
}

const presentation = presentations.theory;
const selection = [
  { deck: "theory", slide: 1, purpose: "cover" },
  { deck: "theory", slide: 2, purpose: "economic problem" },
  { deck: "theory", slide: 3, purpose: "direct ownership matrix" },
  { deck: "theory", slide: 4, purpose: "Leontief inverse" },
  { deck: "theory", slide: 5, purpose: "four-sector network" },
  { deck: "theory", slide: 6, purpose: "worked unveiling result" },
  { deck: "theory", slide: 7, purpose: "2021 versus 2025 operator" },
  { deck: "data", slide: 2, purpose: "identification map" },
  { deck: "data", slide: 8, purpose: "saving and valuation inputs" },
  { deck: "data", slide: 9, purpose: "figure lineage" },
  { deck: "data", slide: 11, purpose: "data-vintage boundary" },
  { deck: "data", slide: 12, purpose: "replication evidence strategy" },
  { deck: "results", slide: 5, purpose: "Figure 1 comparison" },
  { deck: "results", slide: 10, purpose: "Figure 5 comparison" },
  { deck: "figure8", slide: 2, purpose: "Figure 8 estimand and three routes" },
  { deck: "figure8", slide: 6, purpose: "Figure 8 paper comparison" },
  { deck: "figure8", slide: 7, purpose: "Figure 8 same-vintage operator comparison" },
  { deck: "results", slide: 18, purpose: "replication synthesis" },
];

function referencedImages(slideProto) {
  return [...new Set(
    JSON.stringify(slideProto).match(/\/ppt\/media\/[A-Za-z0-9._-]+/g) ?? [],
  )];
}

function bytesEqual(left, right) {
  if (!(left instanceof Uint8Array) || !(right instanceof Uint8Array)) return false;
  if (left.length !== right.length) return false;
  for (let index = 0; index < left.length; index += 1) {
    if (left[index] !== right[index]) return false;
  }
  return true;
}

function replaceStrings(value, replacements) {
  if (typeof value === "string") return replacements.get(value) ?? value;
  if (Array.isArray(value)) return value.map((item) => replaceStrings(item, replacements));
  if (value && typeof value === "object") {
    for (const [key, item] of Object.entries(value)) {
      value[key] = replaceStrings(item, replacements);
    }
  }
  return value;
}

function uniqueImageId(deck, finalSlideNumber, sourceId) {
  const filename = path.posix.basename(sourceId);
  return `/ppt/media/${deck}-${String(finalSlideNumber).padStart(2, "0")}-${filename}`;
}

const importedImageIds = new Set(presentation.images.items.map((image) => image.id));
const finalSlideProtos = [];
for (let index = 0; index < selection.length; index += 1) {
  const item = selection[index];
  const finalSlideNumber = index + 1;
  const sourcePresentation = presentations[item.deck];
  const sourceSlide = sourcePresentation.slides.items[item.slide - 1];
  if (!sourceSlide) {
    throw new Error(`${item.deck} slide ${item.slide} is unavailable.`);
  }

  const proto = structuredClone(sourceSlide.toProto());
  const replacements = new Map();
  for (const sourceId of referencedImages(proto)) {
    const sourceImage = sourcePresentation.images.getById(sourceId);
    if (!sourceImage) {
      throw new Error(`${item.deck} slide ${item.slide}: image ${sourceId} is unavailable.`);
    }
    const existingImage = presentation.images.getById(sourceId);
    const canReuse = existingImage
      && existingImage.contentType === sourceImage.contentType
      && bytesEqual(existingImage.data, sourceImage.data);
    if (canReuse) continue;

    let targetId = uniqueImageId(item.deck, finalSlideNumber, sourceId);
    let suffix = 1;
    while (importedImageIds.has(targetId)) {
      targetId = uniqueImageId(
        item.deck,
        finalSlideNumber,
        sourceId.replace(/(\.[^.]+)$/, `-${suffix}$1`),
      );
      suffix += 1;
    }
    const imageProto = structuredClone(sourceImage.toProto());
    imageProto.id = targetId;
    presentation.images.add(imageProto);
    importedImageIds.add(targetId);
    replacements.set(sourceId, targetId);
  }

  replaceStrings(proto, replacements);
  proto.id = `replication-submission-${String(finalSlideNumber).padStart(2, "0")}`;
  proto.index = index;
  proto.creationId = String(2026081300 + finalSlideNumber);
  finalSlideProtos.push(proto);
}

presentation.slides.replace(finalSlideProtos);

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

async function imageBytes(relativePath) {
  const buffer = await fs.readFile(path.join(root, relativePath));
  return buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength);
}

setText(1, "eyebrow", "REPLICATION PACKAGE · METHODOLOGY, DATA, RESULTS");
setText(1, "title", "Replicating the Saving Glut of the Rich");
setText(
  1,
  "subtitle",
  "Methodology, data lineage, and three version-aware empirical reconstructions",
);
setText(1, "date", "14 August 2026");
setText(1, "cover-thesis-label", "SUBMISSION QUESTION");
setText(
  1,
  "cover-thesis",
  "Which claims can the available data reproduce—and which remain version-bound?",
);
setNotes(
  1,
  "[Sources]\n- MSS_SGR_July242025.pdf (target paper)\n- MSS2021Febreplicationkit/readme.pdf (available authors’ package)\n- Presentation/3_theoretical_methodology/assets/leontief-network-cover.png (project visual)\n- NotebookLM-Present-Unveiling_the_Rich_Saving_Glut.pdf, pp. 1–6 (orientation and visual inspiration only)",
);

const coverVisual = getSlide(1).images.add({
  blob: await imageBytes(
    "Presentation/3_theoretical_methodology/assets/leontief-network-cover.png",
  ),
  contentType: "image/png",
  alt: "Dense financial network resolving into ultimate owners",
  fit: "cover",
  position: { left: 0, top: 0, width: 1280, height: 720 },
});
coverVisual.sendToBack();

for (let slideNumber = 2; slideNumber <= selection.length; slideNumber += 1) {
  setText(slideNumber, "slide-number", String(slideNumber).padStart(2, "0"));
}

setText(2, "kicker", "PART I · THEORETICAL METHODOLOGY");
setText(8, "kicker", "PART II · DATA AND VERSION BOUNDARY");
setText(13, "kicker", "PART III · EMPIRICAL COMPARISONS");

setText(18, "kicker", "REPLICATION SYNTHESIS");
setText(18, "title", "Three reconstructions, each with a declared boundary");
setText(18, "question-body", "What does the submission package substantiate?");
setText(18, "Strong precursor-label", "Figure 1");
setText(
  18,
  "Strong precursor-body",
  "Close old-input stock reconstruction; the exact denominator and classification remain version-specific.",
);
setText(18, "Partial match-label", "Figure 5");
setText(
  18,
  "Partial match-body",
  "High-fidelity saving-flow reconstruction through 2016; the revised paper continues through 2019.",
);
setText(18, "Context only-label", "Figure 8");
setText(
  18,
  "Context only-body",
  "Same-vintage full-inverse reconstruction; old rounds and public FWTW remain separate comparators.",
);
setText(
  18,
  "boundary-body",
  "We reproduced the 2021 package for its own paper version, then reimplemented the 2025 definitions. Exact equality still requires the revised annual matrices and 2017–2019 inputs.",
);
setNotes(
  18,
  "[Sources]\n- Results_Proposal/major_results.md, R-001 to R-003\n- docs/project/tasks/author-data-benchmark.md\n- docs/project/tasks/figure1-replication.md\n- docs/project/tasks/figure5-replication.md\n- docs/project/tasks/figure8-replication.md",
);

await fs.mkdir(path.dirname(output), { recursive: true });
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

const montage = await presentation.export({
  format: "webp",
  montage: true,
  scale: 1,
});
await saveBlobToFile(montage, montagePath);

const snapshot = await presentation.inspect({
  kind: "slide,textbox,shape,image,notes,layout",
  include: "id,slide,name,title,text,textPreview,textChars,textLines,bbox,bboxUnit,isPlaceholder,alt",
  maxChars: 400000,
});
await fs.writeFile(path.join(workspace, "final-inspect.ndjson"), `${snapshot.ndjson}\n`, "utf8");

await fs.writeFile(
  path.join(workspace, "template-frame-map.json"),
  `${JSON.stringify(selection.map((item, index) => ({
    outputSlide: index + 1,
    sourceDeck: path.relative(root, sourcePaths[item.deck]),
    sourceSlide: item.slide,
    purpose: item.purpose,
  })), null, 2)}\n`,
  "utf8",
);

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(output);
try {
  await fs.rename(`${output}.inspect.ndjson`, path.join(workspace, "final-pptx.inspect.ndjson"));
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
}
console.log(output);
