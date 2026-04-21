# streamlit_app.py

import streamlit as st
from interpreter import interpret_result, BLOOD_METRIC_DATA, FULL_BLOOD_COUNT, KIDNEY_FUNCTION, HEART_HEALTH, DIABETES_MARKERS, IRON_STATUS, BONE_PROFILE, MUSCLE_HEALTH, LIVER_FUNCTION, URINE_ANALYSIS, THYROID_FUNCTION, CANCER_MARKERS, VITAMINS
import pandas as pd
from PIL import Image
import pdfplumber
import io
import re
from datetime import date
from pdf_export import generate_pdf_report


st.set_page_config(
    page_title="Blood Test Interpreter",
    layout="wide"
)

hide_streamlit_style = """
    <style>
    /* Removes the Streamlit footer */
    footer {visibility: hidden;}
    /* Removes the 'red line' and hamburger menu at the top */
    header {visibility: hidden;}
    /* Adjusts padding so the app fills the space better */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ===== DESIGN SYSTEM =====
st.markdown("""
<style>
    /* ── Variables ── */
    :root {
        --bg-page:        #F7F7F8;
        --bg-card:        #FFFFFF;
        --bg-elevated:    #EEEEF1;
        --orange:         #FF671D;
        --orange-dim:     rgba(255, 103, 29, 0.10);
        --orange-border:  rgba(255, 103, 29, 0.35);
        --red:            #C52536;
        --red-dim:        rgba(197,  37,  54, 0.08);
        --red-border:     rgba(197,  37,  54, 0.28);
        --green:          #1F8C47;
        --green-dim:      rgba( 31, 140,  71, 0.08);
        --green-border:   rgba( 31, 140,  71, 0.28);
        --text-primary:   #1A1B1E;
        --text-secondary: #4A4B55;
        --text-muted:     #767783;
        --border-subtle:  rgba(0, 0, 0, 0.07);
        --border-medium:  rgba(0, 0, 0, 0.12);
        --radius-sm:      8px;
        --radius-md:      12px;
    }

    /* ── App chrome ── */
    [data-testid="stApp"] {
        background-color: var(--bg-page) !important;
    }
    [data-testid="stHeader"] {
        background: var(--bg-page) !important;
        border-bottom: 1px solid var(--border-subtle) !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* ── Typography ── */
    h1 {
        font-family: 'poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        color: #54565A !important;
        letter-spacing: -0.3px !important;
        line-height: 1.2 !important;
        margin-bottom: 1.25rem !important;
    }
    h2 {
        font-family: 'poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.35rem !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.1px !important;
    }
    h3 {
        font-family: 'poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        color: var(--text-primary) !important;
    }
    p, .stMarkdown p {
        font-family: 'figtree', sans-serif !important;
        color: var(--text-secondary) !important;
        line-height: 1.65 !important;
    }
    hr {
        border: none !important;
        border-top: 1px solid var(--border-subtle) !important;
        margin: 2rem 0 !important;
    }

    /* ── Expanders ── */
    [data-testid="stExpander"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-md) !important;
        margin-bottom: 6px !important;
        overflow: visible !important;
    }
    [data-testid="stExpander"] details summary {
        font-family: 'poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        color: var(--text-primary) !important;
        padding: 13px 18px !important;
        background: transparent !important;
        list-style: none !important;
        border-radius: var(--radius-md) var(--radius-md) 0 0 !important;
    }
    [data-testid="stExpander"] details summary:hover {
        background: var(--bg-elevated) !important;
        cursor: pointer !important;
    }
    [data-testid="stExpander"] details[open] summary {
        color: var(--orange) !important;
        border-bottom: 1px solid var(--border-subtle) !important;
    }
    [data-testid="stExpander"] details[open] summary svg {
        color: var(--orange) !important;
        fill: var(--orange) !important;
    }
    [data-testid="stExpander"] details > div {
        padding: 10px 18px 14px !important;
    }

    /* ── Inputs ── */
    [data-testid="stTextInput"] input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-medium) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: 'figtree', sans-serif !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--orange) !important;
        box-shadow: 0 0 0 3px var(--orange-dim) !important;
    }
    [data-testid="stTextInput"] input::placeholder {
        color: var(--text-muted) !important;
    }

    /* ── Selectbox ── */
    [data-testid="stSelectbox"] > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-medium) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: 'figtree', sans-serif !important;
    }
    [data-testid="stSelectbox"] > div > div:focus-within {
        border-color: var(--orange) !important;
        box-shadow: 0 0 0 3px var(--orange-dim) !important;
    }
    [data-testid="stSelectbox"] label {
        font-family: 'figtree', sans-serif !important;
        color: var(--text-secondary) !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        background: var(--bg-card) !important;
        border: 2px dashed var(--border-medium) !important;
        border-radius: var(--radius-md) !important;
        padding: 20px 24px !important;
        transition: border-color 0.2s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: var(--orange-border) !important;
    }
    [data-testid="stFileUploader"] label {
        font-family: 'figtree', sans-serif !important;
        color: var(--text-secondary) !important;
    }

    /* ── CTA button ── */
    [data-testid="stButton"] > button {
        background: var(--orange) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 14px 32px !important;
        width: 100% !important;
        letter-spacing: 0.2px !important;
        transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
        margin-top: 8px !important;
    }
    [data-testid="stButton"] > button:hover {
        background: #FF7D38 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 24px rgba(255, 103, 29, 0.35) !important;
    }
    [data-testid="stButton"] > button:active {
        transform: translateY(0) !important;
        box-shadow: none !important;
    }
    [data-testid="stButton"] > button p {
        color: #FFFFFF !important;
    }

    /* ── Caption ── */
    .stCaption, [data-testid="stCaptionContainer"] {
        font-family: 'figtree', sans-serif !important;
        color: var(--text-muted) !important;
    }

    /* ── Disclaimer ── */
    .disclaimer-box {
        background: linear-gradient(135deg, rgba(255, 103, 29, 0.08) 0%, rgba(255, 103, 29, 0.04) 100%);
        border: 1.5px solid var(--orange);
        border-radius: var(--radius-md);
        padding: 15px 20px;
        margin-bottom: 24px;
        font-family: 'figtree', sans-serif;
        font-size: 0.84rem;
        color: var(--text-secondary);
        line-height: 1.65;
    }

    /* ── Tooltip ── */
    .tooltip {
        position: relative;
        display: inline-flex;
        align-items: center;
        cursor: pointer;
        margin-left: 6px;
        color: var(--text-secondary);
        font-size: 0.82em;
        vertical-align: middle;
        transition: color 0.15s ease;
    }
    .tooltip:hover {
        color: var(--orange);
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        background: var(--bg-card);
        color: var(--text-secondary);
        text-align: left;
        border-radius: var(--radius-sm);
        padding: 12px 14px;
        border: 1px solid var(--border-medium);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
        position: absolute;
        z-index: 9999;
        bottom: calc(100% + 8px);
        top: auto;
        left: 0;
        transform: none;
        opacity: 0;
        transition: opacity 0.2s ease;
        font-size: 0.8rem;
        font-family: 'figtree', sans-serif;
        width: 280px;
        white-space: normal;
        word-wrap: break-word;
        line-height: 1.55;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }

    /* ── Metric row ── */
    .metric-label {
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 2.5rem;
        padding: 2px 0;
        gap: 1px;
    }
    .metric-name-row {
        display: flex;
        align-items: center;
        font-family: 'figtree', sans-serif;
        font-size: 0.875rem;
        color: var(--text-primary);
        line-height: 1.35;
        gap: 4px;
        flex-wrap: wrap;
    }
    .metric-unit {
        display: block;
        font-family: 'figtree', sans-serif;
        font-size: 0.75rem;
        color: var(--text-muted);
        font-style: italic;
        line-height: 1.2;
    }

    /* ── Logo ── */
    [data-testid="stImage"] img {
        max-width: 100% !important;
        height: auto !important;
    }

    /* ── Summary strip ── */
    .summary-strip {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
    }
    .summary-chip {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 10px;
        border-radius: var(--radius-md);
        padding: 14px 18px;
        font-family: 'figtree', sans-serif;
    }
    .summary-chip-abnormal {
        background: rgba(217, 53, 69, 0.08);
        border: 1px solid var(--red-border);
    }
    .summary-chip-normal {
        background: rgba(61, 184, 102, 0.08);
        border: 1px solid var(--green-border);
    }
    .summary-icon {
        font-size: 1.15rem;
        line-height: 1;
        flex-shrink: 0;
    }
    .summary-count {
        font-size: 1.5rem;
        font-weight: 700;
        font-family: 'poppins', sans-serif;
        line-height: 1;
    }
    .summary-chip-abnormal .summary-count { color: var(--red); }
    .summary-chip-normal  .summary-count { color: var(--green); }
    .summary-label {
        font-size: 0.78rem;
        color: var(--text-secondary);
        margin-top: 2px;
    }

    /* ── Empty state ── */
    .empty-state {
        text-align: center;
        padding: 24px 16px;
        color: var(--text-muted);
        font-family: 'figtree', sans-serif;
        font-size: 0.85rem;
    }
    .empty-state-icon {
        font-size: 1.6rem;
        margin-bottom: 8px;
        opacity: 0.5;
    }

    /* ── Results section labels ── */
    .results-eyebrow {
        font-family: 'poppins', sans-serif;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--orange);
        margin-bottom: 4px;
        margin-top: 8px;
    }

    /* ── Result cards ── */
    .result-card {
        border-radius: var(--radius-md);
        padding: 20px 22px;
        margin-bottom: 10px;
    }
    .result-card-abnormal {
        background: #FFF5F6;
        border: 1.5px solid var(--red);
    }
    .result-card-normal {
        background: #F4FBF6;
        border: 1.5px solid var(--green);
    }
    .result-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        font-family: 'poppins', sans-serif;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .badge-abnormal {
        background: rgba(197, 37, 54, 0.10);
        color: var(--red);
        border: 1px solid rgba(197, 37, 54, 0.25);
    }
    .badge-normal {
        background: rgba(31, 140, 71, 0.10);
        color: var(--green);
        border: 1px solid rgba(31, 140, 71, 0.25);
    }
    .result-name {
        font-family: 'poppins', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .result-body {
        font-family: 'figtree', sans-serif;
        font-size: 0.855rem;
        color: var(--text-secondary);
        line-height: 1.6;
        margin-bottom: 3px;
    }
    .result-body strong {
        color: var(--text-primary);
        font-weight: 600;
    }

    /* ── Results placeholder ── */
    .results-placeholder {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 320px;
        border: 2px dashed var(--border-medium);
        border-radius: var(--radius-md);
        padding: 48px 32px;
        text-align: center;
        color: var(--text-muted);
        font-family: 'figtree', sans-serif;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .results-placeholder-icon {
        font-size: 2.2rem;
        margin-bottom: 12px;
        opacity: 0.35;
    }

    /* ── Responsive: stack all columns on mobile ── */
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        [data-testid="stColumn"] {
            min-width: 100% !important;
            width: 100% !important;
        }
    }

    /* ── Consent flow ── */
    .consent-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 36px 40px;
        margin: 0 auto;
    }
    .consent-step {
        font-family: 'figtree', sans-serif;
        font-size: 0.78rem;
        color: var(--text-muted);
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .consent-title {
        font-family: 'poppins', sans-serif;
        font-weight: 600;
        font-size: 1.3rem;
        color: var(--text-primary);
        margin: 0 0 16px;
    }
    .consent-body {
        font-family: 'figtree', sans-serif;
        font-size: 0.93rem;
        color: var(--text-secondary);
        line-height: 1.7;
        margin-bottom: 20px;
    }
    .consent-toggle-row {
        background: var(--bg-page);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-sm);
        padding: 14px 16px;
        margin-bottom: 10px;
    }
    .consent-toggle-label {
        font-family: 'poppins', sans-serif;
        font-weight: 600;
        font-size: 0.88rem;
        color: var(--text-primary);
        margin-bottom: 3px;
    }
    .consent-toggle-desc {
        font-family: 'figtree', sans-serif;
        font-size: 0.83rem;
        color: var(--text-secondary);
        line-height: 1.55;
    }
    .consent-toggle-locked {
        font-family: 'figtree', sans-serif;
        font-size: 0.76rem;
        color: var(--text-muted);
        margin-top: 4px;
    }
    .consent-checklist {
        font-family: 'figtree', sans-serif;
        font-size: 0.9rem;
        color: var(--text-secondary);
        line-height: 1.8;
        padding-left: 4px;
    }
    .consent-footer {
        font-family: 'figtree', sans-serif;
        font-size: 0.78rem;
        color: var(--text-muted);
        margin-top: 18px;
        padding-top: 14px;
        border-top: 1px solid var(--border-subtle);
    }
    .consent-success-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .data-settings-link {
        font-family: 'figtree', sans-serif;
        font-size: 0.78rem;
        color: var(--text-muted);
        text-decoration: none;
        cursor: pointer;
    }
    .data-settings-link:hover {
        color: var(--orange);
    }
