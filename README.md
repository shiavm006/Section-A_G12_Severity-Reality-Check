# NST DVA Capstone 2 — Severity Reality Check

> **Newton School of Technology | Data Visualization & Analytics**
> A 2-week industry-style capstone using Python, GitHub, and Tableau Public to disentangle **true accident severity** from congestion, time-of-day, and location bias in publicly available US road accident data.

---

## Project Overview


| Field             | Details                                                                           |
| ----------------- | --------------------------------------------------------------------------------- |
| **Project Title** | Severity Reality Check: Disentangling True Accident Severity from Congestion Bias |
| **Sector**        | Transportation & Public Safety                                                    |
| **Team ID**       | *DVA-G12*                                                                         |
| **Section**       | *A*                                                                               |


```
                                                                                                                                   
```

### Team Members


| Role                 | Name   | GitHub Username |
| -------------------- | ------ | --------------- |
| Project Lead         | *Name* | `github-handle` |
| Data Lead            | *Name* | `github-handle` |
| ETL Lead             | *Name* | `github-handle` |
| Analysis Lead        | *Name* | `github-handle` |
| Visualization Lead   | *Name* | `github-handle` |
| Strategy Lead        | *Name* | `github-handle` |
| PPT and Quality Lead | *Name* | `github-handle` |


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
| **License**             | CC BY-NC-SA 4.0 (academic / research only — both Moosavi papers cited in `docs/data_dictionary.md`)                      |
| **Geographic Coverage** | 49 contiguous US states, 6,800+ cities                                                                                   |


### Why a Sampled Dataset

The full 7.7 M-row file is highly imbalanced — Severity 2 represents ~80 % of all records, while Severity 1 and Severity 4 are rare. To support fair statistical analysis across all severity levels, we extracted a **balanced stratified sample of ~100 K rows**, ensuring sufficient representation for every severity tier while retaining geographic diversity. Sampling logic is documented in `notebooks/01_extraction.ipynb` and `scripts/etl_pipeline.py`.

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

### Dashboard 1 — Severity Reality Check (the hook)


| #   | KPI                    | Formula / Computation                                                                                     |
| --- | ---------------------- | --------------------------------------------------------------------------------------------------------- |
| 1   | Total Accidents        | `COUNT([Severity])` — sample size credibility marker                                                      |
| 2   | Nominal Severe (Sev 4) | `SUM(IF [Severity]=4 THEN 1 ELSE 0 END)` — naive severity count                                           |
| 3   | True Severe            | `SUM(IF [Severity]=4 AND [Distance_mi] >= 0.5 THEN 1 ELSE 0 END)` — bias-corrected severity count         |
| 4   | True Severe %          | `SUM(True Severe Count) / SUM(Nominal Severe Count)` — **headline metric**: share of "severe" that's real |
| 5   | Avg Duration of Severe | `AVG(IF [Severity]=4 THEN [Duration_min] END)` — operational cost of major incidents (minutes to clear)   |


### Dashboard 2 — When & Where Risk Actually Strikes (the diagnosis)


| #   | KPI                      | Formula / Computation                                              |
| --- | ------------------------ | ------------------------------------------------------------------ |
| 6   | Worst Season             | Season with highest `{ FIXED [Season] : AVG([Severity]) }`         |
| 7   | Peak Risk Hour           | Hour-of-day with highest `{ FIXED [Hour] : AVG([Severity]) }`      |
| 8   | Top State by True Severe | State with highest `SUM([True Severe Count])`                      |
| 9   | Weekend vs Weekday Δ     | `AVG(Severity | Weekend) − AVG(Severity | Weekday)` — signed delta |
| 10  | Cities Tracked           | `COUNTD([City])` — coverage breadth marker                         |


### Dashboard 3 — Conditions Behind Crashes (the cause)


