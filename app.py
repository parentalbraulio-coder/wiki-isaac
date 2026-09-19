import streamlit as st
import google.generativeai as genai

# 1. Configurar la página web
st.set_page_config(page_title="Wiki Isaac IA", page_icon="📦")
st.title("📦 Wiki IA de Isaac")

# 2. Poner tu clave de API (reemplaza lo que está entre comillas)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Cargar la información de tu archivo de texto
try:
    with open("wiki_isaac.txt", "r", encoding="utf-8") as archivo:
        datos_isaac = archivo.read()
except FileNotFoundError:
    datos_isaac = "No se encontró el archivo de datos."

# 4. Instrucciones para la IA
instrucciones = f"""
Eres un experto en el juego The Binding of Isaac. 
Responde SIEMPRE en español de forma clara y directa.
Usa esta información para responder a las dudas de los usuarios:

{datos_isaac}
"""

modelo = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    system_instruction=instrucciones
)

# 5. Interfaz de chat
if "historial" not in st.session_state:
    st.session_state.historial = []

for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if pregunta := st.chat_input("Pregunta algo sobre un objeto, personaje o sinergia..."):
    st.session_state.historial.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.write(pregunta)

    with st.chat_message("assistant"):
        chat = modelo.start_chat()
        respuesta = chat.send_message(pregunta)
        st.write(respuesta.text)
        
    st.session_state.historial.append({"role": "assistant", "content": respuesta.text})