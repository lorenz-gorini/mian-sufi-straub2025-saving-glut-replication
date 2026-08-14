import fs from "node:fs/promises";
import path from "node:path";

import { Presentation, PresentationFile } from "@oai/artifact-tool";


const projectRoot = process.env.MSS_PROJECT_ROOT;
const workspace = process.env.MSS_DECK_WORKSPACE;
const outputPath = process.env.MSS_DECK_OUTPUT;
if (!projectRoot || !workspace || !outputPath) {
  throw new Error("MSS_PROJECT_ROOT, MSS_DECK_WORKSPACE, and MSS_DECK_OUTPUT are required");
}

const metricsPath = path.join(
  projectRoot,
  "Data/processed/debt_composition_presentation_metrics.csv",
);
const metrics = parseCsv(await fs.readFile(metricsPath, "utf8"));

const WIDTH = 1280;
const HEIGHT = 720;
const NAVY = "#12304A";
const ORANGE = "#C85200";
const BLUE = "#1170AA";
const PALE_BLUE = "#EAF2F7";
const PALE_ORANGE = "#FBEDE4";
const GRAY = "#53616E";
const LIGHT_GRAY = "#DCE3E8";
const WHITE = "#FFFFFF";
const FONT = "Calibri";
const TITLE_FONT = "Calibri Light";

const groupOrder = ["top_1", "next_9", "next_40", "bottom_50"];
const groupLabels = ["Top 1%", "Next 9%", "Next 40%", "Bottom 50%"];

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const headers = lines[0].split(",");
  return lines.slice(1).map((line) => {
    const values = line.split(",");
    return Object.fromEntries(headers.map((header, index) => [header, values[index]]));
  });
}

function metric(metricName, category, group) {
  const row = metrics.find(
    (item) =>
      item.metric === metricName &&
      item.category === category &&
      item.group === group,
  );
  if (!row) {
    throw new Error(`Missing presentation metric ${metricName}/${category}/${group}`);
  }
  return Number(row.value);
}

function signedMetric(value, digits, suffix) {
  const sign = value >= 0 ? "+" : "−";
  return `${sign}${Math.abs(value).toFixed(digits)}${suffix}`;
}

function addText(slide, name, text, position, style = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name,
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontSize: style.fontSize ?? 22,
    color: style.color ?? NAVY,
    bold: style.bold ?? false,
    typeface: style.typeface ?? FONT,
    alignment: style.alignment ?? "left",
    verticalAlignment: style.verticalAlignment ?? "top",
    autoFit: style.autoFit ?? "none",
    wrap: style.wrap ?? "square",
    insets: style.insets ?? { top: 0, right: 0, bottom: 0, left: 0 },
    lineSpacing: style.lineSpacing ?? 1.0,
  };
  return shape;
}

function addRect(slide, name, position, fill, line = "none") {
  return slide.shapes.add({
    geometry: "rect",
    name,
    position,
    fill,
    line:
      line === "none"
        ? { style: "solid", fill: "none", width: 0 }
        : { style: "solid", fill: line, width: 1 },
  });
}

function addChrome(slide, page, title) {
  slide.background.fill = WHITE;
  addText(
    slide,
    `eyebrow-${page}`,
    "RESEARCH EXTENSION  ·  PRELIMINARY EVIDENCE",
    { left: 72, top: 34, width: 700, height: 24 },
    { fontSize: 16, color: ORANGE, bold: true },
  );
  addText(
    slide,
    `page-${page}`,
    String(page).padStart(2, "0"),
    { left: 1180, top: 33, width: 28, height: 24 },
    { fontSize: 16, color: GRAY, alignment: "right" },
  );
  addText(
    slide,
    `title-${page}`,
    title,
    { left: 72, top: 69, width: 1110, height: 58 },
    { fontSize: 47, color: NAVY, typeface: TITLE_FONT, wrap: "none" },
  );
  addRect(
    slide,
    `title-rule-${page}`,
    { left: 72, top: 135, width: 1136, height: 3 },
    ORANGE,
  );
}

function addImplication(slide, page, text) {
  addRect(
    slide,
    `implication-band-${page}`,
    { left: 72, top: 592, width: 1136, height: 62 },
    PALE_BLUE,
  );
  addText(
    slide,
    `implication-${page}`,
    text,
    { left: 94, top: 607, width: 1092, height: 34 },
    { fontSize: 23, color: NAVY, bold: true, verticalAlignment: "middle" },
  );
}

