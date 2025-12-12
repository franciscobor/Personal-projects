import streamlit as st
import random
import time

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("Ineficiencias")

# Mensaje de bienvenida
with st.chat_message("assistant"):
    st.write("Hola 👋")

# Iniciamos historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Muestra historial de mensajes en el chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Reacción al prompt
if prompt := st.chat_input("Preguntame"):
    # Muestra mensaje del usuario en el contenedor del chat
    with st.chat_message("user"):
        st.markdown(prompt)
    # Añade el mensaje del usuario al historial del chat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Muestra la respuesta del asistente en el contnedor de chat
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Añade el mensaje del asistente al historial del chat
    st.session_state.messages.append({"role": "assistant", "content": response})