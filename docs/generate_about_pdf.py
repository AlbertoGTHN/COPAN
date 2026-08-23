"""
Generate docs/about.pdf — faithful reproduction of the app's About page.
Dark-theme, multi-page, matches every section visible in the UI.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "about.pdf")

# ── Dark palette (mirrors app CSS) ───────────────────────────────────────────
BG       = colors.HexColor("#0F1117")   # page background
CARD     = colors.HexColor("#1A1E2E")   # card / glass bg
CARD2    = colors.HexColor("#12151F")   # inner dark cell
WHITE    = colors.HexColor("#E2E8F0")   # body text
DIM      = colors.HexColor("#94A3B8")   # muted text
DIMMER   = colors.HexColor("#64748B")   # very muted
BLUE     = colors.HexColor("#2563EB")   # accent-blue
BLIGHT   = colors.HexColor("#3B82F6")
GREEN    = colors.HexColor("#10B981")   # accent-green
YELLOW   = colors.HexColor("#F59E0B")   # accent-yellow
RED      = colors.HexColor("#EF4444")   # accent-red
PURPLE   = colors.HexColor("#8B5CF6")   # purple
CYAN     = colors.HexColor("#06B6D4")   # cyan
PINK     = colors.HexColor("#EC4899")   # pink
ORANGE   = colors.HexColor("#F97316")   # orange

W_PAGE, H_PAGE = letter
MARGIN = 0.60 * inch
W = W_PAGE - 2 * MARGIN


# ── Dark page background ──────────────────────────────────────────────────────
def _dark_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, W_PAGE, H_PAGE, fill=1, stroke=0)
    # subtle footer
    canvas.setFillColor(DIMMER)
    canvas.setFont("Helvetica", 7)
    canvas.drawCentredString(
        W_PAGE / 2, 0.30 * inch,
        "COPAN — Classification-Oriented Phishing Analysis Network  \u00b7  Loo, Galindo, Romero et al.  "
        "\u00b7  LACCI 2026  \u00b7  Universidad Tecnol\u00f3gica de Honduras"
    )
    canvas.restoreState()


# ── Document setup ────────────────────────────────────────────────────────────
doc = BaseDocTemplate(
    OUT,
    pagesize=letter,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN,  bottomMargin=0.65 * inch,
)
frame = Frame(MARGIN, 0.65 * inch, W, H_PAGE - MARGIN - 0.65 * inch, id="main")
doc.addPageTemplates([PageTemplate(id="dark", frames=[frame], onPage=_dark_bg)])


# ── Style factory ─────────────────────────────────────────────────────────────
def S(name, **kw) -> ParagraphStyle:
    return ParagraphStyle(name, **kw)


S_H1 = S("H1", fontName="Helvetica-Bold", fontSize=18, leading=22,
          textColor=WHITE, spaceBefore=0, spaceAfter=6)
S_H2 = S("H2", fontName="Helvetica-Bold", fontSize=13, leading=17,
          textColor=WHITE, spaceBefore=14, spaceAfter=5)
S_H3 = S("H3", fontName="Helvetica-Bold", fontSize=11, leading=14,
          textColor=WHITE, spaceBefore=0, spaceAfter=4)
S_BODY = S("Body", fontName="Helvetica", fontSize=9, leading=13,
           textColor=WHITE, alignment=TA_JUSTIFY, spaceAfter=4)
S_DIM  = S("Dim",  fontName="Helvetica", fontSize=8.5, leading=12,
           textColor=DIM, alignment=TA_JUSTIFY, spaceAfter=3)
S_BULLET = S("Bullet", fontName="Helvetica", fontSize=9, leading=13,
             textColor=DIM, leftIndent=10, spaceAfter=2)
S_CENTER = S("Center", fontName="Helvetica", fontSize=8.5, leading=11,
             textColor=DIM, alignment=TA_CENTER)
S_KPI_N  = S("KpiN", fontName="Helvetica-Bold", fontSize=20, leading=24,
             alignment=TA_CENTER)
S_KPI_L  = S("KpiL", fontName="Helvetica", fontSize=8, leading=10,
             textColor=DIMMER, alignment=TA_CENTER)
S_TAG_L  = S("TagL", fontName="Helvetica-Bold", fontSize=8, leading=10,
             textColor=BLUE)
S_TAG_V  = S("TagV", fontName="Helvetica", fontSize=9, leading=12,
             textColor=WHITE)


def _kw(color, text):
    return f'<font color="{color.hexval()}">{text}</font>'


# ── Card wrapper helper ───────────────────────────────────────────────────────
def card(content_rows, col_widths, border_color=BLUE, pad=10, style_extra=None):
    """Wrap rows in a card with a dark background and coloured border."""
    ts = [
        ("BACKGROUND",    (0, 0), (-1, -1), CARD),
        ("TOPPADDING",    (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("LEFTPADDING",   (0, 0), (-1, -1), pad),
        ("RIGHTPADDING",  (0, 0), (-1, -1), pad),
        ("LINEABOVE",     (0, 0), (-1, 0),  2, border_color),
        ("ROUNDEDCORNERS", [6]),
    ]
    if style_extra:
        ts.extend(style_extra)
    t = Table(content_rows, colWidths=col_widths)
    t.setStyle(TableStyle(ts))
    return t


def inner_cell(content_rows, col_widths, style_extra=None):
    """Dark inner cell (bg-dark-900)."""
    ts = [
        ("BACKGROUND",    (0, 0), (-1, -1), CARD2),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [5]),
    ]
    if style_extra:
        ts.extend(style_extra)
    t = Table(content_rows, colWidths=col_widths)
    t.setStyle(TableStyle(ts))
    return t


def section_title(text, color=BLUE):
    return Paragraph(
        f'<font color="{color.hexval()}">&#9632;</font> &nbsp;{text}', S_H2)


story = []

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════
hdr = Table([[
    Paragraph("COPAN — Classification-Oriented Phishing Analysis Network", S_H1),
    Paragraph(
        '<font color="#94A3B8">About &amp; Research</font>',
        S("HdrR", fontName="Helvetica", fontSize=9, textColor=DIM,
          alignment=TA_RIGHT)),
]], colWidths=[W * 0.70, W * 0.30])
hdr.setStyle(TableStyle([
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING",   (0, 0), (-1, -1), 0),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))
story.append(hdr)
story.append(HRFlowable(width=W, thickness=1, color=BLUE, spaceAfter=10))

# ═══════════════════════════════════════════════════════════════════════════════
# RESEARCH BACKGROUND
# ═══════════════════════════════════════════════════════════════════════════════
story.append(KeepTogether([
    section_title("Research Background"),
    card([
        [Paragraph(
            'This system is based on the research paper '
            f'<b><font color="{WHITE.hexval()}">"Agentic AI for Phishing Detection '
            f'and Prevention"</font></b> by Loo, Galindo, Romero et al. from the '
            f'<b><font color="{BLUE.hexval()}">Universidad Tecnol\u00f3gica de '
            f'Honduras (UTH), 2025</font></b>.', S_BODY)],
        [Paragraph(
            f'The paper proposes a novel approach to phishing detection that moves '
            f'beyond traditional rule-based systems (like EBIDS) by introducing an '
            f'<b><font color="{WHITE.hexval()}">agentic AI architecture</font></b> '
            f'capable of autonomous monitoring, intelligent classification, and '
            f'continuous self-optimization. The system was validated on a dataset of '
            f'<b><font color="{WHITE.hexval()}">82,500 emails</font></b> from the '
            f'Enron, Ling, and SpamAssassin corpuses.', S_BODY)],
        # KPI row
        [inner_cell([
            [Paragraph(f'<font color="{GREEN.hexval()}">92.5%</font>', S_KPI_N),
             Paragraph(f'<font color="{BLUE.hexval()}">6.25%</font>',  S_KPI_N),
             Paragraph(f'<font color="{YELLOW.hexval()}">1.25%</font>',S_KPI_N),
             Paragraph(f'<font color="{PURPLE.hexval()}">82.5K</font>', S_KPI_N)],
            [Paragraph("Accuracy",           S_KPI_L),
             Paragraph("False Negative Rate", S_KPI_L),
             Paragraph("False Positive Rate", S_KPI_L),
             Paragraph("Emails Tested",       S_KPI_L)],
        ], [W / 4 - 14] * 4,
        style_extra=[("LINEAFTER", (0, 0), (-2, -1), 0.5, colors.HexColor("#2D3748"))])],
    ], [W - 20], border_color=BLUE),
    Spacer(1, 8),
]))

# ═══════════════════════════════════════════════════════════════════════════════
# MCO ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
def mco_phase(num, label, bg):
    s = S(f"MCO{num}", fontName="Helvetica-Bold", fontSize=7.5,
          textColor=WHITE, alignment=TA_CENTER)
    t = Table([[Paragraph(label, s)]], colWidths=[80])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), bg),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t


def mco_box(title, title_color, lines, border_c):
    rows = [[Paragraph(title, S(f"MB{title[:3]}", fontName="Helvetica-Bold",
        fontSize=8.5, textColor=title_color, alignment=TA_CENTER))]]
    for l in lines:
        rows.append([Paragraph(l, S(f"ML{l[:3]}", fontName="Helvetica",
            fontSize=7.5, textColor=DIM, alignment=TA_CENTER, leading=10))])
    t = Table(rows, colWidths=[130])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), CARD2),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("BOX",           (0, 0), (-1, -1), 1.5, border_c),
        ("ROUNDEDCORNERS", [5]),
    ]))
    return t


col3 = (W - 20) / 3

arch_diagram = Table([
    # Phase labels
    [mco_phase(1, "MONITORING",     colors.HexColor("#1D4ED8")),
     mco_phase(2, "CLASSIFICATION", colors.HexColor("#6D28D9")),
     mco_phase(3, "OPTIMIZATION",   colors.HexColor("#065F46"))],
    [Spacer(1, 6), Spacer(1, 6), Spacer(1, 6)],
    # Boxes row
    [mco_box("ENGINE A\nSemantic Understanding",
             GREEN,
             ["DistilBERT Transformer",
              "768-dim [CLS] embedding",
              "+ Rule-based scoring"],
             GREEN),
     mco_box("FEATURE FUSION\n768-d + 50 features",
             YELLOW,
             ["Random Forest (100 trees)"],
             YELLOW),
     mco_box("CLASSIFICATION\nPhishing / Legitimate",
             RED,
             ["Confidence Score",
              "Explainability Report",
              "Action: Quarantine/Alert/Pass"],
             RED)],
    [Spacer(1, 4), Spacer(1, 4), Spacer(1, 4)],
    [mco_box("ENGINE B\nStructural Analysis",
             YELLOW,
             ["URL Analysis + Typosquatting",
              "SPF/DKIM/DMARC Headers",
              "HTML Hidden Elements"],
             YELLOW),
     Spacer(1, 1),
     Spacer(1, 1)],
    [Spacer(1, 4), Spacer(1, 4), Spacer(1, 4)],
    [Paragraph(
        f'<font color="{GREEN.hexval()}">&#9660; Feedback Loop \u2014 '
        'Retraining with labeled samples &#9660;</font>',
        S("FL", fontName="Helvetica-Oblique", fontSize=8, leading=10,
          textColor=GREEN, alignment=TA_CENTER)),
     Spacer(1, 1), Spacer(1, 1)],
], colWidths=[col3] * 3)
arch_diagram.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, -1), CARD2),
    ("TOPPADDING",    (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
    ("SPAN",          (0, 2), (0, 3)),   # Engine A spans
    ("SPAN",          (0, 4), (2, 5)),   # Engine B spans full
    ("SPAN",          (0, 6), (2, 6)),   # Feedback
    ("ROUNDEDCORNERS", [6]),
]))

story.append(KeepTogether([
    section_title("MCO Architecture"),
    card([
        [Paragraph("The system follows a three-phase agentic loop: "
                   "Monitoring, Classification, and Optimization.", S_DIM)],
        [arch_diagram],
    ], [W - 20], border_color=PURPLE),
    Spacer(1, 8),
]))

# ═══════════════════════════════════════════════════════════════════════════════
# ENGINE A & B — side by side
# ═══════════════════════════════════════════════════════════════════════════════
col2 = (W - 10) / 2

engine_a_rows = [
    [Paragraph(f'<font color="{GREEN.hexval()}">Engine A: Semantic Understanding</font>',
               S_H3)],
    [Paragraph(
        "Uses a DistilBERT transformer model to extract deep linguistic features "
        "from email text. The model produces a 768-dimensional embedding from the "
        "[CLS] token that captures semantic meaning.", S_BODY)],
]
for bullet in [
    'Urgency language detection (e.g., \u201caccount suspended\u201d, \u201cact immediately\u201d)',
    "Authority impersonation scoring (CEO, PayPal, Microsoft, etc.)",
    "Pressure tactics identification (deadlines, threats)",
    "Credential harvesting phrase detection",
    "Generic greeting patterns (Dear Customer, Dear User)",
    "Grammatical anomaly analysis",
]:
    engine_a_rows.append([Paragraph(
        f'<font color="{GREEN.hexval()}">\u25ba</font> &nbsp;{bullet}', S_BULLET)])

eng_a_card = Table(engine_a_rows, colWidths=[col2 - 20])
eng_a_card.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, -1), CARD),
    ("LINEABOVE",     (0, 0), (-1, 0),  2.5, GREEN),
    ("TOPPADDING",    (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ("ROUNDEDCORNERS", [6]),
]))

engine_b_rows = [
    [Paragraph(f'<font color="{YELLOW.hexval()}">Engine B: Structural Analysis</font>',
               S_H3)],
    [Paragraph(
        "Analyzes the technical structure of emails including URLs, headers, and "
        "HTML content to identify structural indicators of phishing attacks.", S_BODY)],
]
for bullet in [
    "URL analysis: IP-based, shorteners, suspicious TLDs",
    "Typosquatting detection (Levenshtein distance vs 45+ brands)",
    "SPF / DKIM / DMARC authentication validation",
    "Sender spoofing (display name vs domain mismatch)",
    "Hidden HTML elements and tracking pixels",
    "Embedded forms with external action URLs",
]:
    engine_b_rows.append([Paragraph(
        f'<font color="{YELLOW.hexval()}">\u25ba</font> &nbsp;{bullet}', S_BULLET)])

eng_b_card = Table(engine_b_rows, colWidths=[col2 - 20])
eng_b_card.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, -1), CARD),
    ("LINEABOVE",     (0, 0), (-1, 0),  2.5, YELLOW),
    ("TOPPADDING",    (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ("ROUNDEDCORNERS", [6]),
]))

engines_row = Table([[eng_a_card, Spacer(10, 1), eng_b_card]],
                    colWidths=[col2, 10, col2])
engines_row.setStyle(TableStyle([
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING",   (0, 0), (-1, -1), 0),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))
story.append(engines_row)
story.append(Spacer(1, 8))

# ═══════════════════════════════════════════════════════════════════════════════
# CLASSIFICATION PIPELINE — 5 steps
# ═══════════════════════════════════════════════════════════════════════════════
steps = [
    ("1", BLUE,   "Ingest",        "Parse .eml, text, or OCR screenshot"),
    ("2", GREEN,  "NLP Analysis",  "DistilBERT embedding + rule-based scoring"),
    ("3", YELLOW, "Structural",    "URL, header, HTML analysis (~50 features)"),
    ("4", PURPLE, "Fusion",        "Random Forest on 818-dim vector"),
    ("5", RED,    "Decision",      "Verdict + explainability + action mapping"),
]
step_cw = W / 5 - 3

def step_card(num, color, title, desc):
    badge_s = S(f"SB{num}", fontName="Helvetica-Bold", fontSize=11,
                textColor=color, alignment=TA_CENTER)
    title_s = S(f"ST{num}", fontName="Helvetica-Bold", fontSize=8.5,
                textColor=WHITE, alignment=TA_CENTER)
    desc_s  = S(f"SD{num}", fontName="Helvetica", fontSize=7.5,
                textColor=DIMMER, alignment=TA_CENTER, leading=10)
    inner = Table([
        [Paragraph(num, badge_s)],
        [Paragraph(title, title_s)],
        [Paragraph(desc, desc_s)],
    ], colWidths=[step_cw - 16])
    inner.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), CARD2),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("LINEBEFORE",    (0, 0), (-1, -1), 2, color),
        ("ROUNDEDCORNERS", [5]),
    ]))
    return inner

pipeline_row = Table(
    [[step_card(n, c, t, d) for n, c, t, d in steps]],
    colWidths=[step_cw] * 5,
)
pipeline_row.setStyle(TableStyle([
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING",   (0, 0), (-1, -1), 2),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 2),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))

story.append(KeepTogether([
    section_title("Classification Pipeline"),
    card([[pipeline_row]], [W - 20], border_color=BLUE),
    Spacer(1, 8),
]))

# ═══════════════════════════════════════════════════════════════════════════════
# TECHNOLOGY STACK
# ═══════════════════════════════════════════════════════════════════════════════
tech = [
    (BLUE,   "Backend",      "Python 3.10+ / FastAPI"),
    (GREEN,  "NLP Model",    "DistilBERT (HuggingFace)"),
    (PURPLE, "Classifier",   "Random Forest (scikit-learn)"),
    (YELLOW, "Deep Learning","PyTorch"),
    (RED,    "OCR",          "Tesseract + Pillow"),
    (CYAN,   "Database",     "SQLite (persistent logs)"),
    (PINK,   "Frontend",     "Tailwind CSS / Vanilla JS"),
    (ORANGE, "URL Analysis", "tldextract / Levenshtein"),
    (BLUE,   "AI Chat",      "Claude API (Anthropic)"),
]
tcw = (W - 20 - 8) / 3

def tech_cell(label_color, label, value):
    t = Table([
        [Paragraph(label, S(f"TL{label}", fontName="Helvetica-Bold", fontSize=7.5,
                            textColor=label_color))],
        [Paragraph(value, S(f"TV{label}", fontName="Helvetica", fontSize=9,
                            textColor=WHITE))],
    ], colWidths=[tcw - 16])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), CARD2),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [5]),
    ]))
    return t

tech_grid_rows = []
for i in range(0, len(tech), 3):
    row = []
    for j in range(3):
        if i + j < len(tech):
            lc, lb, lv = tech[i + j]
            row.append(tech_cell(lc, lb, lv))
        else:
            row.append(Spacer(1, 1))
    tech_grid_rows.append(row)

tech_grid = Table(tech_grid_rows, colWidths=[tcw, tcw, tcw],
                  spaceBefore=0, spaceAfter=0)
tech_grid.setStyle(TableStyle([
    ("LEFTPADDING",   (0, 0), (-1, -1), 4),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
    ("TOPPADDING",    (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))

story.append(KeepTogether([
    section_title("Technology Stack"),
    card([[tech_grid]], [W - 20], border_color=BLUE),
    Spacer(1, 8),
]))

# ═══════════════════════════════════════════════════════════════════════════════
# TOP PHISHING TRIGGERS — bar chart via nested tables
# ═══════════════════════════════════════════════════════════════════════════════
triggers = [
    ("Suspicious URLs",       43, RED),
    ("Urgency Language",      32, ORANGE),
    ("Grammatical Anomalies", 15, PURPLE),
    ("Other Indicators",      10, colors.HexColor("#64748B")),
]
BAR_W = W - 20 - 160   # usable bar width

label_s  = S("TrigL", fontName="Helvetica", fontSize=9, textColor=WHITE)
pct_s    = S("TrigP", fontName="Helvetica-Bold", fontSize=9,
             alignment=TA_RIGHT)

trig_rows = []
for name, pct, col in triggers:
    bar_fill = Table([[""]], colWidths=[BAR_W * pct / 100])
    bar_fill.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), col),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROUNDEDCORNERS", [3]),
    ]))
    bar_bg = Table([[bar_fill, ""]], colWidths=[BAR_W * pct / 100,
                                               BAR_W * (100 - pct) / 100])
    bar_bg.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), CARD2),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("ROUNDEDCORNERS", [3]),
    ]))
    trig_rows.append([
        Paragraph(name, label_s),
        bar_bg,
        Paragraph(f'<font color="{col.hexval()}">{pct}%</font>', pct_s),
    ])
    trig_rows.append([Spacer(1, 4), "", ""])

trig_table = Table(trig_rows, colWidths=[130, BAR_W, 30])
trig_table.setStyle(TableStyle([
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING",   (0, 0), (-1, -1), 0),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))

story.append(KeepTogether([
    section_title("Top Phishing Triggers (from paper)", RED),
    card([
        [Paragraph("Distribution of primary indicators that triggered phishing "
                   "classification in the original study:", S_DIM)],
        [trig_table],
    ], [W - 20], border_color=RED),
    Spacer(1, 8),
]))

# ═══════════════════════════════════════════════════════════════════════════════
# AGENTIC ACTION MAPPING — 3 cards
# ═══════════════════════════════════════════════════════════════════════════════
actions = [
    (RED,   "\u2b1b", "Quarantine", "Confidence > 85%",
     "Isolate immediately. High-confidence phishing."),
    (YELLOW,"&#9888;", "Alert",     "Confidence 50%\u201385%",
     "Flag for manual review by security team."),
    (GREEN, "&#10003;","Pass",      "Confidence < 50%",
     "Deliver normally. No significant indicators."),
]
act_cw = (W - 20 - 16) / 3


def action_card(color, icon, title, conf, desc):
    icon_s  = S(f"AI{title}", fontName="Helvetica-Bold", fontSize=18,
                textColor=color, alignment=TA_CENTER)
    title_s = S(f"AT{title}", fontName="Helvetica-Bold", fontSize=11,
                textColor=color, alignment=TA_CENTER)
    conf_s  = S(f"AC{title}", fontName="Helvetica-Bold", fontSize=8,
                textColor=WHITE, alignment=TA_CENTER)
    desc_s  = S(f"AD{title}", fontName="Helvetica", fontSize=8,
                textColor=DIMMER, alignment=TA_CENTER, leading=11)
    t = Table([
        [Paragraph(icon, icon_s)],
        [Paragraph(title, title_s)],
        [Paragraph(conf, conf_s)],
        [Paragraph(desc, desc_s)],
    ], colWidths=[act_cw - 16])
    bg = colors.HexColor(
        "#2D1515" if color == RED else
        "#2D2515" if color == YELLOW else "#152D1F")
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), bg),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("BOX",           (0, 0), (-1, -1), 1, color),
        ("ROUNDEDCORNERS", [6]),
    ]))
    return t


actions_row = Table(
    [[action_card(*a) for a in actions]],
    colWidths=[act_cw, act_cw, act_cw],
)
actions_row.setStyle(TableStyle([
    ("LEFTPADDING",   (0, 0), (-1, -1), 4),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))

story.append(KeepTogether([
    section_title("Agentic Action Mapping", YELLOW),
    card([
        [Paragraph("The system autonomously maps classification results "
                   "to recommended actions:", S_DIM)],
        [actions_row],
    ], [W - 20], border_color=YELLOW),
    Spacer(1, 8),
]))

# ═══════════════════════════════════════════════════════════════════════════════
# DATA FLOW & STORAGE ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
def flow_box(label, sublabel, color):
    ls = S(f"FB{label}", fontName="Helvetica-Bold", fontSize=8,
           textColor=color, alignment=TA_CENTER)
    ss = S(f"FS{label}", fontName="Helvetica", fontSize=7,
           textColor=DIM, alignment=TA_CENTER, leading=9)
    t = Table([[Paragraph(label, ls)],
               [Paragraph(sublabel, ss) if sublabel else Spacer(1, 1)]],
              colWidths=[110])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), CARD2),
        ("BOX",           (0, 0), (-1, -1), 1.2, color),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t


def arr(color=DIM):
    return Paragraph(
        f'<font color="{color.hexval()}">\u2192</font>',
        S("ARR", fontName="Helvetica-Bold", fontSize=14,
          textColor=color, alignment=TA_CENTER))


flow_row1 = Table([[
    flow_box(".eml Upload", "",          BLUE),
    arr(BLUE),
    flow_box("Parsers",    "Normalize input", colors.HexColor("#94A3B8")),
    arr(DIM),
    flow_box("Semantic Engine", "NLP + Patterns", GREEN),
    arr(GREEN),
    flow_box("Classifier", "RF / Heuristic",   PURPLE),
    arr(PURPLE),
    flow_box("Result + Action", "Explainability", RED),
]], colWidths=[90, 18, 90, 18, 100, 18, 90, 18, 100])
flow_row1.setStyle(TableStyle([
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
    ("LEFTPADDING",   (0, 0), (-1, -1), 2),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 2),
    ("TOPPADDING",    (0, 0), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
]))

flow_notes = Table([[
    Paragraph(f'<font color="{GREEN.hexval()}">\u21bb Retraining Pipeline</font>'
              f' \u2014 verified labeled samples feed back into the classifier',
              S("FN", fontName="Helvetica-Oblique", fontSize=8, textColor=GREEN)),
    Paragraph(f'<font color="{CYAN.hexval()}">SQLite DB</font>'
              f' stores scan history, training samples, and audit log (V-06)',
              S("FN2", fontName="Helvetica", fontSize=8, textColor=CYAN)),
]], colWidths=[(W - 20) / 2] * 2)
flow_notes.setStyle(TableStyle([
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 4),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
]))

story.append(KeepTogether([
    section_title("Data Flow &amp; Storage Architecture", CYAN),
    card([
        [Paragraph("How data flows through the system from input to persistent "
                   "storage and retraining.", S_DIM)],
        [flow_row1],
        [flow_notes],
    ], [W - 20], border_color=CYAN),
    Spacer(1, 8),
]))

# ═══════════════════════════════════════════════════════════════════════════════
# ADVERSARIAL ATTACK TAXONOMY — 4 quadrants
# ═══════════════════════════════════════════════════════════════════════════════
quads = [
    (RED,    "Semantic Evasion", [
        "Paraphrasing urgent language to bypass NLP",
        "Using synonyms for credential requests",
        "Embedding text in images (OCR evasion)",
        "Unicode homograph substitution",
    ]),
    (YELLOW, "Structural Obfuscation", [
        "URL shorteners and redirects",
        "IP-based links and hex encoding",
        "Typosquatting (paypa1.com, micros0ft.com)",
        "Header spoofing and forged SPF/DKIM",
    ]),
    (PURPLE, "Content Manipulation", [
        "HTML-based hidden content injection",
        "Base64-encoded payloads",
        "CSS-hidden tracking pixels",
        "Obfuscated JavaScript execution",
    ]),
    (CYAN,   "Social Engineering", [
        "CEO / executive impersonation (BEC)",
        "Brand spoofing with lookalike domains",
        "Reply-to address mismatch",
        "Pretexting with legitimate-looking invoices",
    ]),
]
qcw = (W - 20 - 8) / 2


def quad_card(color, title, bullets):
    title_s  = S(f"QT{title[:3]}", fontName="Helvetica-Bold", fontSize=9.5,
                 textColor=color)
    bullet_s = S(f"QB{title[:3]}", fontName="Helvetica", fontSize=8.5,
                 leading=12, textColor=DIM, leftIndent=8)
    rows = [[Paragraph(title, title_s)]]
    for b in bullets:
        rows.append([Paragraph(f"\u2022 {b}", bullet_s)])
    t = Table(rows, colWidths=[qcw - 20])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), CARD2),
        ("LINEBEFORE",    (0, 0), (-1, -1), 2.5, color),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t


quad_grid = Table([
    [quad_card(*quads[0]), Spacer(8, 1), quad_card(*quads[1])],
    [Spacer(1, 6), Spacer(1, 6), Spacer(1, 6)],
    [quad_card(*quads[2]), Spacer(8, 1), quad_card(*quads[3])],
], colWidths=[qcw, 8, qcw])
quad_grid.setStyle(TableStyle([
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING",   (0, 0), (-1, -1), 0),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))

story.append(KeepTogether([
    section_title("Adversarial Attack Taxonomy", RED),
    card([
        [Paragraph("Categories of adversarial attacks the system is designed "
                   "to detect and resist:", S_DIM)],
        [quad_grid],
    ], [W - 20], border_color=RED),
    Spacer(1, 8),
]))

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: ADVERSARIAL EVALUATION
# ═══════════════════════════════════════════════════════════════════════════════
phase2_items = [
    ("Semantic Paraphrasing",
     "T5/GPT-based rephrasing of phishing content while preserving malicious intent"),
    ("Structural Obfuscation",
     "URL encoding, homograph attacks, header spoofing techniques"),
    ("Adversarial Retraining",
     "Measuring and improving robustness through adversarial sample augmentation"),
    ("Metrics",
     "Accuracy, Precision, Recall, F1, FNR, FPR, Evasion Success Rate, ROC/AUC curves"),
]
ph2_rows = [
    [Paragraph(
        "The follow-up research paper will extend this system with adversarial "
        "testing to evaluate robustness against evasion attacks. This includes:",
        S_DIM)],
]
for title, desc in phase2_items:
    ph2_rows.append([Paragraph(
        f'<font color="{BLUE.hexval()}">\u25ba</font> &nbsp;'
        f'<b><font color="{WHITE.hexval()}">{title}</font></b> \u2014 {desc}',
        S("P2B", fontName="Helvetica", fontSize=9, leading=13,
          textColor=DIM, leftIndent=6, spaceAfter=4))])

story.append(KeepTogether([
    section_title("Phase 2: Adversarial Evaluation", PURPLE),
    card(ph2_rows, [W - 20], border_color=PURPLE),
    Spacer(1, 14),
]))

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER STRIP
# ═══════════════════════════════════════════════════════════════════════════════
footer_s = S("FooterS", fontName="Helvetica", fontSize=8, textColor=DIMMER,
             alignment=TA_CENTER)
story.append(HRFlowable(width=W, thickness=0.5,
                        color=colors.HexColor("#2D3748"), spaceAfter=6))
story.append(Paragraph(
    "Loo \u00b7 Galindo \u00b7 Romero \u00b7 Qui\u00f1onez \u00b7 "
    "Funez \u00b7 Garc\u00eda \u00b7 Jimenez &nbsp;&mdash;&nbsp; "
    "Universidad Tecnol\u00f3gica de Honduras (UTH) &nbsp;&mdash;&nbsp; "
    "LACCI 2026 &nbsp;&mdash;&nbsp; MIT License",
    footer_s))

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF written -> {OUT}")
