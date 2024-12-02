import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPool2D
from sklearn.neighbors import NearestNeighbors
from numpy.linalg import norm
import os
import pickle

# Model ve veri yükleme
@st.cache_resource
def load_model():
    model = ResNet50(weights='imagenet', include_top=False, input_shape=(224,224,3))
    model.trainable = False
    model = tf.keras.models.Sequential([
        model,
        GlobalMaxPool2D()
    ])
    return model

@st.cache_data
def load_data():
    features = pickle.load(open('Images_features.pkl', 'rb'))
    filenames = pickle.load(open('filenames.pkl', 'rb'))
    return features, filenames

model = load_model()
features, filenames = load_data()

# Özellik çıkarma fonksiyonu
def extract_features(img, model):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    return normalized_result

# Streamlit uygulaması
st.set_page_config(page_title="Fashion Item Recommender", page_icon="👚")
st.title('Fashion Item Recommender')

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image.', use_column_width=True)
    
    features = extract_features(img, model)
    
    # En yakın komşuları bul
    neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
    neighbors.fit(features)
    
    distances, indices = neighbors.kneighbors([features])
    
    st.write("Here are similar items:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(filenames[indices[0][i+1]], use_column_width=True)