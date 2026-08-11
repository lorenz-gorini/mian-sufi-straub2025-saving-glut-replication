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
  if (!process.env[variable]) {
    throw new Error(`Missing required environment variable: ${variable}`);
  }
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
const artifactUtilsUrl = pathToFileURL(
  path.join(skillDir, "container_tools/artifact_tool_utils.mjs"),
).href;
const { saveBlobToFile } = await import(artifactUtilsUrl);

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

async function replaceImages(slideNumber, replacements) {
  const slide = getSlide(slideNumber);
  const originals = [...slide.images.items];
  if (originals.length < replacements.length) {
    throw new Error(`Slide ${slideNumber}: expected ${replacements.length} images; found ${originals.length}.`);
  }
  const preserved = replacements.map((replacement, index) => {
    const image = originals[index];
    return {
      replacement,
      frame: image.frame,
      geometry: image.geometry,
      borderRadius: image.borderRadius,
      rotation: image.rotation,
      flipHorizontal: image.flipHorizontal,
      flipVertical: image.flipVertical,
      lockAspectRatio: image.lockAspectRatio,
    };
  });
  for (let index = replacements.length - 1; index >= 0; index -= 1) {
    originals[index].delete();
  }
  for (const item of preserved) {
    const bytes = await fs.readFile(item.replacement.path);
    const image = slide.images.add({
      blob: bytes,
      contentType: "image/png",
      alt: item.replacement.alt,
      fit: "contain",
      position: item.frame,
      geometry: item.geometry,
      borderRadius: item.borderRadius,
    });
    image.rotation = item.rotation;
    image.flipHorizontal = item.flipHorizontal;
    image.flipVertical = item.flipVertical;
    image.lockAspectRatio = item.lockAspectRatio;
  }
}

// Slide 1 — opening taxonomy.
setText(1, "title", "Four figures, one evidence hierarchy");
setText(1, "date", "11 August 2026");
setNotes(
  1,
  "[Sources]\n- docs/project/tasks/figure1-replication.md\n- docs/project/tasks/figure5-replication.md\n- docs/project/tasks/figure6-replication.md\n- docs/project/tasks/figure8-replication.md\n- Presentation/1_replication_package_validation/replication_package_validation.pptx (visual source)",
);

// Slide 2 — evidence roles.
setText(2, "title", "One label cannot mean the same thing across all four figures");
setText(2, "question-body", "Figures 1, 5, 6, and 8\nRevised definitions through 2019");
setText(2, "Context only-body", "Figures 1, 5, and 6: reconstructions. Figure 8: bounded proxy.");
setNotes(
  2,
  "[Sources]\n- MSS_SGR_July242025.pdf, Figures 1, 5, 6, and 8\n- docs/project/tasks/result-selection.md, completed feasibility classification\n- Results_Proposal/major_results.md, R-001 to R-003\n- docs/project/tasks/figure6-replication.md",
);

// Slide 10 — Figure 6 method.
setText(10, "kicker", "FIGURE 6 IDENTIFICATION");
setText(10, "title", "The same saving rate supports rank and wealth-level views");
setText(10, "slide-number", "10");
setText(10, "question", "Target");
setText(10, "question-body", "2025 Figure 6\nNet saving rate by wealth percentile");
setText(10, "Strong precursor-label", "1 · Rebuild bins");
setText(10, "Strong precursor-body", "Raw DINA: bottom 40%, then one-percentile bins through the top 1%.");
setText(10, "Partial match-label", "2 · Match income");
setText(10, "Partial match-body", "Personal plus attributable corporate disposable income, allocated by income and equity shares.");
setText(10, "Context only-label", "3 · Hold rate fixed");
setText(10, "Context only-body", "Active saving divided by disposable income; only the horizontal coordinate changes.");
setText(10, "boundary-title", "Classification");
setText(10, "boundary-body", "Exact-method reconstruction through 2016; the paper's later window ends in 2019.");
setNotes(
  10,
  "[Sources]\n- MSS_SGR_July242025.pdf, Section 3.4 and Figure 6, physical PDF page 24\n- docs/data/figure6-data.md\n- docs/project/tasks/figure6-replication.md\n- Code/unveiling/figure6_authors.py",
);