</style>
""", unsafe_allow_html=True)


# Maps common PDF metric name spellings (lowercase) → app metric keys.
# Sorted longest-first so "hdl cholesterol" matches before "cholesterol".
_PDF_NAME_TO_KEY = {
    # Full blood count
    "haemoglobin":                      "haemoglobin",
    "hemoglobin":                       "haemoglobin",
    "red blood count":                  "red_blood_cell_count",
    "red blood cell count":             "red_blood_cell_count",
    "haematocrit (hct)":                "hct",
    "hct":                              "hct",
    "mean corpuscular volume":          "mcv",
    "mcv":                              "mcv",
    "mean corpuscular haemoglobin concentration (mchc)": "mchc",
    "mean corpuscular haemoglobin":     "mch",
    "mchc":                             "mchc",
    "mch":                              "mch",
    "red cell distribution width":      "rdw",
    "rdw":                              "rdw",
    "platelet count":                   "platelets",
    "platelets":                        "platelets",
    "mean platelet volume (mpv)":       "mpv",
    "mpv":                              "mpv",
    "white blood cell count":           "white_blood_cell_count",
    "white cell count":                 "white_blood_cell_count",
    "neutrophils":                      "neutrophils",
    "lymphocytes":                      "lymphocytes",
    "monocytes":                        "monocytes",
    "eosinophils":                      "eosinophils",
    "basophils":                        "basophils",
    # Kidney function
    "sodium":                           "sodium",
    "potassium":                        "potassium",
    "urea":                             "urea",
    "creatinine":                       "creatinine",
    # Heart health
    "hdl % of total":                   "hdl_percentage_of_total_cholesterol",
    "hdl cholesterol":                  "hdl_cholesterol",
    "ldl cholesterol":                  "ldl_cholesterol",
    "tc/hdl ratio":                     "tc_hdl_ratio",
    "total cholesterol/hdl ratio":      "tc_hdl_ratio",
    "cholesterol":                      "cholesterol",
    "triglycerides":                    "triglycerides",
    "triglyceride":                     "triglycerides",
    "high-sensitivity c-reactive protein": "hs_crp",
    "hs- crp":                          "hs_crp",
    "hs-crp":                           "hs_crp",
    "apolipoprotein a1":                "apolipoprotein_a1",
    "apolipoprotein b":                 "apolipoprotein_b",
    "lipoprotein (a)":                  "lipoprotein_a",
    # Diabetes
    "hba1c":                            "hba1c",
    # Iron status
    "serum iron":                       "serum_iron",
    "transferrin":                      "transferrin",
    "ferritin":                         "ferritin",
    "uric acid":                        "uric_acid",
    # Bone profile
    "vitamin d 25(oh)":                 "vitamin_d",
    "vitamin d":                        "vitamin_d",
    # Muscle health
    "creatine kinase":                  "ck",
    # Liver function
    "alkaline phosphatase":             "alkaline_phosphatase",
    "total bilirubin":                  "total_bilirubin",
    "albumin":                          "albumin",
    "alt/gpt":                          "alt/gpt",
    "ast/got":                          "ast/got",
    "gamma gt":                         "gamma_gt",
    # Urine analysis
    "urine protein":                    "urine_protein",
    "urine glucose":                    "urine_glucose",
    "ketones":                          "ketones",
    "wbc's":                            "wbcs",
    "wbcs":                             "wbcs",
    "rbc's":                            "rbcs",
    "rbcs":                             "rbcs",
    "casts":                            "casts",
    "ph":                               "ph",
    # Thyroid function
    "thyroid stimulating hormone":      "tsh",
    "free thyroxine":                   "free_thyroxine",
    "free t3":                          "ft3",
    # Cancer markers
    "ca125":                            "ca_125",
    "ca 125":                           "ca_125",
    # Vitamins
    "serum folate (vitamin b9)":        "folate",
    "active b12":                       "ab12",
}

_SORTED_PDF_NAMES = sorted(_PDF_NAME_TO_KEY, key=len, reverse=True)
_PRESENCE_KEYS = {"urine_protein", "urine_glucose", "ketones", "wbcs", "rbcs", "casts", "bacterial_count"}
_VALUE_RE = re.compile(
    r'^([<>≤≥]?\s*\d+\.?\d*|negative|positive|not detected|detected)',
    re.IGNORECASE,
)


def _parse_numeric(s):
    s = s.strip().lower()
    if s in ("negative", "not detected", "absent"):
        return 0.0
    if s in ("positive", "detected", "present"):
        return 1.0
    s = re.sub(r'^[<>≤≥]=?\s*', '', s)
    try:
        return float(s)
    except ValueError:
        return None


def _extract_patient_name(lines):
    """Extract patient name from PDF lines (handles surnames split across lines)."""
    for i, line in enumerate(lines):
        m = re.search(r'Patient:\s+(.+?)(?:\s+(?:Sex at birth:|Gender:)|$)', line, re.IGNORECASE)
        if m:
            name = m.group(1).strip()
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not re.match(
                    r'^(DOB:|Name\s|VFH|Patient ID:|Laboratory|Report|Results|Sample)',
                    next_line, re.IGNORECASE
                ):
                    name = f"{name} {next_line}"
            return name
    return ""


def parse_lab_pdf(pdf_bytes):
    """Extract blood test values and patient name from a lab PDF using pdfplumber."""
    results = {}
    hba1c_seen = 0

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        lines = []
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines.extend(text.splitlines())

    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        line_lower = line_clean.lower()

        for pdf_name in _SORTED_PDF_NAMES:
            if not line_lower.startswith(pdf_name):
                continue

            metric_key = _PDF_NAME_TO_KEY[pdf_name]

            # HbA1c appears twice (% then mmol/mol); our metric is mmol/mol so skip first.
            if metric_key == "hba1c":
                hba1c_seen += 1
                if hba1c_seen == 1:
                    break

            if metric_key in results:
                break

            remainder = line_clean[len(pdf_name):].strip()
            m = _VALUE_RE.match(remainder)
            if not m:
                break

            value = _parse_numeric(m.group(1))
            if value is None:
                break

            if metric_key in _PRESENCE_KEYS:
                # "< 1" or 0 both mean not detected for presence metrics
                raw = m.group(1).strip()
                value = 0.0 if (value == 0.0 or raw.startswith('<')) else 1.0

            # HCT: PDFs often report as a ratio (0.40 l/l); convert to %
            if metric_key == "hct" and value <= 1.0:
                value *= 100

            results[metric_key] = value
            break

    return results, _extract_patient_name(lines)


def draw_spectrum(data, gender, bg_color='#FFFFFF'):
    value = data['value']
    data_range = data['range']
    unit = data['unit']
    gender_specific = data['gender_specific']
    metric_type = data.get('type', 'hilo')

    if gender_specific:
        if gender == "Female":
            low, high = data_range[0:2]
        else:
            low, high = data_range[2:4]
    else:
        low, high = data_range

    span = high - low if high > low else low
    if span == 0:
        span = value

    chart_min = min(value, low) - (span * 0.2)
    chart_max = max(value, high) + (span * 0.2)

    if metric_type in ['upper_bound', 'presence']:
        chart_min = 0
    elif metric_type == 'lower_bound':
        # Derive chart bounds so the marker always sits at a fixed visual proportion.
        # Guard against value == low (zero range) by nudging the effective value slightly.
        eff = value if value != low else (low * 1.3 if low > 0 else low + 1)
        if eff >= low:
            # Normal: solve for threshold at 20% from left, marker at 60%
            chart_min = max(0, (3 * low - eff) / 2)
            chart_max = chart_min + (eff - chart_min) / 0.60
        else:
            # Abnormal: solve for marker at 30% from left, threshold at 55%
            chart_min = max(0, 2.2 * eff - 1.2 * low)
            chart_max = chart_min + (low - chart_min) / 0.55

    x_range = chart_max - chart_min

    def pct(v):
        return (v - chart_min) / x_range * 100

    low_pct = pct(low)
    high_pct = pct(high)
    val_pct = max(2.0, min(98.0, pct(value)))

    RED, GREEN = '#D93545', '#3DB866'

    if metric_type == 'lower_bound':
        gradient = (f'linear-gradient(to right,'
                    f'{RED} 0%,{RED} {low_pct:.2f}%,'
                    f'{GREEN} {low_pct:.2f}%,{GREEN} 100%)')
        tick_pcts = [(low_pct, low)]
    elif metric_type == 'upper_bound':
        gradient = (f'linear-gradient(to right,'
                    f'{GREEN} 0%,{GREEN} {high_pct:.2f}%,'
                    f'{RED} {high_pct:.2f}%,{RED} 100%)')
        tick_pcts = [(high_pct, high)]
    else:
        gradient = (f'linear-gradient(to right,'
                    f'{RED} 0%,{RED} {low_pct:.2f}%,'
                    f'{GREEN} {low_pct:.2f}%,{GREEN} {high_pct:.2f}%,'
                    f'{RED} {high_pct:.2f}%,{RED} 100%)')
        tick_pcts = [(low_pct, low), (high_pct, high)]

    ticks_html = ''.join(
        f'<div style="position:absolute;left:{tp:.2f}%;transform:translateX(-50%);'
        f'top:22px;font-size:10px;color:#4A4B55;font-family:Arial,sans-serif;'
        f'white-space:nowrap;">{tv}</div>'
        for tp, tv in tick_pcts
    )

    return (
        f'<!DOCTYPE html><html><body style="margin:0;padding:0;'
        f'background:{bg_color};overflow:hidden;">'
        f'<div style="padding:20px 16px 30px;box-sizing:border-box;">'
        f'<div style="position:relative;height:15px;border-radius:8px;background:{gradient};">'
        f'<div style="position:absolute;left:{val_pct:.2f}%;top:50%;'
        f'transform:translate(-50%,-50%);width:14px;height:14px;border-radius:50%;'
        f'background:white;border:1.5px solid rgba(0,0,0,0.25);box-sizing:border-box;"></div>'
        f'<div style="position:absolute;left:{val_pct:.2f}%;bottom:calc(100% + 5px);'
        f'transform:translateX(-50%);font-size:11px;font-weight:500;color:#1A1B1E;'
        f'font-family:Arial,sans-serif;white-space:nowrap;">{value}</div>'
        f'{ticks_html}'
        f'</div>'
        f'</div>'
        f'</body></html>'
    )


def draw_presence_chart(data, bg_color='#FFFFFF'):
    value = data['value']

    if value == 0:
        bar_html = (
            f'<div style="position:relative;height:15px;border-radius:8px;'
            f'background:#1F8C47;display:flex;align-items:center;justify-content:center;">'
            f'<span style="font-size:11px;color:white;font-family:Arial,sans-serif;'
            f'font-weight:500;position:relative;z-index:1;">Not detected</span>'
            f'</div>'
            f'<div style="margin-top:7px;font-size:10px;color:#4A4B55;'
            f'font-family:Arial,sans-serif;text-align:center;">0 (ideal)</div>'
        )
    else:
        chart_max = value * 2.5
        fill_pct = (value / chart_max) * 100
        val_pct = max(2.0, min(98.0, fill_pct))
        bar_html = (
            f'<div style="position:relative;height:15px;border-radius:8px;background:#EEEEF1;">'
            f'<div style="position:absolute;left:0;top:0;height:100%;width:{fill_pct:.2f}%;'
            f'background:#C52536;border-radius:8px 0 0 8px;"></div>'
            f'<div style="position:absolute;left:{val_pct:.2f}%;top:50%;'
            f'transform:translate(-50%,-50%);width:14px;height:14px;border-radius:50%;'
            f'background:white;border:1.5px solid rgba(0,0,0,0.25);'
            f'box-sizing:border-box;z-index:2;"></div>'
            f'<div style="position:absolute;left:{val_pct:.2f}%;bottom:calc(100% + 5px);'
            f'transform:translateX(-50%);font-size:11px;font-weight:500;color:#1A1B1E;'
            f'font-family:Arial,sans-serif;white-space:nowrap;z-index:3;">{value}</div>'
            f'</div>'
            f'<div style="margin-top:7px;font-size:10px;color:#4A4B55;'
            f'font-family:Arial,sans-serif;">0 (ideal)</div>'
        )

    return (
        f'<!DOCTYPE html><html><body style="margin:0;padding:0;'
        f'background:{bg_color};overflow:hidden;">'
        f'<div style="padding:20px 16px 16px;box-sizing:border-box;">'
        f'{bar_html}'
        f'</div>'
        f'</body></html>'
    )


def fig_to_html_iframe(html_content):
    encoded = html_content.replace('"', '&quot;')
    return f'<iframe srcdoc="{encoded}" scrolling="no" style="width:100%; height:90px; border:none; border-radius:12px; overflow:hidden; display:block;"></iframe>'


def input_blood_metrics(DATA, upload, results):
    for metric, meta in DATA.items():
        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown(
                f"""<div class="metric-label">
                    <div class="metric-name-row">
                        {meta['name']}
                        <div class="tooltip">ⓘ
                            <span class="tooltiptext">{meta['explanation']}</span>
                        </div>
                    </div>
                    <div class="metric-unit">{meta["unit"]}</div>
                </div>""",
                unsafe_allow_html=True
            )

        with col2:
            if upload and metric in results:
                default_val = str(results[metric]['value'])
                raw_value = st.text_input(
                    label=meta['name'],
                    value=default_val,
                    key=f"{metric}_upload" if upload else metric,
                    label_visibility="collapsed",
                    placeholder="0.00"
                )
            else:
                raw_value = st.text_input(
                    label=meta['name'],
                    key=metric,
                    label_visibility="collapsed",
                    placeholder="0.00"
                )
            try:
                value = float(raw_value) if raw_value else 0.0
            except ValueError:
                value = 0.0
                if raw_value:
                    st.caption("Please enter a valid number.")

        if value > 0:
            results[metric] = {**meta, "value": value}


# ── Session state ──
if "last_interp" not in st.session_state:
    st.session_state.last_interp = None
if "patient_name" not in st.session_state:
    st.session_state.patient_name = ""

# ── Consent state ──
if "consent_done" not in st.session_state:
    st.session_state.consent_done = False
if "consent_step" not in st.session_state:
    st.session_state.consent_step = 1
if "consent_improve" not in st.session_state:
    st.session_state.consent_improve = True   # locked on
if "consent_research" not in st.session_state:
    st.session_state.consent_research = False
if "consent_insights" not in st.session_state:
    st.session_state.consent_insights = False


_PRIVACY_NOTICE = """
**Who this applies to**
This section applies to individuals who use our digital application to upload and review their health test results. Use of the app does not create a clinical relationship between you and Vital Flow Health.

