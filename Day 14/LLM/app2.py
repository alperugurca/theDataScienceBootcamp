import streamlit as st
import google.generativeai as genai
genai.configure(api_key='AIzaSyDhD6edcFZSadDoXhzglXAH0WwHGYG44vc')

st.title('Image Analysis AE')

import google.generativeai as genai
model = genai.GenerativeModel('gemini-1.5-flash')
from PIL import Image

resim=st.file_uploader('Upload Image',type=['jpg','jpeg','png'])

if resim is not None:
    img=Image.open(resim)
    st.image(img)
    #response=model.generate_content(img)
    #st.write(response.text)

soru=st.text_input('Soru')
if st.button('Sor'):
    response=model.generate_content([soru,img], stream=True)
    response.resolve()
    st.write(response.text)

