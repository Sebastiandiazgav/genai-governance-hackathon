# app.py

import streamlit as st
from langdetect import detect, LangDetectException
from agents.prompt_guard import is_safe

st.title("Sistema de Gobernanza Multiagente para IA 🤖")
st.header("Asistente Financiero Bilingüe")

st.write("Escribe una consulta para el asistente financiero. El sistema la analizará en busca de contenido inapropiado antes de procesarla.")

user_prompt = st.text_input("Escribe tu consulta aquí (en español o inglés):", key="prompt_input")

if user_prompt:
    try:
        # 1. Detección de Idioma
        lang = detect(user_prompt)
        st.info(f"Idioma detectado: **{lang}**")

        # 2. Análisis con el Agente "Prompt Guard"
        if is_safe(prompt=user_prompt, language=lang):
            st.success("✅ Prompt seguro. Listo para ser procesado por el LLM.")
            # Aquí, en el futuro, llamaríamos al modelo de Amazon Bedrock.
        else:
            st.error("❌ Prompt no seguro. La solicitud ha sido bloqueada por el Agente de Gobernanza.")
    
    except LangDetectException:
        st.warning("No se pudo detectar el idioma. Por favor, escribe una frase más larga.")
    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado: {e}")