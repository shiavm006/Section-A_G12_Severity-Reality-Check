# DeliverIQ — Severity Reality Check

> **Newton School of Technology | Data Visualization & Analytics**
> Section-A · Team G12 · A 2-week industry-style capstone using Python, GitHub, and Tableau Public to disentangle **true accident severity** from congestion, time-of-day, and location bias in publicly available US road accident data.

---

## Project Overview


| Field                | Details                                                                                                                                                              |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Project Codename** | DeliverIQ                                                                                                                                                            |
| **Project Title**    | Severity Reality Check: Disentangling True Accident Severity from Congestion Bias                                                                                    |
| **Sector**           | Transportation & Public Safety                                                                                                                                       |
| **Section**          | A                                                                                                                                                                    |
| **Team ID**          | G12                                                                                                                                                                  |
| **Faculty Mentor**   | *Fill mentor name*                                                                                                                                                   |
| **Institute**        | Newton School of Technology                                                                                                                                          |
| **GitHub Repo**      | [https://github.com/shiavm006/Section-A_G12_DeliverIQ](https://github.com/shiavm006/Section-A_G12_DeliverIQ)                                                         |
| **Tableau Public**   | [https://public.tableau.com/views/RoadAccidentDataofUSA_17773613139680/Dashboard1](https://public.tableau.com/views/RoadAccidentDataofUSA_17773613139680/Dashboard1) |
| **Submission Date**  | April 29, 2026                                                                                                                                                       |


### Team Members


| Role                          | Name             | Email                                                                                         |
| ----------------------------- | ---------------- | --------------------------------------------------------------------------------------------- |
| Project Lead                  | Shivam Mittal    | [shivam.mittal2024@nst.rishihood.edu.in](mailto:shivam.mittal2024@nst.rishihood.edu.in)       |
| Data Lead                     | Satyam Kumar     | [satyam.kumar2024@nst.rishihood.edu.in](mailto:satyam.kumar2024@nst.rishihood.edu.in)         |
| ETL Lead                      | Keshav           | [keshav.2024@nst.rishihood.edu.in](mailto:keshav.2024@nst.rishihood.edu.in)                   |
| Analysis Lead                 | Mohit Singh      | [mohit.singh2024@nst.rishihood.edu.in](mailto:mohit.singh2024@nst.rishihood.edu.in)           |
| Visualization Lead            | Prachee Dhar     | [prachee.dhar2024@nst.rishihood.edu.in](mailto:prachee.dhar2024@nst.rishihood.edu.in)         |
| Strategy + PPT & Quality Lead | Rishita Boisnobi | [rishita.boisnobi2024@nst.rishihood.edu.in](mailto:rishita.boisnobi2024@nst.rishihood.edu.in) |


---

## Business Problem

Road accident data is widely used by logistics companies, insurers, and state policymakers to assess corridor risk, set premiums, and allocate infrastructure dollars. But the most common public severity field — found in the largest US accidents dataset — measures **impact on traffic flow** (short delay vs. long delay), **not collision severity** (injury or property damage). This means a routine fender-bender on a congested highway can be labeled "Severity 4" while a fatal crash on a quiet rural road may be labeled "Severity 1." Decisions made directly on this raw signal are systematically biased toward congestion-prone corridors and away from genuinely high-risk locations.

This project disentangles **true accident severity** from congestion, time-of-day, and location bias by introducing an operational definition of "True Severe" — a Severity-4 accident whose road impact extends at least half a mile — and quantifying how much of the conventional severity signal is actually congestion noise.

### Core Business Question

> **What share of accidents flagged as "severe" in the US Accidents dataset are genuinely severe — and how should logistics planners, insurers, and DOT policymakers adjust their decisions to use a bias-corrected severity signal?**

### Decision Supported

The corrected severity signal enables:

- **Insurers** — adjust risk weights in pricing models when ingesting public severity data
- **State DOTs** — prioritize infrastructure investment based on True Severe hotspots, not raw counts
- **Logistics & fleet operators** — re-rank corridors and dispatch windows using bias-adjusted risk

---

## Dataset


| Attribute               | Details                                                                                                                  |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Source Name**         | Kaggle — *US Accidents (2016 – 2023)* by Sobhan Moosavi                                                                  |
| **Direct Access Link**  | [https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) |
| **Original Size**       | ~7.7 million rows × 46 columns (3.06 GB)                                                                                 |
| **Working Sample**      | 95,607 rows × 49 columns (balanced stratified sample, derived in `01_extraction.ipynb`)                                  |
| **Time Period Covered** | February 2016 – March 2023                                                                                               |
| **Format**              | CSV                                                                                                                      |
| **License**             | CC BY-NC-SA 4.0 (academic / research only)                                                                               |
| **Geographic Coverage** | 49 contiguous US states, 5,558 cities                                                                                    |


### Key Columns Used


| Column Name                              | Description                                                                  | Role in Analysis                                                           |
| ---------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `Severity`                               | Traffic-flow impact (1 = short delay, 4 = long delay) — **not** crash injury | Target field, KPI input, central to bias hypothesis                        |
| `Distance_mi`                            | Length of road segment affected by the accident (miles)                      | Defines `Is True Severe` filter (≥ 0.5 mi)                                 |
| `Start_Time`                             | Local-time accident start (date + hour)                                      | Source of `Year`, `Month`, `Day_of_Week`, `Hour`, `Is_Rush_Hour`, `Season` |
| `State`, `City`                          | Geographic location                                                          | Hotspot analysis, regional bias detection                                  |
| `Weather_Condition`                      | Raw weather text (52 unique values)                                          | Rolled up to `Weather_Category` for visualization                          |
| `Visibility_mi`                          | Visibility at time of accident                                               | Source of `Visibility Bucket`; tested for environmental bias               |
| `Junction`, `Traffic_Signal`, `Crossing` | POI booleans for road infrastructure                                         | Used in lift calculations (Junction Lift, Signal Drop)                     |


For full column definitions, derived features, and cleaning notes, see `[docs/data_dictionary.md](docs/data_dictionary.md)`.

---

## KPI Framework

15 KPIs spread across 3 dashboards. Each KPI is decision-relevant for at least one stakeholder.

### Dashboard 1 — Severity Reality Check


| #   | KPI                       | Formula                                                           |
| --- | ------------------------- | ----------------------------------------------------------------- |
| 1   | Total Accidents           | `COUNT([Severity])`                                               |
| 2   | Critical / Nominal Severe | `SUM(IF [Severity]=4 THEN 1 ELSE 0 END)`                          |
| 3   | True Severe               | `SUM(IF [Severity]=4 AND [Distance_mi] >= 0.5 THEN 1 ELSE 0 END)` |
| 4   | Avg Duration of Severe    | `AVG(IF [Severity]=4 THEN [Duration_min] END)`                    |
| 5   | Severe Distance (mi)      | `SUM(IF [Severity]=4 THEN [Distance_mi] END)`                     |


### Dashboard 2 — When Risk Actually Strikes


| #   | KPI                  | Formula                                                                        |
| --- | -------------------- | ------------------------------------------------------------------------------ |
| 6   | Worst Season         | Season with highest `{ FIXED [Season] : AVG([Severity]) }`                     |
| 7   | Peak Risk Hour       | Hour-of-day with highest `{ FIXED [Hour] : AVG([Severity]) }`                  |
| 8   | Weekend vs Weekday Δ | `AVG(Severity                                                                  |
| 9   | Night Sev 3+ Share   | Proportion of Sev 3+ accidents that happen at night                            |
| 10  | Riskiest Weather     | Weather category with highest `{ FIXED [Weather_Category] : AVG([Severity]) }` |


### Dashboard 3 — Where & Why (Geography & Road-Feature Bias)


| #   | KPI                      | Formula                                                                                                           |
| --- | ------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| 11  | Top State by Volume      | State with highest `COUNT([Severity])`                                                                            |
| 12  | Top State by Severity    | State with highest avg severity above the 500-accident threshold                                                  |
| 13  | Junction Severity (Lift) | `{ FIXED : AVG(IF [Junction]=1 THEN [Severity] END) } - { FIXED : AVG([Severity]) }`                              |
| 14  | Signal Drop              | `{ FIXED : AVG(IF [Traffic_Signal]=0 THEN [Severity]) } - { FIXED : AVG(IF [Traffic_Signal]=1 THEN [Severity]) }` |
| 15  | Cities Tracked           | `COUNTD([City])`                                                                                                  |


KPI computation logic is documented in `notebooks/04_statistical_analysis.ipynb` and `notebooks/05_final_load_prep.ipynb`. Tableau-side calculations are stored in the workbook at `tableau/Road Accident Data of USA.twbx`.

---

## Tableau Dashboards


| Item                | Details                                                                                                                                                              |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Dashboard URL**   | [https://public.tableau.com/views/RoadAccidentDataofUSA_17773613139680/Dashboard1](https://public.tableau.com/views/RoadAccidentDataofUSA_17773613139680/Dashboard1) |
| **Workbook File**   | `tableau/Road Accident Data of USA.twbx`                                                                                                                             |
| **Number of Views** | 3 dashboards (Severity Reality Check / When Risk Actually Strikes / Where & Why)                                                                                     |
| **Worksheet Count** | 30+ (15 KPI cards + 12 chart sheets)                                                                                                                                 |


### Dashboard 1 — Severity Reality Check (Executive view)

KPI strip: Total Incidents · Critical Accidents · True Severe Accidents · Avg Duration Severe · Severe Distance. Visuals: Severity Donut, Severity Impact bar, Rush Hour Analysis, Hourly Trend, Weekend Analysis. **Filters:** Rush Hour, Severity.

### Dashboard 2 — When Risk Actually Strikes (Operational view, temporal/weather drill-down)

KPI strip: Worst Season (Winter) · Peak Risk Hour (12 AM) · Weekend vs Weekday Δ (+0.34) · Night Sev 3+ Share (8.42%) · Riskiest Weather (Drifting Snow / Windy). Visuals: 24-Hour Severity Clock, Day vs Time Heatmap, Weather Severity, Temperature vs Severity by Season, Visibility vs Severity. **Filters:** Visibility Bucket, Time of Day.

### Dashboard 3 — Where & Why (Operational view, geographic/infrastructure drill-down)

KPI strip: Top State by Volume (CA, 8,780) · Top State by Severity (WV) · Junction Severity (+28.8%) · Signal Drop (−62.1%) · Cities Tracked (5,558). Visuals: Top 12 States bubble chart, Road Feature Impact, Top 8 Cities, More Features ≠ More Danger. **Filters:** Severity slider.

Dashboard screenshots are stored in `[tableau/screenshots/](tableau/screenshots/)` and public URLs in `[tableau/dashboard_links.md](tableau/dashboard_links.md)`.

---

## Key Insights

1. **Severity inflation is real and large.** Roughly half of all "Severity 4" accidents fail a basic crash-impact threshold (≥ 0.5 mi road affected). Decisions taken on raw severity counts systematically over-weight congestion-prone corridors.
2. **Peak risk hour is midnight, not rush hour.** Average severity peaks at hour 0 (12 AM). Volume peaks at 5 PM but *severity* peaks 6–7 hours later — a counter-intuitive finding that collapses the rush-hour assumption.
3. **Pennsylvania leads on True Severe — not California.** Despite CA's dominant accident volume, PA records the highest avg severity. Per-accident severity in PA is materially higher than the national average.
4. **West Virginia tops the Severity leaderboard.** When ranked by avg severity (above the 500-accident threshold), WV beats every larger state — likely driven by mountainous interstate corridors and limited EMS access.
5. **Junction proximity raises severity by 28.8%.** Junctions are a measurable infrastructure risk factor — supporting the case for redesigns at top hotspots.
6. **Traffic signals reduce severity by 62.1%.** Locations *with* a traffic signal record dramatically lower severity than those without. Signal installation is a quantifiable, ROI-positive intervention.
7. **More road features ≠ more danger.** Severity doesn't rise monotonically with road-feature count — the relationship oscillates. Single hotspots matter more than dense feature combinations.
8. **Weekend severity is +0.34 points higher** than weekday, despite lower volume — leisure / DUI driving compensates for fewer trips.

---

## Recommendations


| #   | Insight Reference                | Recommendation                                                                                                                | Expected Impact                                                                   |
| --- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 1   | #1 — Severity inflation          | **Insurers**: Apply a ~50% discount factor when using publicly reported Severity 4 in pricing; switch to a True-Severe metric | More accurate risk-tier pricing; recovery of mis-priced urban-policy margin       |
| 2   | #6 — Signal Drop                 | **State DOTs**: Prioritize traffic-signal installations at top-N junction hotspots from Dashboard 3                           | ~62% severity reduction at signal-equipped sites; measurable per-installation ROI |
| 3   | #2 + #5 — Night & junction risk  | **Logistics fleets**: Re-rank corridors by True-Severe Index; shift long-haul dispatch off PA + winter night windows          | Lower expected claim frequency and severity per million route-miles               |
| 4   | #4 — WV / PA over-representation | **Federal grants**: Reweight per-state safety allocations using True-Severe counts rather than raw volume                     | Federal dollars track real severity outcomes, not raw reporting frequency         |
| 5   | #3 — CA volume vs PA severity    | **Ride-share / fleet operators**: Adjust state-level driver pay differentials and rest-cycle mandates by True-Severe density  | Driver-safety alignment with actual risk; lower carrier liability exposure        |


---

## Repository Structure

```text
Section-A_G12_DeliverIQ/
├── README.md                                # this file
│
├── data/
│   ├── raw/                                 # original Kaggle dataset (never edited)
│   └── processed/                           # cleaned + Tableau-ready outputs
│
├── notebooks/
│   ├── 01_extraction.ipynb                  # balanced sampling from 7.7M rows
│   ├── 02_cleaning.ipynb                    # context-aware imputation + ETL
│   ├── 03_eda.ipynb                         # 6-section EDA incl. congestion bias
│   ├── 04_statistical_analysis.ipynb        # chi-square, Kruskal-Wallis, location bias
│   └── 05_final_load_prep.ipynb             # Tableau feature engineering
│
├── scripts/
│   └── etl_pipeline.py                      # reusable ETL module
│
├── tableau/
│   ├── Road Accident Data of USA.twbx       # workbook (3 dashboards, 30+ sheets)
│   ├── dashboard_links.md
│   └── screenshots/                         # dashboard_1.png · dashboard_2.png · dashboard_3.png
│
├── reports/
│   ├── project_report.pdf                   # final report (10-15 pages)
│   ├── presentation.pdf                     # final deck (11 slides)
│   ├── project_report.md                    # source markdown (re-renderable)
│   ├── presentation.pptx                    # source deck (editable)
│   ├── build_deck.py                        # rebuild script
│   └── eda_plots/                           # 8 EDA visualizations
│
├── docs/
│   └── data_dictionary.md                   # full column definitions
│
├── DVA-oriented-Resume/                     # one resume per team member
└── DVA-focused-Portfolio/                   # one portfolio per team member
```

---

## Analytical Pipeline

1. **Define** — Sector & problem statement scoped; mentor approval at Gate 1.
2. **Extract** — Kaggle US Accidents (7.7M rows) → balanced sample of 95,607 rows in `01_extraction.ipynb`.
3. **Clean & Transform** — `02_cleaning.ipynb` + `scripts/etl_pipeline.py` with context-aware imputation.
4. **Analyze** — EDA (`03_eda.ipynb`) + statistical tests (`04_statistical_analysis.ipynb`).
5. **Visualize** — Three Tableau Public dashboards (`tableau/Road Accident Data of USA.twbx`).
6. **Recommend** — Five business recommendations tied to insights with expected impact.
7. **Report** — Final PDF report + 11-slide deck shipped in `reports/`.

---

## Tech Stack


| Tool                       | Status    | Purpose                                              |
| -------------------------- | --------- | ---------------------------------------------------- |
| Python + Jupyter Notebooks | Mandatory | ETL, cleaning, statistical analysis, KPI computation |
| Google Colab               | Supported | Cloud notebook environment                           |
| Tableau Public             | Mandatory | Dashboard design + publishing                        |
| GitHub                     | Mandatory | Version control + collaboration audit                |


**Python libraries**: `pandas`, `numpy`, `scipy`, `statsmodels`, `matplotlib`, `seaborn`. Full requirements in `[requirements.txt](requirements.txt)`.

---

## Evaluation Rubric


| Area                        | Marks   | Focus                                                       |
| --------------------------- | ------- | ----------------------------------------------------------- |
| Problem Framing             | 10      | Is the business question clear and well-scoped?             |
| Data Quality and ETL        | 15      | Is the cleaning pipeline thorough and documented?           |
| Analysis Depth              | 25      | Are statistical methods applied correctly with insight?     |
| Dashboard and Visualization | 20      | Is the Tableau dashboard interactive and decision-relevant? |
| Business Recommendations    | 20      | Are insights actionable and well-reasoned?                  |
| Storytelling and Clarity    | 10      | Is the presentation professional and coherent?              |
| **Total**                   | **100** |                                                             |


---

## Submission Checklist

### GitHub Repository

- Public repository: `Section-A_G12_DeliverIQ`
- All five notebooks committed in `.ipynb`
- `data/raw/` contains the original Kaggle dataset
- `data/processed/` contains the cleaned + Tableau-ready outputs
- `tableau/screenshots/` contains 3 dashboard screenshots
- `tableau/dashboard_links.md` contains the Tableau Public URL
- `docs/data_dictionary.md` complete
- `README.md` explains project, dataset, KPIs, insights, team
- All members have visible GitHub commits + PRs

### Tableau Dashboard

- Three dashboards published on Tableau Public
- At least one interactive filter on each dashboard
- Dashboards directly address the bias-correction problem

### Project Report

- Final report exported as `reports/project_report.pdf`
- All 18 sections complete (cover → contribution matrix)

### Presentation Deck

- Final deck exported as `reports/presentation.pdf` (11 slides)

### Individual Assets

- DVA-oriented resume per team member
- DVA-focused portfolio per team member

---

## Contribution Matrix


| Team Member      | Dataset & Sourcing | ETL & Cleaning | EDA & Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT & Viva |
| ---------------- | ------------------ | -------------- | -------------- | -------------------- | ----------------- | -------------- | ---------- |
| Shivam Mittal    | Owner              | Owner          | Support        | Support              | Owner             | Owner          | Owner      |
| Satyam Kumar     | Owner              | Support        | Support        | Owner                | Support           | Support        | Support    |
| Keshav           | Support            | Owner          | Support        | Support              | Support           | Support        | Support    |
| Mohit Singh      | Support            | Support        | Owner          | Owner                | Support           | Support        | Support    |
| Prachee Dhar     | Support            | Support        | Support        | Support              | Owner             | Support        | Support    |
| Rishita Boisnobi | Support            | Support        | Support        | Support              | Support           | Owner          | Owner      |


> Adjust each cell to match actual GitHub commit / PR history before final submission.

**Declaration:** We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts.

**Team Lead:** Shivam Mittal

**Date:** April 29, 2026

---

## Academic Integrity

All analysis, code, and recommendations in this repository are the original work of the team listed above. No analysis was copied from public Kaggle notebooks. Free-riding is tracked via GitHub Insights and pull-request history.

---

## Reproducibility

```bash
git clone https://github.com/shiavm006/Section-A_G12_DeliverIQ.git
cd Section-A_G12_DeliverIQ

python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

jupyter notebook
```

Run notebooks in order: `01_extraction → 02_cleaning → 03_eda → 04_statistical_analysis → 05_final_load_prep`. Open `tableau/Road Accident Data of USA.twbx` in Tableau Public Desktop to inspect dashboards.

---

## Citation

If you reference the underlying dataset, please cite:

> Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, and Rajiv Ramnath. *"A Countrywide Traffic Accident Dataset."* 2019.
>
> Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, Radu Teodorescu, and Rajiv Ramnath. *"Accident Risk Prediction based on Heterogeneous Sparse Data: New Dataset and Insights."* 27th ACM SIGSPATIAL Conf., 2019.

---

*Newton School of Technology · Data Visualization & Analytics · Capstone 2 · April 2026*