| #   | KPI                                    | Formula / Computation                                                                                                     |
| --- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 11  | Riskiest Weather                       | Weather category with highest `{ FIXED [Weather_Category] : AVG([Severity]) }`                                            |
| 12  | Junction Lift                          | `{ FIXED : AVG(IF [Junction]=1 THEN [Severity] END) } - { FIXED : AVG([Severity]) }`                                      |
| 13  | Signal Drop                            | `{ FIXED : AVG(IF [Traffic_Signal]=0 THEN [Severity] END) } - { FIXED : AVG(IF [Traffic_Signal]=1 THEN [Severity] END) }` |
| 14  | Avg Visibility During Severe Accidents | `AVG(IF [Severity]=4 THEN [Visibility_mi] END)` — counter-intuitive environmental finding                                 |
| 15  | Night Severe Share                     | `SUM(IF Time_of_Day="Night" AND Severity>=3 THEN 1 ELSE 0 END) / COUNT([Severity])`                                       |


KPI computation logic is documented in `notebooks/04_statistical_analysis.ipynb` and `notebooks/05_final_load_prep.ipynb`. Tableau-side calculations are stored in the workbook at `tableau/Road Accident Data of USA.twbx`.

---

## Tableau Dashboard


| Item                 | Details                                    |
| -------------------- | ------------------------------------------ |
| **Dashboard URL**    | *Paste Tableau Public link here*           |
| **Executive View**   | *Describe the high-level KPI summary view* |
| **Operational View** | *Describe the detailed drill-down view*    |
| **Main Filters**     | *List the interactive filters used*        |


Store dashboard screenshots in `[tableau/screenshots/](tableau/screenshots/)` and document the public links in `[tableau/dashboard_links.md](tableau/dashboard_links.md)`.

---

## Key Insights

Eight decision-language insights distilled from EDA, statistical analysis, and dashboarding.

1. **Severity inflation is real and large.** Roughly **half of all accidents labeled "Severity 4" fail a basic crash-impact threshold** of 0.5 miles of road affected. Decisions taken on raw severity counts systematically over-weight congestion-prone corridors.
2. **Peak risk hour is midnight, not rush hour.** Average severity peaks at hour 0 (12 AM) and stays elevated through the early morning hours — counter to the assumption that 5 PM rush hour is the most dangerous window. Volume peaks at 5 PM; *severity* peaks at midnight.
3. **Pennsylvania leads on True Severe — not California.** Despite CA having the highest accident *volume*, PA records the most True Severe accidents. Per-accident severity in PA is roughly 3 × the national average, likely driven by interstate trucking corridors, mountainous terrain, and winter conditions.
4. **Most severe accidents happen in *clear* weather.** Average visibility during Severity 4 events is ~9.1 miles — well above the threshold for poor visibility. The popular assumption that fog/storms drive severity is largely wrong in this dataset.
5. **Traffic signals measurably reduce severity.** Locations *without* a traffic signal record ~0.4 severity points higher per accident. Signal installation is a quantifiable, ROI-positive infrastructure intervention.
6. **Junction proximity adds 0.2 – 0.5 severity points.** Junctions are a measurable risk factor — supporting the case for redesigns (roundabouts, additional signage, dedicated turn lanes) at top hotspots.
7. **Weekend ≠ weekday severity is a weak signal.** The Δ between weekend and weekday average severity is small (~ ±0.1 points). Day-of-week is largely noise once temporal patterns within a day are controlled for.
8. **Severe accidents take ~3.5 hours to clear.** Average traffic-impact duration for Severity 4 events is ~212 minutes — about 7× longer than typical fender-benders. This validates the True Severe definition and quantifies real EMS / dispatch costs.

> Insights are written in *decision* language — each tells the reader what to think or what to act on, not merely what a chart shows.

---

## Recommendations

Five actionable recommendations, each linked to a specific insight.


| #   | Insight Reference                   | Recommendation                                                                                                                                  | Expected Impact                                                                                                         |
| --- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 1   | #1 — Severity inflation             | **Insurers**: Apply a ~50 % discount factor when using publicly reported `Severity = 4` as a risk input; switch to a True Severe metric instead | More accurate risk-tier pricing; estimated ~$10-15 M annual margin recovery on mis-priced urban policies (illustrative) |
| 2   | #5 — Signal Drop                    | **State DOTs**: Prioritize traffic-signal installations at the top-N junction hotspots from Dashboard 3                                         | Per-accident severity reduction of ~0.4 points at retrofit sites; measurable ROI per signal installed                   |
| 3   | #2 + #6 — Night & junction risk     | **Logistics fleets**: Re-rank corridors by True Severe Index; shift long-haul dispatch away from PA + winter night windows where feasible       | Lower expected claim frequency and severity per million route-miles; reduced delivery delay variance                    |
| 4   | #4 — Clear-weather severe events    | **Infrastructure planners**: Avoid over-investing in fog/visibility-only interventions; rebalance toward junction redesigns and signal coverage | Better $/severity-point reduction than visibility-targeted spend                                                        |
| 5   | #3 — Geographic mismatch (PA vs CA) | **Federal grant programs**: Reweight per-state safety allocations using True Severe counts rather than total accident volume                    | Aligns federal dollars with actual severity outcomes, not raw accident reporting frequency                              |