**What data we collect**
We may collect and process: health test results uploaded by you; basic personal identifiers (e.g. name); and usage data relating to how you interact with the app. Some of this data constitutes special category health data under UK GDPR.

**Important limitation of the data**
Data uploaded to the app is provided directly by users and may not be independently verified for accuracy or completeness. Outputs generated by the app are informational only and must not be relied upon as medical advice.

**How we use your data**
We process your data for the following purposes, based on your consent:
1. *Service improvement* — to improve our health screening services and compare results against anonymised reference data.
2. *Anonymised research and reporting* — to analyse health trends using anonymised and aggregated data. You will not be identifiable in any outputs.
3. *Commercial health insights* — to develop future health insight products using anonymised, aggregated data. This purpose is optional and only applies where you have given explicit consent.

**Lawful basis**
We rely on explicit consent for processing health data. Consent can be withdrawn at any time.

**Data sharing**
We do not sell or share identifiable personal data. Where data is used for research or commercial purposes it is anonymised and cannot be used to identify you.

**Your rights**
You have the right to: withdraw consent at any time; request access to, correction of, or deletion of your data; and lodge a complaint with the Information Commissioner's Office (ICO).

**Data retention**
We retain your data only for as long as necessary for the purposes described above, unless you request deletion.
"""


def _show_consent_flow():
    """Renders the multi-step consent flow and stops page rendering until complete."""
    step = st.session_state.consent_step

    _, col, _ = st.columns([1, 2, 1])
    with col:

        # ── Screen 1: Before You Upload ──────────────────────────────────────
        if step == 1:
            st.markdown("""
