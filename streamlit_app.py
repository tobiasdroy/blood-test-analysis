# streamlit_app.py

import streamlit as st
from interpreter import interpret_result, BLOOD_METRIC_DATA, FULL_BLOOD_COUNT, KIDNEY_FUNCTION, HEART_HEALTH, DIABETES_MARKERS, IRON_STATUS, BONE_PROFILE, MUSCLE_HEALTH, LIVER_FUNCTION, URINE_ANALYSIS, THYROID_FUNCTION, CANCER_MARKERS, VITAMINS
import pandas as pd
from PIL import Image
import plotly.graph_objects as go


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
st.markdown("""
<style>
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
        margin-left: 5px;
        color: #155724;
        font-weight: regular;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        background-color: #FFFFFF;
        color: #54565A;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        top: 50%;
        left: 105%;
        margin-left: 0px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 14px;
        font-weight: normal;
        max-width: 70vw;
        width: max-content;
        min-width: 300px;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

def draw_spectrum(data, gender):
    value = data['value']
    data_range = data['range']
    unit = data['unit']
    metric_name = data['name']
    gender_specific = data['gender_specific']
    metric_type = data.get('type', 'hilo')

    # 1. Determine the reference limits based on gender
    if gender_specific:
        if gender == "Female":
            low, high = data_range[0:2]
        else: # Male
            low, high = data_range[2:4]
    else:
        low, high = data_range

    # 2. Calculate dynamic chart bounds (padding)
    # We want to make sure the "Normal" green zone is always visible
    span = high - low if high > low else low
    if span == 0: span = value # Fallback for 'presence' types
    
    chart_min = min(value, low) - (span * 0.2)
    chart_max = max(value, high) + (span * 0.2)
    
    # Adjust bounds for specific types
    if metric_type in ['upper_bound', 'presence']:
        chart_min = 0
    
    fig = go.Figure()

    # 3. Create the background "Spectrum" using shapes
    # This prevents the 'staircase' effect caused by go.Bar
    shapes = []
    
    # Normal Zone (Green) - Defined first so it's the baseline
    shapes.append(dict(
        type="rect", x0=low, x1=high, y0=0, y1=1,
        fillcolor="#D4EDDA", line_width=0, layer="below"
    ))

    # Low Zone (Red) - Only if it's a hilo type
    if chart_min < low:
        shapes.append(dict(
            type="rect", x0=chart_min, x1=low, y0=0, y1=1,
            fillcolor="#F8D7DA", line_width=0, layer="below"
        ))

    # High Zone (Red)
    if chart_max > high:
        shapes.append(dict(
            type="rect", x0=high, x1=chart_max, y0=0, y1=1,
            fillcolor="#F8D7DA", line_width=0, layer="below"
        ))

    # 4. Add the user's result marker (Diamond)
    fig.add_trace(go.Scatter(
        x=[value], y=[0.5], # 0.5 centers it vertically in the box
        mode='markers+text',
        marker=dict(color='black', size=15, symbol='diamond', line=dict(width=2, color="white")),
        text=[f"<b>{value}</b>"],
        textposition="top center",
        name="Your Result",
        hovertemplate=f"Result: {value} {unit}<extra></extra>"
    ))

    # 5. Clean up the Layout
    fig.update_layout(
        shapes=shapes,
        height=130,
        margin=dict(l=20, r=20, t=40, b=40),
        xaxis=dict(
            showgrid=False, 
            zeroline=False, 
            range=[chart_min, chart_max],
            tickvals=[low, high],
            ticktext=[f"Low: {low}", f"High: {high}"],
            fixedrange=True
        ),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0, 1], fixedrange=True),
        plot_bgcolor='white'
    )

    return fig

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
                    <div class="tooltip">ⓘ
                        <span class="tooltiptext">{meta['explanation']}</span>
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
            with st.container():
                st.markdown(f"<div class='abnormal-box'><h6>{status} {data['name']}</h6><p>{explanation}</p></div>", unsafe_allow_html=True)
        
                # Display the chart
                fig = draw_spectrum(data, sex)
                st.plotly_chart(fig, use_container_width=True)
                
                st.write(f"**Advice:** {advice}")
    st.subheader("Abnormal Results")
    for metric, (data, status, explanation, advice) in abnormal_results.items():
        st.markdown(
            f"""
            <div class='abnormal-box'>
                <h6>{status} {data['name']}</h6>
                <p>{explanation}</p>
                <p><strong>Result:</strong> {data['value']} {data['unit']}</p>
                <p><strong>Advice:</strong> {advice}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.subheader("Normal Results")
    for metric, (data, status, explanation, advice) in normal_results.items():
        st.markdown(f"""
        <h6 style="margin: 0;">
            {data['name']}
            <div class="tooltip">ⓘ
                <span class="tooltiptext">{explanation}</span>
            </div>
        </h6>
        <p><strong>Result:</strong> {data['value']} {data['unit']}</p>
""", unsafe_allow_html=True)
