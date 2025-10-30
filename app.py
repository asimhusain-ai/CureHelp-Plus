import os
import uuid
import joblib
import numpy as np
import streamlit as st
from fpdf import FPDF
import plotly.graph_objects as go
from makepdf import generate_pdf_report
from consultant import render_consultant_tab
from helper import fetch_gemini_recommendations
from chatbot import render_chatbot_tab
from profile_manager import profile_manager 
from datetime import datetime 


st.set_page_config(page_title="CureHelp+ ", layout="wide")

# Cache CSS as a constant to avoid re-rendering (OPTIMIZATION)
CUSTOM_CSS = """
<style>

    .main-chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 0;
    }
    .user-message {
        background: #D3D3D3;
        color: #2d3748;
        padding: 12px 16px;
        border-radius: 18px 18px 5px 18px;
        margin: 8px 0;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        font-size: 14px;
        line-height: 1.4;
    }
    .bot-message {
        background: #D3D3D3;
        color: #2d3748;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 5px;
        margin: 8px 0;
        max-width: 75%;
        margin-right: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        font-size: 14px;
        line-height: 1.4;
    }
    .message-header {
        font-weight: 600;
        margin-bottom: 6px;
        font-size: 14px;
        opacity: 0.9;
    }
    .symptom-list {
        margin: -10px 0;
        padding-left: 30px;
        font-size: 15px;
        padding-bottom: 40px;
    }
    
    .precaution-list {
        margin: -10px 0;
        padding-left: 30px;
        font-size: 14px;
        padding-bottom: 40px;
    }
    
    
    .symptom-item, .precaution-item {
        margin: 3px 0;
        padding: 2px 0;
    }
    .confidence-badge {
        background: #48bb78;
        color: white;
        padding: 4px 10px;
        border-radius: 10px;
        font-size: 11px;
        margin-left: 8px;
        font-weight: 600;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
        padding: 12px 18px;
        border: 2px solid #e2e8f0;
        font-size: 14px;
        background: #f8fafc;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
    }
    .chat-header {
        text-align: center;
        padding: 15px 0;
        background: #3b82f6;
        color: white;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .chat-input-container {
        background: white;
        padding: 12px;
        border-radius: 20px;
        box-shadow: 0 -2px 15px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-top: 20px;
    }
    .chat-history {
        margin-bottom: 20px;
        max-height: 60vh;
        overflow-y: auto;
        padding: 10px;
    }
    .stButton > button {
        border-radius: 20px;
        padding: 10px 24px;
        font-size: 14px;
        font-weight: 600;
        background: #3b82f6;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        background: #3b82f6;
    }
    .section-header {
        font-weight: 600;
        color: #2d3748;
        margin: 12px 0 6px 0;
        font-size: 14px;
    }
    /* Scrollbar styling */
    .chat-history::-webkit-scrollbar {
        width: 6px;
    }
    .chat-history::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    .chat-history::-webkit-scrollbar-thumb {
        background: #cbd5e0;
        border-radius: 3px;
    }
    .chat-history::-webkit-scrollbar-thumb:hover {
        background: #a0aec0;
    }
    
    /* Primary button styling for all blue buttons */
    .stButton > button[kind="primary"] {
        background: #3b82f6;
        color: white;
        border: none;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #3b82f6;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Secondary button styling */
    .stButton > button[kind="secondary"] {
        background: #3b82f6;
        color: white;
        border: none;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #4b5563;
        transform: translateY(-1px);
    }
</style>
"""

# Initialize all session state 
def initialize_session_state():
    """Initialize all session state variables - Optimized to check once"""
    # Check if already initialized to avoid redundant operations (OPTIMIZATION)
    if "initialized" not in st.session_state:
        st.session_state.page = "landing"
        st.session_state.predictions = {}
        st.session_state.current_profile = None
        st.session_state.current_profile_id = None
        st.session_state.user_profiles = []
        st.session_state.initialized = True
        profile_manager.load_profiles()


initialize_session_state()
    
# Apply CSS once (OPTIMIZATION)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Navigation Functions with Auto-save
def go_to_patient_details():
    """Navigate to patient details with auto-save"""
    profile_manager.auto_save_profile()
    st.session_state.page = "patient_details"

def go_to_input():
    """Navigate to input page with auto-save"""
    profile_manager.auto_save_profile()
    st.session_state.page = "input"

def go_to_landing():
    """Navigate to landing page with auto-save"""
    profile_manager.auto_save_profile()
    st.session_state.page = "landing"

