# streamlit_app.py

import streamlit as st
from interpreter import interpret_result, BLOOD_METRIC_DATA, FULL_BLOOD_COUNT, KIDNEY_FUNCTION, HEART_HEALTH, DIABETES_MARKERS, IRON_STATUS, BONE_PROFILE, MUSCLE_HEALTH, LIVER_FUNCTION, URINE_ANALYSIS, THYROID_FUNCTION, CANCER_MARKERS, VITAMINS
import pandas as pd


st.set_page_config(
    page_title="Blood Test Interpreter", 
    layout="wide"
)

def input_blood_metrics(DATA):
    for metric, meta in DATA.items():
        col1, col2 = st.columns([2, 1])

        with col1:
            value = st.number_input(
                label=meta['name'],
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key=metric
            )
        with col2:
            st.markdown(f"**{meta['unit']}**")

        if value > 0:
            results[metric] = {
                **meta,
                "value": value
            }


st.title("Blood Test Interpreter")

st.info("Disclaimer: This tool is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Please consult a healthcare professional if you have any medical concerns.")

sex = st.selectbox(
    label="Select your biological sex:",
    options=["Female", "Male"],
    index=None,
    placeholder="Select sex"
)

results = {}

st.header("Enter your blood test results")
st.write("Please only input results for the metrics you have tested, making sure the units match those specified.")

with st.expander("Full Blood Count"):
    input_blood_metrics(FULL_BLOOD_COUNT)
with st.expander("Kidney Function"):
    input_blood_metrics(KIDNEY_FUNCTION)
with st.expander("Heart Health"):
    input_blood_metrics(HEART_HEALTH)
with st.expander("Diabetes Markers"):
    input_blood_metrics(DIABETES_MARKERS)
with st.expander("Iron Status"):
    input_blood_metrics(IRON_STATUS)
with st.expander("Bone Profile"):
    input_blood_metrics(BONE_PROFILE)
with st.expander("Muscle Health"):
    input_blood_metrics(MUSCLE_HEALTH)
with st.expander("Liver Function"):
    input_blood_metrics(LIVER_FUNCTION)
with st.expander("Urine Analysis"):
    input_blood_metrics(URINE_ANALYSIS)
with st.expander("Thyroid Function"):
    input_blood_metrics(THYROID_FUNCTION)
with st.expander("Cancer Markers"):
    input_blood_metrics(CANCER_MARKERS)
with st.expander("Vitamins"):
    input_blood_metrics(VITAMINS)

if st.button("Interpret Results"):
    if not results:
        st.warning("Please enter at least one blood test result.")
    else:
        st.divider()
        st.header("Interpretation")
        for metric, data in results.items():
            interpretation = interpret_result(metric, data, sex)
            st.subheader(data['name'])
            st.write(f"**Result:** {data['value']} {data['unit']}")
            st.write(interpretation)