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
from salesforce_client import submit_results


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
        padding-bottom: 72px !important;
        max-width: 1400px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* ── Typography ── */
    h1 {
        font-family: 'figtree', sans-serif !important;
        font-weight: 500 !important;
        font-size: 2rem !important;
        color: #54565A !important;
        letter-spacing: -0.3px !important;
        line-height: 1.2 !important;
        margin-bottom: 1.25rem !important;
    }
    h2 {
        font-family: 'figtree', sans-serif !important;
        font-weight: 500 !important;
        font-size: 1.35rem !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.1px !important;
    }
    h3 {
        font-family: 'figtree', sans-serif !important;
        font-weight: 500 !important;
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
        font-family: 'figtree', sans-serif !important;
        font-weight: 500 !important;
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
    [data-testid="InputInstructions"] {
        display: none !important;
    }

    /* ── Metric search selectbox ── */
    .st-key-metric_search [data-testid="stSelectbox"] > div > div {
        border: 1.5px solid var(--orange) !important;
        margin-bottom: 0.75rem !important;
    }
    .st-key-metric_search [data-testid="stSelectbox"] > div > div:focus-within {
        box-shadow: 0 0 0 3px var(--orange-dim) !important;
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
        font-family: 'figtree', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        padding: 14px 32px !important;
        width: 100% !important;
        letter-spacing: 0.2px !important;
        transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
        margin-top: 0 !important;
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
    .metric-row-col [data-testid="stColumn"]:first-child {
        display: flex !important;
        align-items: center !important;
    }
    .metric-label {
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 6px 0;
        gap: 2px;
    }
    .metric-name-row {
        display: flex;
        align-items: center;
        font-family: 'figtree', sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--text-primary);
        line-height: 1.35;
        gap: 4px;
        flex-wrap: wrap;
    }
    .metric-unit {
        display: block;
        font-family: 'figtree', sans-serif;
        font-size: 0.72rem;
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
        font-weight: 500;
        font-family: 'figtree', sans-serif;
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
        font-family: 'figtree', sans-serif;
        font-size: 0.68rem;
        font-weight: 500;
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
        font-weight: 500;
        font-family: 'figtree', sans-serif;
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
        font-family: 'figtree', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
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
        font-weight: 500;
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
        font-family: 'figtree', sans-serif;
        font-weight: 500;
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
        font-family: 'figtree', sans-serif;
        font-weight: 500;
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
    .consent-toggle-divider {
        border: none;
        border-top: 1px solid var(--border-subtle);
        margin: 0;
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

    /* ── App footer: fixed at bottom of viewport, always visible ── */
    [data-testid="stHorizontalBlock"]:has(#footer-outer-marker) {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        z-index: 50 !important;
        background: var(--bg-page) !important;
        border-top: 1px solid var(--border-subtle) !important;
        padding: 10px 0 !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
        gap: 0 !important;
        height: auto !important;
        overflow: visible !important;
    }
    /* Each footer column: shrink to content width, vertically centred */
    [data-testid="stHorizontalBlock"]:has(#footer-outer-marker) > div[data-testid="stColumn"] {
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: 0 !important;
        min-height: unset !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 20px !important;
    }
    /* Normalise the markdown container holding the mailto link so it sits at
       the same vertical position as the st.button text in adjacent columns */
    [data-testid="stHorizontalBlock"]:has(#footer-outer-marker) [data-testid="stMarkdownContainer"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }
    [data-testid="stHorizontalBlock"]:has(#footer-outer-marker) [data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }
    /* Hide the marker span itself (HTML hidden attr may not always suppress layout) */
    #footer-outer-marker { display: none !important; }
    /* Footer link-style buttons */
    [data-testid="stHorizontalBlock"]:has(#footer-outer-marker) [data-testid="stButton"] > button {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        height: auto !important;
        min-height: unset !important;
        width: auto !important;
        text-align: center !important;
        font-family: 'figtree', sans-serif !important;
        font-size: 0.80rem !important;
        color: var(--text-muted) !important;
        text-decoration: none !important;
        letter-spacing: 0 !important;
        margin-top: 0 !important;
        line-height: 1 !important;
        white-space: nowrap !important;
    }
    [data-testid="stHorizontalBlock"]:has(#footer-outer-marker) [data-testid="stButton"] > button p {
        color: var(--text-muted) !important;
        font-family: 'figtree', sans-serif !important;
        font-size: 0.80rem !important;
        text-decoration: underline !important;
        margin: 0 !important;
        line-height: 1 !important;
        white-space: nowrap !important;
    }
    [data-testid="stHorizontalBlock"]:has(#footer-outer-marker) [data-testid="stButton"] > button:hover {
        background: none !important;
        color: var(--orange) !important;
        transform: none !important;
        box-shadow: none !important;
    }
    [data-testid="stHorizontalBlock"]:has(#footer-outer-marker) [data-testid="stButton"] > button:hover p {
        color: var(--orange) !important;
    }
    /* Footer mailto link — matches the link-style button appearance */
    [data-testid="stHorizontalBlock"]:has(#footer-outer-marker) a.footer-mailto {
        display: block;
        text-align: center;
        font-family: 'figtree', sans-serif;
        font-size: 0.80rem;
        color: var(--text-muted);
        text-decoration: underline;
        line-height: 1;
        white-space: nowrap;
        background: none;
        border: none;
        padding: 0;
        margin: 0;
    }
    [data-testid="stHorizontalBlock"]:has(#footer-outer-marker) a.footer-mailto:hover {
        color: var(--orange);
    }
    /* "Where do I find my lab report?" link-style button.
       :not(:has(#col-results-marker)) excludes the outer st.columns([1,1])
       horizontal block (which also propagates :has on the marker) so the
       rule only matches the inner st.columns([1,8]) wrapper. */
    [data-testid="stHorizontalBlock"]:has(#lab-report-help-marker):not(:has(#col-results-marker)) {
        margin-top: -10px !important;
        gap: 0 !important;
    }
    [data-testid="stHorizontalBlock"]:has(#lab-report-help-marker):not(:has(#col-results-marker)) [data-testid="stButton"] > button {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        height: auto !important;
        min-height: unset !important;
        width: auto !important;
        margin-top: 0 !important;
    }
    [data-testid="stHorizontalBlock"]:has(#lab-report-help-marker):not(:has(#col-results-marker)) [data-testid="stButton"] > button p {
        color: var(--text-muted) !important;
        font-family: 'figtree', sans-serif !important;
        font-size: 0.80rem !important;
        text-decoration: underline !important;
        white-space: nowrap !important;
        margin: 0 !important;
    }
    [data-testid="stHorizontalBlock"]:has(#lab-report-help-marker):not(:has(#col-results-marker)) [data-testid="stButton"] > button:hover {
        background: none !important;
        transform: none !important;
        box-shadow: none !important;
    }
    [data-testid="stHorizontalBlock"]:has(#lab-report-help-marker):not(:has(#col-results-marker)) [data-testid="stButton"] > button:hover p {
        color: var(--orange) !important;
    }
    /* "Clear all values" link-style button */
    .st-key-clear_all_values [data-testid="stButton"] > button {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        height: auto !important;
        min-height: unset !important;
        width: 100% !important;
        margin: 0 !important;
    }
    .st-key-clear_all_values [data-testid="stButton"] > button p {
        color: var(--text-muted) !important;
        font-family: 'figtree', sans-serif !important;
        font-size: 0.80rem !important;
        text-decoration: underline !important;
        text-align: center !important;
        margin: 0 !important;
    }
    .st-key-clear_all_values [data-testid="stButton"] > button:hover {
        background: none !important;
        transform: none !important;
        box-shadow: none !important;
    }
    .st-key-clear_all_values [data-testid="stButton"] > button:hover p {
        color: var(--orange) !important;
    }
    /* Data settings modal: pad the content column (two selectors for robustness) */
    [data-testid="stColumn"]:has(#ds-modal-marker) > div > [data-testid="stVerticalBlock"],
    [data-testid="stColumn"]:has(#ds-modal-marker) > div > div > [data-testid="stVerticalBlock"] {
        padding: 32px 36px 28px !important;
        box-sizing: border-box !important;
    }
    /* Save/cancel row in ds modal should not look like toggle-row cards */
    [data-testid="stColumn"]:has(#ds-modal-marker) [data-testid="stHorizontalBlock"] {
        background: none !important;
        border: none !important;
        border-radius: 0 !important;
        margin: 16px 0 0 !important;
        width: 100% !important;
        gap: 8px !important;
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


def _clear_all_values():
    st.session_state.manual_values = {}
    st.session_state.last_interp = None
    st.session_state.patient_name = ""
    for key in BLOOD_METRIC_DATA:
        if key in st.session_state:
            st.session_state[key] = ""
        upload_key = f"{key}_upload"
        if upload_key in st.session_state:
            st.session_state[upload_key] = ""


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
                # Restore display value if Streamlit cleared widget state while metric was hidden
                if metric not in st.session_state and metric in st.session_state.manual_values:
                    saved = st.session_state.manual_values[metric]
                    st.session_state[metric] = str(int(saved)) if saved == int(saved) else str(saved)
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
            st.session_state.manual_values[metric] = value
        else:
            st.session_state.manual_values.pop(metric, None)


# ── Session state ──
if "last_interp" not in st.session_state:
    st.session_state.last_interp = None
if "patient_name" not in st.session_state:
    st.session_state.patient_name = ""

# ── Consent state ──
if "consent_done" not in st.session_state:
    st.session_state.consent_done = False
if "consent_improve" not in st.session_state:
    st.session_state.consent_improve = True   # locked on
if "consent_research" not in st.session_state:
    st.session_state.consent_research = False
if "consent_insights" not in st.session_state:
    st.session_state.consent_insights = False
if "show_modal" not in st.session_state:
    st.session_state.show_modal = None
if "sf_submitted_hash" not in st.session_state:
    st.session_state.sf_submitted_hash = None
if "manual_values" not in st.session_state:
    st.session_state.manual_values = {}


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



def _show_privacy_notice_modal():
    """Renders the privacy notice as a fixed modal overlay (session-state driven)."""
    st.markdown("""
<style>
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(15,15,20,0.45);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    z-index: 1099;
    pointer-events: all;
}
[data-testid="stHorizontalBlock"]:has(#pn-modal-marker) {
    height: 0 !important;
    overflow: visible !important;
    margin: 0 !important;
    padding: 0 !important;
}
[data-testid="stColumn"]:has(#pn-modal-marker) {
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    z-index: 1100 !important;
    width: min(560px, 92vw) !important;
    max-height: 84vh !important;
    overflow-x: hidden !important;
    overflow-y: auto !important;
    border-radius: 16px !important;
    background: #FFFFFF !important;
    box-shadow: 0 32px 80px rgba(0,0,0,0.22), 0 0 0 1px rgba(0,0,0,0.06) !important;
    padding: 28px 32px 24px !important;
    pointer-events: all !important;
}
[data-testid="stColumn"]:has(#pn-modal-marker) > div {
    background: #FFFFFF !important;
}
/* Close button row: taken out of normal flow */
[data-testid="stColumn"]:has(#pn-modal-marker) [data-testid="stHorizontalBlock"]:has(#pn-close-marker) {
    height: 0 !important;
    overflow: visible !important;
    margin: 0 !important;
    padding: 0 !important;
}
/* Close column: pinned to the top-right corner of the modal card */
[data-testid="stColumn"]:has(#pn-modal-marker) [data-testid="stColumn"]:has(#pn-close-marker) {
    position: absolute !important;
    top: 12px !important;
    right: 16px !important;
    width: auto !important;
    flex: none !important;
    min-width: unset !important;
    z-index: 1 !important;
}
[data-testid="stColumn"]:has(#pn-close-marker) [data-testid="stButton"] > button {
    background: rgba(0,0,0,0.07) !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 50% !important;
    width: 30px !important;
    height: 30px !important;
    min-height: 30px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-top: 0 !important;
}
[data-testid="stColumn"]:has(#pn-close-marker) [data-testid="stButton"] > button p {
    color: #555 !important;
    margin: 0 !important;
    font-size: 1rem !important;
    line-height: 1 !important;
}
[data-testid="stColumn"]:has(#pn-close-marker) [data-testid="stButton"] > button:hover {
    background: rgba(0,0,0,0.14) !important;
    transform: none !important;
    box-shadow: none !important;
}
[data-testid="stColumn"]:has(#pn-close-marker) [data-testid="stButton"] > button:hover p {
    color: #111 !important;
}
</style>
""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.markdown('<span id="pn-modal-marker" hidden aria-hidden="true"></span>',
                    unsafe_allow_html=True)

        st.markdown(
            '<div style="font-family:\'figtree\',sans-serif;font-weight:500;'
            'font-size:1.2rem;color:var(--text-primary);line-height:1.3;'
            'padding-right:44px;margin-bottom:8px;">Privacy Notice</div>',
            unsafe_allow_html=True,
        )
        (close_col,) = st.columns([1])
        with close_col:
            st.markdown('<span id="pn-close-marker" hidden aria-hidden="true"></span>',
                        unsafe_allow_html=True)
            if st.button("✕", key="close_pn_modal"):
                st.session_state.show_modal = None
                st.rerun()

        st.markdown(_PRIVACY_NOTICE)


def _show_data_settings_modal():
    """Renders the data settings as a fixed modal overlay (session-state driven)."""
    st.markdown("""
<style>
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(15,15,20,0.45);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    z-index: 1099;
    pointer-events: all;
}
[data-testid="stHorizontalBlock"]:has(#ds-modal-marker) {
    height: 0 !important;
    overflow: visible !important;
    margin: 0 !important;
    padding: 0 !important;
}
[data-testid="stColumn"]:has(#ds-modal-marker) {
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    z-index: 1100 !important;
    width: min(460px, 92vw) !important;
    max-height: 80vh !important;
    overflow-x: hidden !important;
    overflow-y: auto !important;
    border-radius: 16px !important;
    background: #FFFFFF !important;
    box-shadow: 0 32px 80px rgba(0,0,0,0.22), 0 0 0 1px rgba(0,0,0,0.06) !important;
    padding: 28px 32px 24px !important;
    pointer-events: all !important;
}
[data-testid="stColumn"]:has(#ds-modal-marker) > div {
    background: #FFFFFF !important;
}
[data-testid="stColumn"]:has(#ds-modal-marker) [data-testid="stColumn"]:has(#pn-link-ds-marker) [data-testid="stButton"] > button {
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    height: auto !important;
    min-height: unset !important;
    width: auto !important;
    margin-top: 0 !important;
}
[data-testid="stColumn"]:has(#ds-modal-marker) [data-testid="stColumn"]:has(#pn-link-ds-marker) [data-testid="stButton"] > button p {
    color: var(--text-muted) !important;
    font-family: 'figtree', sans-serif !important;
    font-size: 0.78rem !important;
    text-decoration: underline !important;
    margin: 0 !important;
}
[data-testid="stColumn"]:has(#ds-modal-marker) [data-testid="stColumn"]:has(#pn-link-ds-marker) [data-testid="stButton"] > button:hover {
    background: none !important;
    transform: none !important;
    box-shadow: none !important;
}
[data-testid="stColumn"]:has(#ds-modal-marker) [data-testid="stColumn"]:has(#pn-link-ds-marker) [data-testid="stButton"] > button:hover p {
    color: var(--orange) !important;
}
</style>
""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<span id="ds-modal-marker" hidden aria-hidden="true"></span>',
                    unsafe_allow_html=True)

        st.markdown("""
<div style="margin-bottom:20px;">
  <div style="font-family:'figtree',sans-serif;font-weight:500;font-size:1.2rem;
              color:var(--text-primary);margin:0 0 10px;">Privacy Settings</div>
  <div style="font-family:'figtree',sans-serif;font-size:0.88rem;color:var(--text-secondary);
              line-height:1.65;">
    Manage how your data is used. <em>Improve our service</em> is required and cannot be disabled.
  </div>
</div>
""", unsafe_allow_html=True)

        new_research = st.toggle(
            "Contribute to health research",
            value=st.session_state.consent_research,
            key="ds_research",
        )
        new_insights = st.toggle(
            "Help build future health insights products",
            value=st.session_state.consent_insights,
            key="ds_insights",
        )

        st.markdown(
            '<div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--border-subtle);"></div>',
            unsafe_allow_html=True,
        )
        (link_col,) = st.columns([1])
        with link_col:
            st.markdown('<span id="pn-link-ds-marker" hidden aria-hidden="true"></span>',
                        unsafe_allow_html=True)
            if st.button("Read our Privacy Notice", key="open_pn_from_ds"):
                st.session_state.show_modal = "privacy_notice"
                st.rerun()

        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("Save preferences", key="save_ds_modal",
                         use_container_width=True, type="primary"):
                st.session_state.consent_research = new_research
                st.session_state.consent_insights = new_insights
                st.session_state.show_modal = None
                st.rerun()
        with c2:
            if st.button("Cancel", key="close_ds_modal", use_container_width=True):
                st.session_state.show_modal = None
                st.rerun()


def _show_consent_flow():
    """Renders the consent flow as a single-screen modal overlay."""

    # ── Modal overlay + toggle row CSS ──────────────────────────────────────
    # body::before creates a blurred backdrop. The consent center column is
    # identified by #consent-col-marker and lifted to a fixed position via :has().
    # Toggle rows (stHorizontalBlock inside the center column) get card styling
    # with symmetric 40px horizontal inset matching the header card padding.
    st.markdown("""
<style>
/* ── Backdrop ── */
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(15, 15, 20, 0.45);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    z-index: 999;
    pointer-events: all;
}
/* ── Collapse the outer layout row so app fills the viewport behind the modal ── */
[data-testid="stHorizontalBlock"]:has(#consent-col-marker) {
    height: 0 !important;
    overflow: visible !important;
    margin: 0 !important;
    padding: 0 !important;
}
/* ── Float the consent center column as a fixed modal ── */
[data-testid="stColumn"]:has(#consent-col-marker) {
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    z-index: 1000 !important;
    width: min(560px, 92vw) !important;
    max-height: 88vh !important;
    overflow-x: hidden !important;
    overflow-y: auto !important;
    border-radius: 16px !important;
    background: #FFFFFF !important;
    box-shadow: 0 32px 80px rgba(0, 0, 0, 0.22), 0 0 0 1px rgba(0,0,0,0.06) !important;
    padding: 0 !important;
    pointer-events: all !important;
}
[data-testid="stColumn"]:has(#consent-col-marker) > div {
    background: #FFFFFF !important;
}
[data-testid="stColumn"]:has(#consent-col-marker) .consent-card {
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

/* ── Toggle row card container ──
   width: calc(100% - 80px) + margin-left: 40px gives symmetric 40px insets.
   margin-right is intentionally omitted — the width calc handles the right side,
   since Streamlit sets an explicit width on stHorizontalBlock that would ignore
   a margin-right offset.                                                        */
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"] {
    background: var(--bg-page) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    align-items: center !important;
    gap: 0 !important;
    margin-bottom: 10px !important;
    margin-left: 40px !important;
    width: calc(100% - 80px) !important;
    overflow: hidden !important;
}
/* ── Text column ── */
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"]
    [data-testid="stColumn"]:first-child {
    padding: 16px 8px 16px 16px !important;
    box-sizing: border-box !important;
}
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"]
    [data-testid="stColumn"]:first-child > div,
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"]
    [data-testid="stColumn"]:first-child [data-testid="stVerticalBlock"],
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"]
    [data-testid="stColumn"]:first-child [data-testid="stMarkdownContainer"] {
    padding: 0 !important;
    margin: 0 !important;
    gap: 0 !important;
}
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"] p {
    margin: 0 !important;
}
/* ── Toggle column: vertical centering ──
   align-items:center on the row (stHorizontalBlock) centers each column within
   the row height, so we just need to right-align and strip spacing here.
   All intermediate wrappers (> div, stVerticalBlock, element-container) are made
   flex so they pass the centering through without adding extra height.            */
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"]
    [data-testid="stColumn"]:last-child {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    padding: 0 16px !important;
    box-sizing: border-box !important;
    gap: 0 !important;
}
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"]
    [data-testid="stColumn"]:last-child > div,
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"]
    [data-testid="stColumn"]:last-child [data-testid="stVerticalBlock"],
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"]
    [data-testid="stColumn"]:last-child [data-testid="element-container"] {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    padding: 0 !important;
    margin: 0 !important;
    gap: 0 !important;
}
/* ── Opacity: cancel Streamlit's disabled-widget fade ── */
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"] * {
    opacity: 1 !important;
}
/* ── Locked toggle: force track to orange, thumb to light grey ──
   ToggleTrack (> div:first-child of the label container) gets orange.
   ToggleThumb (sole child inside the track) gets a light grey — visible against
   the orange but not white, so it reads as non-interactive.                      */
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"]:first-of-type
    *:has(> input:checked:disabled) > div:first-child {
    background-color: var(--orange) !important;
}
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"]:first-of-type
    *:has(> input:checked:disabled) > div:first-child > div:first-child {
    background-color: #e2e2e2 !important;
}
/* ── HR divider ── */
[data-testid="stColumn"]:has(#consent-col-marker) hr {
    margin: 20px 40px 14px !important;
}
/* ── Expander: same width-calc trick as toggle rows ── */
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stExpander"] {
    margin-left: 40px !important;
    width: calc(100% - 80px) !important;
}
/* ── Button: target stButton directly (avoids fragile deep-child selectors);
   bottom padding gives breathing room at the modal base              ── */
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stButton"] {
    padding: 0 40px 32px !important;
    box-sizing: border-box !important;
}
/* ── "Read our full Privacy Notice" link-style button ── */
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stHorizontalBlock"]:has(#pn-link-consent-marker) {
    background: none !important;
    border: none !important;
    border-radius: 0 !important;
    margin-left: 40px !important;
    margin-bottom: 4px !important;
    width: calc(100% - 80px) !important;
    overflow: visible !important;
}
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stColumn"]:has(#pn-link-consent-marker) [data-testid="stButton"] {
    padding: 0 !important;
}
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stColumn"]:has(#pn-link-consent-marker) [data-testid="stButton"] > button {
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    height: auto !important;
    min-height: unset !important;
    width: auto !important;
    margin-top: 0 !important;
}
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stColumn"]:has(#pn-link-consent-marker) [data-testid="stButton"] > button p {
    color: var(--text-muted) !important;
    font-family: 'figtree', sans-serif !important;
    font-size: 0.80rem !important;
    text-decoration: underline !important;
    margin: 0 !important;
}
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stColumn"]:has(#pn-link-consent-marker) [data-testid="stButton"] > button:hover {
    background: none !important;
    transform: none !important;
    box-shadow: none !important;
}
[data-testid="stColumn"]:has(#consent-col-marker) [data-testid="stColumn"]:has(#pn-link-consent-marker) [data-testid="stButton"] > button:hover p {
    color: var(--orange) !important;
}
</style>
""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<span id="consent-col-marker" hidden aria-hidden="true"></span>',
                    unsafe_allow_html=True)

        # ── Header ──────────────────────────────────────────────────────────
        st.markdown("""
<div class="consent-card" style="padding-bottom:16px;">
  <div class="consent-title">Before you upload your results</div>
  <div class="consent-body">
    This app helps you understand your health data. It does not provide medical advice,
    and uploading results does not create a clinical relationship with Vital Flow Health.
  </div>
  <div style="font-family:'figtree',sans-serif;font-size:0.75rem;letter-spacing:0.6px;
              text-transform:uppercase;color:var(--text-muted);font-weight:500;
              padding-top:16px;border-top:1px solid var(--border-subtle);margin-bottom:10px;">
    Your data choices
  </div>
  <div class="consent-body" style="margin-bottom:0;">
    Choose how your data is used. You can update these at any time.
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("")

        # ── Toggle rows ──────────────────────────────────────────────────────
        # Row 1 — locked (disabled=True keeps it non-interactive; opacity reset
        # in CSS cancels Streamlit's ~40% disabled fade)
        cl1, cl2 = st.columns([5, 1])
        with cl1:
            st.markdown("""
<div class="consent-toggle-label">Improve our service</div>
<div class="consent-toggle-desc">We use your data to improve our health checks and compare results against anonymised reference data.</div>
<div class="consent-toggle-locked" style="margin-top:4px;">Required — this cannot be turned off</div>
""", unsafe_allow_html=True)
        with cl2:
            st.toggle("Improve", value=True, disabled=True, key="toggle_improve", label_visibility="collapsed")

        # Row 2 — research (optional)
        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown("""
<div class="consent-toggle-label">Contribute to health research</div>
<div class="consent-toggle-desc">Your data can be used in anonymous, grouped form to identify health trends. You will never be personally identified.</div>
""", unsafe_allow_html=True)
        with c2:
            research = st.toggle("Research", value=st.session_state.consent_research, key="toggle_research", label_visibility="collapsed")

        st.markdown("<hr>", unsafe_allow_html=True)

        # Row 3 — insights (optional)
        c3, c4 = st.columns([5, 1])
        with c3:
            st.markdown("""
<div class="consent-toggle-label">Help build future health insights products</div>
<div class="consent-toggle-desc">Your anonymous data may be used to develop future paid health insight tools. Your identity will never be shared.</div>
""", unsafe_allow_html=True)
        with c4:
            insights = st.toggle("Insights", value=st.session_state.consent_insights, key="toggle_insights", label_visibility="collapsed")

        # ── Confirmations + footer ───────────────────────────────────────────
        st.markdown("""
<div style="margin:4px 40px 0;">
  <div style="font-family:'figtree',sans-serif;font-size:0.83rem;font-weight:500;
              color:var(--text-primary);padding-top:18px;
              border-top:1px solid var(--border-subtle);margin-bottom:8px;">
    By uploading your results, you confirm that:
  </div>
  <div class="consent-checklist">
    ☑ &nbsp;The data you provide may not be independently verified<br>
    ☑ &nbsp;Results and insights are for information only<br>
    ☑ &nbsp;You should speak to a qualified healthcare professional for medical advice
  </div>
  <div class="consent-footer">
    You're in control of your data — you can withdraw consent or request deletion at any time.
    Data choices can be updated via the settings link at the bottom of the page.
  </div>
</div>
""", unsafe_allow_html=True)

        (link_col,) = st.columns([1])
        with link_col:
            st.markdown('<span id="pn-link-consent-marker" hidden aria-hidden="true"></span>',
                        unsafe_allow_html=True)
            if st.button("Read our full Privacy Notice", key="open_pn_from_consent"):
                st.session_state.show_modal = "privacy_notice"
                st.rerun()

        st.markdown("")
        if st.button("I agree, continue to the app →", key="c1", use_container_width=True):
            st.session_state.consent_research = research
            st.session_state.consent_insights = insights
            st.session_state.consent_done = True
            st.rerun()


# Run consent flow until complete
if not st.session_state.consent_done:
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
    "if you have any medical concerns."
    "</div>",
    unsafe_allow_html=True
)

_dem_col1, _dem_col2 = st.columns([1, 1])
with _dem_col1:
    sex = st.selectbox(
        label="Biological sex",
        options=["Female", "Male"],
        index=None,
        placeholder="Select sex"
    )
with _dem_col2:
    _age_str = st.text_input(label="Age", placeholder="Enter your age")
    age = (
        int(_age_str)
        if _age_str and _age_str.strip().isdigit() and 1 <= int(_age_str) <= 120
        else None
    )

# ── Footer (fixed at bottom, always accessible before and after sex selection) ─
# The marker lives inside _fb1 so the stHorizontalBlock that :has(#footer-outer-marker)
# is the inner row itself — giving it position:fixed and width:100vw directly.
_fb1, _fb2, _fb3 = st.columns([1, 1, 1])
with _fb1:
    if st.button("Privacy Settings", key="open_ds_modal"):
        st.session_state.show_modal = "data_settings"
        st.rerun()
with _fb2:
    if st.button("Privacy Notice", key="open_pn_modal"):
        st.session_state.show_modal = "privacy_notice"
        st.rerun()
with _fb3:
    # Marker is inline here — same element container as the link, so all three
    # columns have exactly one element-container and align on the same baseline.
    st.markdown(
        '<span id="footer-outer-marker" hidden aria-hidden="true"></span>'
        '<a class="footer-mailto" href="mailto:admin@vitalflow-health.com'
        '?subject=Bug%20Report">Report a Bug</a>',
        unsafe_allow_html=True,
    )

# ── Modals (session-state driven) ─────────────────────────────────────────────
if st.session_state.show_modal == "privacy_notice":
    _show_privacy_notice_modal()
elif st.session_state.show_modal == "data_settings":
    _show_data_settings_modal()

if not sex or age is None:
    st.stop()

st.divider()

results = {}

@st.dialog("Where do I find my lab report?")
def lab_report_help_dialog():
    st.markdown(
        """
        <div style='font-family:figtree,sans-serif;line-height:1.7;'>

        <ol style='padding-left:1.2rem;margin-bottom:16px;'>
          <li style='margin-bottom:8px;'><strong>Check your email</strong> for a message from Vital Flow Health
          containing a link to view your documents on the portal.</li>
          <li style='margin-bottom:8px;'><strong>Open the link</strong> and enter your date of birth when prompted.</li>
          <li style='margin-bottom:8px;'><strong>Click "View test results"</strong> to open your report.</li>
          <li style='margin-bottom:8px;'><strong>Click the print button</strong> in the top right corner of the
          page, then save or download as a PDF.</li>
        </ol>

        <p style='font-size:0.82rem;color:var(--text-secondary);margin-top:12px;'>
        Once you have the PDF, drag it into the upload box to autofill your results.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


upload = False

# ── Two-column layout ──
col_input, col_results = st.columns([1, 1], gap="large")

with col_input:
    st.header("Enter your blood test results")
    st.markdown(
        "<p style='font-family:figtree,sans-serif;font-size:0.88rem;color:var(--text-secondary);"
        "line-height:1.65;margin:0 0 16px;'>"
        "Enter values only for the metrics you have results for. Make sure the units match those shown."
        "</p>",
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Vital Flow Health patient? Upload your lab report PDF to autofill.",
        type=["pdf"]
    )
    _lrh_col, _ = st.columns([1, 8])
    with _lrh_col:
        st.markdown('<span id="lab-report-help-marker" hidden aria-hidden="true"></span>', unsafe_allow_html=True)
        if st.button("Where do I find my lab report?", key="lab_report_help"):
            lab_report_help_dialog()
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

    st.divider()
    interpret_clicked_top = st.button("Interpret Results", key="interpret_top", use_container_width=True)

    sorted_metrics = dict(sorted(BLOOD_METRIC_DATA.items(), key=lambda x: x[1]['name'].lower()))

    name_to_key = {v['name']: k for k, v in sorted_metrics.items()}

    with st.container(key="metric_search"):
        selected_name = st.selectbox(
            "Search metrics",
            options=list(name_to_key.keys()),
            index=None,
            placeholder="Search metrics…",
            label_visibility="collapsed",
        )

    if selected_name:
        selected_key = name_to_key[selected_name]
        display_metrics = {selected_key: sorted_metrics[selected_key]}
    else:
        display_metrics = sorted_metrics

    input_blood_metrics(display_metrics, upload, results)

    # Collect values the user entered for metrics now hidden by the search filter
    for metric, meta in sorted_metrics.items():
        if metric in display_metrics or metric in results:
            continue
        value = st.session_state.manual_values.get(metric, 0.0)
        if value > 0:
            results[metric] = {**meta, "value": value}

    st.divider()
    interpret_clicked_bottom = st.button("Interpret Results", key="interpret_bottom", use_container_width=True)
    with st.container(key="clear_all_values"):
        st.button("Clear all values", key="clear_btn", on_click=_clear_all_values)

    interpret_clicked = interpret_clicked_top or interpret_clicked_bottom

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
            submit_results(results, sex, age)

with col_results:
    st.markdown('<span id="col-results-marker" hidden aria-hidden="true"></span>', unsafe_allow_html=True)
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
            placeholder="",
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

