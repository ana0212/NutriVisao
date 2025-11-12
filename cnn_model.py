import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from PIL import Image
import pickle
import os
import gdown

@st.cache_resource
def carregar_modelo():
    model_path = "modelos/melhor_modelo.keras"
    indices_path = "modelos/class_indices.pkl"

    # Se o modelo não existir, faz download do Google Drive
    if not os.path.exists(model_path):
        st.info("Baixando o modelo... isso pode levar alguns minutos.")
        url = "https://drive.google.com/file/d/1-4JsC2MtuAhJabNXF1nvk7ZF-_WJuONt/view"
        os.makedirs("modelos", exist_ok=True)
        gdown.download(url, model_path, quiet=False)

    # Carrega o modelo e o dicionário de classes
    modelo = load_model(model_path)
    with open(indices_path, "rb") as f:
        class_indices = pickle.load(f)
    indices_classes = {v: k for k, v in class_indices.items()}

    return modelo, indices_classes

def preprocessar_imagem(img: Image.Image) -> np.ndarray:
    img = img.resize((224, 224))  # mesma dimensão usada no treino
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # normaliza como ResNet espera
    return img_array

def classificar_imagem(img: Image.Image) -> str:
    modelo, indices_classes = carregar_modelo()
    entrada = preprocessar_imagem(img)
    pred = modelo.predict(entrada)
    classe_id = np.argmax(pred)
    return indices_classes[classe_id]

