import streamlit as st
import pandas as pd
st.title("Formdan Veri Alma ve CSV dosyasına Yazma :broken_heart:")

isim=st.text_input("İsim")

sifre=st.text_input("Şifre",type="password")

dob=st.date_input("Doğum Tarihi")

yas=st.slider("Yaş",1,100)

mesaj=st.text_area("Mesajınızı Yazınız",height=100)

if st.button("Gönder"):
    ndf=pd.DataFrame({
        "İsim":[isim],
        "Sifre":[sifre],
        "dob":[dob],
        "yas":[yas],
        "mesaj":[mesaj]
    })
    st.write(ndf)
    ndf.to_csv("katilimformu.csv",index=False)
st.divider()







