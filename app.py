import streamlit as st
import pandas as pd
from utils.auth import authenticate_user, get_password_hash
from utils.medical import get_medical_advice, recommend_doctor, send_email
import extra_streamlit_components as stx
import time
import os
from streamlit import config as _config

_config.set_option("server.port", 8501)
_config.set_option("theme.primaryColor", "#0288d1")
_config.set_option("theme.backgroundColor", "#f8f9fa")
_config.set_option("theme.secondaryBackgroundColor", "#e3f2fd")
_config.set_option("theme.textColor", "#212121")
_config.set_option("theme.font", "sans serif")

# Page configuration
st.set_page_config(
    page_title="DIU MedicalHub",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def inject_custom_css():
    st.markdown("""
        <style>
            /* Main container */
            .main {
                background-color: #f8f9fa;
            }
            
            /* Sidebar */
            .css-1d391kg {
                background-color: #e3f2fd;
                background-image: url('https://www.transparenttextures.com/patterns/medical-cross.png');
                border-right: 5px solid #0288d1;
            }
            
            /* Titles */
            h1 {
                color: #0288d1;
                border-bottom: 2px solid #4fc3f7;
                padding-bottom: 10px;
            }
            
            /* Buttons */
            .stButton>button {
                background-color: #0288d1;
                color: white;
                border-radius: 8px;
                padding: 10px 24px;
                border: none;
            }
            
            .stButton>button:hover {
                background-color: #0277bd;
            }
            
            /* Input fields */
            .stTextInput>div>div>input {
                border-radius: 8px;
                border: 2px solid #e0e0e0;
            }
            
            /* Dataframes */
            .stDataFrame {
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            /* Success messages */
            .stAlert {
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'doctors_df' not in st.session_state:
    st.session_state.doctors_df = pd.read_csv("doctors.csv")

# Authentication check
def check_authentication():
    if not st.session_state.authenticated:
        st.warning("Please login to access the MedicalHub")
        st.stop()

# Login page redirect
def redirect_to_login():
    st.session_state.authenticated = False
    st.experimental_rerun()

# Main application
def main_app():
    check_authentication()
    
    # Sidebar content
    with st.sidebar:
        st.image("https://i.imgur.com/JbIq3Xz.png", width=150)  # Replace with your logo
        st.title(f"Welcome, {st.session_state.username}!")
        
        st.markdown("---")
        st.header("🩺 Available Doctors")
        available_doctors = st.session_state.doctors_df[st.session_state.doctors_df["Available"] == "Yes"]
        st.dataframe(available_doctors[["Name", "Department", "Shift"]], hide_index=True)
        
        st.markdown("---")
        st.header("🚑 Emergency Contacts")
        st.markdown("📞 **Ambulance:** 01847334999")
        st.markdown("📞 **Medical Center:** 01847140120")
        
        st.markdown("---")
        if st.button("Logout", key="logout_btn"):
            redirect_to_login()
    
    # Main content
    st.title("DIU MedicalHub Assistant")
    st.markdown("Type in your symptoms and let your AI assistant take care of the rest.")
    
    symptom = st.text_area("Describe your symptoms:", height=150)
    
    if st.button("Get Medical Advice"):
        if symptom:
            with st.spinner("Analyzing your symptoms..."):
                advice = get_medical_advice(symptom)
                st.success("AI Medical Advice:")
                st.markdown(f"<div style='background-color:#e3f2fd; padding:20px; border-radius:10px;'>{advice}</div>", 
                           unsafe_allow_html=True)
                
                st.session_state.advice = advice
                st.session_state.show_recommendation = True
        else:
            st.warning("Please describe your symptoms")
    
    if st.session_state.get('show_recommendation', False):
        if st.button("Get Doctor Recommendations"):
            with st.spinner("Finding suitable doctors..."):
                recommended_doctors = recommend_doctor(symptom, st.session_state.doctors_df)
                st.session_state.recommended_doctors = recommended_doctors
                st.session_state.show_booking = True
    
    if st.session_state.get('show_booking', False) and 'recommended_doctors' in st.session_state:
        st.subheader("Recommended Doctors")
        st.dataframe(st.session_state.recommended_doctors, hide_index=True)
        
        st.subheader("Book Appointment")
        doctor_names = st.session_state.recommended_doctors["Name"].tolist()
        selected_doctor = st.selectbox("Select a doctor:", doctor_names)
        
        user_email = st.text_input("Your email address:")
        
        if st.button("Confirm Appointment"):
            if user_email:
                doctor_info = st.session_state.recommended_doctors[
                    st.session_state.recommended_doctors["Name"] == selected_doctor].iloc[0]
                
                with st.spinner("Booking your appointment..."):
                    send_email(
                        user_email,
                        selected_doctor,
                        doctor_info["Email"],
                        doctor_info["Phone"],
                        doctor_info["Shift"]
                    )
                    st.success(f"Appointment confirmed with Dr. {selected_doctor} at {doctor_info['Shift']}. Details sent to your email.")
            else:
                st.warning("Please enter your email address")

# Run the appropriate page
if st.session_state.authenticated:
    main_app()
else:
    st.switch_page("pages/1_Login.py")