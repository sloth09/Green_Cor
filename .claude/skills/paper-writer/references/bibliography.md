# Bibliography: Seed References and Search Slots

This document provides seed references for the paper and WebSearch query templates for finding additional literature.

---

## 1. Seed References (Known Relevant Papers)

These are starting-point references. During Phase 2 (Literature Matrix), use WebSearch to verify, update, and expand this list.

### 1.1 Ammonia as Marine Fuel

```
[1] Al-Enazi, A., Okonkwo, E. C., Bicer, Y., & Al-Ansari, T. (2021).
    "A review of cleaner alternative fuels for maritime transportation."
    Energy Reports, 7, 1962-1985.
    RELEVANCE: Comprehensive review of alternative marine fuels; ammonia properties and challenges.
    GAP: Does not address bunkering infrastructure optimization or fleet sizing.

[2] Imhoff, T. B., Gkantonas, S., & Mastorakos, E. (2021).
    "Analysing the performance of ammonia powertrains in the marine environment."
    Energies, 14(21), 7447.
    RELEVANCE: Ammonia engine performance data; SFOC values.
    GAP: Focus on propulsion, not supply chain logistics.

[3] Kim, K., Roh, G., Kim, W., & Chun, K. (2020).
    "A preliminary study on an alternative ship propulsion system fueled by ammonia:
     Environmental and economic assessments."
    Journal of Marine Science and Engineering, 8(3), 183.
    RELEVANCE: Economic assessment framework for ammonia-fueled ships.
    GAP: Single-vessel economics only; no fleet-level optimization.
```

### 1.2 Maritime Fuel Supply Chain

```
[4] **NEEDS VERIFICATION** - Current entry (Persson & Johansson, 2021) has discrepancies
    in author, title, and year per reference review. Use WebSearch to find correct metadata.
    Original claim: "Ammonia as a marine fuel: A techno-economic review."
    NOTE: This reference is cited inline in the paper (line 45: "Persson and Johansson [4]").
    If author names change, inline citations must also be updated.
    RELEVANCE: Cost parameters for ammonia bunkering.
    GAP: No optimization model; parameter estimation only.

[5] Xing, H., Stuart, C., Spence, S., & Chen, H. (2021).
    "Alternative fuel options for low carbon maritime transportation:
     Pathways to 2050."
    Journal of Cleaner Production, 297, 126651.
    RELEVANCE: Green corridor concept; decarbonization pathways.
    GAP: Policy-focused; no quantitative infrastructure optimization.
```

### 1.3 Green Corridors

```
[6] Getting to Zero Coalition. (2021).
    "The Next Wave: Green Corridors."
    Global Maritime Forum.
    RELEVANCE: Green corridor framework; Busan as candidate port.
    GAP: Strategic vision; no operational cost modeling.

[7] Lloyd's Register & UMAS. (2020).
    "Techno-economic assessment of zero-carbon fuels."
    RELEVANCE: Cost benchmarks for alternative fuels.
    GAP: Macro-level analysis; no port-specific infrastructure sizing.
```

### 1.4 MILP Optimization in Maritime

```
[8] Fagerholt, K. (2004).
    "A computer-based decision support system for vessel fleet scheduling --
     Experience and future research."
    Decision Support Systems, 37(1), 35-47.
    RELEVANCE: Fleet sizing methodology; MILP formulation for maritime.
    GAP: Focus on liner shipping; not applicable to bunkering operations.

[9] Christiansen, M., Fagerholt, K., Nygreen, B., & Ronen, D. (2013).
    "Ship routing and scheduling in the new millennium."
    European Journal of Operational Research, 228(3), 467-483.
    RELEVANCE: State-of-the-art in maritime optimization models.
    GAP: Routing focus; does not address bunkering infrastructure investment.
```

### 1.5 Bunkering Operations

```
[10] Wang, Y., & Wright, L. A. (2021).
     "A comparative review of alternative fuels for the maritime sector:
      Economic, technology, and policy challenges for clean energy implementation."
     World, 2(4), 456-481.
     RELEVANCE: Bunkering infrastructure requirements for alternative fuels.
     GAP: Qualitative review; no optimization framework.
```

---

## 2. WebSearch Query Templates

Use these during Phase 2 to find additional references. Replace placeholders with specific terms.

### Query Set A: Core Topic
```
1. "ammonia bunkering infrastructure optimization" OR "ammonia bunker vessel sizing"
2. "green corridor ammonia" AND "cost analysis" OR "economic assessment"
3. "MILP" AND "maritime fuel" AND "fleet sizing"
4. "ammonia ship-to-ship bunkering" AND "logistics"
5. "levelized cost ammonia bunkering" OR "LCOA maritime"
```

### Query Set B: Methodology Benchmarks
```
6. "mixed integer linear programming" AND "maritime infrastructure" AND "investment planning"
7. "fleet sizing optimization" AND "annualized cost" AND "maritime"
8. "shuttle tanker optimization" AND "offshore bunkering"
9. "net present cost" AND "maritime fuel supply chain"
10. "pump rate optimization" AND "bunkering operations"
```

### Query Set C: Comparison Values
```
11. "ammonia fuel cost per ton" AND "2024" OR "2025"
12. "Busan port ammonia" OR "Korea ammonia bunkering"
13. "LNG bunkering cost comparison" AND "ammonia"
14. "IMO 2050 decarbonization" AND "ammonia"
15. "ammonia storage terminal" AND "cost" AND "port"
```

