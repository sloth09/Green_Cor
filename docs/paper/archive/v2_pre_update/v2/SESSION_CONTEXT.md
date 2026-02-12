# Session Context (2026-02-03) - Do Not Delete

## Current Task
1. PDF 수식 렌더링 수정 (docx 경유가 아닌 markdown -> pandoc+xelatex 직접 변환)
2. paper-writer skill 개선 (PDF 생성 시 수식 깨짐 방지)
3. Yang & Lam (2023) 논문 분석 후 Section 5.4 강화

## Yang & Lam NotebookLM Prompts (user will provide answers)

**Prompt 1: Model Structure**
> Describe the complete DES model architecture. What are the entities (ships, bunker vessels, berths, etc.)? What events trigger state changes? What is the exact sequence of activities in the bunkering supply chain from ammonia arrival to delivery to the receiving vessel? Include both inbound and outbound supply chain flows.

**Prompt 2: Input Parameters (Exact Values)**
> List ALL input parameters used in the simulation with their exact numerical values and units. Specifically: (1) number of bunker supply vessels and their capacities (m3 or tons), (2) bunkering flow rates (m3/h), (3) number of receiving vessels / demand level, (4) bunker volume per call, (5) travel times or distances, (6) setup/connection times, (7) any cost parameters (CAPEX, OPEX, fuel price). Present as a table if possible.

**Prompt 3: Scenarios and Sensitivity Design**
> What scenarios were tested? For each parameter varied in sensitivity analysis, what was the range (e.g., flow rate varied by +/-50%)? How many simulation runs per scenario? Was there a base case, and what were its exact parameter values? Were multiple supply chain configurations compared, or only one?

**Prompt 4: Key Quantitative Results**
> Provide ALL key numerical results: (1) the 51.3% flow rate impact on service time - what exactly was the base value and the changed value? (2) the 15.2% vessel count impact on annual cost - same detail. (3) bunkering service time values in hours for different configurations. (4) annual operational cost values in dollars. (5) any cycle time, waiting time, or utilization rate results.

**Prompt 5: What the Model Does NOT Do**
> What does this paper explicitly NOT address? Does it: (1) optimize (find minimum cost) or only simulate predefined configurations? (2) model demand growth over multiple years, or use static/fixed demand? (3) determine optimal vessel size or fleet count, or only evaluate given configurations? (4) compare port-based storage vs remote supply alternatives? (5) include CAPEX (capital cost) of vessels, or only operational costs? (6) use any mathematical programming (LP, MILP)?

**Prompt 6: Cost Model Details**
> What costs are included in the economic evaluation? Is there a breakdown of CAPEX vs OPEX? What is the total annual cost or per-ton cost reported? How is the cost of ammonia bunkering quantified (USD/ton, USD/year, or other metric)? Are there any levelized cost figures?

## Key Decisions Made
- "Validation"이 아닌 "Cross-model comparison" / "Convergent evidence"로 프레이밍
- Yang & Lam [11] + Turkey LNG [12] 두 논문과 동시 비교가 Section 5.4 강화에 최적
- PDF는 markdown -> pandoc+xelatex 직접 변환이 수식 렌더링에 가장 깔끔

## Figure Mapping (paper_final.md figure labels -> image files)
Fig.1=D7, Fig.2=D1, Fig.3=D10, Fig.4=D6, Fig.5=D9, Fig.6=D2, Fig.7=D8,
Fig.8=D3, Fig.9=D5, Fig.10=FIG7, Fig.11=FIG8, Fig.12=FIG9, Fig.13=FIG10,
Fig.14=S7, FigS1=D12, FigS2=D11, FigS3=D4, FigS4=FIGS4, FigS5=FIGS5
All in results/paper_figures/ with .png extension