---

## Repository Structure

```text
SectionName_TeamID_ProjectName/
├── README.md                                # this file
│
├── data/
│   ├── raw/                                 # original Kaggle dataset (never edited)
│   └── processed/                           # cleaned + Tableau-ready outputs
│       ├── extracted_sample.csv
│       ├── cleaned_dataset.csv
│       ├── tableau_ready_dataset.csv
│       └── tableau_state_summary.csv
│
├── notebooks/
│   ├── 01_extraction.ipynb                  # balanced sampling from 7.7 M rows
│   ├── 02_cleaning.ipynb                    # context-aware imputation + ETL
│   ├── 03_eda.ipynb                         # 6-section EDA incl. congestion bias check
│   ├── 04_statistical_analysis.ipynb        # chi-square, Kruskal-Wallis, location bias
│   └── 05_final_load_prep.ipynb             # Tableau feature engineering
│
├── scripts/
│   └── etl_pipeline.py                      # reusable ETL module (Python)
│
├── tableau/
│   ├── Road Accident Data of USA.twbx       # workbook (3 dashboards, 30+ sheets)
│   ├── dashboard_links.md                   # Tableau Public URLs
│   └── screenshots/                         # exported dashboard images
│
├── reports/
│   ├── README.md
│   ├── project_report.pdf                   # 10–15 page final report
│   ├── presentation.pdf                     # 10–12 slide final deck
│   ├── project_report_template.md           # working draft (markdown)
│   ├── presentation_outline.md              # working draft (markdown)
│   └── eda_plots/                           # 8 EDA visualizations
│
├── docs/
│   └── data_dictionary.md                   # full column definitions + cleaning notes
│
├── DVA-oriented-Resume/                     # one resume per team member
└── DVA-focused-Portfolio/                   # one portfolio per team member
```

---

## Analytical Pipeline

The project follows the official 7-step Capstone 2 workflow.

1. **Define** — Sector (Transportation/Public Safety) selected; problem statement framed around severity bias; mentor approval secured at Gate 1.
2. **Extract** — Kaggle US Accidents (7.7 M rows) committed to `data/raw/`. Balanced sample of ~100 K rows extracted in `notebooks/01_extraction.ipynb`. Data dictionary drafted in `docs/data_dictionary.md`.
3. **Clean and Transform** — Python ETL pipeline in `notebooks/02_cleaning.ipynb` and `scripts/etl_pipeline.py`. Drops 100 %-null columns, applies context-aware imputation (median by State + Month + Hour), removes outliers.
4. **Analyze** — EDA in `notebooks/03_eda.ipynb` (6 sections including a dedicated congestion-vs-severity investigation). Statistical tests in `notebooks/04_statistical_analysis.ipynb` (chi-square for congestion bias, Kruskal-Wallis for duration differences, location-bias analysis).
5. **Visualize** — Three interactive dashboards built in Tableau Public (`tableau/Road Accident Data of USA.twbx`).
6. **Recommend** — Five business recommendations delivered (above), each tied to an insight + expected impact.
7. **Report** — Final PDF report (`reports/project_report.pdf`) and presentation deck (`reports/presentation.pdf`) shipped.

---

## Tech Stack


| Tool                       | Status    | Purpose                                                                |
| -------------------------- | --------- | ---------------------------------------------------------------------- |
| Python + Jupyter Notebooks | Mandatory | ETL, cleaning, statistical analysis, KPI computation                   |
| Google Colab               | Supported | Cloud notebook environment (notebooks committed to GitHub in `.ipynb`) |
| Tableau Public             | Mandatory | Dashboard design + publishing                                          |
| GitHub                     | Mandatory | Version control + collaboration audit                                  |
| SQL                        | Optional  | Not used in this project                                               |


