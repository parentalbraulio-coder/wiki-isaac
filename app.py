import streamlit as st
import google.generativeai as genai

# 1. Configuración de la API Key desde Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Falta la clave GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# 2. Cargar el archivo de la Wiki
try:
    with open("wiki_isaac.txt", "r", encoding="utf-8") as f:
        datos_isaac = f.read()[:15000]
except FileNotFoundError:
    datos_isaac = "Información general sobre The Binding of Isaac."

# 3. Configuración del modelo Gemini
instrucciones = f"""
Eres un experto en el juego The Binding of Isaac.
Responde SIEMPRE en español de forma clara, directa y concisa.
Usa esta información de referencia para responder a las dudas:

{datos_isaac}
"""

modelo = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instrucciones
)

# 4. Interfaz de chat
st.title("📦 Wiki IA - The Binding of Isaac")
st.write("Pregúntame sobre cualquier objeto, personaje o sinergia del juego.")

if "historial" not in st.session_state:
    st.session_state.historial = []

for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

pregunta = st.chat_input("Escribe tu duda aquí...")

if pregunta:
    st.session_state.historial.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.write(pregunta)

    with st.chat_message("assistant"):
        try:
            chat = modelo.start_chat()
            respuesta = chat.send_message(pregunta)
            st.write(respuesta.text)
            st.session_state.historial.append({"role": "assistant", "content": respuesta.text})
        except Exception as e:
            st.error(f"Error al procesar la respuesta: {e}")