<div class="consent-card">
  <div class="consent-step">Step 1 of 4</div>
  <div class="consent-title">Before you upload your results</div>
  <div class="consent-body">
    We want to be clear about how your data is used.
    <ul style="margin:12px 0 0 16px;padding:0;line-height:2;">
      <li>This app helps you understand your health data</li>
      <li>It does not provide medical advice</li>
      <li>Uploading results does not create a clinical relationship with Vital Flow Health</li>
    </ul>
    <br>You'll be able to choose how your data is used on the next screen.
  </div>
</div>
""", unsafe_allow_html=True)
            st.markdown("")
            if st.button("Continue →", key="c1", use_container_width=True):
                st.session_state.consent_step = 2
                st.rerun()

        # ── Screen 2: Your Data, Your Choice ─────────────────────────────────
        elif step == 2:
            st.markdown("""
<div class="consent-card">
  <div class="consent-step">Step 2 of 4</div>
  <div class="consent-title">Your data, your choice</div>
  <div class="consent-body">We use your data in a few different ways. Please choose what you're comfortable with.</div>
</div>
""", unsafe_allow_html=True)

            st.markdown("")

            # Toggle 1 — locked on
            st.markdown("""
<div class="consent-toggle-row">
  <div class="consent-toggle-label">✅ &nbsp;Improve our service</div>
  <div class="consent-toggle-desc">We use your data to improve our health checks and compare results against anonymised reference data.</div>
  <div class="consent-toggle-locked">Required — this cannot be turned off</div>
