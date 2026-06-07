import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Planificador Litoral", layout="wide")

st.title("📋 Planificador de Ruta Comercial")

# Configuración de API Key desde los Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Por favor, configura la GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Configuración del modelo
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

uploaded_file = st.file_uploader("Subí tu planilla:", type=["jpg", "png", "jpeg"])

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
                st.session_state['reporte'] = response.text
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error al generar: {e}")

if 'reporte' in st.session_state:
    st.markdown("---")
    st.download_button("Descargar Reporte", st.session_state['reporte'], "reporte.txt")
