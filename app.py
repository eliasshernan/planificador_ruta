import streamlit as st
from PIL import Image
from google import genai
import io
import os

st.set_page_config(page_title="Planificador Litoral Móvil", layout="wide")

try:
    if os.path.exists("logo_empresa.png"):
        st.image("logo_empresa.png", width=400)
except: pass

st.title("📋 Planificador de Ruta Comercial")

# Validación más estricta de la API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("ERROR: No se encuentra la GEMINI_API_KEY en los secretos. Revisa el panel de control.")
    st.stop() # Detiene la ejecución aquí si no hay clave

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Error al iniciar cliente de IA: {e}")
    st.stop()

uploaded_file = st.file_uploader("Subí tu planilla:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    if st.button("🚀 Generar Reportes"):
        with st.spinner("Analizando..."):
            prompt = """Analiza la ruta. Devuelve 'REPORTE TOTAL' y 'TOP 15 MÁS URGENTES'. 
            Usa ### Nombre para títulos y viñetas para alertas. 
            Prioridad: ICB 0 > Metas > Claro Pay."""
            
            try:
                response = client.models.generate_content(
                    model='gemini-1.5-flash', 
                    contents=[image, prompt]
                )
                st.session_state['reporte'] = response.text
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error específico de la API al generar: {e}")
                st.write("Verifica que tu API Key sea válida y tenga acceso a Gemini 1.5 Flash.")

if 'reporte' in st.session_state:
    st.markdown("---")
    st.download_button("📲 Descargar TODO el reporte", st.session_state['reporte'], "reporte_total.txt")
