import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("Planificador de Ruta")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("No configuraste el Secret GEMINI_API_KEY en Streamlit.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Subí tu planilla:", type=["jpg", "png"])

if uploaded_file:
    if st.button("🚀 Generar"):
        try:
            img = Image.open(uploaded_file)
            response = model.generate_content(["Analiza esta imagen y dame un reporte", img])
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
