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

API_KEY = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

uploaded_file = st.file_uploader("Subí tu planilla:", type=["jpg", "jpeg", "png"])

if uploaded_file and client and st.button("🚀 Generar Reportes"):
    image = Image.open(uploaded_file)
    with st.spinner("Analizando todos los críticos y preparando el Top 15..."):
        prompt = """
        Analiza esta ruta comercial. Devuélveme dos secciones claramente separadas:
        
        SECCIÓN 1: 'REPORTE COMPLETO DE CRÍTICOS' (Todos los clientes que detectes con problemas).
        SECCIÓN 2: 'TOP 15 MÁS URGENTES' (Filtra de los anteriores solo los 15 más críticos, dando prioridad absoluta a clientes con ventas > 0 que están cerca de la meta de $13.000).
        
        Para ambos, usa formato ### Nombre del Cliente y viñetas cortas.
        """
        response = client.models.generate_content(model='gemini-2.5-flash', contents=[image, prompt])
        st.session_state['reporte_completo'] = response.text
        st.markdown(response.text)

if 'reporte_completo' in st.session_state:
    st.markdown("---")
    st.markdown("### 💾 Opciones de Descarga")
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button("📲 Descargar TODO el reporte", st.session_state['reporte_completo'], "reporte_total.txt")
    with col2:
        # Extraemos solo el bloque del Top 15 para la segunda descarga
        texto = st.session_state['reporte_completo']
        top15 = texto.split("TOP 15 MÁS URGENTES")[1] if "TOP 15 MÁS URGENTES" in texto else texto
        st.download_button("🔥 Descargar solo el TOP 15", top15, "top_15_criticos.txt")
