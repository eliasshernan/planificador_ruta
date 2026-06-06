import streamlit as st
from PIL import Image
from google import genai
from google.genai import types
import io
import os

# Configuración de la página
st.set_page_config(page_title="Planificador Inteligente", layout="wide")

st.title("📋 Planificador de Ruta Comercial")
st.subheader("Subí la foto de tu ruta para analizar los objetivos críticos del día")

# CONFIGURACIÓN 100% SEGURA: La clave se maneja SÓLO desde los Secrets de Streamlit
API_KEY = None

if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
    API_KEY = os.environ["GEMINI_API_KEY"]

try:
    if API_KEY:
        client = genai.Client(api_key=API_KEY)
    else:
        # Si estás en tu PC local, te va a pedir que la pongas en la barra lateral
        st.sidebar.warning("Falta configurar la API Key.")
        api_key_manual = st.sidebar.text_input("Ingresá tu Gemini API Key de forma manual:", type="password")
        if api_key_manual:
            client = genai.Client(api_key=api_key_manual)
        else:
            client = None
except Exception as e:
    st.error(f"Error al inicializar el cliente de IA: {e}")
    client = None

uploaded_file = st.file_uploader("Selecciona la captura de la planilla...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ruta cargada exitosamente", use_container_width=True)
    
    if st.button("🚀 Analizar Ruta con IA"):
        if client is None:
            st.error("Por favor, configura la API Key en los secretos de Streamlit o en la barra lateral.")
        else:
            with st.spinner("Generando reporte estructurado por cliente..."):
                try:
                    # Prompt definitivo con separación de bloques estricta por cliente
                    prompt = """
                    Actúa como un analista comercial de calle. Tu objetivo es armar un reporte ultra corto, compacto y al grano para el vendedor. Elimina CUALQUIER tipo de introducción, saludo, texto explicativo o fecha. Empezá directamente con la información útil.

                    REGLA DE LÍMITE Y PRIORIDAD:
                    Muestra ÚNICAMENTE a los 15 clientes MÁS CRÍTICOS (filtra por saldos más bajos, saldo sin ventas o mayores caídas). Haz un corte estricto en el top 15 y descarta el resto. El informe no puede tener más de 15 clientes bajo ninguna circunstancia.

                    REGLA DE FORMATO OBLIGATORIA (SARTÉN POR EL MANGO):
                    Cada cliente debe figurar como un bloque independiente. Escribe el nombre del cliente en una línea propia usando un título de tercer nivel de Markdown (### Nombre del Cliente).
                    BAJO el nombre, coloca las alertas en renglones separados usando viñetas (*). 
                    Está TERMINANTEMENTE PROHIBIDO juntar el nombre de un cliente al final de la línea o viñeta de otro comercio. Cada cliente empieza en una línea nueva.

                    Reglas para las viñetas de cada cliente:
                    - Si 'Tiene Claro P' es No: "* No tiene Claro Pay, foco ahí." (Si es No, no pongas la alerta de % Claro P).
                    - Si 'Tiene Claro P' es Sí pero '% Claro P' es 0,00%: "* No compró saldo por Claro Pay este mes, foco ahí."
                    - Si 'Saldo' es mayor a $2.000 y 'Sell Out' es 0: "* Tiene saldo disponible pero NO HA VENDIDO NADA este mes, ¡foco crítico acá!"
                    - Si 'Saldo' es menor a $8.000: "* Tiene saldo crítico de $[Valor], gestionar compra de saldo urgente."
                    - Si 'Sell Out' es menor a $13.000: "* Le faltan $[Monto restante] para cumplir la meta."
                    - Si hay caída drástica de ventas respecto al mes anterior, agrégalo al final de la viñeta de la meta: "¡Foco y analizar caída!"
                    - Si 'ICB Al' es mayor a 0 pero 'I' es 0: "* El mes pasado hizo [X] icb y este mes 0, ¡foco acá!"

                    Estructura exacta del reporte final que debes devolver:
                    VENDEDOR: [NOMBRE EN MAYÚSCULAS]
                    Top 15 clientes críticos que necesitan foco hoy:

                    ### [Primer Cliente]
                    * [Alerta 1]
                    * [Alerta 2]

                    ### [Segundo Cliente]
                    * [Alerta 1]
                    """

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[image, prompt]
                    )
                    
                    st.session_state['reporte_texto'] = response.text
                    st.success("¡Análisis completado con éxito!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Hubo un problema al procesar la imagen con Gemini: {e}")

    if 'reporte_texto' in st.session_state:
        st.markdown("### 💾 Descargar Reporte")
        
        texto_bytes = io.BytesIO(st.session_state['reporte_texto'].encode('utf-8'))
        st.download_button(
            label="📲 Descargar para WhatsApp (.txt)",
            data=texto_bytes,
            file_name="plan_de_ruta.txt",
            mime="text/plain"
        )
        
        csv_data = "Reporte de Ruta\n\n" + st.session_state['reporte_texto']
        csv_bytes = io.BytesIO(csv_data.encode('utf-8-sig'))
        st.download_button(
            label="📊 Descargar para Excel (.csv)",
            data=csv_bytes,
            file_name="plan_de_ruta.csv",
            mime="text/csv"
        )