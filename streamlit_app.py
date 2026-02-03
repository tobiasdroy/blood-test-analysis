# streamlit_app.py

import streamlit as st
from interpreter import interpret_result, BLOOD_METRIC_DATA, FULL_BLOOD_COUNT, KIDNEY_FUNCTION, HEART_HEALTH, DIABETES_MARKERS, IRON_STATUS, BONE_PROFILE, MUSCLE_HEALTH, LIVER_FUNCTION, URINE_ANALYSIS, THYROID_FUNCTION, CANCER_MARKERS, VITAMINS
import pandas as pd


st.set_page_config(
    page_title="Blood Test Interpreter", 
    layout="wide"
)

def input_blood_metrics(DATA, upload):
    for metric, meta in DATA.items():
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.markdown(
                f"""
                <div style='
                    display: flex;
                    align-items: center;
                    height: 3rem;
                    justify-content: flex-end;
                '>
                    {meta['name']}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            if upload:
                value = st.number_input(
                    label=meta['name'],
                    value = results[metric]['value'] if metric in results else 0.0,
                    format="%.2f",
                    key=f"{metric}_upload",
                    label_visibility="collapsed"
                )
            else:   
                value = st.number_input(
                    label=meta['name'],
                    format="%.2f",
                    key=metric,
                    label_visibility="collapsed"
                )
        with col3:
            st.markdown(
                f"""
                <div style='
                    display: flex;
                    align-items: center;
                    height: 3rem;
                '>
                    {meta['unit']}
                </div>
                """,
                unsafe_allow_html=True
            )

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

upload = False
uploaded_file = st.file_uploader("Or upload a CSV file with your blood test results", type=["csv"]) 
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    upload = True

    for _, row in df.iterrows():
        metric = row['Metric']
        value = row['Result']
        if metric in BLOOD_METRIC_DATA:
            meta = BLOOD_METRIC_DATA[metric]
            results[metric] = {
                **meta,
                "value": value
            }



st.header("Enter your blood test results")
st.write("Please only input results for the metrics you have tested, making sure the units match those specified.")

with st.expander("Full Blood Count"):
    input_blood_metrics(FULL_BLOOD_COUNT, upload)
with st.expander("Kidney Function"):
    input_blood_metrics(KIDNEY_FUNCTION, upload)
with st.expander("Heart Health"):
    input_blood_metrics(HEART_HEALTH, upload)
with st.expander("Diabetes Markers"):
    input_blood_metrics(DIABETES_MARKERS, upload)
with st.expander("Iron Status"):
    input_blood_metrics(IRON_STATUS, upload)
with st.expander("Bone Profile"):
    input_blood_metrics(BONE_PROFILE, upload)
with st.expander("Muscle Health"):
    input_blood_metrics(MUSCLE_HEALTH, upload)
with st.expander("Liver Function"):
    input_blood_metrics(LIVER_FUNCTION, upload)
with st.expander("Urine Analysis"):
    input_blood_metrics(URINE_ANALYSIS, upload)
with st.expander("Thyroid Function"):
    input_blood_metrics(THYROID_FUNCTION, upload)
with st.expander("Cancer Markers"):
    input_blood_metrics(CANCER_MARKERS, upload)
with st.expander("Vitamins"):
    input_blood_metrics(VITAMINS, upload)

if st.button("Interpret Results"):
    normal_results = {}
    abnormal_results = {}
    if not results:
        st.warning("Please enter at least one blood test result.")
    else:
        st.divider()
        st.header("Interpretation")
        for metric, data in results.items():
            status, explanation, advice = interpret_result(metric, data, sex)
            if status == "Normal":
                normal_results[metric] = (data, status, explanation, advice)
            else:       
                abnormal_results[metric] = (data, status, explanation, advice)

    st.subheader("Abnormal Results")
    for metric, (data, status, explanation, advice) in abnormal_results.items():
        st.subheader(data['name'])
        st.write(f"**Result:** {data['value']} {data['unit']}")
        st.write(status)
        st.write(explanation)
        st.write(advice)
    st.subheader("Normal Results")
    for metric, (data, status, explanation, advice) in normal_results.items():
        st.subheader(data['name'])
        st.write(f"**Result:** {data['value']} {data['unit']}")
        st.write(status)
        st.write(explanation)