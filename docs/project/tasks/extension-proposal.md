# T-008: Feasible Extension Proposal

## Objective

Develop one compact proposal that extends the paper's economic or
methodological contribution. The course deliverable needs a defensible idea,
data plan, and identifying logic; implementation is optional and must not be
claimed unless it is actually completed and verified.

Status: **In progress.** The selected proposal now asks whether financial
intermediation transformed rich saving into cheaper mortgage credit and how
nominal ownership differs from ultimate risk-bearing. The verified four-group
debt evidence selects the pre-2008 mortgage setting; the exact Figure 6
percentile decomposition, causal design, and loss-incidence layer remain.

## Deferred alternative: unveil AI circular financing

The idea is to adapt the paper's ownership-unveiling operator to the
AI financing network. Direct contracts among hyperscalers, chip and server
vendors, AI firms, special-purpose vehicles, private-credit funds, banks, and
ultimate investors can conceal who ultimately finances whom and who bears
exposure to rapidly depreciating GPU collateral.

For a liability or contractual-claim network with ultimate-owner block
$B_t$ and intermediary block $Q_t$, the same proportional allocation
would imply

$$
\Omega_t = B_t + Q_t\Omega_t
          = (I-Q_t)^{-1}B_t.
$$

The proposed outcome would be an ultimate-financier or ultimate-exposure
matrix, not a replication of the paper's household saving series. A useful
dynamic extension could stress the network after a fall in GPU collateral
values and compare direct with unveiled losses.

## Feasibility boundary

The conceptual mapping is strong, but the 2021 replication package does not
contain the contract-level AI financing network. Implementation would require
a separate evidence base covering loans, leases, securitizations, equity,
purchase commitments, guarantees, and ultimate fund investors. Private
contracts, inconsistent valuation dates, and non-proportional seniority are
likely to be the binding constraints.

Therefore the report should present this as a research design unless an
auditable public dataset can support at least a small illustrative network.
It should not imply that broad Financial Accounts or DINA data identify
firm-level AI circular financing.

## 2026-08-11 scoping questions

The first design step is to separate **ultimate ownership of financial
claims** from **ultimate incidence of credit losses**. The paper's
proportional ownership operator can trace a loan, lease, bond, fund claim, or
special-purpose-vehicle security through intermediaries to ultimate investors.
It does not by itself model default waterfalls, collateral liquidation,
guarantees, seniority, or correlated losses after GPU prices fall.

Today's scoping output should answer:

1. Which single claim type is the first empirical object: secured loans, GPU
   leases, asset-backed securities, vendor finance, or another clearly defined
   liability?
2. Which entities are issuers, financial intermediaries, and ultimate owners?
   Candidate nodes include AI labs, hyperscalers, chip/server vendors, leasing
   SPVs, private-credit funds, banks, insurers, pensions, and fund investors.
3. Which direct-dollar matrix is observable from public filings, credit
   agreements, fund disclosures, regulatory data, or commercial deal data?
4. Which row-sum or balance-sheet identity validates the direct matrix, and
   what assumption allocates claims when multiple cells are unobserved?
5. Does the contribution stop at unveiled claim ownership, or is a separate
   loss-propagation model needed to allocate collateral and default risk?

The minimum credible output is a one-page node/claim map plus a
required-versus-observable data table. A toy network may illustrate the idea,
but it must be labelled illustrative rather than empirical.

## Selection criteria

Before selecting the working extension, compare it with at least one lower-
data-cost or higher-novelty alternative. Score the alternatives on:

1. economic relevance;
2. novelty relative to the paper;
3. availability and provenance of required data;
4. identification and accounting invariants; and
5. feasibility within the course deadline.

## Working extension: from unveiled ownership to unveiled risk

[`research_extension_idea_2.md`](../../../Extension_Proposal/research_extension_idea_2.md)
is the canonical extension note. It asks whether the expansion of
intermediation transformed demand for claims by rich savers into cheaper and
more abundant mortgage credit, thereby lowering measured saving among
middle-wealth households, and who ultimately bore the associated losses.

The current authors-kit pipeline now implements a mortgage-versus-consumer-
credit decomposition through 2016 for the four broad wealth groups. It covers
liability stocks, write-down-adjusted active-saving contributions, and
category-specific ultimate ownership. Detailed credit-card, vehicle, student,
and medical-debt splits still require SCF or SIPP microdata and cannot be
recovered from the current DINA nonmortgage share. This evidence is now a
target moment and mechanism-selection result, not the novelty claim.