# Load Models
@st.cache_resource
def load_models():
    """Loads all machine learning models and scalers from 'models/' folder."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, "models")

    return {
        # Diabetes
        "diabetes_model": joblib.load(os.path.join(MODEL_DIR, "diabetes_model.pkl")),
        "diabetes_scaler": joblib.load(os.path.join(MODEL_DIR, "diabetes_scaler.pkl")),

        # Heart Disease
        "heart_model": joblib.load(os.path.join(MODEL_DIR, "heart_model.pkl")),
        "heart_scaler": joblib.load(os.path.join(MODEL_DIR, "heart_scaler.pkl")),

        # Fever
        "fever_severity_model": joblib.load(os.path.join(MODEL_DIR, "fever_severity_model.pkl")),
        "fever_risk_model": joblib.load(os.path.join(MODEL_DIR, "fever_risk_model.pkl")),
        "fever_scaler": joblib.load(os.path.join(MODEL_DIR, "fever_scaler.pkl")),
        "fever_target_le": joblib.load(os.path.join(MODEL_DIR, "fever_target_encoder.pkl")),
        "fever_le_dict": joblib.load(os.path.join(MODEL_DIR, "fever_label_encoders.pkl")),

        # Anemia
        "anemia_risk_model": joblib.load(os.path.join(MODEL_DIR, "anemia_risk_model.pkl")),
        "anemia_type_model": joblib.load(os.path.join(MODEL_DIR, "anemia_type_model.pkl")),
        "anemia_scaler": joblib.load(os.path.join(MODEL_DIR, "feature_scaler.pkl")),
        "anemia_label_encoder": joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl")),
    }

# Preload models at app start
models = load_models()

# Feature Lists & Normal Values
fever_numeric_cols = ["Temperature (°C)", "Age", "BMI", "Humidity (%)", "Air Quality Index", "Heart Rate"]
fever_categorical_cols = [
    "Gender", "Headache", "Body_Ache", "Fatigue", "Chronic_Conditions",
    "Allergies", "Smoking_History", "Alcohol_Consumption", "Physical_Activity",
    "Diet_Type", "Blood_Pressure", "Previous_Medication"
]

# Dictionaries for "Normal" values for the feature comparison chart
diabetes_normals = {
    "Pregnancies": 3, "Glucose": 100, "Blood Pressure": 120, "Skin Thickness": 20,
    "Insulin": 80, "BMI": 22.0, "Diabetes Pedigree Function": 0.4, "Age": 40
}

heart_normals = {
    "Age": 50, "Sex": 1, "Chest Pain Type": 4, "Resting BP": 120, "Cholesterol": 200,
    "Fasting BS > 120?": 0, "Resting ECG": 0, "Max Heart Rate": 150, "Exercise Angina": 0,
    "ST Depression": 0.0, "Slope of ST": 1, "Major Vessels (ca)": 0, "Thal": 3
}

fever_normals = {
    "Temperature (°C)": 37.0, "Age": 40, "BMI": 22.0, "Humidity (%)": 50,
    "Air Quality Index": 50, "Heart Rate": 75
}

# ADVANCED VISUALIZATION
def show_risk_assessment_v2(title, value, user_inputs, normal_ranges, extra_text=None, suffix=None):
    """
    Displays a modern horizontal layout with a feature comparison chart, a risk meter,
    and Gemini-based recommendations (Prevention + Medicine).
    """
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f"### {title} Risk Assessment")
    st.markdown("<br>", unsafe_allow_html=True)
    
    left_col, center_col, right_col = st.columns([1, 6, 1]) 

    if suffix is None:
        suffix = str(uuid.uuid4())

    with left_col:
        st.empty()  

    with center_col:
        graph_col, gauge_col = st.columns([3, 4]) 
        
        with graph_col:
            numeric_user_inputs = {k: v for k, v in user_inputs.items() if isinstance(v, (int, float))}
            common_keys = list(set(numeric_user_inputs.keys()) & set(normal_ranges.keys()))
            
            user_values = [numeric_user_inputs[k] for k in common_keys]
            normal_values = [normal_ranges[k] for k in common_keys]

            fig_bar = go.Figure(data=[
                go.Bar(name='Your Value', x=common_keys, y=user_values, marker_color='orange'),
                go.Bar(name='Normal Range', x=common_keys, y=normal_values, marker_color='gray')
            ])
            fig_bar.update_layout(
                barmode='group',
                title_text="Your Inputs  vs  Normal Values",
                xaxis_title="Health Metrics",
                yaxis_title="Value",
                legend_title="Legend",
                height=350,
                margin=dict(t=50, b=10, l=10, r=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig_bar, use_container_width=True, key=f"{title}_bar_{suffix}")
        
        with gauge_col:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                number={'font': {'size': 80, 'color': '#333'}},
                title={'text': "Predicted Risk", 'font': {'size': 24}},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
                    'bar': {'thickness': 0},
                    'steps': [
                        {'range': [0, 40], 'color': 'green'},
                        {'range': [40, 60], 'color': 'yellowgreen'},
                        {'range': [60, 80], 'color': 'orange'},
                        {'range': [80, 100], 'color': 'red'}
                    ],
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=300,
                margin=dict(l=10, r=10, t=50, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True, key=f"{title}_gauge_{suffix}")

            if extra_text:
                st.markdown(
                    f"<h4 style='text-align:center; color:#333; margin-top: 10px;'>Predicted Severity: {extra_text}</h4>",
                    unsafe_allow_html=True,
                )

    with right_col:
        st.empty() 

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("## Clinical Guidance")
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.spinner("Fetching AI-powered prevention & medicine suggestions..."):
        data = fetch_gemini_recommendations(title, value)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Risk Reduction Protocols")
            st.markdown("<div style='margin-left: 20px;'>", unsafe_allow_html=True)
            for item in data.get("prevention_measures", []):
                st.markdown(f"• {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("### Clinical Interventions")
            st.markdown("<div style='margin-left: 20px;'>", unsafe_allow_html=True)
            for item in data.get("medicine_suggestions", []):
                st.markdown(f"• {item}")
            st.markdown("</div>", unsafe_allow_html=True)

# Landing Page
def render_landing_page():
    st.markdown(
        """
        <h1 style='text-align:center;'>
        <span style="font-size:90px;">CureHelp<span style="color:red; font-weight:bold; font-size:120px;">+</span></span> 
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.header("Your Personal Health Risk Analyzer")
    st.markdown("---")
    st.markdown(
        """
    CureHelp provides predictive insights into potential health risks based on your inputs. 
    Our application leverages machine learning models to analyze your health data for:
    - **Diabetes Risk**
    - **Heart Disease Risk**
    - **Fever Risk + Severity**
    - **Anemia Risk**
    
    """
    )
    st.markdown("   ")
    st.markdown("   ")
    st.markdown("   ")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.button("Get Started", on_click=go_to_patient_details, use_container_width=True)
        