function addSourceRail(slide, page, text) {
  addText(
    slide,
    `source-${page}`,
    text,
    { left: 72, top: 670, width: 1136, height: 24 },
    { fontSize: 16, color: GRAY },
  );
}

function setNotes(slide, lines) {
  slide.speakerNotes.textFrame.setText(
    ["[Sources]", ...lines.map((line) => `- ${line}`), "[/Sources]"].join("\n"),
  );
  slide.speakerNotes.setVisible(true);
}

function addClusteredColumn(slide, values, position, yAxis) {
  slide.charts.add("bar", {
    position,
    categories: groupLabels,
    series: [
      {
        name: "Home mortgages",
        values: values.homeMortgage,
        fill: ORANGE,
        valuesFormatCode: "0.0",
      },
      {
        name: "Consumer credit",
        values: values.consumerCredit,
        fill: BLUE,
        valuesFormatCode: "0.0",
      },
    ],
    barOptions: {
      direction: "column",
      grouping: "clustered",
      gapWidth: 72,
      overlap: 0,
    },
    hasLegend: true,
    legend: {
      position: "top",
      overlay: false,
      textStyle: { fontSize: 18, fill: NAVY },
    },
    xAxis: {
      tickLabelPosition: "low",
      textStyle: { fontSize: 18, fill: NAVY },
      line: { style: "solid", fill: LIGHT_GRAY, width: 1 },
      majorGridlines: null,
    },
    yAxis: {
      title: { text: yAxis.title, textStyle: { fontSize: 17, fill: GRAY } },
      min: yAxis.min,
      max: yAxis.max,
      majorUnit: yAxis.majorUnit,
      numberFormatCode: "0.0",
      textStyle: { fontSize: 17, fill: GRAY },
      line: { style: "solid", fill: LIGHT_GRAY, width: 1 },
      majorGridlines: { style: "solid", fill: LIGHT_GRAY, width: 1 },
    },
    dataLabels: {
      showValue: true,
      position: "outEnd",
      textStyle: { fontSize: 17, fill: NAVY, bold: true },
    },
    chartFill: WHITE,
    chartLine: { style: "solid", fill: "none", width: 0 },
    plotAreaFill: WHITE,
    plotAreaLine: { style: "solid", fill: "none", width: 0 },
  });
}

const presentation = Presentation.create({
  slideSize: { width: WIDTH, height: HEIGHT },
});

// Slide 1: minimal opening thesis.
{
  const slide = presentation.slides.add();
  slide.background.fill = WHITE;
  addText(
    slide,
    "title-eyebrow",
    "PROPOSED EXTENSION  ·  PRELIMINARY ACCOUNTING EVIDENCE",
    { left: 88, top: 70, width: 760, height: 30 },
    { fontSize: 18, color: ORANGE, bold: true },
  );
  addRect(slide, "title-accent", { left: 88, top: 133, width: 8, height: 304 }, ORANGE);
  addText(
    slide,
    "deck-title",
    "Mortgages link rich saving\nto middle-wealth borrowing",
    { left: 126, top: 132, width: 1000, height: 184 },
    { fontSize: 68, color: NAVY, typeface: TITLE_FONT, lineSpacing: 0.92 },
  );
  addText(
    slide,
    "deck-subtitle",
    "A category-specific extension of Mian, Straub, and Sufi",
    { left: 128, top: 345, width: 900, height: 40 },
    { fontSize: 28, color: GRAY },
  );
  addText(
    slide,
    "deck-boundary",
    "1963–2016 authors-kit inputs  ·  full Leontief unveiling  ·  descriptive, not causal",
    { left: 128, top: 420, width: 960, height: 34 },
    { fontSize: 21, color: NAVY, bold: true },
  );
  addRect(slide, "title-bottom-rule", { left: 88, top: 616, width: 1130, height: 2 }, LIGHT_GRAY);
  addText(
    slide,
    "title-footer",
    "Research-extension evidence for the course submission",
    { left: 88, top: 642, width: 800, height: 24 },
    { fontSize: 17, color: GRAY },
  );
  setNotes(slide, [
    "MSS_SGR_July242025.pdf, Sections 3.1, 3.5, and 4.1–4.2.",
    "research_extension_idea_2.md, Stage 1 research design.",
    "Data/processed/debt_composition_presentation_metrics.csv, generated 2026-08-14.",
  ]);
}