</div>
""", unsafe_allow_html=True)

            # Toggle 2 — optional
            st.markdown("""
<div class="consent-toggle-row">
  <div class="consent-toggle-label">Contribute to health research</div>
  <div class="consent-toggle-desc">Your data can be used in anonymous, grouped form to identify health trends. You will never be personally identified.</div>
</div>
""", unsafe_allow_html=True)
            research = st.checkbox(
                "I consent to contributing to health research",
                value=st.session_state.consent_research,
                key="toggle_research",
            )

            # Toggle 3 — optional, visually separated
            st.markdown("<div style='margin-top:6px'>", unsafe_allow_html=True)
            st.markdown("""
<div class="consent-toggle-row">
  <div class="consent-toggle-label">Help build future health insights products</div>
  <div class="consent-toggle-desc">Your anonymous data may be used to develop future paid health insight tools. Your identity will never be shared.</div>
</div>
""", unsafe_allow_html=True)
            insights = st.checkbox(
                "I consent to helping build future health insights products",
                value=st.session_state.consent_insights,
                key="toggle_insights",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
<div class="consent-footer">You can change these choices at any time via the data settings link at the bottom of the page.</div>
""", unsafe_allow_html=True)
            st.markdown("")

            if st.button("Continue →", key="c2", use_container_width=True):
                st.session_state.consent_research = research
                st.session_state.consent_insights = insights
                st.session_state.consent_step = 3
                st.rerun()

        # ── Screen 3: Important Information ──────────────────────────────────
        elif step == 3:
            st.markdown("""
<div class="consent-card">
  <div class="consent-step">Step 3 of 4</div>
  <div class="consent-title">Important to know</div>
  <div class="consent-body">By uploading your results, you confirm that:</div>
  <div class="consent-checklist">
    ☑ &nbsp;The data you provide may not be independently verified<br>
    ☑ &nbsp;Results and insights are for information only<br>
    ☑ &nbsp;You should speak to a qualified healthcare professional for medical advice
  </div>
</div>
""", unsafe_allow_html=True)
            st.markdown("")
            if st.button("I understand →", key="c3", use_container_width=True):
                st.session_state.consent_step = 4
                st.rerun()

        # ── Screen 4: Final Confirmation ──────────────────────────────────────
        elif step == 4:
            st.markdown("""
<div class="consent-card">
  <div class="consent-step">Step 4 of 4</div>
  <div class="consent-title">Confirm and continue</div>
  <div class="consent-body">
    You're in control of your data. You can:
    <ul style="margin:10px 0 0 16px;padding:0;line-height:2;">
      <li>Withdraw consent at any time</li>
      <li>Request deletion of your data</li>
    </ul>
  </div>
</div>
""", unsafe_allow_html=True)

            with st.expander("Read our full Privacy Notice"):
                st.markdown(_PRIVACY_NOTICE)

            st.markdown("")
            if st.button("Continue to the app →", key="c4", use_container_width=True):
                st.session_state.consent_step = 5
                st.session_state.consent_done = True
                st.rerun()

        # ── Screen 5: Success ─────────────────────────────────────────────────
        elif step == 5:
            st.markdown("""
<div class="consent-card" style="text-align:center;">
  <div class="consent-success-icon">✅</div>
  <div class="consent-title" style="text-align:center;">You're all set</div>
  <div class="consent-body" style="text-align:center;">
    Your preferences have been saved.<br>
    Remember: insights are informational and not a diagnosis.
  </div>
</div>
""", unsafe_allow_html=True)
            st.markdown("")
            if st.button("Go to the app →", key="c5", use_container_width=True):
                st.session_state.consent_step = 6   # past all screens
                st.rerun()

    st.stop()


