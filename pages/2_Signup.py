import streamlit as st
from utils.auth import register_user
import time

st.set_page_config(
    page_title="Sign Up - DIU MedicalHub",
    page_icon="🩺",
    layout="centered"
)

# Custom CSS for signup page
st.markdown("""
    <style>
        .signup-container {
            max-width: 400px;
            padding: 2rem;
            margin: auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-top: 5px solid #0288d1;
            background-image: url('https://www.transparenttextures.com/patterns/medical-cross.png');
        }
        
        .signup-title {
            color: #0288d1;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        
        .signup-input {
            margin-bottom: 1rem;
        }
        
        .signup-button {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            background-color: #0288d1;
            color: white;
            border: none;
        }
        
        .signup-button:hover {
            background-color: #0277bd;
        }
        
        .login-link {
            text-align: center;
            margin-top: 1.5rem;
            color: #616161;
        }
    </style>
""", unsafe_allow_html=True)

# Signup form
with st.container():
    st.markdown("<div class='signup-container'>", unsafe_allow_html=True)
    
    st.markdown("<h1 class='signup-title'>Create Account</h1>", unsafe_allow_html=True)
    
    full_name = st.text_input("Full Name", key="full_name_input")
    email = st.text_input("Email", key="email_input")
    username = st.text_input("Username", key="signup_username_input")
    password = st.text_input("Password", type="password", key="signup_password_input")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password_input")
    
    if st.button("Sign Up", key="signup_button"):
        if password == confirm_password:
            if full_name and email and username and password:
                if register_user(username, password, email, full_name):
                    st.success("Registration successful! Please login.")
                    time.sleep(2)
                    st.switch_page("pages/1_Login.py")
                else:
                    st.error("Username already exists")
            else:
                st.warning("Please fill in all fields")
        else:
            st.error("Passwords do not match")
    
    st.markdown("<div class='login-link'>Already have an account? <a href='/Login' target='_self'>Login</a></div>", 
                unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)