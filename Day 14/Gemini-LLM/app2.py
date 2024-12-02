from dotenv import load_dotenv # dotenv kütüphanesini import ediyoruz
load_dotenv() # dotenv kütüphanesini yüklüyoruz
import streamlit as st # streamlit kütüphanesini import ediyoruz
import os # os kütüphanesini import ediyoruz
import google.generativeai as genai # google.generativeai kütüphanesini import ediyoruz

os.getenv('GOOGLE_API_KEY') # GOOGLE_API_KEY'i alıyoruz
genai.configure(api_key=os.getenv('GOOGLE_API_KEY')) # GOOGLE_API_KEY'i configure ediyoruz

model=genai.GenerativeModel('gemini-1.0-pro') # Modeli tanımlıyoruz
chat=model.start_chat(history=[]) # Chat oluşturuyoruz

def get_response(question): # get_response fonksiyonunu tanımlıyoruz
    response=chat.send_message(question,stream=True) #response'u alıyoruz
    return response # response'u döndürüyoruz

st.balloons() # Balloons çıktısını gösteriyoruz

st.header('Gemini Pro Chatbot') # Başlık
input=st.text_input('Input',key='input') # Input alıyoruz
submit=st.button('Ask Me Anything') # Buton oluşturuyoruz


if submit: # Eğer buton tıklanırsa
    response=get_response(input) # response'u alıyoruz
    st.header('AI Response') # response'u yazdırıyoruz
    
    # Yanıtı parça parça göster
    response_container = st.empty()
    full_response = ""
    for chunk in response:
        full_response += chunk.text
        response_container.markdown(full_response + "▌")
    
    # Son hali göster
    response_container.markdown(full_response)

    # Chat geçmişini güncelle
    chat.history.append((input, full_response))
