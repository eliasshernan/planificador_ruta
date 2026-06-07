import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="Planificador Litoral Móvil", layout="wide")

# Configuración de API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Falta configurar la API KEY en los Secrets.")
    st.stop()

# Configuración del modelo (La versión más estable)
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📋 Planificador de Ruta Comercial")

uploaded_file = st.file_uploader("Subí tu planilla:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    if st.button("🚀 Generar Reportes"):
        with st.spinner("Analizando..."):
            prompt = """
            Analiza esta imagen de una planilla comercial. 
            Devuelve:
            1. REPORTE TOTAL
            2. TOP 15 MÁS URGENTES
            Usa viñetas y formato claro.
            """
            try:
                response = model.generate_content([prompt, image])
                st.markdown(response.text)
                st.session_state['reporte'] = response.text
            except Exception as e:
                st.error(f"Error: {e}")

if 'reporte' in st.session_state:
    st.download_button("Descargar Reporte", st.session_state['reporte'], "reporte.txt")
