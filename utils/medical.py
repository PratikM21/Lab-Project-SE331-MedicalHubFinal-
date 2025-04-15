import pandas as pd
from groq import Groq
import smtplib
from email.message import EmailMessage
import os

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_medical_advice(symptom: str):
    """Get medical advice using Groq's API"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"Provide medical advice for these symptoms: {symptom}. Keep the response concise and professional."}],
        temperature=0.7
    )
    return response.choices[0].message.content

def recommend_doctor(symptom: str, doctors_df: pd.DataFrame):
    """Recommend a doctor based on the symptom"""
    symptom_mapping = {
        "heart": "Cardiologist",
        "chest pain": "Cardiologist",
        "heartattack": "Cardiologist",
        "teeth": "Dentist",
        "toothache": "Dentist",
        "gum": "Dentist",
        "back pain": "Physiotherapist",
        "muscle pain": "Physiotherapist",
        "pain": "Physiotherapist",
        "injury": "Physiotherapist",
        "body": "Physiotherapist",
        "bleeding": "Physiotherapist",
        "joint pain": "Physiotherapist",
        "brain": "Neurologist",
        "headache": "Neurologist",
        "brain tumors": "Neurologist",
        "seizures": "Neurologist",
        "stroke": "Neurologist",
        "memory loss": "Neurologist",
        "concussion": "Neurologist",
        "mental health": "Psychiatrist",
        "depression": "Psychiatrist",
        "anxiety": "Psychiatrist",
        "PTSD": "Psychiatrist",
        "schizophrenia": "Psychiatrist",
        "insomnia": "Psychiatrist",
        "hallucination": "Psychiatrist",
        "trauma": "Psychiatrist",
        "therapy": "Psychiatrist",
        "panic": "Psychiatrist",
        "children": "Pediatrician",
        "fever": "General Physician",
        "stomach": "General Physician",
        "digestion": "General Physician",
        "food": "General Physician",
        "food poisioning": "General Physician",
        "cold": "General Physician",
        "breathing": "General Physician"
    }

    for key, department in symptom_mapping.items():
        if key in symptom.lower():
            doctors = doctors_df[doctors_df['Department'] == department]
            if not doctors.empty:
                return doctors

    # Default to General Physician if no match is found
    return doctors_df[doctors_df['Department'] == "General Physician"]

def send_email(to_email: str, doctor_name: str, doctor_email: str, doctor_phone: str, shift_time: str):
    """Send appointment confirmation email"""
    sender_email = os.getenv("SMTP_EMAIL")
    app_password = os.getenv("SMTP_PASSWORD")

    subject = "DIU MedicalHub - Appointment Confirmation"
    body = f"""
    Dear Patient,
    
    Your appointment with Dr. {doctor_name} has been confirmed for {shift_time}.
    
    Doctor's Contact Information:
    - Email: {doctor_email}
    - Phone: {doctor_phone}
    
    Please arrive 10 minutes before your scheduled time.
    
    Best regards,
    DIU MedicalHub Team
    """

    message = EmailMessage()
    message.set_content(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(message)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False