### Query Set D: Recent Publications (2023-2026)
```
16. "ammonia bunkering" site:sciencedirect.com 2024 OR 2025
17. "green shipping corridor" AND "infrastructure" 2024 OR 2025
18. "alternative marine fuel" AND "optimization model" 2024 OR 2025
```

---

## 3. Literature Matrix Template

For each reference found, fill in this matrix during Phase 2:

| # | Authors (Year) | Title | Journal | Method | Fuel | Fleet Sizing? | Cost Model? | Multi-period? | Infrastructure? | What they did NOT do |
|---|---------------|-------|---------|--------|------|---------------|-------------|---------------|-----------------|---------------------|
| 1 | Al-Enazi et al. (2021) | Review of cleaner alternative fuels | Energy Reports | Review | Multiple | No | No | No | No | No optimization model |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**The "What they did NOT do" column is the most important.** It directly feeds into the research gap statement (Phase 1) and contributions (Phase 3).

---

## 4. Reference Formatting

Use numbered citation style: `[1]`, `[2]`, etc.

### In-text citation patterns:
```
Single: "Al-Enazi et al. [1] reviewed..."
Multiple: "Several studies [1, 3, 5] have examined..."
Comparison: "Unlike Kim et al. [3] who focused on single-vessel economics,
            our model optimizes fleet-level infrastructure investment."
```

### Reference list format (journal paper style):
```
[N] Author, A., Author, B., & Author, C. (Year). Title of paper.
    Journal Name, Volume(Issue), Pages. DOI: xxx
```

---

## 5. Citation Slots in Paper

Estimated citation needs by section:

| Section | Expected Citations | Purpose |
|---------|-------------------|---------|
| 1. Introduction | 8-12 | Motivation, background, gap |
| 2. Literature Review | 15-25 | Comprehensive coverage |
| 3. Methodology | 3-5 | Method justification, parameter sources |
| 4. Results | 0-2 | Comparison benchmarks |
| 5. Discussion | 5-8 | Comparison with literature |
| 6. Conclusion | 1-2 | Future work references |
| **Total** | **30-50** | |

---

## 6. Key Numbers for Literature Comparison

When comparing our results with literature, these are the most useful metrics:

| Metric | Our Value | Literature Range | Source |
|--------|----------|-----------------|--------|
| LCOA (USD/ton) | [Extract from CSV: optimal row `LCOAmmonia_USD_per_ton`] | TBD (find via WebSearch) | Phase 2 |
| Shuttle CAPEX scaling | 0.75 exponent | 0.6-0.8 typical | [verify] |
| Annualization rate | 7% | 5-10% in maritime | [verify] |
| Planning horizon | 21 years | 20-30 years typical | [verify] |
| Fuel price (NH3) | [Extract from config: `economy.fuel_price_usd_per_ton`] | 400-1000 range | [verify] |

**WARNING:** "Our Value" column must be filled from CSV/config during Phase 0. Never copy from this file.

---

## 7. v2 Reference Correction Notes

The following references have known discrepancies (from `References/Reference 검토 결과 차이점 정리.txt`).
**All must be verified via WebSearch before v2 paper finalization.**

| Ref | Issue | Details |
|-----|-------|---------|
| [4] | Author+Title+Year all different | Inline citation exists: "Persson and Johansson [4]" |
| [12] | Missing author | Turkey LNG study, no author name in paper |
| [14] | Year different | Bakkehaug et al., inline citation exists |
| [15] | Author different | Galan-Martin et al. (2021) |
| [20] | Author different | Kim, S. et al. (2025) |
| [21] | Author+Year different | Trivyza, N.L. et al. (2022) |
| [22] | Year different | Fullonton, A. et al. (2024) |
| [27] | Author different | Park, N.K. & Park, S.K. (2024) |
| [29] | Author different | Karatsidadou, D. et al. (2023) |
| [35] | Author different | Qu, Y. et al. (2024) |

**Workflow:** For each ref, WebSearch the paper title -> confirm correct author/year/journal -> update in all 4 files:
1. `docs/paper/v2/paper_final.md` (References + inline)
2. `docs/paper/v2/09_references.md`
3. `docs/paper/v2/09_references_full.md`
4. This file (`bibliography.md`)

---

## 8. Yang & Lam DES Comparison Framing Guide

When writing about the Yang & Lam comparison (Section 5.4), follow these rules from `yang_lam_evaluation.md`:

**DO use:**
- "shows consistency in shared components"
- "benchmarking against published results"
- "demonstrates reasonable calibration"
- "complementary approaches" (DES for operations, MILP for investment)

**DO NOT use:**
- "validates our model"
- "cross-validation"
- "confirms accuracy"
- "Service time agrees within 1.1%" (as headline -- pumping component only)

**Contribution strength ranking:**
1. Methodology comparison table (A) -- strongest, use as main table
2. Flow rate sensitivity gap 7.5pp (B+) -- meaningful, explain DES TRIA smoothing
3. Service time consistency (B-) -- supporting only, explain 2.4h overhead gap
4. Annual cost similarity (C) -- coincidental, mention but don't claim validation