# Run consent flow until complete
if not st.session_state.consent_done or st.session_state.consent_step <= 5:
    _show_consent_flow()

# ── Full-width header ──
st.markdown("<h1>Blood Test Interpreter</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-family:figtree,sans-serif;font-size:0.95rem;line-height:1.7;"
    "color:var(--text-secondary);margin:0 0 20px;'>"
    "The Vital Flow Health blood test interpreter helps you understand what your blood test results actually mean. "
    "Enter your values and the tool compares each one against established reference ranges, "
    "flags anything outside normal bounds, and explains what it may indicate in language that you can understand. "
    "It's designed for anyone who has received a blood test report and wants a clearer picture "
    "of their results before, or alongside, a conversation with their doctor."
    "</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<div class='disclaimer-box'>"
    "<strong>Disclaimer:</strong> This tool is for informational purposes only and is not a substitute "
    "for professional medical advice, diagnosis, or treatment. Please consult a healthcare professional "
    "if you have any medical concerns. Your data is private and not stored by Vital Flow Health for any purposes."
    "</div>",
    unsafe_allow_html=True
)

sex = st.selectbox(
    label="Biological sex",
    options=["Female", "Male"],
    index=None,
    placeholder="Select sex"
)

if not sex:
    st.stop()

results = {}
upload = False