// Slide 4: unveiled net positions.
{
  const slide = presentation.slides.add();
  addChrome(slide, 4, "Unveiling separates mortgage lenders from borrowers");
  const values = {
    homeMortgage: groupOrder.map((group) =>
      metric("net_position_change_1982_to_2007_pp_ni", "home_mortgage", group),
    ),
    consumerCredit: groupOrder.map((group) =>
      metric("net_position_change_1982_to_2007_pp_ni", "consumer_credit", group),
    ),
  };
  addClusteredColumn(
    slide,
    values,
    { left: 76, top: 160, width: 850, height: 365 },
    {
      title: "Assets minus liabilities, 1982–2007 change (pp NI)",
      min: -23,
      max: 12,
      majorUnit: 5,
    },
  );
  addRect(slide, "unveiling-callout", { left: 955, top: 190, width: 245, height: 286 }, PALE_BLUE);
  addText(
    slide,
    "unveiling-callout-head",
    "Mortgage net positions",
    { left: 978, top: 214, width: 202, height: 36 },
    { fontSize: 22, color: BLUE, bold: true },
  );
  addText(
    slide,
    "unveiling-top1",
    signedMetric(
      metric("net_position_change_1982_to_2007_pp_ni", "home_mortgage", "top_1"),
      2,
      " pp",
    ),
    { left: 978, top: 272, width: 202, height: 44 },
    { fontSize: 37, color: NAVY, bold: true },
  );
  addText(
    slide,
    "unveiling-top1-label",
    "Top 1%",
    { left: 978, top: 319, width: 202, height: 28 },
    { fontSize: 20, color: GRAY },
  );
  addText(
    slide,
    "unveiling-next40",
    signedMetric(
      metric("net_position_change_1982_to_2007_pp_ni", "home_mortgage", "next_40"),
      2,
      " pp",
    ),
    { left: 978, top: 367, width: 202, height: 44 },
    { fontSize: 37, color: NAVY, bold: true },
  );
  addText(
    slide,
    "unveiling-next40-label",
    "Next 40%",
    { left: 978, top: 414, width: 202, height: 28 },
    { fontSize: 20, color: GRAY },
  );
  addImplication(
    slide,
    4,
    "The same mortgage expansion creates a widening lender–borrower split once banks, funds, insurers, and GSE chains are unveiled.",
  );
  addSourceRail(
    slide,
    4,
    "Source: 2021 direct cells + full Leontief solve; positive net position means ultimate assets exceed debt owed.",
  );
  setNotes(slide, [
    "Data/processed/debt_composition_2021_direct.csv, net_debt_relative_to_1982.",
    "Code/unveiling/figure8_2021_direct.py, category-specific Omega = (I - Q)^(-1) B allocation.",
    "Data/interim/debt_composition_accounting_diagnostics.csv; category additivity error at most 9.31e-10 million dollars and spectral radius at most 0.180.",
    "MSS_SGR_July242025.pdf, Sections 2.1–2.2 and 4.1–4.2.",
  ]);
}

