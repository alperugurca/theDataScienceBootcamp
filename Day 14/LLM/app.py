import streamlit as st
import google.generativeai as genai
genai.configure(api_key='AIzaSyDhD6edcFZSadDoXhzglXAH0WwHGYG44vc')

st.title('Alper')

model = genai.GenerativeModel('gemini-1.5-pro')
chat=model.start_chat(history=[])

question=st.text_input('Enter your question:')
if st.button('Submit'):
    response=chat.send_message(question)
    st.write(response.text)
    st.write(chat.history)
