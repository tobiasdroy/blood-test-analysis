# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the app
streamlit run streamlit_app.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

This is a single-page Streamlit app with two Python files:

- **`interpreter.py`** — Pure data and logic layer. Contains all metric definitions as dictionaries (grouped by panel: `FULL_BLOOD_COUNT`, `KIDNEY_FUNCTION`, etc.) and the `interpret_result(metric, data, gender)` function which returns `(status, explanation, advice)`. All dictionaries are merged into `BLOOD_METRIC_DATA` at module level.

- **`streamlit_app.py`** — UI layer. Imports all metric group dicts and the interpreter function. Handles user input (manual or CSV upload), calls `interpret_result`, and renders results with Plotly spectrum charts embedded as iframes.

### Metric data structure

Each metric entry in `interpreter.py` follows this shape:
```python
"metric_key": {
    "name": str,
    "type": "hilo" | "upper_bound" | "lower_bound" | "presence",
    "gender_specific": bool,
    "range": (low, high) or (female_low, female_high, male_low, male_high),
    "unit": str,
    "explanation": str,
    "advice_high": str,
    "advice_low": str,
}
```

Gender-specific metrics use a 4-tuple range: `(female_low, female_high, male_low, male_high)`.

### CSV upload format

Uploaded CSVs must have columns `Metric` and `Result`, where `Metric` values match keys in `BLOOD_METRIC_DATA`.

### Theming

`.streamlit/config.toml` configures the dark theme with custom Poppins (headings) and Figtree (body) fonts served as static files from `static/`.
