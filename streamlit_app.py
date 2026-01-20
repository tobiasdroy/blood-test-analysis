# streamlit_app.py

import streamlit as st
from interpreter import interpret_result, BLOOD_METRIC_DATA
import pandas as pd


st.set_page_config(
    page_title="Blood Test Interpreter", 
    layout="wide"
)


st.title("Blood Test Interpreter")

st.info("Disclaimer: This tool is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Please consult a healthcare professional if you have any medical concerns.")

results = {}

st.subheader("Enter your blood test results")
st.write("Please only input results for the metrics you have tested, making sure the units match those specified.")

for metric, meta in BLOOD_METRIC_DATA.items():
    col1, col2 = st.columns([2, 1])

    with col1:
        value = st.number_input(
            label=metric,
            min_value=0.0,
            step=0.01,
            format="%.2f",
            key=metric
        )
    with col2:
        st.markdown(f"**{meta['unit']}**")

    if value > 0:
        results[metric] = {
            "value": value,
            "unit": meta["unit"]
        }

if st.button("Interpret Results"):
    if not results:
        st.warning("Please enter at least one blood test result.")
    else:
        st.divider()
        st.header("Interpretation")

        for metric, data in results.items():
            interpretation = interpret_result(
                metric,
                data["value"],
                data["unit"]
            )

            st.subheader(metric)
            st.write(f"**Result:** {data['value']} {data['unit']}")
            st.write(interpretation)