Pure debt composition is not sufficient novelty: CBO tabulations and Bartscher
et al. (2025) already document debt composition and long-run household debt
heterogeneity, while a large mortgage literature studies securitization and
credit supply. The proposed contribution instead joins Figures 1, 6, and 8 in
one quantitative mechanism and extends MSS's payoff-blind ownership operator
with a separate state-contingent loss-pass-through map. It distinguishes
pooling and funding benefits from weakened screening, capital absorption, and
government guarantees.

### Provisional comparison

Scores use 1 (weak) to 5 (strong) and are design judgments, not empirical
results.

| Dimension | Debt composition alone | Financialization and risk-bearing | AI circular financing |
| --- | ---: | ---: | ---: |
| Economic relevance to the target paper | 5 | 5 | 3 |
| Potential novelty | 3 | 4 | 5 |
| Public/supplied data availability | 5 | 3 | 1 |
| Accounting identification | 5 | 4 | 2 |
| Causal identification with current data | 2 | 3 | 1 |
| Feasibility for the course deadline | 5 | 4 | 1 |

The financialization/risk-bearing design is the strongest course proposal: it
uses the implemented debt evidence but has a clearer conceptual increment over
MSS. Debt composition remains the feasible empirical foundation. The AI
network remains the more speculative, high-novelty direction for a future
project if contract-level data become available.

## Definition of done

- [x] Two or more candidate extensions are stated as testable economic
      questions.
- [x] Each candidate has a required-data map, empirical or accounting design,
      expected contribution, and binding limitation.
- [x] The selected proposal is approved by the user for the extension deck.
- [x] The short extension deck labels it as preliminary, descriptive, and
      partially implemented.
- [x] The combined report clearly labels it as proposed, partially illustrated, or
      implemented.
- [x] The separate extension deck uses more than one slide only because
      verified empirical evidence has been produced.
- [ ] The final combined presentation uses at most one slide for the extension unless
      an empirical result is actually produced.

## Decision log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-08-10 | Treat AI circular financing as the leading candidate rather than an approved extension. | The unveiling logic transfers naturally, but the necessary contract-level data are not supplied by the authors' package and feasibility has not yet been established. |
| 2026-08-11 | Begin by distinguishing ultimate claim ownership from ultimate loss incidence. | The Leontief-style ownership operator traces proportional financial claims; collateral depreciation, seniority, guarantees, and defaults require additional state-contingent assumptions. |
| 2026-08-14 | Add debt composition and ultimate financing as the lower-data-cost candidate. | Existing DINA and direct-cell inputs distinguish mortgages from broad nonmortgage debt; SCF can add detailed borrower categories. This begins directly from Figures 5, 6, and 8, but causal and novelty claims require narrower wording. |
| 2026-08-14 | Use debt composition, saving, and ultimate financing as the current working extension and consolidate its two drafts. | The user is actively using the replication package to study debt composition and saving-rate evolution. The consolidated design links Figure 6, Table A2, and Figure 8 while deferring both the causal mechanism and final-submission approval until the evidence is known. |
| 2026-08-14 | Implement the broad-group mortgage-versus-consumer-credit evidence and use it as the selected extension. | The same-vintage direct-cell network and Figure 5 write-down inputs identify group stocks, active-saving contributions, and ultimate ownership without importing another vintage. The observed mortgage magnitudes justify prioritizing the housing-credit branch while retaining a causal boundary. |
| 2026-08-14 | Separate the extension into pre-2008 mortgage and post-2008 consumer-credit regimes. | Mortgage borrowing dominates the boom-era debt-related saving drag but largely disappears after 2008, while consumer credit remains negative. One common post-1980 credit mechanism would conceal this break. |
| 2026-08-15 | Use the debt-composition design as the written submission extension. | It is the most direct and best-supported continuation of Figure 6: verified same-vintage evidence selects a mortgage mechanism before 2008, while the report can state the remaining measurement and causal work without overstating it as completed. |
| 2026-08-15 | Refocus the written extension on financialization and ultimate risk-bearing. | Debt composition and the mortgage boom are heavily studied. The sharper increment is to use the mortgage evidence as motivation, open the MSS intermediation block, and distinguish nominal ownership from state-contingent loss incidence. |

## Session record: 2026-08-15 financialization and risk refocus

- Starting branch/commit: `main` at `f5d3211`; the worktree was clean.
- Goal: replace debt composition as the final novelty claim with a sharper,
  model-based extension while preserving the verified evidence.
- Changed files: the canonical design note, two-page LaTeX brief, extension
  README, three moved-file links, this task record, and the T-008 dashboard row.
