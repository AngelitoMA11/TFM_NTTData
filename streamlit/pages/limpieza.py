import streamlit as st
import requests
import os

st.title("🧹 Limpieza del Dataset")
CLOUD_FUNCTION_URL = os.getenv("FUNCTION_LIMPIEZA")

uploaded_file = st.file_uploader("Selecciona el archivo CSV", type=["csv"])

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