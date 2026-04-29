"""
DeliverIQ — Severity Reality Check
NST DVA Capstone 2 Presentation Deck (Section-A · Team G12)
11 slides, Midnight Executive palette.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pathlib import Path

# ─── Palette ───────────────────────────────────────────────────────
NAVY     = RGBColor(0x1E, 0x27, 0x61)
ICE      = RGBColor(0xCA, 0xDC, 0xFC)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
CORAL    = RGBColor(0xF9, 0x61, 0x67)
GRAY     = RGBColor(0x64, 0x74, 0x8B)
DARKGRAY = RGBColor(0x1E, 0x29, 0x3B)
SOFT     = RGBColor(0xF1, 0xF5, 0xF9)

# ─── Setup ─────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]

PROJECT_ROOT = Path("/sessions/adoring-charming-hawking/mnt/Dva Capstone 2 ")

# ─── Helpers ───────────────────────────────────────────────────────

def add_text(slide, x, y, w, h, text, *, size=14, bold=False, color=DARKGRAY,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri",
             italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return tb

def add_bullets(slide, x, y, w, h, items, *, size=14, color=DARKGRAY,
                bullet_color=NAVY, line_spacing=1.25):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        r1 = p.add_run()
        r1.text = "■  "
        r1.font.name = "Calibri"
        r1.font.size = Pt(size)
        r1.font.bold = True
        r1.font.color.rgb = bullet_color
        r2 = p.add_run()
        r2.text = item
        r2.font.name = "Calibri"
        r2.font.size = Pt(size)
        r2.font.color.rgb = color
    return tb

def add_rect(slide, x, y, w, h, fill, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(0.5)
    s.shadow.inherit = False
    return s

def add_card(slide, x, y, w, h, fill=WHITE, border=ICE):
    return add_rect(slide, x, y, w, h, fill, border)

def add_footer(slide, page_num, total=11):
    add_rect(slide, 0, 7.2, 13.333, 0.3, NAVY)
    add_text(slide, 0.5, 7.235, 8, 0.25,
             "DeliverIQ · Severity Reality Check  ·  NST DVA Capstone 2  ·  Section-A · G12",
             size=9, color=ICE, font="Calibri")
    add_text(slide, 12.0, 7.235, 1.0, 0.25,
             f"{page_num} / {total}", size=9, color=ICE, font="Calibri",
             align=PP_ALIGN.RIGHT)

def kpi_card(slide, x, y, w, h, label, value, sublabel="", value_color=CORAL):
    add_card(slide, x, y, w, h, fill=WHITE, border=ICE)
    add_text(slide, x + 0.15, y + 0.15, w - 0.3, 0.35, label,
             size=11, bold=True, color=GRAY)
    add_text(slide, x + 0.15, y + 0.55, w - 0.3, h - 1.1, value,
             size=28, bold=True, color=value_color, font="Calibri")
    if sublabel:
        add_text(slide, x + 0.15, y + h - 0.45, w - 0.3, 0.35, sublabel,
                 size=9, color=GRAY, italic=True)

# ─── Slide 1 — Title ───────────────────────────────────────────────
s1 = prs.slides.add_slide(BLANK)
add_rect(s1, 0, 0, 13.333, 7.5, NAVY)
add_rect(s1, 0, 0, 0.5, 7.5, CORAL)

add_text(s1, 1.0, 1.4, 11.5, 0.5,
         "NST DVA  ·  CAPSTONE 2  ·  SECTION-A  ·  TEAM G12",
         size=12, bold=True, color=ICE, font="Calibri")

add_text(s1, 1.0, 1.95, 11.5, 1.0,
         "DeliverIQ",
         size=64, bold=True, color=CORAL, font="Calibri")
add_text(s1, 1.0, 2.95, 11.5, 0.7,
         "Severity Reality Check",
         size=42, bold=True, color=WHITE, font="Calibri")

add_text(s1, 1.0, 3.95, 11.5, 0.6,
         "Disentangling true accident severity from congestion,",
         size=18, color=ICE, font="Calibri")
add_text(s1, 1.0, 4.30, 11.5, 0.6,
         "time-of-day, and location bias",
         size=18, color=ICE, font="Calibri")

add_text(s1, 1.0, 5.20, 6.0, 0.4,
         "ANALYZING 95K US ROAD ACCIDENTS  ·  2016–2023",
         size=11, bold=True, color=CORAL, font="Calibri")

add_rect(s1, 1.0, 5.85, 11.3, 0.025, ICE)
add_text(s1, 1.0, 5.95, 5.8, 0.4,
         "Newton School of Technology",
         size=12, bold=True, color=WHITE, font="Calibri")
add_text(s1, 1.0, 6.30, 5.8, 0.3,
         "Team: Shivam · Satyam · Keshav · Mohit · Prachee · Rishita",
         size=10, color=ICE, font="Calibri")
add_text(s1, 1.0, 6.60, 5.8, 0.3,
         "Mentor: <fill>   ·   Submission: April 29, 2026",
         size=9, color=ICE, italic=True, font="Calibri")

add_text(s1, 7.5, 5.95, 4.8, 0.3,
         "GitHub:  github.com/shiavm006/Section-A_G12_DeliverIQ",
         size=10, color=ICE, font="Calibri")
add_text(s1, 7.5, 6.30, 4.8, 0.3,
         "Tableau:  public.tableau.com/.../RoadAccidentDataofUSA",
         size=10, color=ICE, font="Calibri")
add_text(s1, 7.5, 6.60, 4.8, 0.3,
         "Project Lead: Shivam Mittal",
         size=9, color=ICE, italic=True, font="Calibri")

# ─── Slide 2 — Context & Problem ───────────────────────────────────
s2 = prs.slides.add_slide(BLANK)
add_rect(s2, 0, 0, 13.333, 7.5, WHITE)
add_text(s2, 0.6, 0.4, 12, 0.5, "02  ·  CONTEXT", size=11, bold=True, color=GRAY)
add_text(s2, 0.6, 0.8, 12, 0.9, "Public severity data is widely used —", size=32, bold=True, color=NAVY)
add_text(s2, 0.6, 1.5, 12, 0.9, "but it measures the wrong thing.", size=32, bold=True, color=CORAL)

add_text(s2, 0.6, 2.7, 6.0, 0.4, "WHAT'S WRONG", size=11, bold=True, color=GRAY)
add_bullets(s2, 0.6, 3.1, 6.0, 3.5, [
    "The most common severity field measures traffic-flow impact (short delay → long delay), not crash physical severity.",
    "A fender-bender at rush hour can register Severity 4. A fatal crash on a quiet road can register Severity 1.",
    "Insurers, DOTs, and logistics planners use this field directly in pricing models, capital plans, and routing — silently absorbing the bias.",
], size=13, line_spacing=1.35)

add_card(s2, 7.0, 2.6, 5.8, 4.0, fill=NAVY, border=NAVY)
add_text(s2, 7.25, 2.85, 5.4, 0.4,
         "OUR CORE BUSINESS QUESTION", size=11, bold=True, color=ICE)
add_text(s2, 7.25, 3.3, 5.4, 3.0,
         'How much of what is labeled "severe" in public US accident data is genuinely severe — and how should insurers, DOTs, and logistics planners adjust their decisions to use a bias-corrected signal?',
         size=14, color=WHITE)
add_text(s2, 7.25, 6.05, 5.4, 0.4,
         "→  Decision: down-weight raw severity in pricing,",
         size=10, color=CORAL, italic=True)
add_text(s2, 7.25, 6.30, 5.4, 0.4,
         "    capital allocation, and corridor routing.",
         size=10, color=CORAL, italic=True)

add_footer(s2, 2)

# ─── Slide 3 — Data Engineering ────────────────────────────────────
s3 = prs.slides.add_slide(BLANK)
add_rect(s3, 0, 0, 13.333, 7.5, WHITE)
add_text(s3, 0.6, 0.4, 12, 0.5, "03  ·  DATA ENGINEERING", size=11, bold=True, color=GRAY)
add_text(s3, 0.6, 0.8, 12, 0.9, "From 7.7M raw rows to a 95K balanced sample", size=28, bold=True, color=NAVY)

kpi_card(s3, 0.6, 2.2, 2.95, 1.4, "ORIGINAL ROWS", "7.7M", "raw Kaggle dataset", value_color=NAVY)
kpi_card(s3, 3.7, 2.2, 2.95, 1.4, "WORKING SAMPLE", "95,607", "balanced across Sev 1–4", value_color=CORAL)
kpi_card(s3, 6.8, 2.2, 2.95, 1.4, "COLUMNS", "49", "incl. 13 derived features", value_color=NAVY)
kpi_card(s3, 9.9, 2.2, 2.95, 1.4, "STATES COVERED", "49", "5,558 cities", value_color=NAVY)

add_text(s3, 0.6, 3.95, 6.0, 0.4, "CLEANING PIPELINE  (notebooks/02_cleaning.ipynb)",
         size=11, bold=True, color=GRAY)
add_bullets(s3, 0.6, 4.35, 6.0, 2.6, [
    "Drop high-null + zero-variance columns (End_Lat/Lng, Country, Turning_Loop)",
    "Validate geographic bounds (lat 24–50, lng −125 to −66)",
    "Cap Distance_mi outliers at 99th percentile",
    "Context-aware imputation (median by State + Month + Hour)",
    "Cast booleans to int for Tableau",
], size=12, line_spacing=1.25)

add_card(s3, 7.0, 3.95, 5.8, 3.0, fill=SOFT, border=ICE)
add_text(s3, 7.25, 4.10, 5.4, 0.4, "KEY DERIVED FEATURES", size=11, bold=True, color=NAVY)
add_bullets(s3, 7.25, 4.55, 5.4, 2.4, [
    "Severity_Label · Weather_Category · State_Region",
    "Time_of_Day · Season · Is_Rush_Hour · Is_Weekend",
    "Duration_min · Road_Feature_Count",
    "Is True Severe = Sev=4 AND Distance ≥ 0.5 mi",
], size=11, line_spacing=1.3)

add_footer(s3, 3)

# ─── Slide 4 — KPI Framework ───────────────────────────────────────
s4 = prs.slides.add_slide(BLANK)
add_rect(s4, 0, 0, 13.333, 7.5, WHITE)
add_text(s4, 0.6, 0.4, 12, 0.5, "04  ·  KPI FRAMEWORK", size=11, bold=True, color=GRAY)
add_text(s4, 0.6, 0.8, 12, 0.9, "15 decision-relevant KPIs across 3 dashboards", size=28, bold=True, color=NAVY)

def kpi_col(x, w, headline, color, sub, items):
    add_card(s4, x, 2.0, w, 4.85, fill=WHITE, border=ICE)
    add_rect(s4, x, 2.0, w, 0.5, color)
    add_text(s4, x + 0.2, 2.05, w - 0.4, 0.4, headline, size=14, bold=True, color=WHITE)
    add_text(s4, x + 0.2, 2.6, w - 0.4, 0.3, sub, size=10, color=GRAY, italic=True)
    add_bullets(s4, x + 0.2, 2.95, w - 0.4, 3.8, items,
                size=11, line_spacing=1.25, bullet_color=color)

kpi_col(0.6, 4.0,
        "D1 — Severity Reality Check",
        NAVY,
        "the hook",
        ["Total Incidents (95,607)", "Critical Accidents (18,023)",
         "True Severe Accidents (9,155)",
         "Avg Duration Severe (1,829 m)",
         "Severe Distance (24,415 mi)"])

kpi_col(4.75, 4.0,
        "D2 — When Risk Strikes",
        CORAL,
        "the diagnosis",
        ["Worst Season (Winter)",
         "Peak Risk Hour (12 AM)",
         "Weekend vs Weekday Δ (+0.34)",
         "Night Sev 3+ Share (8.42%)",
         "Riskiest Weather (Drifting Snow)"])

kpi_col(8.9, 4.0,
        "D3 — Where & Why",
        NAVY,
        "the cause",
        ["Top State by Volume (CA · 8,780)",
         "Top State by Severity (WV)",
         "Junction Severity (+28.8%)",
         "Signal Drop (−62.1%)",
         "Cities Tracked (5,558)"])

add_footer(s4, 4)

# ─── Slide 5 — Key EDA Insights ────────────────────────────────────
s5 = prs.slides.add_slide(BLANK)
add_rect(s5, 0, 0, 13.333, 7.5, WHITE)
add_text(s5, 0.6, 0.4, 12, 0.5, "05  ·  KEY EDA INSIGHTS", size=11, bold=True, color=GRAY)
add_text(s5, 0.6, 0.8, 12, 0.9, "Five observations that reframe the data", size=28, bold=True, color=NAVY)

plot_path = PROJECT_ROOT / "reports/eda_plots/severity_rush_hour.png"
if plot_path.exists():
    s5.shapes.add_picture(str(plot_path), Inches(7.6), Inches(2.1),
                          width=Inches(5.3), height=Inches(4.2))
    add_text(s5, 7.6, 6.3, 5.3, 0.3,
             "Severity proportions: Rush Hour vs Non-Rush — barely shift",
             size=9, color=GRAY, italic=True)

add_bullets(s5, 0.6, 2.1, 6.7, 4.6, [
    "Severity-2 dominance dropped after balanced sampling — every tier now has enough N for cross-tier comparison.",
    "Volume peaks at 5 PM rush hour — but per-accident severity is barely different between rush and non-rush.",
    "Weekday volume rises Tue–Wed, falls weekend. Severity does not follow the same curve.",
    "Top-volume state: CA (8,780). Top-severity state: WV — geography differs once bias is corrected.",
    "Most accidents happen in fair weather. Severe accidents are no exception.",
], size=13, line_spacing=1.4)

add_footer(s5, 5)

# ─── Slide 6 — Advanced Analysis ───────────────────────────────────
s6 = prs.slides.add_slide(BLANK)
add_rect(s6, 0, 0, 13.333, 7.5, WHITE)
add_text(s6, 0.6, 0.4, 12, 0.5, "06  ·  ADVANCED ANALYSIS", size=11, bold=True, color=GRAY)
add_text(s6, 0.6, 0.8, 12, 0.9, "Statistical tests aligned with the bias hypothesis", size=28, bold=True, color=NAVY)

def test_card(x, y, label, method, finding):
    add_card(s6, x, y, 6.0, 1.95, fill=WHITE, border=ICE)
    add_rect(s6, x, y, 0.12, 1.95, NAVY)
    add_text(s6, x + 0.3, y + 0.15, 5.6, 0.4, label, size=12, bold=True, color=NAVY)
    add_text(s6, x + 0.3, y + 0.6, 5.6, 0.4, "Method:  " + method, size=10, color=GRAY, italic=True)
    add_text(s6, x + 0.3, y + 1.0, 5.6, 0.9, finding, size=11, color=DARKGRAY)

test_card(0.6, 2.1,
          "Test 1 — Congestion Bias",
          "Chi-square (Rush Hour × Severity)",
          "Significant by N, but proportions barely shift. Rush-hour volume is NOT the dominant severity driver.")
test_card(6.75, 2.1,
          "Test 2 — Duration × Severity",
          "Kruskal-Wallis H (non-parametric)",
          "Median duration rises monotonically: Sev 1 ≈ 30 min → Sev 4 ≈ 210 min. Validates True-Severe definition.")
test_card(0.6, 4.2,
          "Test 3 — Weather × Severity",
          "Chi-square (top 5 weather × Sev)",
          "Statistically significant but small effect size. Weather is NOT the primary driver of severity.")
test_card(6.75, 4.2,
          "Test 4 — Location Bias",
          "State × Severity cross-tab",
          "WV, PA, MD, NC over-represented in Sev 3+4. Reporting bias is real and must be corrected.")

add_card(s6, 0.6, 6.4, 12.15, 0.65, fill=NAVY, border=NAVY)
add_text(s6, 0.85, 6.50, 11.7, 0.5,
         "Net finding:  Severity in this dataset is partly real, partly noise. The True-Severe filter (Sev 4 + Dist ≥ 0.5 mi) cleanly separates them.",
         size=12, bold=True, color=WHITE)

add_footer(s6, 6)

# ─── Slide 7 — Tableau Walkthrough (with screenshots) ──────────────
s7 = prs.slides.add_slide(BLANK)
add_rect(s7, 0, 0, 13.333, 7.5, WHITE)
add_text(s7, 0.6, 0.4, 12, 0.5, "07  ·  TABLEAU DASHBOARDS", size=11, bold=True, color=GRAY)
add_text(s7, 0.6, 0.8, 12, 0.9, "Three dashboards: What → When → Where & Why", size=28, bold=True, color=NAVY)

# 3 dashboard thumbnails with annotations
dashboards = [
    ("D1", "Severity Reality Check", "The hook", NAVY,
     "True Severe = 9,155 of 18,023  (~51%)",
     "Half of \"severe\" is congestion noise.",
     "dashboard_1.png"),
    ("D2", "When Risk Strikes", "The diagnosis", CORAL,
     "Peak Risk Hour: 12 AM   ·   Worst Season: Winter",
     "Risk peaks at midnight, not rush hour.",
     "dashboard_2.png"),
    ("D3", "Where & Why", "The cause", NAVY,
     "Junction +28.8%   ·   Signal −62.1%   ·   Top: WV",
     "Infrastructure has measurable lifts.",
     "dashboard_3.png"),
]

col_w = 4.0
for i, (label, name, sub, color, kpi_line, hook, img) in enumerate(dashboards):
    x = 0.6 + i * (col_w + 0.15)
    # header bar
    add_rect(s7, x, 1.95, col_w, 0.4, color)
    add_text(s7, x + 0.15, 2.0, 0.7, 0.3, label, size=11, bold=True, color=WHITE)
    add_text(s7, x + 0.85, 2.0, col_w - 1.0, 0.3, name, size=11, bold=True, color=WHITE)
    # image
    img_path = PROJECT_ROOT / f"tableau/screenshots/{img}"
    if img_path.exists():
        s7.shapes.add_picture(str(img_path), Inches(x), Inches(2.4),
                              width=Inches(col_w), height=Inches(2.0))
    # KPI line
    add_text(s7, x, 4.55, col_w, 0.3, kpi_line, size=10, bold=True, color=color)
    # hook
    add_text(s7, x, 4.85, col_w, 0.4, hook, size=11, color=DARKGRAY, italic=True)
    # sub
    add_text(s7, x, 5.3, col_w, 0.3, sub.upper(), size=9, bold=True, color=GRAY)

# Filters footer
add_text(s7, 0.6, 6.85, 12, 0.3,
         "Interactive filters: Rush Hour · Severity · Visibility Bucket · Time of Day  (across 30+ worksheets)",
         size=10, color=GRAY, italic=True)

add_footer(s7, 7)

# ─── Slide 8 — Recommendations ─────────────────────────────────────
s8 = prs.slides.add_slide(BLANK)
add_rect(s8, 0, 0, 13.333, 7.5, WHITE)
add_text(s8, 0.6, 0.4, 12, 0.5, "08  ·  RECOMMENDATIONS", size=11, bold=True, color=GRAY)
add_text(s8, 0.6, 0.8, 12, 0.9, "Five actions, each tied to an insight", size=28, bold=True, color=NAVY)

add_rect(s8, 0.6, 2.0, 12.1, 0.45, NAVY)
add_text(s8, 0.75, 2.07, 1.0, 0.3, "#",  size=10, bold=True, color=WHITE)
add_text(s8, 1.85, 2.07, 2.6, 0.3, "STAKEHOLDER", size=10, bold=True, color=WHITE)
add_text(s8, 4.55, 2.07, 5.5, 0.3, "RECOMMENDATION", size=10, bold=True, color=WHITE)
add_text(s8, 10.1, 2.07, 2.6, 0.3, "EXPECTED IMPACT", size=10, bold=True, color=WHITE)

recs = [
    ("1", "Insurer", "Discount publicly-reported Severity 4 by ~50%; switch to True-Severe-based pricing.",
     "Mis-priced urban-policy margin recovered."),
    ("2", "State DOT", "Prioritize signal installations at top junction hotspots (D3).",
     "~62% severity reduction at signal-equipped sites; per-installation ROI."),
    ("3", "Logistics fleet", "Re-rank corridors by True-Severe Index; shift dispatch off PA/WV winter night windows.",
     "Lower expected claim frequency / severity per million miles."),
    ("4", "Federal grants", "Reweight per-state safety allocation using True-Severe counts, not raw volume.",
     "Capital tracks real severity, not reporting frequency."),
    ("5", "Ride-share / Fleet", "Adjust state-level driver pay & rest-cycle by True-Severe density.",
     "Driver-safety alignment with actual risk; lower carrier liability."),
]
y = 2.55
row_h = 0.85
for i, (n, who, rec, imp) in enumerate(recs):
    bg = SOFT if i % 2 == 0 else WHITE
    add_rect(s8, 0.6, y, 12.1, row_h, bg)
    add_text(s8, 0.75, y + 0.05, 1.0, row_h - 0.1, n,
             size=20, bold=True, color=CORAL, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s8, 1.85, y + 0.10, 2.6, row_h - 0.2, who,
             size=11, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s8, 4.55, y + 0.10, 5.5, row_h - 0.2, rec,
             size=10, color=DARKGRAY, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s8, 10.1, y + 0.10, 2.6, row_h - 0.2, imp,
             size=10, color=DARKGRAY, italic=True, anchor=MSO_ANCHOR.MIDDLE)
    y += row_h

add_footer(s8, 8)

# ─── Slide 9 — Impact & Value ──────────────────────────────────────
s9 = prs.slides.add_slide(BLANK)
add_rect(s9, 0, 0, 13.333, 7.5, WHITE)
add_text(s9, 0.6, 0.4, 12, 0.5, "09  ·  IMPACT & VALUE", size=11, bold=True, color=GRAY)
add_text(s9, 0.6, 0.8, 12, 0.9, "Why this work pays off — directional estimates", size=28, bold=True, color=NAVY)

add_card(s9, 0.6, 2.0, 4.0, 2.5, fill=NAVY, border=NAVY)
add_text(s9, 0.85, 2.20, 3.5, 0.3, "INSURER  ·  REC #1", size=10, bold=True, color=ICE)
add_text(s9, 0.85, 2.6,  3.5, 1.0, "~50%", size=64, bold=True, color=CORAL)
add_text(s9, 0.85, 3.55, 3.5, 0.9, "of Severity-4 in pricing models is over-weighted; bias-correction unlocks ~$100M risk-adj premium reallocation per $10B book.",
         size=10, color=ICE)

add_card(s9, 4.75, 2.0, 4.0, 2.5, fill=WHITE, border=ICE)
add_text(s9, 5.00, 2.20, 3.5, 0.3, "STATE DOT  ·  REC #2", size=10, bold=True, color=GRAY)
add_text(s9, 5.00, 2.6,  3.5, 1.0, "−62%", size=54, bold=True, color=NAVY)
add_text(s9, 5.00, 3.55, 3.5, 0.9, "severity drop at locations with traffic signals vs. without — quantifies per-installation infrastructure ROI.",
         size=10, color=DARKGRAY)

add_card(s9, 8.90, 2.0, 4.0, 2.5, fill=WHITE, border=ICE)
add_text(s9, 9.15, 2.20, 3.5, 0.3, "FLEETS  ·  REC #3", size=10, bold=True, color=GRAY)
add_text(s9, 9.15, 2.6,  3.5, 1.0, "5–10%", size=54, bold=True, color=NAVY)
add_text(s9, 9.15, 3.55, 3.5, 0.9, "expected reduction in severe-corridor exposure when routing on True-Severe Index instead of raw volume.",
         size=10, color=DARKGRAY)

add_text(s9, 0.6, 4.85, 12.1, 0.4, "WHY ACT NOW", size=11, bold=True, color=GRAY)
add_bullets(s9, 0.6, 5.25, 12.1, 1.7, [
    "Real-time accident APIs increasingly feed pricing engines — bias compounds quickly.",
    "Post-COVID vehicle-miles-traveled have rebounded; more decisions flow through the same biased input.",
    "Signal Drop is one of the most cost-effective infrastructure levers — and the data quantifies it.",
], size=12, line_spacing=1.3)

add_footer(s9, 9)

# ─── Slide 10 — Limitations & Next Steps ───────────────────────────
s10 = prs.slides.add_slide(BLANK)
add_rect(s10, 0, 0, 13.333, 7.5, WHITE)
add_text(s10, 0.6, 0.4, 12, 0.5, "10  ·  LIMITATIONS & NEXT STEPS", size=11, bold=True, color=GRAY)
add_text(s10, 0.6, 0.8, 12, 0.9, "Honesty about what this analysis can and cannot say", size=28, bold=True, color=NAVY)

add_text(s10, 0.6, 2.0, 6.0, 0.4, "LIMITATIONS", size=12, bold=True, color=CORAL)
add_bullets(s10, 0.6, 2.45, 6.0, 4.4, [
    "Severity is a flow-impact label, not a crash-injury label — True Severe is a proxy.",
    "0.5-mi threshold is defensible but not absolute; sensitivity tested at 0.25 and 1.0 mi.",
    "All findings are correlational, not causal.",
    "API coverage varies by state; 2020+ volume spike is partly artefact.",
    "No injury / fatality outcomes available in this dataset.",
    "Balanced sample changes base rates — most KPIs use ratios to control.",
], size=11, line_spacing=1.35)

add_text(s10, 7.0, 2.0, 6.0, 0.4, "NEXT STEPS", size=12, bold=True, color=NAVY)
add_bullets(s10, 7.0, 2.45, 6.0, 4.4, [
    "Join FARS / state crash records to validate True-Severe against real injury data.",
    "Add quasi-experimental causal layer for Signal Drop estimate.",
    "Wrap corrected severity index as a real-time API for fleets and insurers.",
    "Train a gradient-boosted classifier on incoming reports (predict True Severe).",
    "Geospatial drill-down map (Mapbox / Leaflet) for DOT use.",
    "Attach cost-benefit modelling using FHWA retrofit cost data.",
], size=11, line_spacing=1.35, bullet_color=NAVY)

add_footer(s10, 10)

# ─── Slide 11 — Team & Artefacts ───────────────────────────────────
s11 = prs.slides.add_slide(BLANK)
add_rect(s11, 0, 0, 13.333, 7.5, WHITE)
add_text(s11, 0.6, 0.4, 12, 0.5, "11  ·  TEAM & ARTEFACTS", size=11, bold=True, color=GRAY)
add_text(s11, 0.6, 0.8, 12, 0.9, "Team G12 · Section A · DeliverIQ", size=28, bold=True, color=NAVY)

add_text(s11, 0.6, 1.95, 12, 0.4, "TEAM ROLES", size=11, bold=True, color=GRAY)
roles = [
    ("Project Lead",            "Shivam Mittal"),
    ("Data Lead",               "Satyam Kumar"),
    ("ETL Lead",                "Keshav"),
    ("Analysis Lead",           "Mohit Singh"),
    ("Visualization Lead",      "Prachee Dhar"),
    ("Strategy + PPT Lead",     "Rishita Boisnobi"),
]
for i, (role, name) in enumerate(roles):
    col = i % 3
    row = i // 3
    x = 0.6 + col * 4.15
    y = 2.40 + row * 1.15
    add_card(s11, x, y, 4.0, 1.0, fill=SOFT, border=ICE)
    add_text(s11, x + 0.15, y + 0.10, 3.7, 0.35, role,
             size=10, bold=True, color=GRAY)
    add_text(s11, x + 0.15, y + 0.45, 3.7, 0.5, name,
             size=15, bold=True, color=NAVY)

add_text(s11, 0.6, 4.85, 12, 0.4, "ARTEFACTS  ·  GitHub  +  Tableau  +  Reports", size=11, bold=True, color=GRAY)
add_card(s11, 0.6, 5.30, 12.1, 1.7, fill=NAVY, border=NAVY)
add_text(s11, 0.85, 5.45, 11.5, 0.4, "▸  GitHub Repo:", size=11, bold=True, color=ICE)
add_text(s11, 2.85, 5.45, 9.5, 0.4, "github.com/shiavm006/Section-A_G12_DeliverIQ",
         size=11, color=WHITE)
add_text(s11, 0.85, 5.78, 11.5, 0.4, "▸  Tableau Public:", size=11, bold=True, color=ICE)
add_text(s11, 2.85, 5.78, 9.5, 0.4, "public.tableau.com/views/RoadAccidentDataofUSA_17773613139680/Dashboard1",
         size=10, color=WHITE)
add_text(s11, 0.85, 6.13, 11.5, 0.4, "▸  Project Report:", size=11, bold=True, color=ICE)
add_text(s11, 2.85, 6.13, 9.5, 0.4, "reports/project_report.pdf  (18 sections, ~22 pages)", size=11, color=WHITE)
add_text(s11, 0.85, 6.48, 11.5, 0.4, "▸  This Deck:", size=11, bold=True, color=ICE)
add_text(s11, 2.85, 6.48, 9.5, 0.4, "reports/presentation.pdf  (11 slides)", size=11, color=WHITE)
add_text(s11, 0.85, 6.83, 11.5, 0.3, "Submitted Apr 29, 2026  ·  Newton School of Technology  ·  DVA Capstone 2",
         size=9, italic=True, color=ICE)

# ─── Save ──────────────────────────────────────────────────────────
out = Path("/sessions/adoring-charming-hawking/mnt/outputs/deck_build/presentation.pptx")
prs.save(out)
print(f"Saved: {out}  ({out.stat().st_size:,} bytes, {len(prs.slides)} slides)")
