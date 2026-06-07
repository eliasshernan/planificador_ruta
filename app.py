import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="App Comercial", layout="wide")

st.title("Planificador")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("No hay API KEY configurada.")
    st.stop()

# Configuración básica y directa
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Subí planilla", type=["jpg", "png"])

if uploaded_file and st.button("Generar"):
    try:
        img = Image.open(uploaded_file)
        # LLAMADA SIMPLE: Sin v1beta, sin cosas raras
        response = model.generate_content(["Analiza esta imagen y haz un reporte", img])
        st.write(response.text)
    except Exception as e:
        st.error(f"Error definitivo: {e}")
