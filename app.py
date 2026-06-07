import streamlit as st
import google.generativeai as genai

st.title("Diagnóstico de Modelos")

API_KEY = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

if st.button("Ver modelos disponibles"):
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
        st.write("Modelos disponibles para tu API Key:")
        st.write(models)
    except Exception as e:
        st.error(f"Error de acceso: {e}")
        st.write("Si ves un error aquí, tu API KEY no tiene permiso para acceder a NINGÚN modelo.")