// Slide 5: research implication and causal boundary.
{
  const slide = presentation.slides.add();
  addChrome(slide, 5, "The next step is a causal mortgage-credit test");
  addText(
    slide,
    "step-1-number",
    "01",
    { left: 86, top: 180, width: 70, height: 54 },
    { fontSize: 40, color: ORANGE, bold: true },
  );
  addText(
    slide,
    "step-1-head",
    "Established here",
    { left: 166, top: 180, width: 270, height: 36 },
    { fontSize: 27, color: NAVY, bold: true },
  );
  addText(
    slide,
    "step-1-body",
    "Mortgages dominate the pre-2008 debt build-up and saving drag for the next 40% and bottom 50%; the top 1% becomes a net ultimate lender.",
    { left: 166, top: 229, width: 280, height: 160 },
    { fontSize: 22, color: GRAY, lineSpacing: 1.05 },
  );
  addRect(slide, "step-divider-1", { left: 468, top: 178, width: 2, height: 276 }, LIGHT_GRAY);
  addText(
    slide,
    "step-2-number",
    "02",
    { left: 500, top: 180, width: 70, height: 54 },
    { fontSize: 40, color: ORANGE, bold: true },
  );
  addText(
    slide,
    "step-2-head",
    "Not identified",
    { left: 580, top: 180, width: 270, height: 36 },
    { fontSize: 27, color: NAVY, bold: true },
  );
  addText(
    slide,
    "step-2-body",
    "These accounts do not establish that credit supply caused house-price growth or lower saving. Age, homeownership, income, and housing supply remain confounders.",
    { left: 580, top: 229, width: 280, height: 160 },
    { fontSize: 22, color: GRAY, lineSpacing: 1.05 },
  );
  addRect(slide, "step-divider-2", { left: 856, top: 178, width: 2, height: 276 }, LIGHT_GRAY);
  addText(
    slide,
    "step-3-number",
    "03",
    { left: 884, top: 180, width: 70, height: 54 },
    { fontSize: 40, color: ORANGE, bold: true },
  );
  addText(
    slide,
    "step-3-head",
    "Proposed test",
    { left: 964, top: 180, width: 240, height: 36 },
    { fontSize: 27, color: NAVY, bold: true },
  );
  addText(
    slide,
    "step-3-body",
    "Combine SCF or DFA borrower detail with ultimate owners; then exploit mortgage-policy or credit-supply shocks.",
    { left: 964, top: 229, width: 240, height: 160 },
    { fontSize: 22, color: GRAY, lineSpacing: 1.05 },
  );
  addImplication(
    slide,
    5,
    "Research question: did expanded mortgage credit transmit top-wealth saving into house prices and lower measured saving below the top?",
  );
  addSourceRail(
    slide,
    5,
    "Next data: SCF/DFA borrower composition; causal design must separate credit supply from demand and wealth-rank mechanics.",
  );
  setNotes(slide, [
    "research_extension_idea_2.md, Stages 2–4 and measurement safeguards.",
    "Federal Reserve Survey of Consumer Finances: https://www.federalreserve.gov/econres/scfindex.htm",
    "Federal Reserve Distributional Financial Accounts: https://www.federalreserve.gov/releases/z1/dataviz/dfa/index.html",
    "CBO, Trends in the Distribution of Family Wealth, 1989 to 2022: https://www.cbo.gov/publication/60807",
    "Bartscher, Kuhn, Schularick, and Steins (2025): https://doi.org/10.1016/j.red.2025.101288",
  ]);
}

// Slide 2: gross liabilities.
{
  const slide = presentation.slides.insert({
    after: presentation.slides.items[0],
  }).slide;
  addChrome(slide, 2, "Mortgage debt dominated below the top 10%");
  const values = {
    homeMortgage: groupOrder.map((group) =>
      metric("liability_change_1982_to_2007_pp_ni", "home_mortgage", group),
    ),
    consumerCredit: groupOrder.map((group) =>
      metric("liability_change_1982_to_2007_pp_ni", "consumer_credit", group),
    ),
  };
  addClusteredColumn(
    slide,
    values,
    { left: 76, top: 160, width: 850, height: 410 },
    {
      title: "1982–2007 change (pp national income)",
      min: 0,
      max: 27,
      majorUnit: 5,
    },
  );
  addRect(slide, "borrower-callout", { left: 955, top: 204, width: 245, height: 260 }, PALE_ORANGE);
  addText(
    slide,
    "borrower-callout-head",
    "Largest mortgage build-up",
    { left: 978, top: 228, width: 202, height: 52 },
    { fontSize: 23, color: ORANGE, bold: true },
  );
  addText(
    slide,
    "borrower-next40",
    signedMetric(
      metric("liability_change_1982_to_2007_pp_ni", "home_mortgage", "next_40"),
      1,
      " pp",
    ),
    { left: 978, top: 300, width: 202, height: 46 },
    { fontSize: 40, color: NAVY, bold: true },
  );
  addText(
    slide,
    "borrower-next40-label",
    "Next 40% mortgage liabilities",
    { left: 978, top: 350, width: 202, height: 56 },
    { fontSize: 20, color: GRAY },
  );
  addText(
    slide,
    "borrower-contrast",
    `Top 1%: ${signedMetric(
      metric("liability_change_1982_to_2007_pp_ni", "home_mortgage", "top_1"),
      1,
      " pp",
    )}`,
    { left: 978, top: 420, width: 202, height: 30 },
    { fontSize: 20, color: NAVY, bold: true },
  );
  addImplication(
    slide,
    2,
    "The housing channel is quantitatively much larger than consumer credit for the middle 40% and bottom half.",
  );
  addSourceRail(
    slide,
    2,
    "Source: 2021 authors-kit Financial Accounts and DINA shares; positive liabilities owed; 1982–2007 change.",
  );
  setNotes(slide, [
    "Data/processed/debt_composition_2021_direct.csv, debt_liabilities_relative_to_1982.",
    "MSS2021Febreplicationkit/data/finalfiles/Yunveilhhd.dta, d_hh_hmort and d_hh_ccred.",
    "MSS2021Febreplicationkit/data/PSZusdina/Yszshares_fine.dta, owner-mortgage and nonmortgage wealth shares.",
    "Code/scripts/build_debt_composition_extension.py.",
  ]);
}

