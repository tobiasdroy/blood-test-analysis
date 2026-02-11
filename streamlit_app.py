# streamlit_app.py

import streamlit as st
from interpreter import interpret_result, BLOOD_METRIC_DATA, FULL_BLOOD_COUNT, KIDNEY_FUNCTION, HEART_HEALTH, DIABETES_MARKERS, IRON_STATUS, BONE_PROFILE, MUSCLE_HEALTH, LIVER_FUNCTION, URINE_ANALYSIS, THYROID_FUNCTION, CANCER_MARKERS, VITAMINS
import pandas as pd
from PIL import Image


st.set_page_config(
    page_title="Blood Test Interpreter", 
    layout="wide"
)

warning_box_style = """
<style>
    .warning-box {
        background-color: #FDE9D6; 
        color: #F88D2A;             
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
</style>
"""

abnormal_box_style = """
<style>
    .abnormal-box {
        background-color: #F8D7DA; 
        color: #721C24;             
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
</style>"""

st.markdown(warning_box_style, unsafe_allow_html=True)
st.markdown(abnormal_box_style, unsafe_allow_html=True)

def input_blood_metrics(DATA, upload, results):
    for metric, meta in DATA.items():
        col1, col2, col3 = st.columns([2, 1, 3])

        with col1:
            st.markdown(
                f"""
                <div style='
                    display: flex;
                    align-items: center;
                    min-height: 2.5rem;
                    width: 100%;
                    line-height: 1.2;
                    justify-content: flex-start;
                    text-align: left;
                '>
                    {meta['name']}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            if upload and metric in results:
                default_val = str(results[metric]['value'])
                raw_value = st.text_input(
                    label=meta['name'],
                    value = default_val,
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
                    st.caption(f"Please enter a valid number.")
            
        with col3:
            st.markdown(
                f"""
                <div style='
                    display: flex;
                    align-items: center;
                    min-height: 2.5rem;
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

image = Image.open('assets/logo.png')
st.image(image, width=500)
st.title("Blood Test Interpreter")

st.markdown(
    "<div class='warning-box'>Disclaimer: This tool is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Please consult a healthcare professional if you have any medical concerns.</div>",
    unsafe_allow_html=True
)

sex = st.selectbox(
    label="Please select your biological sex:",
    options=["Female", "Male"],
    index=None,
    placeholder="Select sex"
)

if not sex:
    st.stop()

results = {}

upload = False

st.header("Enter your blood test results")
st.write("Please only input results for the metrics you have tested, making sure the units match those specified.")

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

with st.expander("Full Blood Count", expanded=True):
    input_blood_metrics(FULL_BLOOD_COUNT, upload, results)
with st.expander("Kidney Function"):
    input_blood_metrics(KIDNEY_FUNCTION, upload, results)
with st.expander("Heart Health"):
    input_blood_metrics(HEART_HEALTH, upload, results)
with st.expander("Diabetes Markers"):
    input_blood_metrics(DIABETES_MARKERS, upload, results)
with st.expander("Iron Status"):
    input_blood_metrics(IRON_STATUS, upload, results)
with st.expander("Bone Profile"):
    input_blood_metrics(BONE_PROFILE, upload, results)
with st.expander("Muscle Health"):
    input_blood_metrics(MUSCLE_HEALTH, upload, results)
with st.expander("Liver Function"):
    input_blood_metrics(LIVER_FUNCTION, upload, results)
with st.expander("Urine Analysis"):
    input_blood_metrics(URINE_ANALYSIS, upload, results)
with st.expander("Thyroid Function"):
    input_blood_metrics(THYROID_FUNCTION, upload, results)
with st.expander("Cancer Markers"):
    input_blood_metrics(CANCER_MARKERS, upload, results)
with st.expander("Vitamins"):
    input_blood_metrics(VITAMINS, upload, results)
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
        '''
        st.subheader(data['name'])
        st.write(f"**Result:** {data['value']} {data['unit']}")
        st.write(status)
        st.write(explanation)
        st.write(advice)
        '''
        st.markdown(
            f"""
            <div class='abnormal-box'>
                <h3>{data['name']}</h3>
                <p><strong>Result:</strong> {data['value']} {data['unit']}</p>
                <p><strong>Status:</strong> {status}</p>
                <p><strong>Explanation:</strong> {explanation}</p>
                <p><strong>Advice:</strong> {advice}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.subheader("Normal Results")
    for metric, (data, status, explanation, advice) in normal_results.items():
        st.subheader(data['name'])
        st.write(f"**Result:** {data['value']} {data['unit']}")
        st.write(status)
        st.write(explanation)