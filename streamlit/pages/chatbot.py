import streamlit as st
import requests
import os
from google.cloud import firestore

FIRESTORE = os.getenv("firestore_url", "chatbot-conversations")
db = firestore.Client(database=FIRESTORE)

# ESTILOS MEJORADOS
st.markdown("""
    <style>
        .block-container {
            max-width: 1000px;
            padding-top: 3rem;
            margin: auto;
        }
        h1 {
            font-size: 2.5rem;
        }
        h3 {
            margin-top: 2rem;
        }
        p {
            font-size: 1.1rem;
        }
        button[kind="secondary"] {
            font-size: 1rem;
            padding: 0.5rem 1.25rem;
        }
    </style>
""", unsafe_allow_html=True)

# Estado inicial
if "user_step" not in st.session_state:
    st.session_state.user_step = None
if "username" not in st.session_state:
    st.session_state.username = ""
if "selected_conversation" not in st.session_state:
    st.session_state.selected_conversation = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Funciones
def crear_usuario(nombre):
    ref = db.collection("usuarios").document(nombre)
    if not ref.get().exists:
        ref.set({"conversaciones": []})

def usuario_existe(nombre):
    return db.collection("usuarios").document(nombre).get().exists

def obtener_conversaciones(nombre):
    doc = db.collection("usuarios").document(nombre).get()
    if doc.exists:
        return doc.to_dict().get("conversaciones", [])
    return []

def guardar_conversacion(nombre, titulo, mensajes):
    ref = db.collection("usuarios").document(nombre)
    convs = obtener_conversaciones(nombre)
    convs.append({"titulo": titulo, "mensajes": mensajes})
    ref.update({"conversaciones": convs})

# Pantalla de inicio
if st.session_state.user_step is None:
    st.title("🤖 Chatbot")
    st.markdown("""
    <p>Bienvenido a tu asistente de selección de modelos de lenguaje.</p>
    <p>Este chatbot te ayudará a identificar qué modelo de IA se adapta mejor a tus necesidades, ya sea generación de video, imágenes, transcripción de audios a texto... Además, si quieres montar tu propio modelo, te diremos qué necesitas y cuánto cuesta.</p>
    <p>Para guardar tu progreso y tus conversaciones personalizadas, necesitas un nombre de usuario.</p>
    """, unsafe_allow_html=True)

    st.markdown("### ¿Cómo quieres continuar?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🙋 Ya tengo usuario", key="btn_login_inicio"):
            st.session_state.user_step = "login"
            st.session_state._rerun = True
    with col2:
        if st.button("🆕 Soy nuevo", key="btn_register_inicio"):
            st.session_state.user_step = "register"
            st.session_state._rerun = True

# Registro
elif st.session_state.user_step == "register":
    st.markdown("### 🆕 Crear un nuevo usuario")
    st.markdown("""
    <p>Elige un nombre de usuario único para comenzar tu experiencia con el chatbot.</p>
    <p>Este nombre te permitirá recuperar tus conversaciones más adelante.</p>
    """, unsafe_allow_html=True)

    with st.form("form_registro"):
        username = st.text_input("🧑 Nuevo nombre de usuario", key="register_user_form")
        submitted = st.form_submit_button("✅ Registrarme y empezar")

        if submitted:
            if username:
                if usuario_existe(username):
                    st.error("⚠️ Ese usuario ya existe, por favor elige otro nombre.")
                else:
                    crear_usuario(username)
                    st.session_state.username = username
                    st.session_state.messages = []
                    st.session_state.selected_conversation = "Nueva conversación"
                    st.session_state.user_step = "chat"
                    st.session_state._rerun = True
            else:
                st.warning("Por favor, introduce un nombre de usuario.")

    if st.button("⬅️ Volver al inicio", key="btn_volver_registro"):
        st.session_state.user_step = None
        st.session_state.username = ""
        st.session_state.selected_conversation = None
        st.session_state.messages = []
        st.session_state._rerun = True

