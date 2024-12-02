import streamlit as st
import pandas as pd
import plotly.express as px

st.title("MLOps Streamlit App :sunglasses: :coffee: :flag-tr:")

isim=st.text_input("İsim:", max_chars=15)

#st.video("data\secret_of_success.mp4")
#st.camera_input("camera")

st.date_input("Tarih Seçiniz")

st.time_input("Zaman Seçiniz")

st.text_input("Sifre", type="password")

st.text_area("Mesajınız", height=100)

st.number_input("Yaşınızı Giriniz", min_value=1, max_value=100)

st.radio("Medeni Haliniz", ["Evli", "Bekar", "Dul", "Boşanmış"])

st.selectbox("Bildiğiniz Programlama Dilleri", ["Python", "Java", "C#", "JavaScript", "C++", "R", "SQL", "Julia"])

st.multiselect("Hobileriniz", ["Kitap Okumak", "Sinema", "Gezmek", "Spor", "Müzik", "Yazılım", "Bilgisayar Oyunları"])

#st.video("https://192.168.0.12:8080/video.mp4")

st.image("data/image_01.jpg")

st.divider()

df=pd.read_csv("data/Iris.csv")

st.write(df)

st.area_chart(df)

st.code("""
        import pandas as pd
        df=pd.read_excel("cars.xlsx")
        """)

st.success("Başarılı")

st.error("Bir Hata Oluştu")

menu = ["Anasayfa", "Hakkımda", "İletişim"]

st.sidebar.selectbox("Menu", menu)

df=pd.read_csv("data/prog_languages_data.csv")

fig=px.pie(df,values="Sum")

st.plotly_chart(fig)

fig2=px.bar(df,x="lang",y="Sum",color="lang",title="Programlama Dilleri")

st.plotly_chart(fig2)

file=st.file_uploader("Dosya Seçiniz")

st.warning("Dosya Seçilmedi")

st.info("Dosya Seçildi")

st.slider("Bir Rakam Seçiniz", min_value=0, max_value=100)

st.audio("data/song.mp3")






