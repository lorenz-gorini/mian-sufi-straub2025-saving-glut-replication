# Pinned Raw Additions

These files are immutable inputs added for the independent Figure 1
reconstruction. Do not edit them in place.

| File | Source and retrieval | Unit | SHA-256 |
| --- | --- | --- | --- |
| `fwtw/fwtw_data_2026-06-18.csv` | Federal Reserve Enhanced Financial Accounts, issuer-to-holder FWTW CSV, release updated 2026-06-18; retrieved 2026-08-05 from `https://www.federalreserve.gov/releases/efa/fwtw_data.csv` | Quarterly stocks, millions of current dollars | `ca1305edd96f18da50030f784264213b37024bc046b114431167a50158aeb892` |
| `national_income/A032RC1A027NBEA_2026-08-05.csv` | BEA national income series distributed by FRED; retrieved 2026-08-05 from `https://fred.stlouisfed.org/graph/fredgraph.csv?id=A032RC1A027NBEA` | Annual flow, billions of current dollars | `38ebbe60b8cab35813c12ee9e0e9bec5ab21164031699de5ffe28ed59d9f956d` |

The producing script converts national income to millions before merging.
Detailed schemas, filters, and the vintage limitation are in
[`../../docs/data/figure1-data.md`](../../docs/data/figure1-data.md).
