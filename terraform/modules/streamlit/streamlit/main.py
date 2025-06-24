import streamlit as st
import requests
import os

CLOUD_FUNCTION_URL =  os.getenv("FUNCTION_LIMPIEZA")

# Configuración de la página
st.set_page_config(page_title="TFM NTT Data", layout="wide")

# Barra lateral
with st.sidebar:
    st.image("assets/logo.png", width=150)
    st.markdown("<h2 style='text-align: center;'>TFM NTT Data</h2>", unsafe_allow_html=True)

# Título central
st.markdown("<h1 style='text-align: center; font-size: 50px;'>TFM NTT Data</h1>", unsafe_allow_html=True)
st.markdown("---")

# Tabs para navegación
tab1, tab2 = st.tabs(["🤖 Chatbot", "🧹 Limpieza del Dataset"])

with tab1:
    st.subheader("Asistente IA para consultas de mejor modelo")
    st.markdown("Aquí se pondra interactuar con el chatbot (a implementar).")

with tab2:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Sube un archivo CSV para procesarlo")
        uploaded_file = st.file_uploader("Selecciona el archivo", type=["csv"], label_visibility="collapsed")

        if uploaded_file is not None:
            st.write(f"Archivo subido: {uploaded_file.name}")
            if st.button("Enviar a procesar"):
                files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
                try:
                    response = requests.post(CLOUD_FUNCTION_URL, files=files)
                    if response.status_code == 200:
                        st.success("Archivo procesado correctamente.")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Fallo la petición: {e}")