from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Google API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Initialize the model and start a chat session
model = genai.GenerativeModel('gemini-1.0-pro')
chat = model.start_chat(history=[])

# Function to get a response from the AI model
def get_response(question):
    response = chat.send_message(question, stream=True)
    response.resolve()  # Yanıtın tamamlanmasını bekliyor
    return response

# Streamlit UI components
st.balloons()
st.header('Gemini Pro Chatbot')
input_text = st.text_input('Input', key='input')
submit = st.button('Ask Me Anything')

# Handle button click
if submit:
    if input_text:  # Ensure there's input before making the API call
        response = get_response(input_text)
        st.header('AI Response')
        st.text(response.text)  # Display the AI response
    else:
        st.warning('Please enter a question before submitting.')