- Evidence: target-paper Figures 1, 6, and 8, Table A2, and conclusion; the
  verified mortgage-versus-consumer-credit outputs; and primary literature on
  securitization, mortgage credit supply, originate-to-distribute incentives,
  and safe-asset creation.
- Reasoning: the MSS operator allocates nominal claims but is silent about
  pooling, screening, spreads, capital, guarantees, and realized losses. A
  separate state-contingent loss operator makes that boundary explicit and
  creates a quantitative counterfactual for middle borrowing and saving.
- Result: the extension now proposes a borrower--saver--intermediary model,
  testable mechanisms, an empirical sequence using HMDA/Call Reports/GSE and
  wealth data, and a 1982-intermediation counterfactual. Existing mortgage
  results remain descriptive motivating evidence.
- Next action: close the exact Figure 6 group-income contribution, then choose
  and validate one causal design before estimating the model.

## Session record: 2026-08-15 compact submission brief

- Starting branch/commit: `main`; mixed tracked and untracked work from the
  report and presentation tasks remains in the worktree.
- Goal: convert the selected extension and its verified preliminary evidence
  into a concise one-to-two-page LaTeX component matching the compact
  replication-summary style.
- Changed files: `Extension_Proposal/extension_proposal.tex`, its generated value macros
  and generator, report/code build documentation, this task record, and the
  T-008 dashboard row.
- Reasoning: begin with the paper's two-period Figure 6 profile and the
  project's time-resolved heatmap, then use the category decomposition to
  select a pre-2008 mortgage branch and a distinct post-2008 consumer-credit
  branch. Preserve the distinction between national-income-scaled preliminary
  evidence, the remaining exact group-income decomposition, and causal
  identification.
- Result: the submission brief states the research question, measurement
  equation, generated borrower/saving/ultimate-financing evidence, novelty
  relative to the paper and `Indebted Demand`, proposed empirical sequence,
  and evidentiary boundary in two pages.
- Next action: review the course-facing wording, then complete the exact Figure
  6 category-by-group-income closure and select one defensible mortgage-credit
  shock for the causal stage.

## Session record: 2026-08-15 artifact relocation

- Goal: keep the extension deliverable separate from the replication and
  referee-report sources under `Report/`.
- Changed: moved the LaTeX entry point, compiled PDF, generated value macros,
  and build documentation to `Extension_Proposal/`; updated the numerical
  producer and all live project links to the new paths.
- Validation: regenerated the macros at their new destination, rebuilt the
  two-page PDF from the relocated entry point, and visually checked both
  rendered pages.
- Result: `Extension_Proposal/` is now the self-contained submission folder;
  empirical transformation code remains under `Code/` and the authors'
  package remains unchanged.

## Session record: 2026-08-14 evidence integration and research redirection

- Starting branch/commit: `main` at `2af9442`; staged and unstaged work from
  the replication and presentation tasks remains in the worktree.
- Goal: embed the verified Stage 1 analysis in the two research-extension
  notes and convert its time pattern into an explicit next research direction.
- Changed files: `research_extension_idea_1.md`,
  `research_extension_idea_2.md`,
  `docs/data/debt-composition-extension-data.md`, this task record, and the
  T-008 row and immediate sequence in `docs/project/progress.md`.
- Evidence: all five slides of
  `Presentation/7_debt_composition_extension/presentation.pptx`; the generated
  stock, flow, period-summary, headline-metric, and diagnostics CSVs; and the
  producing code and tests.
- Validation: the current deck source matches its retained full-resolution QA
  renders; all five slides were inspected; CSV values reconcile with the slide
  claims; and the six focused debt-composition and 2021-direct tests pass.
- Result: the durable notes now distinguish the established accounting result
  from the untested causal mechanism. Mortgages dominate the pre-2008 debt
  build-up and saving drag; after 2008 mortgage borrowing contracts while
  consumer credit remains a negative contribution.
- Next action: complete the exact Figure 6 percentile/group-income
  decomposition, then design a pre-2008 mortgage-credit identification strategy
  and a separate post-2008 consumer-credit disaggregation.

## Session record: 2026-08-14 preliminary implementation

- Starting branch/commit: `main` at `0a927e3`; substantial unrelated and
  earlier project changes remain in the worktree.
- Goal: implement the selected mortgage-versus-consumer-credit extension and
  build a very short preliminary-evidence presentation.
- Changed: category-preserving Figure 8 logic, a debt-saving module, a bounded
  entry point, focused tests, generated stock/flow/period/diagnostic outputs, a
  data contract, the canonical research-design note, and a five-slide
  PowerPoint.