**Python libraries used**: `pandas`, `numpy`, `scipy`, `statsmodels`, `matplotlib`, `seaborn`. Full requirements in `[requirements.txt](requirements.txt)`.

---

---

## Submission Checklist

### GitHub Repository

- Public repository named `SectionName_TeamID_ProjectName`
- All five notebooks committed in `.ipynb`
- `data/raw/` contains the original Kaggle dataset
- `data/processed/` contains the cleaned + Tableau-ready outputs
- `tableau/screenshots/` contains updated dashboard screenshots
- `tableau/dashboard_links.md` contains the new Tableau Public URLs
- `docs/data_dictionary.md` complete with column-by-column notes
- `README.md` explains the project, dataset, KPIs, insights, and team
- All members have visible GitHub commits + PRs

### Tableau Dashboard

- Three dashboards published on Tableau Public (publicly accessible)
- At least one interactive filter on each dashboard (Severity, State, Year, Season, Time_of_Day, Weather_Category)
- Dashboards directly address the bias-correction problem

### Project Report

- Final report exported as `reports/project_report.pdf` (10 – 15 pages)
- Cover page, executive summary, sector context, problem statement
- Data description, cleaning methodology, KPI framework
- EDA write-up + statistical analysis results
- Dashboard screenshots + walkthrough
- 8 – 12 key insights in decision language
- 3 – 5 actionable recommendations with impact estimates
- Contribution matrix matches GitHub history

### Presentation Deck

- Final deck exported as `reports/presentation.pdf` (10 – 12 slides)
- Title → context → data → KPIs → insights → recommendations → impact → limitations → next steps

### Individual Assets

- DVA-oriented resume per team member (in `DVA-oriented-Resume/`)
- DVA-focused portfolio per team member (in `DVA-focused-Portfolio/`)

---

## Contribution Matrix

This table must match evidence in GitHub Insights, PR history, and committed files.


| Team Member   | Dataset & Sourcing | ETL & Cleaning  | EDA & Analysis  | Statistical Analysis | Tableau Dashboard | Report Writing  | PPT & Viva      |
| ------------- | ------------------ | --------------- | --------------- | -------------------- | ----------------- | --------------- | --------------- |
| Shivam Mittal | Owner              |                 | support         | support              | support           | Owner           | Owner           |
| Satyam        | Owner / support    | Owner / support | Owner / support | Owner / support      | Owner / support   | Owner / support | Owner / support |
| *Member 3*    | Owner / support    | Owner / support | Owner / support | Owner / support      | Owner / support   | Owner / support | Owner / support |
| *Member 4*    | Owner / support    | Owner / support | Owner / support | Owner / support      | Owner / support   | Owner / support | Owner / support |
| *Member 5*    | Owner / support    | Owner / support | Owner / support | Owner / support      | Owner / support   | Owner / support | Owner / support |
| *Member 6*    | Owner / support    | Owner / support | Owner / support | Owner / support      | Owner / support   | Owner / support | Owner / support |


> Replace each cell with **Owner** or **Support** based on actual contribution. Replace *italicized* placeholders with team member names. The matrix must align with GitHub Insights / PR history.

**Declaration:** We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts.

---

## Academic Integrity

All analysis, code, and recommendations in this repository are the original work of the team listed above. No analysis was copied from public Kaggle notebooks. Free-riding is tracked via GitHub Insights and pull-request history; any mismatch between the contribution matrix and actual commit activity may result in individual grade adjustments.

---

## Reproducibility

To reproduce the analysis locally:

```bash
git clone <repo-url>
cd <repo-name>

python -m venv .venv
source .venv/bin/activate     # on Windows: .venv\Scripts\activate
pip install -r requirements.txt

jupyter notebook
```

Then run the notebooks in order: `01_extraction → 02_cleaning → 03_eda → 04_statistical_analysis → 05_final_load_prep`. Open `tableau/Road Accident Data of USA.twbx` in Tableau Public Desktop to inspect the dashboards.

---