// Slide 11 — paper versus old-input reconstruction.
setText(11, "kicker", "FIGURE 6 PRIMARY COMPARISON");
setText(11, "title", "The older inputs reproduce the cross-sectional saving pattern");
setText(11, "slide-number", "11");
setText(11, "left-label", "2025 paper · 1963–82 and 1983–2019");
setText(11, "right-label", "Our reconstruction · second period ends in 2016");
setText(11, "verdict", "CLOSE SHAPE MATCH");
setText(11, "assessment", "Correlations: 0.991 / 0.969; MAE: 1.46 / 1.22 pp.");
setText(11, "difference", "Top 1%: ours 28.8%→36.2%; paper ≈43%→54%. The old inputs end in 2016, not 2019.");
await replaceImages(11, [
  {
    path: path.join(
      root,
      "Presentation/4_figure_comparison/assets/paper_figure6_no_caption.png",
    ),
    alt: "2025 paper Figure 6, caption removed",
  },
  {
    path: path.join(root, "Results_Proposal/figures/figure6_authors_data_percentiles.png"),
    alt: "Figure 6 reconstructed saving rates by wealth percentile",
  },
]);
setNotes(
  11,
  "[Sources]\n- MSS_SGR_July242025.pdf, Figure 6, physical PDF page 24; embedded chart extracted without caption\n- Results_Proposal/figures/figure6_authors_data_percentiles.png\n- Data/processed/figure6_authors_comparison.csv\n- Data/processed/figure6_digitization_audit.csv\n- docs/project/tasks/figure6-replication.md",
);

// Slide 12 — paper-raster digitization audit.
setText(12, "kicker", "DIGITIZATION AUDIT");
setText(12, "title", "Recovered centerlines match the paper pixels");
setText(12, "slide-number", "12");
setText(12, "left-label", "Calibration and trace");
setText(12, "right-label", "Original raster + recovered centerlines");
setText(12, "table-title", "No hand-clicking or screenshot interpolation");
setText(12, "cell-0-0", "Object");
setText(12, "cell-0-1", "Audit");
setText(12, "cell-0-2", "Result");
setText(12, "cell-1-0", "Source");
setText(12, "cell-1-1", "1047×698");
setText(12, "cell-1-2", "Embedded");
setText(12, "cell-2-0", "Grid");
setText(12, "cell-2-1", "61 × 2");
setText(12, "cell-2-2", "122 samples");
setText(12, "cell-3-0", "Matches");
setText(12, "cell-3-1", "122 / 122");
setText(12, "cell-3-2", "0 filled");
setText(12, "cell-4-0", "Scale");
setText(12, "cell-4-1", "1 pixel");
setText(12, "cell-4-2", "0.129 pp");
setText(12, "verdict", "PIXEL TRACE PASSES");
setText(12, "assessment", "Solid recovered centerlines overlap the original dashed curves.");
setText(12, "difference", "The overlay corrected the blue top-1 endpoint by ≈1.3 pp; post-period correlation / MAE are 0.969 / 1.22 pp.");
await replaceImages(12, [
  {
    path: path.join(root, "Results_Proposal/figures/figure6_digitization_overlay_slide.png"),
    alt: "Recovered Figure 6 curve coordinates over the original embedded paper raster",
  },
]);
setNotes(
  12,
  "[Sources]\n- MSS_SGR_July242025.pdf, Figure 6, physical PDF page 24; original embedded raster\n- Results_Proposal/figures/figure6_digitization_overlay_slide.png\n- Data/processed/figure6_digitization_audit.csv\n- Code/unveiling/paper_benchmarks.py\n- Code/scripts/build_figure6_authors_data.py\n- docs/data/figure6-data.md, Paper-curve digitization",
);