- Inputs: the 2021 authors-kit completed direct cells, fine DINA shares,
  Financial Accounts balance sheets/national income, and supplied mortgage and
  consumer-debt write-down factors. No seven-round output field enters the new
  ownership calculation.
- Validation: 54 annual observations; spectral radius at most 0.180; category
  asset closure below $4.17\times10^{-16}$; liability closure below
  $1.86\times10^{-9}$ million; category-to-total additivity below
  $9.31\times10^{-10}$ million; six focused tests pass. The five-slide deck was
  rendered from the exported PPTX, inspected at full size, and passed the
  automated overflow test.
- Result: from 1982 to 2007, mortgage liabilities increased by 23.63 points of
  national income for the next 40% and 13.85 points for the bottom 50%, versus
  4.50 points for the top 1%. During 1998--2007 the mortgage contribution to
  active saving averaged -3.09, -2.28, and -0.43 points per year for those
  groups. After unveiling, their mortgage net-position changes were -19.02,
  -13.73, and +8.69 points, respectively.
- Limitation: these are four-group descriptive accounts. Consumer credit is
  not split by expenditure purpose; the exact Figure 6 percentile saving-rate
  decomposition and a causal credit-supply design remain open.
- Next action: decide whether to add the exact Figure 6 percentile
  decomposition before integrating one extension slide into the combined
  submission.

## Session record: 2026-08-14 extension-note consolidation

- Starting branch/commit: `main` at `0a927e3`; substantial unrelated and
  earlier project changes remain in the worktree.
- Goal: merge the parallel debt-composition drafts into one canonical note
  ready to receive verified evidence from the coding session.
- Changed files: `research_extension_idea_2.md`; removed the superseded
  `research_extension_idea_2B.md`; updated this task record and
  `docs/project/progress.md`.
- Reasoning: retain the rigorous data, notation, invariants, and staged design
  from the main note; incorporate the sharper distinction between explaining
  why debt rose and measuring which debt reduced saving; and sequence the work
  as fact, accounting decomposition, ultimate financing, then mechanism.
- Validation: checked the framing against the target paper's Sections 3.4–3.5,
  Figures 6 and 8, Table A1, Table A2, Appendix C.4, and the existing Figure 6
  and Figure 8 project contracts.
- Result: one canonical proposal now connects category-specific debt flows to
  the Figure 6 saving-rate denominator and the Figure 8 unveiling operator,
  with instrument-versus-purpose and causal-identification boundaries explicit.
- Next action: add only coding results that pass category-to-total stock, flow,
  saving-rate, income-weighting, and unveiling closure checks.

## Session record: 2026-08-14 debt-composition scoping

- Starting branch/commit: `main` at `0a927e3`; substantial unrelated and
  earlier project changes remain in the worktree.
- Goal: formalize the user's proposed debt-composition extension, determine
  what the current files identify, and relate it to the other extension
  directions without claiming implementation.
- Changed files: `research_extension_idea_2.md`,
  `research_extension_idea_1.md`, this task record, and
  `docs/project/progress.md`.
- Evidence: the target paper's Sections 3.1, 3.5, and 4.1–4.2; Table A1; Table
  A2; Appendix C.4; the two Figure 8 data contracts; the existing Python
  instrument mappings; and official SCF, DFA, FWTW, SIPP, PSID, and Financial
  Accounts documentation.
- Result: a two-stage boundary is explicit. Mortgage versus nonmortgage
  ownership and saving contributions are feasible with current inputs;
  category-rich borrower incidence requires SCF/SIPP, and causal claims require
  a separate shock-based design.
- Next action: select the course extension. If debt composition is selected,
  implement Stage 1 before acquiring additional microdata.

## Session record: 2026-08-11 activation

- Starting branch/commit: `main` at `880b14b`; unrelated and earlier project
  changes remain in the worktree.
- Goal: activate the AI circular-financing idea as today's bounded research-
  design task without claiming an implementation.
- Changed files: this task record and `docs/project/progress.md`.
- Result: T-008 now has a first deliverable, candidate network nodes, a public-
  data question, and an explicit boundary between ownership unveiling and loss
  propagation.
- Next action: choose one claim type and draw its direct issuer--holder map
  before searching for data.

## Session record: 2026-08-10 task refresh

- Starting version: the workspace is not recognized as a Git worktree, so no
  branch or commit identifier is available.
- Goal: preserve the user's extension idea without mixing speculative work
  into the three core replication figures.
- Result: the AI application is scoped as an ultimate-financing/exposure
  network and explicitly separated from the paper's household-saving
  measurement.
- Next action: formulate and score a lower-data-cost alternative before the
  user chooses the final report proposal.
