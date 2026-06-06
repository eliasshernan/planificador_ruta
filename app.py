import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

st.set_page_config(page_title="Planificador Litoral Móvil", layout="wide")

# Logo
try:
    if os.path.exists("logo_empresa.png"):
        st.image("logo_empresa.png", width=400)
except: pass

st.title("📋 Planificador de Ruta Comercial")

# Configuración privada (Streamlit Secrets)
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("Error: No encontré la API Key en los Secrets.")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
    # Este modelo es el más estable actualmente
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error al configurar: {e}")
    st.stop()

uploaded_file = st.file_uploader("Subí tu planilla:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    if st.button("🚀 Generar Reportes"):
        with st.spinner("Analizando..."):
            prompt = """
            Actúa como un analista comercial de calle. Tu objetivo es armar un reporte detallado.
            1. ICB en 0: Alerta máxima.
            2. Metas de Venta y Saldo: Prioridad secundaria.
            3. Claro Pay: Menor urgencia.
            FORMATO: Usa ### Nombre del Cliente y viñetas (*). 
            ESTRUCTURA: Devuélveme dos secciones: 'REPORTE TOTAL' y 'TOP 15 MÁS URGENTES'.
            """
            try:
                response = model.generate_content([prompt, image])
                st.session_state['reporte_completo'] = response.text
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error en la generación: {e}")

if 'reporte_completo' in st.session_state:
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📲 Descargar TODO", st.session_state['reporte_completo'], "reporte_total.txt")
    with col2:
        top15 = st.session_state['reporte_completo'].split("TOP 15 MÁS URGENTES")[1] if "TOP 15 MÁS URGENTES" in st.session_state['reporte_completo'] else st.session_state['reporte_completo']
        st.download_button("🔥 Descargar TOP 15", top15, "top_15_criticos.txt")