# Login
elif st.session_state.user_step == "login":
    st.markdown("### 🔐 Accede con tu usuario")
    st.markdown("""
    <p>Introduce tu nombre de usuario para recuperar tus conversaciones anteriores.</p>
    <p>Si no tienes uno aún, puedes volver atrás y registrarte.</p>
    """, unsafe_allow_html=True)

    username = st.text_input("👤 Nombre de usuario", key="login_user")

    col_login, col_back = st.columns([2, 1])
    with col_login:
        if username:
            if usuario_existe(username):
                st.session_state.username = username
                conversaciones = obtener_conversaciones(username)
                opciones = [conv["titulo"] for conv in conversaciones] + ["Nueva conversación"]
                seleccion = st.selectbox("📁 Selecciona una conversación:", opciones)
                st.session_state.selected_conversation = seleccion
                if seleccion == "Nueva conversación":
                    st.session_state.messages = []
                else:
                    idx = opciones.index(seleccion)
                    st.session_state.messages = conversaciones[idx]["mensajes"]
                if st.button("➡️ Continuar", key="btn_continuar_login"):
                    st.session_state.user_step = "chat"
                    st.session_state._rerun = True
            else:
                st.error("❌ Usuario no encontrado. ¿Quieres registrarte?")
    with col_back:
        if st.button("⬅️ Volver al inicio", key="btn_volver_login"):
            st.session_state.user_step = None
            st.session_state.username = ""
            st.session_state.selected_conversation = None
            st.session_state.messages = []
            st.session_state._rerun = True


 # Chatbot
elif st.session_state.user_step == "chat":
    # Saludo con tema si está definido
    titulo_chat = f"## 🧠 Bienvenido al chatbot, **{st.session_state.username}**"
    if "titulo_conv" in st.session_state and st.session_state.titulo_conv:
        titulo_chat += f" · Tema: **{st.session_state.titulo_conv}**"
    st.markdown(titulo_chat)

    # Tema de nueva conversación (solo una vez)
    if st.session_state.selected_conversation == "Nueva conversación":
        if "titulo_conv" not in st.session_state:
            st.markdown("#### 🧩 ¿Qué tema te gustaría tratar?")
            tema = st.text_input("📝 Tema de la conversación:", key="tema_input")
            if tema:
                st.session_state.titulo_conv = tema
                st.rerun()

        else:
            st.markdown(f"#### 🧩 Tema seleccionado: **{st.session_state.titulo_conv}**")

    if st.button("🧹 Limpiar conversación", key="btn_limpiar"):
        st.session_state.messages = []
        st.session_state._rerun = True

    # Mostrar mensajes anteriores
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada de usuario
    if st.session_state.selected_conversation:
        if prompt := st.chat_input("Escribe tu consulta:"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    try:
                        url = os.getenv("AGENT_URL")
                        response = requests.post(f"{url}/preguntar", json={"text": prompt})
                        if response.status_code == 200:
                            respuesta = response.json().get("respuesta", "")
                        else:
                            respuesta = f"Error {response.status_code}: {response.text}"
                    except Exception as e:
                        respuesta = f"Fallo la petición: {e}"
                    st.markdown(respuesta)
                    st.session_state.messages.append({"role": "assistant", "content": respuesta})

            # Guardar automáticamente
            if st.session_state.selected_conversation == "Nueva conversación":
                if "titulo_conv" in st.session_state and st.session_state.titulo_conv:
                    guardar_conversacion(
                        st.session_state.username,
                        st.session_state.titulo_conv,
                        st.session_state.messages
                    )
                    st.session_state.selected_conversation = st.session_state.titulo_conv
                    st.rerun()

            else:
                conversaciones = obtener_conversaciones(st.session_state.username)
                for conv in conversaciones:
                    if conv["titulo"] == st.session_state.selected_conversation:
                        conv["mensajes"] = st.session_state.messages
                        break
                db.collection("usuarios").document(st.session_state.username).update({
                    "conversaciones": conversaciones
                })

    # Botón para cerrar sesión
    st.markdown("---")
    if st.button("🔄 ¿Eres un usuario distinto?", key="btn_cambiar_usuario"):
        st.session_state.user_step = None
        st.session_state.username = ""
        st.session_state.selected_conversation = None
        st.session_state.messages = []
        if "titulo_conv" in st.session_state:
            del st.session_state.titulo_conv
        st.session_state._rerun = True