def render_patient_details_page():
    """Render the patient details form"""
    profile_manager.render_patient_details_page()
    
# Helper function
def create_input_row(inputs_config, start_index):
    """Creates a row with exactly 6 input boxes"""
    cols = st.columns(6)
    for i in range(6):
        if start_index + i < len(inputs_config):
            input_config = inputs_config[start_index + i]
            with cols[i]:
                if input_config["type"] == "selectbox":
                    st.selectbox(
                        input_config["label"],
                        options=input_config["options"],
                        key=input_config["key"],
                        index=input_config.get("index", 0)
                    )
                elif input_config["type"] == "number_input":
                    st.number_input(
                        input_config["label"],
                        min_value=input_config["min"],
                        max_value=input_config["max"],
                        value=input_config["value"],
                        key=input_config["key"]
                    )


# Input Page with Tabs 
def render_input_page():
    
    
    
    if st.session_state.current_profile:
        profile = st.session_state.current_profile
        st.info(f"**Current Patient:** ㅤ {profile['name']} ㅤ | ㅤ Age: {profile['age']} ㅤ| ㅤ Gender: {profile['gender']}")
    
    tabs = st.tabs(["Diabetesㅤ", "Heart Diseaseㅤ", "Feverㅤ", "Anemiaㅤ", "Reportㅤ", "Assistantㅤ", "Profilesㅤ", "Consultants"])

    # ------------------ Diabetes Tab ------------------
    with tabs[0]:
        st.markdown("<h3 style='margin-bottom: 20px;'>Enter Your Health Metrics</h3>", 
                   unsafe_allow_html=True)
        user_inputs = {}

        diabetes_inputs = [
            {"type": "selectbox", "label": "Gender", "options": ["Female", "Male"], "key": "diabetes_gender"},
            {"type": "number_input", "label": "Age", "min": 1, "max": 120, "value": 40, "key": "diabetes_age"},
            {"type": "number_input", "label": "BMI", "min": 10.0, "max": 70.0, "value": 25.0, "key": "diabetes_bmi"},
            {"type": "number_input", "label": "Glucose", "min": 0.0, "max": 300.0, "value": 100.0, "key": "diabetes_glucose"},
            {"type": "number_input", "label": "Blood Pressure", "min": 50.0, "max": 200.0, "value": 120.0, "key": "diabetes_bp"},
            {"type": "number_input", "label": "Pregnancies", "min": 0, "max": 20, "value": 0, "key": "diabetes_pregnancies"},
            {"type": "number_input", "label": "Skin Thickness", "min": 0, "max": 100, "value": 20, "key": "diabetes_skin"},
            {"type": "number_input", "label": "Insulin", "min": 0, "max": 900, "value": 79, "key": "diabetes_insulin"},
            {"type": "number_input", "label": "Diabetes Pedigree Function", "min": 0.0, "max": 5.0, "value": 0.5, "key": "diabetes_dpf"},
        ]

        for i in range(0, len(diabetes_inputs), 6):
            create_input_row(diabetes_inputs, i)
        
        # Store inputs
        gender = st.session_state.diabetes_gender
        user_inputs["Age"] = st.session_state.diabetes_age
        user_inputs["BMI"] = st.session_state.diabetes_bmi
        user_inputs["Glucose"] = st.session_state.diabetes_glucose
        user_inputs["Blood Pressure"] = st.session_state.diabetes_bp
        user_inputs["Pregnancies"] = st.session_state.diabetes_pregnancies
        user_inputs["Skin Thickness"] = st.session_state.diabetes_skin
        user_inputs["Insulin"] = st.session_state.diabetes_insulin
        user_inputs["Diabetes Pedigree Function"] = st.session_state.diabetes_dpf

        # Prediction Button 
        st.markdown("<br>", unsafe_allow_html=True)
        colA, colB, colC = st.columns([2, 1, 2])
        with colB:
            if st.button("Predict Diabetes Risk", 
                        type="primary", 
                        key="diabetes_btn"):
                preg_val = user_inputs["Pregnancies"] if gender == "Female" else 0
                arr = np.array([[preg_val, user_inputs["Glucose"], user_inputs["Blood Pressure"], user_inputs["Skin Thickness"], user_inputs["Insulin"], user_inputs["BMI"], user_inputs["Diabetes Pedigree Function"], user_inputs["Age"]]], dtype=np.float64)
                arr_scaled = models["diabetes_scaler"].transform(arr)
                prob = models["diabetes_model"].predict_proba(arr_scaled)[0][1] * 100
                st.session_state.predictions["Diabetes"] = {"prob": prob, "inputs": user_inputs}
                
                profile_manager.auto_save_profile()
                st.rerun()
        
        if "Diabetes" in st.session_state.predictions:
            data = st.session_state.predictions["Diabetes"]
            show_risk_assessment_v2("Diabetes", data["prob"], data["inputs"], diabetes_normals)

    # ------------------ Heart Disease Tab ------------------
    with tabs[1]:
        st.markdown("<h3 style='margin-bottom: 20px;'>Enter Your Health Metrics</h3>", 
                   unsafe_allow_html=True)
        user_inputs_heart = {}
        
        # Define all heart disease inputs in order
        heart_inputs = [
            {"type": "selectbox", "label": "Gender", "options": ["Female", "Male"], "key": "heart_gender"},
            {"type": "number_input", "label": "Age", "min": 1, "max": 120, "value": 40, "key": "heart_age"},
            {"type": "number_input", "label": "Resting BP", "min": 50.0, "max": 250.0, "value": 130.0, "key": "heart_trestbps"},
            {"type": "number_input", "label": "Cholesterol", "min": 100.0, "max": 600.0, "value": 220.0, "key": "heart_chol"},
            {"type": "selectbox", "label": "Chest Pain Type", "options": ["1 - typical angina", "2 - atypical angina", "3 - non-anginal pain", "4 - asymptomatic"], "key": "heart_cp"},
            {"type": "selectbox", "label": "Fasting BS > 120", "options": ["No", "Yes"], "key": "heart_fbs"},
            {"type": "selectbox", "label": "Resting ECG", "options": ["0 - normal", "1 - ST-T abnormality", "2 - LV hypertrophy"], "key": "heart_restecg"},
            {"type": "number_input", "label": "Max Heart Rate", "min": 60.0, "max": 250.0, "value": 150.0, "key": "heart_thalach"},
            {"type": "selectbox", "label": "Exercise Angina", "options": ["No", "Yes"], "key": "heart_exang"},
            {"type": "number_input", "label": "ST Depression", "min": 0.0, "max": 10.0, "value": 1.0, "key": "heart_oldpeak"},
            {"type": "selectbox", "label": "Slope of ST", "options": ["1 - upsloping", "2 - flat", "3 - downsloping"], "key": "heart_slope"},
            {"type": "number_input", "label": "Major Vessels (ca)", "min": 0, "max": 3, "value": 0, "key": "heart_ca"},
            {"type": "selectbox", "label": "Thalassemia", "options": ["3 - normal", "6 - fixed defect", "7 - reversible defect"], "key": "heart_thal"},
        ]
        
        for i in range(0, len(heart_inputs), 6):
            create_input_row(heart_inputs, i)
        
        # Store inputs
        gender = st.session_state.heart_gender
        user_inputs_heart["Age"] = st.session_state.heart_age
        user_inputs_heart["Resting BP"] = st.session_state.heart_trestbps
        user_inputs_heart["Cholesterol"] = st.session_state.heart_chol
        cp = st.session_state.heart_cp
        fbs = st.session_state.heart_fbs
        restecg = st.session_state.heart_restecg
        user_inputs_heart["Max Heart Rate"] = st.session_state.heart_thalach
        exang = st.session_state.heart_exang
        user_inputs_heart["ST Depression"] = st.session_state.heart_oldpeak
        slope = st.session_state.heart_slope
        user_inputs_heart["Major Vessels (ca)"] = st.session_state.heart_ca
        thal = st.session_state.heart_thal

        # Prediction Button 
        st.markdown("<br>", unsafe_allow_html=True)
        colA, colB, colC = st.columns([2, 1, 2]) 
        with colB:
            if st.button("Predict Heart Disease Risk", 
                        type="primary", 
                        key="heart_btn"):
                sex_code = 1 if gender == "Male" else 0
                cp_code = int(cp.split(" ")[0])
                fbs_code = 1 if fbs == "Yes" else 0
                restecg_code = int(restecg.split(" ")[0])
                exang_code = 1 if exang == "Yes" else 0
                slope_code = int(slope.split(" ")[0])
                thal_code = int(thal.split(" ")[0])

                user_inputs_heart.update({
                    "Sex": sex_code, 
                    "Chest Pain Type": cp_code, 
                    "Fasting BS > 120?": fbs_code, 
                    "Resting ECG": restecg_code, 
                    "Exercise Angina": exang_code, 
                    "Slope of ST": slope_code, 
                    "Thal": thal_code
                })

                arr = np.array([[
                    user_inputs_heart["Age"], sex_code, cp_code, user_inputs_heart["Resting BP"], 
                    user_inputs_heart["Cholesterol"], fbs_code, restecg_code, 
                    user_inputs_heart["Max Heart Rate"], exang_code, user_inputs_heart["ST Depression"], 
                    slope_code, user_inputs_heart["Major Vessels (ca)"], thal_code
                ]], dtype=np.float64)
                arr_scaled = models["heart_scaler"].transform(arr)
                prob = models["heart_model"].predict_proba(arr_scaled)[0][1] * 100
                st.session_state.predictions["Heart Disease"] = {"prob": prob, "inputs": user_inputs_heart}
                
                profile_manager.auto_save_profile()
                st.rerun()

        if "Heart Disease" in st.session_state.predictions:
            data = st.session_state.predictions["Heart Disease"]
            show_risk_assessment_v2("Heart Disease", data["prob"], data["inputs"], heart_normals)

    # ------------------ Fever Tab ------------------
    with tabs[2]:
        st.markdown("<h3 style='margin-bottom: 20px;'>Enter Your Health Metrics</h3>", 
                   unsafe_allow_html=True)
        user_inputs_fever = {}
        
        # Define all fever inputs in order
        fever_inputs = [
            {"type": "number_input", "label": "Age", "min": 1, "max": 120, "value": 40, "key": "fever_age"},
            {"type": "number_input", "label": "BMI", "min": 10.0, "max": 70.0, "value": 25.0, "key": "fever_bmi"},
            {"type": "number_input", "label": "Temperature (°C)", "min": 34.0, "max": 42.0, "value": 36.5, "key": "fever_temp"},
            {"type": "number_input", "label": "Humidity (%)", "min": 0.0, "max": 100.0, "value": 50.0, "key": "fever_humidity"},
            {"type": "number_input", "label": "Air Quality Index", "min": 0.0, "max": 500.0, "value": 50.0, "key": "fever_aqi"},
            {"type": "number_input", "label": "Heart Rate", "min": 40.0, "max": 200.0, "value": 70.0, "key": "fever_hr"},
            {"type": "selectbox", "label": "Gender", "options": ["Female", "Male"], "key": "fever_gender"},
            {"type": "selectbox", "label": "Headache", "options": ["Yes", "No"], "key": "fever_headache"},
            {"type": "selectbox", "label": "Body Ache", "options": ["Yes", "No"], "key": "fever_body"},
            {"type": "selectbox", "label": "Fatigue", "options": ["Yes", "No"], "key": "fever_fatigue"},
            {"type": "selectbox", "label": "Chronic Conditions", "options": ["Yes", "No"], "key": "fever_chronic"},
            {"type": "selectbox", "label": "Allergies", "options": ["Yes", "No"], "key": "fever_allergies"},
            {"type": "selectbox", "label": "Smoking History", "options": ["Yes", "No"], "key": "fever_smoking"},
            {"type": "selectbox", "label": "Alcohol Consumption", "options": ["Yes", "No"], "key": "fever_alcohol"},
            {"type": "selectbox", "label": "Physical Activity", "options": ["Sedentary", "Moderate", "Active"], "key": "fever_activity"},
            {"type": "selectbox", "label": "Diet Type", "options": ["Vegan", "Vegetarian", "Non-Vegetarian"], "key": "fever_diet"},
            {"type": "selectbox", "label": "Blood Pressure", "options": ["Low", "Normal", "High"], "key": "fever_bp"},
            {"type": "selectbox", "label": "Previous Medication", "options": ["None", "Ibuprofen", "Paracetamol", "Other"], "key": "fever_prev_med"},
        ]
        
        for i in range(0, len(fever_inputs), 6):
            create_input_row(fever_inputs, i)
        
        # Store inputs
        user_inputs_fever["Age"] = st.session_state.fever_age
        user_inputs_fever["BMI"] = st.session_state.fever_bmi
        user_inputs_fever["Temperature (°C)"] = st.session_state.fever_temp
        user_inputs_fever["Humidity (%)"] = st.session_state.fever_humidity
        user_inputs_fever["Air Quality Index"] = st.session_state.fever_aqi
        user_inputs_fever["Heart Rate"] = st.session_state.fever_hr
        gender = st.session_state.fever_gender
        headache = st.session_state.fever_headache
        body_ache = st.session_state.fever_body
        fatigue = st.session_state.fever_fatigue
        chronic = st.session_state.fever_chronic
        allergies = st.session_state.fever_allergies
        smoking = st.session_state.fever_smoking
        alcohol = st.session_state.fever_alcohol
        activity = st.session_state.fever_activity
        diet = st.session_state.fever_diet
        blood_pressure = st.session_state.fever_bp
        prev_med = st.session_state.fever_prev_med

        # Prediction Button 
        st.markdown("<br>", unsafe_allow_html=True)
        colA, colB, colC = st.columns([2, 1, 2])  
        with colB:
            if st.button("Predict Fever Risk + Severity", 
                        type="primary", 
                        key="fever_btn"):
                numeric_vals = np.array([[
                    user_inputs_fever["Temperature (°C)"], 
                    user_inputs_fever["Age"], 
                    user_inputs_fever["BMI"], 
                    user_inputs_fever["Humidity (%)"], 
                    user_inputs_fever["Air Quality Index"], 
                    user_inputs_fever["Heart Rate"]
                ]], dtype=np.float64)
                numeric_scaled = models["fever_scaler"].transform(numeric_vals)

                encoded = []
                categorical_inputs = [gender, headache, body_ache, fatigue, chronic, allergies, smoking, alcohol, activity, diet, blood_pressure, prev_med]
                for col, val in zip(fever_categorical_cols, categorical_inputs):
                    le = models["fever_le_dict"][col]
                    encoded_val = le.transform([val])[0] if val in le.classes_ else le.transform([le.classes_[0]])[0]
                    encoded.append(encoded_val)
                
                final_input = np.hstack([numeric_scaled, np.array([encoded])])
                
                severity_idx = int(models["fever_severity_model"].predict(final_input)[0])
                severity_label = models["fever_target_le"].inverse_transform([severity_idx])[0]
                risk_percent = models["fever_risk_model"].predict(final_input)[0]
                risk_percent = np.clip(risk_percent, 0, 100)

                st.session_state.predictions["Fever"] = {
                    "prob": risk_percent, 
                    "inputs": user_inputs_fever, 
                    "severity": severity_label
                }
                
                profile_manager.auto_save_profile()
                st.rerun()
        
        if "Fever" in st.session_state.predictions:
            data = st.session_state.predictions["Fever"]
            show_risk_assessment_v2("Fever", data["prob"], data["inputs"], fever_normals, extra_text=data.get("severity"))

    # ------------------ Anemia Tab ------------------
    with tabs[3]:
        st.markdown("<h3 style='margin-bottom: 20px;'>Enter Your Health Metrics</h3>", 
                   unsafe_allow_html=True)
        user_inputs_anemia = {}

        # Define all anemia inputs in order
        anemia_inputs = [
            {"type": "selectbox", "label": "Gender", "options": ["Female", "Male"], "key": "anemia_gender"},
            {"type": "number_input", "label": "RBC (10^6/µL)", "min": 2.0, "max": 7.0, "value": 5.0, "key": "anemia_rbc"},
            {"type": "number_input", "label": "Hemoglobin (g/dL)", "min": 5.0, "max": 18.0, "value": 14.0, "key": "anemia_hb"},
            {"type": "number_input", "label": "Hematocrit", "min": 20.0, "max": 55.0, "value": 42.0, "key": "anemia_hct"},
            {"type": "number_input", "label": "MCV (fL)", "min": 60.0, "max": 120.0, "value": 90.0, "key": "anemia_mcv"},
            {"type": "number_input", "label": "MCH (pg)", "min": 15.0, "max": 35.0, "value": 30.0, "key": "anemia_mch"},
            {"type": "number_input", "label": "MCHC (g/dL)", "min": 25.0, "max": 38.0, "value": 34.0, "key": "anemia_mchc"},
            {"type": "number_input", "label": "WBC (10^3/µL)", "min": 2.0, "max": 15.0, "value": 7.0, "key": "anemia_wbc"},
            {"type": "number_input", "label": "Platelets (10^3/µL)", "min": 100.0, "max": 450.0, "value": 250.0, "key": "anemia_platelets"},
            {"type": "number_input", "label": "RDW", "min": 10.0, "max": 20.0, "value": 13.5, "key": "anemia_rdw"},
            {"type": "number_input", "label": "PDW", "min": 10.0, "max": 20.0, "value": 12.0, "key": "anemia_pdw"},
            {"type": "number_input", "label": "PCT", "min": 0.1, "max": 0.3, "value": 0.22, "key": "anemia_pct"},
            {"type": "number_input", "label": "Lymphocytes", "min": 15.0, "max": 50.0, "value": 30.0, "key": "anemia_lymph"},
            {"type": "number_input", "label": "Neutrophils", "min": 30.0, "max": 70.0, "value": 60.0, "key": "anemia_neutro_pct"},
            {"type": "number_input", "label": "Neutrophils", "min": 1.5, "max": 8.0, "value": 4.2, "key": "anemia_neutro_num"},
        ]
        
        for i in range(0, len(anemia_inputs), 6):
            create_input_row(anemia_inputs, i)
        
        # Store inputs
        gender = st.session_state.anemia_gender
        user_inputs_anemia["Gender"] = gender
        user_inputs_anemia["RBC"] = st.session_state.anemia_rbc
        user_inputs_anemia["Hemoglobin (Hb)"] = st.session_state.anemia_hb
        user_inputs_anemia["Hematocrit (HCT)"] = st.session_state.anemia_hct
        user_inputs_anemia["MCV"] = st.session_state.anemia_mcv
        user_inputs_anemia["MCH"] = st.session_state.anemia_mch
        user_inputs_anemia["MCHC"] = st.session_state.anemia_mchc
        user_inputs_anemia["WBC"] = st.session_state.anemia_wbc
        user_inputs_anemia["Platelets"] = st.session_state.anemia_platelets
        user_inputs_anemia["RDW"] = st.session_state.anemia_rdw
        user_inputs_anemia["PDW"] = st.session_state.anemia_pdw
        user_inputs_anemia["PCT"] = st.session_state.anemia_pct
        user_inputs_anemia["Lymphocytes"] = st.session_state.anemia_lymph
        user_inputs_anemia["Neutrophils %"] = st.session_state.anemia_neutro_pct
        user_inputs_anemia["Neutrophils #"] = st.session_state.anemia_neutro_num

        # Prediction Button
        st.markdown("<br>", unsafe_allow_html=True)
        colA, colB, colC = st.columns([2, 1, 2]) 
        with colB:
            if st.button("Predict Anemia Risk", 
                        type="primary", 
                        key="anemia_btn"):
                try:
                    input_array = np.array([
                        user_inputs_anemia["RBC"],
                        user_inputs_anemia["Hemoglobin (Hb)"],
                        user_inputs_anemia["MCV"],
                        user_inputs_anemia["MCH"],
                        user_inputs_anemia["MCHC"],
                        user_inputs_anemia["Hematocrit (HCT)"],
                        user_inputs_anemia["WBC"],
                        user_inputs_anemia["Platelets"],
                        user_inputs_anemia["PDW"],
                        user_inputs_anemia["PCT"],
                        user_inputs_anemia["Lymphocytes"],
                        user_inputs_anemia["Neutrophils %"],
                        user_inputs_anemia["Neutrophils #"]
                    ]).reshape(1, -1)

                    # Scale and predict
                    input_scaled = models["anemia_scaler"].transform(input_array)
                    risk_prob = models["anemia_risk_model"].predict_proba(input_scaled)[0][1] * 100

                    try:
                        type_pred = models["anemia_type_model"].predict(input_scaled)[0]
                        anemia_type_label = models["anemia_label_encoder"].inverse_transform([type_pred])[0]
                    except:
                        mcv = user_inputs_anemia["MCV"]
                        anemia_type_label = "Microcytic" if mcv < 80 else ("Normocytic" if mcv <= 100 else "Macrocytic")

                    # Save to session state
                    st.session_state.predictions["Anemia"] = {
                        "prob": risk_prob,
                        "inputs": user_inputs_anemia,
                        "severity": anemia_type_label
                    }
                    
                    # AUTO-SAVE after prediction
                    profile_manager.auto_save_profile()
                    st.rerun()

                except Exception as e:
                    st.error(f"Error predicting anemia: {e}")

        # Normal Values for chart
        anemia_normals = {
            "Hemoglobin (Hb)": 13.5 if gender == "Male" else 12.0,
            "RBC": 5.0 if gender == "Male" else 4.5,
            "Hematocrit (HCT)": 41.0 if gender == "Male" else 36.0,
            "MCV": 90.0,
            "MCH": 30.0,
            "MCHC": 34.0,
            "RDW": 14.0,
            "Platelets": 250.0,
            "WBC": 7.0,
            "PDW": 12.0,
            "PCT": 0.22,
            "Lymphocytes": 30.0,
            "Neutrophils %": 60.0,
            "Neutrophils #": 4.2
        }

        # Show Results
        if "Anemia" in st.session_state.predictions:
            data = st.session_state.predictions["Anemia"]
            show_risk_assessment_v2(
                "Anemia",
                data["prob"],
                data["inputs"],
                anemia_normals,
                extra_text=data.get("severity")
            )

    # ------------------ Summary Tab ------------------
    with tabs[4]:
        st.markdown("<h3 style='margin-bottom: 20px;'>Predictive Diagnostics Report</h3>", 
                unsafe_allow_html=True)
        preds = st.session_state.get("predictions", {})

        if not preds:
            st.warning("No Analysis Yet !!")
        else:
            # Define normal ranges
            normals_dict = {
                "Diabetes": diabetes_normals,
                "Heart Disease": heart_normals,
                "Fever": fever_normals,
                "Anemia": anemia_normals
            }

            # Display each disease summary if prediction exists
            for disease in ["Diabetes", "Heart Disease", "Fever", "Anemia"]:
                if disease in preds:
                    data = preds[disease]
                    normals = normals_dict.get(disease, {})
                    extra = data.get("severity") if disease in ["Fever", "Anemia"] else None

                    # Show risk assessment chart / summary
                    show_risk_assessment_v2(
                        disease, 
                        data.get("prob", 0), 
                        data.get("inputs", {}), 
                        normals, 
                        extra_text=extra,
                        suffix=f"summary_{disease}"
                    )
                    st.markdown("---")
                    st.markdown("---")

            if preds:
                pdf_file = generate_pdf_report(st.session_state.predictions, list(preds.keys()))
                col1, col2, col3 = st.columns([2, 1, 2])  
                with col2:
                    st.download_button(
                        "📄 Download Report",
                        data=pdf_file,
                        file_name="CureHelp_Report.pdf",
                        mime="application/pdf",
                        type="primary"
                    )  
                    
    # ------------------ Assistant Tab ------------------
    with tabs[5]:
        render_chatbot_tab()  
        
        
    with tabs[6]:
        profile_manager.render_profiles_tab()


    with tabs[7]: 
        render_consultant_tab()

def auto_save_on_exit():
    """Attempt to auto-save when the app is closing"""
    profile_manager.auto_save_profile()

# Router
if st.session_state.page == "landing":
    render_landing_page()
elif st.session_state.page == "patient_details":
    render_patient_details_page()
elif st.session_state.page == "input":
    render_input_page()

auto_save_on_exit()

st.markdown("---")
st.caption("Disclaimer: All predictions are based on machine learning models and are not a substitute for professional medical advice. Always consult a qualified doctor for any health concerns.")