# ── Two-column layout ──
col_input, col_results = st.columns([1, 1], gap="large")

with col_input:
    st.header("Enter your blood test results")
    st.write("Input values only for the metrics you have tested, ensuring units match those shown.")

    uploaded_file = st.file_uploader(
        "If you have had a blood test with Vital Flow Health, upload your lab report to autofill the form.",
        type=["pdf", "csv"]
    )
    if uploaded_file is not None:
        if uploaded_file.name.lower().endswith(".pdf"):
            with st.spinner("Reading your lab report..."):
                try:
                    parsed, extracted_name = parse_lab_pdf(uploaded_file.read())
                    upload = True
                    if extracted_name:
                        st.session_state.patient_name = extracted_name
                    for metric_key, value in parsed.items():
                        if metric_key in BLOOD_METRIC_DATA:
                            meta = BLOOD_METRIC_DATA[metric_key]
                            results[metric_key] = {**meta, "value": float(value)}
                    st.success(f"Extracted {len(results)} metric(s) from your report.")
                except Exception as e:
                    st.error(f"Could not parse PDF: {e}")
        else:
            df = pd.read_csv(uploaded_file)
            upload = True
            for _, row in df.iterrows():
                metric = row['Metric']
                value = row['Result']
                if metric in BLOOD_METRIC_DATA:
                    meta = BLOOD_METRIC_DATA[metric]
                    results[metric] = {**meta, "value": value}

    interpret_clicked = st.button("Interpret Results")

    sorted_metrics = dict(sorted(BLOOD_METRIC_DATA.items(), key=lambda x: x[1]['name'].lower()))
    input_blood_metrics(sorted_metrics, upload, results)

    if interpret_clicked:
        if not results:
            st.session_state.last_interp = {"error": True}
        else:
            normal_results = {}
            abnormal_results = {}
            for metric, data in results.items():
                status, explanation, advice = interpret_result(metric, data, sex)
                if status == "Normal":
                    normal_results[metric] = (data, status, explanation, advice)
                else:
                    abnormal_results[metric] = (data, status, explanation, advice)
            st.session_state.last_interp = {
                "normal": normal_results,
                "abnormal": abnormal_results,
                "sex": sex,
            }

