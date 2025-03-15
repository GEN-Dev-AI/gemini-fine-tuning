import os
from google import genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  
API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY) 
model_name = "gemini-1.5-flash-001-tuning"

st.set_page_config(page_title="Asistente gastronómico", page_icon="🍔")

st.title("Asistente gastronómico 👨🏽‍🍳🤖🍔")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Escribe tu mensaje aqui"):
    with st.chat_message("user"):
        st.markdown(f"Yo: {prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})

    responseFromGemini =  client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
    response = f"Gastro-bot: {responseFromGemini.candidates[0].content.parts[0].text}"

    with st.chat_message("assistant"):
        st.markdown(response)
        
    st.session_state.messages.append({"role": "assistant", "content": response})