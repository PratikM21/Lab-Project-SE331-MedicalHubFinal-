import streamlit as st
from utils.auth import authenticate_user
import time

st.set_page_config(
    page_title="Login - DIU MedicalHub",
    page_icon="🩺",
    layout="centered"
)

# Custom CSS for login page
st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            padding: 2rem;
            margin: auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-top: 5px solid #0288d1;
            background-image: url('https://www.transparenttextures.com/patterns/medical-cross.png');
        }
        
        .login-title {
            color: #0288d1;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        
        .login-input {
            margin-bottom: 1rem;
        }
        
        .login-button {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            background-color: #0288d1;
            color: white;
            border: none;
        }
        
        .login-button:hover {
            background-color: #0277bd;
        }
        
        .signup-link {
            text-align: center;
            margin-top: 1.5rem;
            color: #616161;
        }
    </style>
""", unsafe_allow_html=True)

# Login form
with st.container():
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    
    st.markdown("<h1 class='login-title'>DIU MedicalHub Login</h1>", unsafe_allow_html=True)
    
    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")
    
    if st.button("Login", key="login_button"):
        if username and password:
            if authenticate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                time.sleep(1)
                st.switch_page("app.py")
            else:
                st.error("Invalid username or password")
        else:
            st.warning("Please enter both username and password")
    
    st.markdown("<div class='signup-link'>Don't have an account? <a href='/Signup' target='_self'>Sign up</a></div>", 
                unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)