with col_results:
    interp = st.session_state.last_interp

    if interp is None:
        st.markdown(
            "<div class='results-placeholder'>"
            "<div class='results-placeholder-icon'>&#128203;</div>"
            "Enter your blood test values,<br>then click <strong>Interpret Results</strong>."
            "</div>",
            unsafe_allow_html=True
        )
    elif interp.get("error"):
        st.markdown(
            "<div class='disclaimer-box' role='alert'>"
            "<strong>No results entered.</strong> Please enter at least one blood test value before interpreting."
            "</div>",
            unsafe_allow_html=True
        )
    else:
        interp_sex = interp["sex"]
        normal_results = interp["normal"]
        abnormal_results = interp["abnormal"]
        n_abnormal = len(abnormal_results)
        n_normal = len(normal_results)

        st.header("Interpretation")

        patient_name = st.text_input(
            "Name for report",
            value=st.session_state.patient_name,
            placeholder="Optional — leave blank to omit",
            label_visibility="visible",
        )
        pdf_bytes = generate_pdf_report(
            abnormal_results=abnormal_results,
            normal_results=normal_results,
            sex=interp_sex,
            report_date=date.today(),
            patient_name=patient_name,
        )
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"blood_test_report{'_' + patient_name.replace(' ', '_') if patient_name else ''}_{date.today().isoformat()}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

        st.markdown(f"""
            <div class="summary-strip">
                <div class="summary-chip summary-chip-abnormal">
                    <div class="summary-icon">&#9888;</div>
                    <div>
                        <div class="summary-count">{n_abnormal}</div>
                        <div class="summary-label">Abnormal result{"s" if n_abnormal != 1 else ""}</div>
                    </div>
                </div>
                <div class="summary-chip summary-chip-normal">
                    <div class="summary-icon">&#10003;</div>
                    <div>
                        <div class="summary-count">{n_normal}</div>
                        <div class="summary-label">Normal result{"s" if n_normal != 1 else ""}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("Abnormal Results")
        if abnormal_results:
            for metric, (data, status, explanation, advice) in abnormal_results.items():
                fig = draw_presence_chart(data, bg_color='#FFF5F6') if data.get('type') == 'presence' else draw_spectrum(data, interp_sex, bg_color='#FFF5F6')
                chart_iframe = fig_to_html_iframe(fig)
                st.markdown(f"""
                    <div class="result-card result-card-abnormal">
                        <div class="result-badge badge-abnormal">&#9888; {status}</div>
                        <div class="result-name">{data['name']}</div>
                        <div class="result-body">{explanation}</div>
                        <div class="result-body" style="margin-top:6px;">
                            <strong>Result:</strong> {data['value']} {data['unit']}
                        </div>
                        <div style="margin-top:12px; border-radius:12px; overflow:hidden;">
                            {chart_iframe}
                        </div>
                        <div class="result-body" style="margin-top:10px;">
                            <strong>Advice:</strong> {advice}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="empty-state">'
                '<div class="empty-state-icon">&#10003;</div>'
                'All your results are within normal range.'
                '</div>',
                unsafe_allow_html=True
            )

        st.subheader("Normal Results")
        if normal_results:
            for metric, (data, status, explanation, advice) in normal_results.items():
                fig = draw_presence_chart(data, bg_color='#F4FBF6') if data.get('type') == 'presence' else draw_spectrum(data, interp_sex, bg_color='#F4FBF6')
                chart_iframe = fig_to_html_iframe(fig)
                st.markdown(f"""
                    <div class="result-card result-card-normal">
                        <div class="result-badge badge-normal">&#10003; {status}</div>
                        <div class="result-name">{data['name']}</div>
                        <div class="result-body">{explanation}</div>
                        <div class="result-body" style="margin-top:6px;">
                            <strong>Result:</strong> {data['value']} {data['unit']}
                        </div>
                        <div style="margin-top:12px; border-radius:12px; overflow:hidden;">
                            {chart_iframe}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="empty-state">'
                '<div class="empty-state-icon">&#9432;</div>'
                'No results in the normal range.'
                '</div>',
                unsafe_allow_html=True
            )

