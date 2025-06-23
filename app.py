# app.py

import streamlit as st
from langdetect import detect, LangDetectException
from agents.prompt_guard import is_safe
from agents.policy_enforcer import has_permission

# --- Configuración de la Página ---
st.set_page_config(page_title="Sistema de Gobernanza de IA", layout="centered")
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
st.write("Escribe una consulta para el asistente financiero. El sistema la analizará basado en tu rol y el contenido del prompt.")
user_prompt = st.text_input("Escribe tu consulta aquí (en español o inglés):", key="prompt_input")

if user_prompt:
    try:
        # 1. Detección de Idioma
        lang = detect(user_prompt)
        st.info(f"Idioma detectado: **{lang}**")

        # --- Cadena de Agentes de Gobernanza ---
        # Agente 1: Prompt Guard (Seguridad básica)
        if is_safe(prompt=user_prompt, language=lang):
            # Si es seguro, pasa al siguiente agente
            # Agente 2: Policy Enforcer (Permisos por rol)
            if has_permission(prompt=user_prompt, role=user_role, language=lang):
                st.success("✅ Acceso permitido. El prompt es seguro y tienes los permisos necesarios.")
                st.write("*En un sistema real, aquí se haría la llamada al LLM de Amazon Bedrock.*")
            else:
                st.warning("⚠️ Acceso denegado. No tienes los permisos necesarios para realizar esta consulta.")
        else:
            st.error("❌ Prompt no seguro. La solicitud ha sido bloqueada por contenido inapropiado.")
    
    except LangDetectException:
        st.warning("No se pudo detectar el idioma. Por favor, escribe una frase más larga.")
    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado: {e}")