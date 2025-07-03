import streamlit as st
import requests
import os

st.title("🤖 Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu consulta:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                url = os.getenv("AGENT_URL")  
                response = requests.post(
                    f"{url}/preguntar",
                    json={"text": prompt}
                )
                if response.status_code == 200:
                    respuesta = response.json().get("respuesta", "")
                else:
                    respuesta = f"Error {response.status_code}: {response.text}"
            except Exception as e:
                respuesta = f"Fallo la petición: {e}"
            st.markdown(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})