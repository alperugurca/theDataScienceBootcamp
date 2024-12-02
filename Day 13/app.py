import streamlit as st
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import cv2

# Eğitilmiş modeli yükle
model = load_model('skin_cancer_model.h5')

def process_image(img):
    # PIL Image'ı numpy dizisine çevir
    img = np.array(img)
    # Görüntüyü yeniden boyutlandır
    img = cv2.resize(img, (170, 170))
    # Piksel değerlerini 0-1 arasına normalize et
    img = img / 255.0
    # Modele uygun şekilde boyut ekle
    img = np.expand_dims(img, axis=0)
    return img

# Streamlit uygulamasının başlığını ayarla
st.title('Skin Cancer Classification :stethoscope:')
st.write('Upload a image and model will predict if it is a skin cancer or not')

# Kullanıcıdan dosya yükleme
file = st.file_uploader('Choose a image...', type=['jpg', 'jpeg', 'png'])

if file is not None:
    # Yüklenen dosyayı aç ve göster
    img = Image.open(file)
    st.image(img, caption='Uploaded Image')
    
    # Görüntüyü işle ve tahmin yap
    image = process_image(img)
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction)

    # Sonucu göster
    class_names = ['Not Cancer', 'Cancer']
    st.write(class_names[predicted_class])