// Slide 13 — rank versus matched wealth level.
setText(13, "kicker", "FIGURE 6 MECHANISM VIEW");
setText(13, "title", "Rising wealth alone does not explain the saving-rate shift");
setText(13, "slide-number", "13");
setText(13, "left-label", "Same rates · wealth percentile");
setText(13, "right-label", "Same rates · mean real wealth per adult");
setText(13, "verdict", "NOT PURE COMPOSITION");
setText(13, "assessment", "At similar mean wealth, post-1982 cohorts often save less.");
setText(13, "difference", "Near $300k mean wealth: pre p90 saves 31.5%; post p80 saves 7.4%. Cohort means are not fixed-dollar bins.");
await replaceImages(13, [
  {
    path: path.join(root, "Results_Proposal/figures/figure6_authors_data_percentiles.png"),
    alt: "Figure 6 saving rates indexed by wealth percentile",
  },
  {
    path: path.join(root, "Results_Proposal/figures/figure6_authors_data_wealth_levels.png"),
    alt: "The same Figure 6 cohort saving rates indexed by mean real wealth",
  },
]);
setNotes(
  13,
  "[Sources]\n- Results_Proposal/figures/figure6_authors_data_percentiles.png\n- Results_Proposal/figures/figure6_authors_data_wealth_levels.png\n- Data/processed/figure6_authors_data.csv\n- docs/project/personal-considerations-saving-inequality.md\n- docs/data/figure6-data.md",
);

// Slide 14 — trailing-five-year diagnostic.
setText(14, "kicker", "FIGURE 6 TIME EVOLUTION");
setText(14, "title", "Upper-middle rates trend down; the top 1% remains volatile");
setText(14, "slide-number", "14");
setText(14, "left-label", "Full distribution · trailing five-year means");
setText(14, "right-label", "Selected upper-tail percentiles");
setText(14, "verdict", "NOT A SINGLE BREAK");
setText(14, "assessment", "The 80th–90th percentiles decline persistently after the late 1980s.");
setText(14, "difference", "The top 1% oscillates sharply, including a 2008 five-year peak; this is not one smooth monotone trend.");
await replaceImages(14, [
  {
    path: path.join(root, "Results_Proposal/figures/figure6_rolling5_heatmap.png"),
    alt: "Trailing five-year Figure 6 saving rates across wealth percentiles",
  },
  {
    path: path.join(root, "Results_Proposal/figures/figure6_rolling5_selected_percentiles.png"),
    alt: "Trailing five-year Figure 6 saving rates for selected percentiles",
  },
]);
setNotes(
  14,
  "[Sources]\n- Data/processed/figure6_authors_rolling5.csv\n- Results_Proposal/figures/figure6_rolling5_heatmap.png\n- Results_Proposal/figures/figure6_rolling5_selected_percentiles.png\n- Code/scripts/build_figure6_authors_data.py\n- docs/data/figure6-data.md",
);

// Slides 15–16 — preserve Figure 8 content, update numbering.
setText(15, "slide-number", "15");
setText(16, "slide-number", "16");

// Slide 17 — synthesis.
setText(17, "title", "Figures 1, 5, and 6 reconstruct; Figure 8 remains a proxy");
setText(17, "slide-number", "17");
setText(17, "Partial match-label", "Figures 5–6");
setText(17, "Partial match-body", "High-fidelity saving-flow and saving-rate reconstructions through 2016.");
setText(17, "boundary-body", "The 2021 inputs reproduce the paper's core patterns and support a new Figure 6 mechanism diagnostic. Figure 8 alone remains method-bounded.");
setNotes(
  17,
  "[Sources]\n- Results_Proposal/major_results.md, R-001 to R-003\n- docs/project/tasks/figure1-replication.md\n- docs/project/tasks/figure5-replication.md\n- docs/project/tasks/figure6-replication.md\n- docs/project/tasks/figure8-replication.md",
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

const montage = await presentation.export({
  format: "png",
  montage: { format: "png", columns: 4, slideWidth: 480, padding: 18, gap: 18, background: "#dfe5eb" },
});
await saveBlobToFile(montage, path.join(workspace, "final-montage.png"));

const snapshot = await presentation.inspect({
  kind: "slide,textbox,shape,image,notes,layout",
  include: "id,slide,name,title,text,textPreview,textChars,textLines,bbox,bboxUnit,isPlaceholder,alt",
  maxChars: 300000,
});
await fs.writeFile(path.join(workspace, "final-inspect.ndjson"), `${snapshot.ndjson}\n`, "utf8");

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
