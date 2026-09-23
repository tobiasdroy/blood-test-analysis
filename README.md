# Blood Test Interpreter

A Streamlit app that takes blood test results and explains them in plain language — what each marker means, whether your result is normal, and what you can do about it.

## Features

- **Manual entry** — enter values for individual metrics using dropdowns and number inputs
- **CSV upload** — bulk-import results with a `Metric` / `Result` CSV
- **PDF upload** — extract results directly from a blood test PDF report
- **Interpreted results** — each metric gets a plain-English explanation, a normal/high/low status, and personalised advice
- **Visual spectrum charts** — Plotly gauge charts show where your result sits relative to the reference range
- **PDF export** — download a formatted report of your results
- **Gender-specific ranges** — reference ranges adjust for biological sex where clinically relevant

## Panels covered

| Panel | Examples |
|---|---|
| Full Blood Count | Haemoglobin, WBC, Platelets |
| Kidney Function | Creatinine, eGFR, Urea |
| Liver Function | ALT, AST, Bilirubin, GGT |
| Heart Health | Cholesterol, LDL, HDL, Triglycerides |
| Diabetes Markers | HbA1c, Fasting Glucose |
| Iron Status | Ferritin, Serum Iron, Transferrin |
| Thyroid Function | TSH, Free T4, Free T3 |
| Vitamins | Vitamin D, B12, Folate |
| Bone Profile | Calcium, Phosphate, ALP |
| Cancer Markers | PSA, CA-125, CEA |
| Urine Analysis | Urine ACR, Urine PCR |
| Muscle Health | CK, Creatinine |
| Consultation Results | Blood Pressure, BMI, Peak Flow |

## Setup

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Requires Python 3.10+.

## CSV format

Upload a CSV with two columns:

```
Metric,Result
haemoglobin,14.2
hba1c,5.4
vitamin_d,62
```

`Metric` values must match keys in `BLOOD_METRIC_DATA` (see `interpreter.py`).

## Architecture

```
interpreter.py      — metric definitions and interpret_result() logic
streamlit_app.py    — UI layer (input, rendering, PDF export)
pdf_export.py       — ReportLab PDF generation
salesforce_client.py — results submission integration
static/             — font files for custom typography
.streamlit/         — Streamlit theme config
```

## Stack

- [Streamlit](https://streamlit.io) — UI framework
- [Plotly](https://plotly.com/python/) — spectrum charts
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF text extraction
- [ReportLab](https://www.reportlab.com) — PDF report generation
- [pandas](https://pandas.pydata.org) — CSV handling
