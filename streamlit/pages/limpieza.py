import streamlit as st
import requests
import os

# Estilos para hacer la página más grande y el título centrado y grande
st.markdown("""
<style>
.block-container {
    max-width: 1000px !important;
    margin: auto;
}
.titulo-limpieza {
    text-align: center;
    font-size: 3.5em !important;
    font-weight: bold;
    margin-bottom: 0.2em;
}
h3 {
    font-size: 2.2em !important;
}
p, li {
    font-size: 1.3em !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo-limpieza">🧹 Proceso de Limpieza de Datasets CSV</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;">
    <h3>Bienvenido al portal de preprocesamiento de datos para BigQuery</h3>
    <p>
        Carga tu archivo CSV para iniciar el pipeline automatizado de limpieza y preparación.<br>
        El sistema aplicará transformaciones predefinidas para optimizar la calidad del dataset antes de su ingestión en BigQuery.
    </p>
    <div style="text-align:left; display:inline-block;">
        <b>Características del proceso:</b>
        <ul>
            <li>• Eliminación de registros duplicados basados en claves definidas</li>
            <li>• Estandarización de formatos (fechas, decimales, strings)</li>
            <li>• Imputación o eliminación de valores nulos según reglas</li>
            <li>• Validación estructural contra esquema BigQuery</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

CLOUD_FUNCTION_URL = os.getenv("FUNCTION_LIMPIEZA")

uploaded_file = st.file_uploader("Selecciona el archivo CSV", type=["csv"])

if uploaded_file is not None:
    st.success(f"Archivo subido: {uploaded_file.name}")
    st.markdown("Haz clic en <b>Enviar a procesar</b> para limpiar tu dataset.", unsafe_allow_html=True)
    if st.button("Enviar a procesar"):
        files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
        try:
            with st.spinner("Procesando archivo..."):
                response = requests.post(CLOUD_FUNCTION_URL, files=files)
            if response.status_code == 200:
                st.success("Archivo procesado correctamente.")
                if response.headers.get("Content-Type") == "text/csv":
                    st.download_button(
                        label="Descargar CSV limpio",
                        data=response.content,
                        file_name=f"limpio_{uploaded_file.name}",
                        mime="text/csv"
                    )
                else:
                    st.info("Procesamiento completado.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Fallo la petición: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")