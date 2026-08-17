import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const root = process.env.MSS_PROJECT_ROOT;
const workspace = process.env.MSS_DECK_WORKSPACE;
const output = process.env.MSS_DECK_OUTPUT;
if (!root || !workspace || !output) {
  throw new Error("MSS_PROJECT_ROOT, MSS_DECK_WORKSPACE, and MSS_DECK_OUTPUT are required");
}

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const headers = lines[0].split(",");
  return lines.slice(1).map((line) => {
    const values = line.split(",");
    return Object.fromEntries(headers.map((header, index) => [header, values[index]]));
  });
}

const figure6Profiles = parseCsv(await fs.readFile(
  path.join(root, "Data/processed/figure6_authors_data.csv"),
  "utf8",
));
const figure6Rolling = parseCsv(await fs.readFile(
  path.join(root, "Data/processed/figure6_authors_rolling5.csv"),
  "utf8",
));

function profile(window, percentileBin) {
  const row = figure6Profiles.find(
    (item) => item.window === window && Number(item.percentile_bin) === percentileBin,
  );
  if (!row) throw new Error(`Missing Figure 6 profile ${window}/${percentileBin}`);
  return row;
}

function rollingRate(percentileBin, windowEndYear) {
  const row = figure6Rolling.find(
    (item) => Number(item.percentile_bin) === percentileBin && Number(item.window_end_year) === windowEndYear,
  );
  if (!row) throw new Error(`Missing Figure 6 rolling rate ${percentileBin}/${windowEndYear}`);
  return 100 * Number(row.rolling_mean_net_saving_rate);
}

function rollingPeak(percentileBin) {
  const rows = figure6Rolling.filter(
    (item) => Number(item.percentile_bin) === percentileBin,
  );
  if (rows.length === 0) throw new Error(`Missing Figure 6 rolling series ${percentileBin}`);
  return rows.reduce((best, item) =>
    Number(item.rolling_mean_net_saving_rate) > Number(best.rolling_mean_net_saving_rate)
      ? item
      : best
  );
}

async function readImage(relativePath) {
  const buffer = await fs.readFile(path.join(root, relativePath));
  return buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength);
}

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

const presentation = await PresentationFile.importPptx(
  await FileBlob.load(path.join(workspace, "template-starter.pptx")),
);

function slide(number) {
  return presentation.slides.items[number - 1];
}

function shape(number, name) {
  const item = slide(number).shapes.items.find((candidate) => candidate.name === name);
  if (!item) throw new Error(`Slide ${number}: missing inherited shape ${name}`);
  return item;
}

function setText(number, name, value) {
  shape(number, name).text = value;
}

function setFontSize(number, name, value) {
  shape(number, name).text.fontSize = value;
}

function setNotes(number, lines) {
  slide(number).speakerNotes.textFrame.setText(
    ["[Sources]", ...lines.map((line) => `- ${line}`), "[/Sources]"].join("\n"),
  );
  slide(number).speakerNotes.setVisible(true);
}

async function replaceChartWithImage(number, relativePath, alt) {
  const targetSlide = slide(number);
  const chart = targetSlide.charts.items[0];
  if (!chart) throw new Error(`Slide ${number}: inherited chart not found`);
  targetSlide.charts.deleteById(chart.id);
  targetSlide.images.add({
    blob: await readImage(relativePath),
    contentType: "image/png",
    alt,
    fit: "contain",
    crop: { left: 0, top: 0.07, right: 0, bottom: 0 },
    position: { left: 76, top: 158, width: 850, height: 410 },
  });
}

