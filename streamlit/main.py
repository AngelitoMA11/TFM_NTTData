import streamlit as st


st.set_page_config(page_title="TFM NTT Data", layout="wide")

# Espaciado superior
st.markdown("<br><br>", unsafe_allow_html=True)

# Centrar contenido
col1, col2, col3 = st.columns([3, 4, 3])

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

with col2:
    st.image("assets/logo.png", width=750)

with col2:
    st.markdown("""
        <h1 style="text-align: center; font-size: 40px; margin-bottom: 0.2em;">Bienvenido a la página interactiva de NTT Data</h1>
        <p style="text-align: center; font-size: 22px; margin-bottom: 0.5em;">
            Este entorno ha sido diseñado para facilitarte dos tareas clave en cualquier proyecto que tengas en mente:

- 🧠 Obtener recomendaciones de modelos mediante un chatbot inteligente.
- 🧹 Limpiar y preparar tus datasets de forma visual e intuitiva.

Selecciona una de las opciones para comenzar a trabajar.
        </p>
        <p style="text-align: center; font-size: 18px; margin-bottom: 2em;">¿Qué deseas hacer?</p>
    """, unsafe_allow_html=True)

    # Botones personalizados con CSS
    st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            font-size: 18px;
            padding: 0.75em 0;
            margin-bottom: 1em;
            background-color: #00539f;
            color: white;
            border: none;
        }
        .stButton > button:hover {
            background-color: #0074d9;
            color: #fff;
        }
        </style>
    """, unsafe_allow_html=True)

    b1, b2, b3 = st.columns([1, 0.2, 1])
    with b1:
        if st.button("🧠 Ir al Chatbot"):
            st.switch_page("pages/chatbot.py")
    with b3:
        if st.button("🧹 Herramienta de Limpieza"):
            st.switch_page("pages/limpieza.py")