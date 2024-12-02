import streamlit as st
import pickle
import numpy as np
st.title("Tecrube, Yazılı ve Sözlü Sınava Göre Maaş Tahmini :dollar: :heavy_dollar_sign:")
model=pickle.load(open("maas.pkl","rb"))

tecrube=st.number_input("Tecrübenizi Giriniz",1,10)     
yazili=st.number_input("Yazılı Notunuzu Giriniz",1,10)
mulakat=st.number_input("Mülakat Notunuzu Giriniz",1,10)


if st.button("Tahmin Et"):       
    tahmin=model.predict([[tecrube,yazili,mulakat]])
    tahmin=np.round(tahmin[0],2)
    st.success(f"Maaşınız: {tahmin} $")










