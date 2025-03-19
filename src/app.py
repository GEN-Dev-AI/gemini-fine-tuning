import os
from google import genai
import streamlit as st
from dotenv import load_dotenv
# from google.genai import types


load_dotenv()  
API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY) 
# model_name = "gemini-1.5-flash-001-tuning"

# for model_info in client.models.list():
#     print(model_info.name)

# create tuning model
# training_dataset =  [
#     ["¿Cómo diferencio el corte juliana del brunoise?", "🥕 Juliana: tiras finas y largas. 🔪 Brunoise: cubos pequeños."],
#     ["¿Cómo hacer un roux sin grumos?", "🍞 Derrite mantequilla, agrega harina y remueve constantemente."],
#     ["¿Por qué es importante la mise en place?", "🍽️ Tener todo listo antes de cocinar ahorra tiempo y evita errores."],
#     ["¿Qué métodos de cocción existen?", "🔥 Hervido, asado, frito, al vapor, salteado… ¡Cada técnica cambia el sabor!"],
#     ["¿Cómo evitar que los huevos revueltos queden gomosos?", "🍳 Usa fuego bajo, remueve con suavidad y retira antes de que se sequen."],
#     ["¿Por qué la sal es importante en panadería?", "🥖 Controla la fermentación, mejora el sabor y da estructura."],
#     ["¿Cómo recuperar una mayonesa cortada?", "🥚 Agrega una yema extra y emulsiona poco a poco. ¡Magia! ✨"],
#     ["¿Cómo saber si un filete está en su punto sin termómetro?", "🥩 Usa la prueba del tacto con la mano. (Tierno = rojo, firme = bien cocido)."],
#     ["¿Cómo lograr una pasta cremosa sin crema?", "🍝 Usa agua de cocción, queso 🧀 y mantequilla 🧈 para una salsa sedosa."],
#     ["¿Qué cortes de carne son mejores para estofar? ", "🐄 Osobuco, falda, carrillera, pecho. Más colágeno = más jugosidad."],
#     ["¿Cómo hacer una bechamel sin grumos?", "🥛 Agrega la leche caliente poco a poco mientras bates con energía."],
#     ["¿Diferencia entre levadura fresca y seca?", "🍞 Fresca = más humedad. 🌾 Seca = concentrada y dura más tiempo."],
#     ["¿Cómo evitar que el arroz quede pastoso?", "🍚 Lávalo bien antes de cocinar y usa la proporción correcta de agua."],
#     ["¿Por qué mi bizcocho no sube?", "🎂 Puede ser por levadura vieja, horno frío o abrir la puerta antes de tiempo."],
#     ["¿Cuánto tiempo debe reposar la carne después de cocinarla?", "🥩 De 5 a 10 minutos para que los jugos se redistribuyan."],
# ]
# training_dataset=types.TuningDataset(
#         examples=[
#             types.TuningExample(
#                 text_input=i,
#                 output=o,
#             )
#             for i,o in training_dataset
#         ],
#     )
# tuning_job = client.tunings.tune(
#     base_model='models/gemini-1.5-flash-001-tuning',
#     training_dataset=training_dataset,
#     config=types.CreateTuningJobConfig(
#         epoch_count= 5,
#         batch_size=4,
#         learning_rate=0.001,
#         tuned_model_display_name="gastronomic-assistant"
#     )
# )

# # generate content with the tuned model
# response = client.models.generate_content(
#     model=tuning_job.tuned_model.model,
#     contents='¿Por qué mi bizcocho no sube?',
# )

# # generate content with the tuned model
# response = client.models.generate_content(
#     model="tunedModels/asistente-de-gastronomia-6aszd436vezn",
#     contents='¿Por qué mi bizcocho no sube?',
# )

# print(response.text)



model_name = "tunedModels/asistente-de-gastronomia-6aszd436vezn"

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