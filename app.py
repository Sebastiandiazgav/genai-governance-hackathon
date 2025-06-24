# app.py

import streamlit as st
from langdetect import detect, LangDetectException

# Nuestros módulos locales
from agents.prompt_guard import is_safe
from agents.policy_enforcer import has_permission
from agents.advisory_agent import get_rejection_reason
from utils.bedrock_client import invoke_model

# --- Configuración de la Página ---
st.set_page_config(page_title="Sistema de Gobernanza de IA", layout="wide")
st.title("Sistema de Gobernanza Multiagente para IA 🤖")
st.header("Asistente Financiero Bilingüe")

# --- Simulación de Roles de Usuario ---
st.sidebar.title("Configuración de Simulación")
user_role = st.sidebar.selectbox(
    "Selecciona tu rol:",
    ("Usuario Anónimo", "Usuario Registrado", "Gestor Financiero")
)
st.sidebar.info(f"Actualmente operando como: **{user_role}**")

# --- Interfaz Principal ---
st.write("Escribe una consulta para el asistente financiero. El sistema la analizará antes de generar una respuesta.")
user_prompt = st.text_input("Escribe tu consulta aquí (en español o inglés):", key="prompt_input")

if user_prompt:
    try:
        lang = detect(user_prompt)
        st.info(f"Idioma detectado: **{lang}**")

        # --- Cadena de Agentes de Gobernanza ---
        if is_safe(prompt=user_prompt, language=lang):
            if has_permission(prompt=user_prompt, role=user_role, language=lang):
                st.success("✅ Acceso permitido. Generando respuesta...")
                with st.spinner("El asistente de IA está pensando..."):
                    # ¡Llamada real a Bedrock!
                    final_prompt = f"Eres un asistente financiero. Responde a la siguiente pregunta: {user_prompt}"
                    response = invoke_model(prompt=final_prompt)
                    st.markdown(response)
            else:
                # Bloqueado por el Agente de Políticas
                st.warning("⚠️ Acceso denegado por políticas de permisos.")
                with st.spinner("Generando explicación..."):
                    reason = get_rejection_reason(user_prompt, "Permisos insuficientes", lang)
                    st.error(reason)
        else:
            # Bloqueado por el Agente de Seguridad
            st.error("❌ Solicitud bloqueada por contenido inapropiado.")
            with st.spinner("Generando explicación..."):
                reason = get_rejection_reason(user_prompt, "Contenido inapropiado detectado", lang)
                st.warning(reason)
    
    except LangDetectException:
        st.warning("No se pudo detectar el idioma. Por favor, escribe una frase más larga.")
    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado: {e}")