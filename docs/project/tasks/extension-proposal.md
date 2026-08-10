# T-008: Feasible Extension Proposal

## Objective

Develop one compact proposal that extends the paper's economic or
methodological contribution. The course deliverable needs a defensible idea,
data plan, and identifying logic; implementation is optional and must not be
claimed unless it is actually completed and verified.

## Leading candidate: unveil AI circular financing

The leading idea is to adapt the paper's ownership-unveiling operator to the
AI financing network. Direct contracts among hyperscalers, chip and server
vendors, AI firms, special-purpose vehicles, private-credit funds, banks, and
ultimate investors can conceal who ultimately finances whom and who bears
exposure to rapidly depreciating GPU collateral.

For a liability or contractual-claim network with ultimate-owner block
\(B_t\) and intermediary block \(Q_t\), the same proportional allocation
would imply

\[
\Omega_t = B_t + Q_t\Omega_t
          = (I-Q_t)^{-1}B_t.
\]

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

## Alternative required before selection

Develop at least one lower-data-cost alternative that reuses the supplied
macro-financial inputs—for example, testing the sensitivity of unveiled
household-debt ownership to alternative proportional-allocation or sector-
aggregation assumptions. Score the alternatives on:

1. economic relevance;
2. novelty relative to the paper;
3. availability and provenance of required data;
4. identification and accounting invariants; and
5. feasibility within the course deadline.

## Definition of done

- [ ] Two or more candidate extensions are stated as testable economic
      questions.
- [ ] Each candidate has a required-data map, empirical or accounting design,
      expected contribution, and binding limitation.
- [ ] The selected proposal is approved by the user.
- [ ] The report clearly labels it as proposed, partially illustrated, or
      implemented.
- [ ] The final presentation uses at most one slide for the extension unless
      an empirical result is actually produced.

## Decision log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-08-10 | Treat AI circular financing as the leading candidate rather than an approved extension. | The unveiling logic transfers naturally, but the necessary contract-level data are not supplied by the authors' package and feasibility has not yet been established. |

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