const pre90 = profile("pre_1982", 90);
const post80 = profile("post_1982", 80);
setText(5, "page-4", "05");
setText(5, "title-4", "Similar wealth carries much lower saving after 1982");
setText(5, "unveiling-callout-head", "Comparable mean wealth");
setText(5, "unveiling-top1", `$${Math.round(Number(pre90.real_mean_wealth_per_adult_2018_usd) / 1000)}k · ${(100 * Number(pre90.mean_annual_net_saving_rate)).toFixed(1)}%`);
setText(5, "unveiling-top1-label", "Pre: 90th pct.");
setText(5, "unveiling-next40", `$${Math.round(Number(post80.real_mean_wealth_per_adult_2018_usd) / 1000)}k · ${(100 * Number(post80.mean_annual_net_saving_rate)).toFixed(1)}%`);
setText(5, "unveiling-next40-label", "Post: 80th pct.");
setFontSize(5, "unveiling-top1", 29);
setFontSize(5, "unveiling-top1-label", 16);
setFontSize(5, "unveiling-next40", 29);
setFontSize(5, "unveiling-next40-label", 16);
setText(5, "implication-4", "The saving-rate decline is not only a change in percentile labels: similarly wealthy cohorts save much less in the later period.");
setText(5, "source-4", "Source: Figure 6 exact-method reconstruction; cohort means in 2018 dollars, not fixed-dollar bins.");
await replaceChartWithImage(
  5,
  "Results_Proposal/figures/figure6_authors_data_wealth_levels.png",
  "Figure 6 net saving rates indexed by mean real wealth per adult",
);
setNotes(5, [
  "Results_Proposal/figures/figure6_authors_data_wealth_levels.png.",
  "Data/processed/figure6_authors_data.csv, pre-1982 90th-percentile and post-1982 80th-percentile rows.",
  "Code/scripts/build_figure6_authors_data.py.",
  "docs/project/tasks/figure6-replication.md, matched wealth-level interpretation and repeated-cross-section boundary.",
]);

const rate80In1982 = rollingRate(80, 1982);
const rate80In2016 = rollingRate(80, 2016);
const top1Peak = rollingPeak(100);
setText(6, "page-4", "06");
setText(6, "title-4", "Upper-middle saving falls; the top 1% stays volatile");
setText(6, "unveiling-callout-head", "Five-year rates");
setText(6, "unveiling-top1", `${rate80In1982.toFixed(1)}% → ${rate80In2016.toFixed(1)}%`);
setText(6, "unveiling-top1-label", "80th pct.: 1982 → 2016");
setText(6, "unveiling-next40", `${(100 * Number(top1Peak.rolling_mean_net_saving_rate)).toFixed(1)}% peak`);
setText(6, "unveiling-next40-label", `Top 1% · ${top1Peak.window_end_year} window`);
setFontSize(6, "unveiling-top1", 29);
setFontSize(6, "unveiling-top1-label", 16);
setFontSize(6, "unveiling-next40", 29);
setFontSize(6, "unveiling-next40-label", 16);
setText(6, "implication-4", "The paper’s two periods compress heterogeneous dynamics: upper-middle rates trend down while the top 1% remains highly volatile.");
setText(6, "source-4", "Source: trailing five-year means of the same annual Figure 6 net saving rate; vertical line marks 1982.");
await replaceChartWithImage(
  6,
  "Results_Proposal/figures/figure6_rolling5_heatmap.png",
  "Trailing-five-year Figure 6 saving-rate heat map across wealth percentiles",
);
setNotes(6, [
  "Results_Proposal/figures/figure6_rolling5_heatmap.png.",
  "Data/processed/figure6_authors_rolling5.csv.",
  "Code/scripts/build_figure6_authors_data.py.",
  "docs/project/tasks/figure6-replication.md, time-evolution interpretation and nonmonotonicity boundary.",
]);

setText(7, "page-5", "07");

const renderDir = path.join(workspace, "final-renders");
const layoutDir = path.join(workspace, "final-layout");
await fs.mkdir(renderDir, { recursive: true });
await fs.mkdir(layoutDir, { recursive: true });
for (const [index, currentSlide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await writeBlob(
    path.join(renderDir, `${stem}.png`),
    await presentation.export({ slide: currentSlide, format: "png", scale: 2 }),
  );
  const layout = await currentSlide.export({ format: "layout" });
  await fs.writeFile(path.join(layoutDir, `${stem}.layout.json`), await layout.text());
}
await writeBlob(
  path.join(workspace, "final-montage.webp"),
  await presentation.export({ format: "webp", montage: true, scale: 1 }),
);
const inspection = await presentation.inspect({
  kind: "slide,textbox,shape,image,chart,notes,layout",
  maxChars: 120000,
});
await fs.writeFile(path.join(workspace, "final-inspect.ndjson"), inspection.ndjson);

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
