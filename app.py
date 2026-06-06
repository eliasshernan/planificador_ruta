import streamlit as st
from PIL import Image
import google.generativeai as genai # Cambiamos la librería aquí
import os

# Configuración de la página
st.set_page_config(page_title="Planificador Litoral Móvil", layout="wide")

# Logo corporativo
try:
    if os.path.exists("logo_empresa.png"):
        st.image("logo_empresa.png", width=400)
except Exception: pass

st.title("📋 Planificador de Ruta Comercial")

# Configuración API Key (usamos la misma variable)
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("Error: API Key no configurada en los Secrets.")
    st.stop()

# Configuración estable de la librería clásica
try:
    genai.configure(api_key=API_KEY)
    # Usamos el modelo estable
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error al configurar la IA: {e}")
    st.stop()

uploaded_file = st.file_uploader("Subí tu planilla:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    if st.button("🚀 Generar Reportes"):
        with st.spinner("Analizando con el motor estable..."):
            prompt = """
            Actúa como un analista comercial de calle. Tu objetivo es armar un reporte detallado.
            1. ICB en 0: Alerta máxima.
            2. Metas de Venta y Saldo: Prioridad secundaria.
            3. Claro Pay: Menor urgencia.
            FORMATO: Usa ### Nombre del Cliente y viñetas (*). Desglosa las alertas tal como te indiqué anteriormente.
            ESTRUCTURA: Devuélveme dos secciones: 'REPORTE TOTAL' y 'TOP 15 MÁS URGENTES'.
            """
            
            try:
                # Llamada directa al modelo
                response = model.generate_content([prompt, image])
                st.session_state['reporte_completo'] = response.text
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error crítico en la generación: {e}")

# Opciones de descarga
if 'reporte_completo' in st.session_state:
    st.markdown("---")
    st.markdown("### 💾 Opciones de Descarga")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📲 Descargar TODO el reporte", st.session_state['reporte_completo'], "reporte_total.txt")
    with col2:
        texto = st.session_state['reporte_completo']
        # Buscamos el corte para el top 15
        if "TOP 15 MÁS URGENTES" in texto:
            top15 = texto.split("TOP 15 MÁS URGENTES")[1]
        else:
            top15 = texto
        st.download_button("🔥 Descargar solo el TOP 15", top15, "top_15_criticos.txt")
