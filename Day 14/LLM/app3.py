import google.generativeai as genai
import streamlit as st

# API anahtarınızı ayarlayın
genai.configure(api_key="AIzaSyDhD6edcFZSadDoXhzglXAH0WwHGYG44vc")

# Modeli yapılandırın
model = genai.GenerativeModel('gemini-pro')

prompt = st.text_input('Prompt')

# Prompt'un boş olup olmadığını kontrol edin
if st.button('Submit'):
    # Güvenlik ayarlarını düşük seviyeye ayarlayın
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    ]

    # Modele istek gönderin
    response = model.generate_content(
        prompt,
        safety_settings=safety_settings
    )

    st.write(response.text)

# ... existing code ...