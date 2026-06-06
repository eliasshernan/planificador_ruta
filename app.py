import streamlit as st
from PIL import Image
from google import genai
import io
import os

# Configuración de la página
st.set_page_config(page_title="Planificador Litoral Móvil", layout="wide")

# Logo corporativo
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
    with st.spinner("Analizando con el desglose detallado..."):
        # Prompt con tu desglose preferido y la jerarquía de prioridades
        prompt = """
        Actúa como un analista comercial. Tu objetivo es armar un reporte detallado.
        
        JERARQUÍA Y PRIORIDAD:
        1. ICB en 0: Alerta máxima.
        2. Metas de Venta y Saldo: Prioridad secundaria.
        3. Claro Pay: Importante pero menos urgente.

        FORMATO DE SALIDA (ESTRICTO):
        - Usa ### Nombre del Cliente para los títulos.
        - BAJO cada nombre, coloca las alertas en viñetas (*).
        - Desglosa la información para que sea útil al vendedor:
          - Si 'ICB Al' > 0 pero 'I' = 0: "* El mes pasado hizo [X] icb y este mes 0, ¡foco acá!"
          - Si 'Saldo' > $2.000 y 'Sell Out' = 0: "* Tiene saldo disponible pero NO HA VENDIDO NADA este mes."
          - Si 'Tiene Claro P' es Sí pero '% Claro P' es 0,00%: "* No compró saldo por Claro Pay este mes."
          - Si 'Sell Out' < $13.000: "* Le faltan $[Monto restante] para cumplir la meta."
        
        ESTRUCTURA:
        Devuélveme dos secciones claramente tituladas: 'REPORTE TOTAL' y 'TOP 15 MÁS URGENTES'.
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
        texto = st.session_state['reporte_completo']
        # Lógica para extraer solo el bloque del Top 15
        top15 = texto.split("TOP 15 MÁS URGENTES")[1] if "TOP 15 MÁS URGENTES" in texto else texto
        st.download_button("🔥 Descargar solo el TOP 15", top15, "top_15_criticos.txt")
