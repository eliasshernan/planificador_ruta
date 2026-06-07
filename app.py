import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("Prueba de Fuego")

# NO USES SECRETS. Pega la clave aquí directamente entre comillas.
# IMPORTANTE: No compartas esta clave con nadie más después del parcial.
api_key = "AQ.Ab8RN6IAOe6U-iIgmLG8oX9eADyaJ0Zu6pQWCfOATRPgQ7Qanw" 

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.write("Configuración cargada correctamente.")
except Exception as e:
    st.write(f"Error: {e}")

uploaded_file = st.file_uploader("Subí planilla", type=["jpg", "png"])
if uploaded_file and st.button("Probar"):
    img = Image.open(uploaded_file)
    try:
        response = model.generate_content(["Analiza esta imagen", img])
        st.write(response.text)
    except Exception as e:
        st.write(f"Error al generar: {e}")
