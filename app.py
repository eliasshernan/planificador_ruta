import streamlit as st
from PIL import Image
from google import genai
import os

st.set_page_config(page_title="Planificador Litoral Móvil", layout="wide")

try:
    if os.path.exists("logo_empresa.png"):
        st.image("logo_empresa.png", width=400)
except Exception: pass

st.title("📋 Planificador de Ruta Comercial")

API_KEY = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    st.error("Error: API Key no configurada.")
    st.stop()

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Error al iniciar cliente: {e}")
    st.stop()

uploaded_file = st.file_uploader("Subí tu planilla:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    if st.button("🚀 Generar Reportes"):
        with st.spinner("Conectando y analizando..."):
            prompt = """
            Actúa como un analista comercial de calle. Tu objetivo es armar un reporte detallado para el vendedor.
            1. ICB en 0: Alerta máxima (primero).
            2. Metas de Venta y Saldo: Prioridad secundaria.
            3. Claro Pay: Menor urgencia.
            FORMATO: Usa ### Nombre del Cliente y viñetas (*). Desglosa las alertas tal como te indiqué anteriormente.
            ESTRUCTURA: Devuélveme dos secciones: 'REPORTE TOTAL' y 'TOP 15 MÁS URGENTES'.
            """
            
            try:
                # Usamos gemini-1.5-flash-latest, que suele resolver el problema de versión
                response = client.models.generate_content(
                    model='gemini-1.5-flash-latest', 
                    contents=[image, prompt]
                )
                st.session_state['reporte_completo'] = response.text
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error de conexión con el modelo: {e}")
                st.info("Intenta verificar en Google AI Studio si tu API Key tiene acceso al modelo 'gemini-1.5-flash-latest'.")

if 'reporte_completo' in st.session_state:
    st.markdown("---")
    st.markdown("### 💾 Opciones de Descarga")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📲 Descargar TODO el reporte", st.session_state['reporte_completo'], "reporte_total.txt")
    with col2:
        texto = st.session_state['reporte_completo']
        top15 = texto.split("TOP 15 MÁS URGENTES")[1] if "TOP 15 MÁS URGENTES" in texto else texto
        st.download_button("🔥 Descargar solo el TOP 15", top15, "top_15_criticos.txt")