// Slide 3: active-saving contribution.
{
  const slide = presentation.slides.insert({
    after: presentation.slides.items[1],
  }).slide;
  addChrome(slide, 3, "Mortgages drove the housing-boom saving drag");
  const values = {
    homeMortgage: groupOrder.map((group) =>
      metric(
        "mean_active_saving_contribution_1998_2007_pp_ni",
        "home_mortgage",
        group,
      ),
    ),
    consumerCredit: groupOrder.map((group) =>
      metric(
        "mean_active_saving_contribution_1998_2007_pp_ni",
        "consumer_credit",
        group,
      ),
    ),
  };
  addClusteredColumn(
    slide,
    values,
    { left: 76, top: 160, width: 850, height: 410 },
    {
      title: "Average annual contribution (pp national income)",
      min: -3.7,
      max: 0.5,
      majorUnit: 1,
    },
  );
  addRect(slide, "saving-callout", { left: 955, top: 204, width: 245, height: 260 }, PALE_ORANGE);
  addText(
    slide,
    "saving-callout-head",
    "1998–2007",
    { left: 978, top: 228, width: 202, height: 36 },
    { fontSize: 22, color: ORANGE, bold: true },
  );
  addText(
    slide,
    "saving-next40",
    signedMetric(
      metric(
        "mean_active_saving_contribution_1998_2007_pp_ni",
        "home_mortgage",
        "next_40",
      ),
      2,
      " pp/yr",
    ),
    { left: 978, top: 286, width: 202, height: 46 },
    { fontSize: 37, color: NAVY, bold: true },
  );
  addText(
    slide,
    "saving-next40-label",
    "Next 40% mortgage contribution to active saving",
    { left: 978, top: 342, width: 202, height: 70 },
    { fontSize: 20, color: GRAY },
  );
  addText(
    slide,
    "saving-contrast",
    `Top 1%: ${signedMetric(
      metric(
        "mean_active_saving_contribution_1998_2007_pp_ni",
        "home_mortgage",
        "top_1",
      ),
      2,
      " pp/yr",
    )}`,
    { left: 978, top: 426, width: 202, height: 30 },
    { fontSize: 20, color: NAVY, bold: true },
  );
  addImplication(
    slide,
    3,
    "Write-down-adjusted mortgage borrowing explains most of the selected debt-related saving reduction in the boom.",
  );
  addSourceRail(
    slide,
    3,
    "Source: Figure 5 balance sheets and debt write-down factors; negative values mean active borrowing reduced saving.",
  );
  setNotes(slide, [
    "Data/processed/debt_composition_period_summary.csv, 1998–2007 period averages.",
    "MSS2021Febreplicationkit/data/finalfiles/YwealthFOF.dta, group debt levels after DINA allocation.",
    "MSS2021Febreplicationkit/data/finalfiles/Ywealthreturns.dta, mortgage and consumer-debt write-down factors.",
    "Code/unveiling/debt_composition_extension.py, S[g,k,t] = W[g,k,t] - (1 + pi[g,k,t]) W[g,k,t-1].",
  ]);
}

await fs.mkdir(workspace, { recursive: true });
await fs.mkdir(path.join(workspace, "qa", "renders"), { recursive: true });
await fs.mkdir(path.join(workspace, "qa", "layouts"), { recursive: true });

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await writeBlob(
    path.join(workspace, "qa", "renders", `${stem}.png`),
    await presentation.export({ slide, format: "png", scale: 2 }),
  );
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(
    path.join(workspace, "qa", "layouts", `${stem}.layout.json`),
    await layout.text(),
  );
}

await writeBlob(
  path.join(workspace, "qa", "montage.webp"),
  await presentation.export({ format: "webp", montage: true, scale: 1 }),
);
const inspection = await presentation.inspect({
  kind: "slide,textbox,shape,chart,notes,layout",
  maxChars: 30000,
});
await fs.writeFile(path.join(workspace, "qa", "inspect.ndjson"), inspection.ndjson);

const pptx = await PresentationFile.exportPptx(presentation);
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await pptx.save(outputPath);

console.log(`Wrote ${outputPath}`);
console.log(`Rendered ${presentation.slides.items.length} slides under ${path.join(workspace, "qa")}`);
