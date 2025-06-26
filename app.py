# app.py

import streamlit as st
from langdetect import detect, LangDetectException

# Nuestros módulos locales
from agents.prompt_guard import is_safe
from agents.policy_enforcer import has_permission
from agents.advisory_agent import get_rejection_reason
from agents.output_auditor import audit_output
from agents.audit_logger import log_interaction
from utils.bedrock_client import invoke_model

# --- Configuración de la Página ---
st.set_page_config(page_title="Sistema de Gobernanza de IA", layout="wide")
st.title("Sistema de Gobernanza Multiagente para IA 🤖")
st.header("Asistente Financiero Bilingüe")

# --- Simulación de Roles de Usuario ---
st.sidebar.title("Configuración de Simulación")
user_role = st.sidebar.selectbox("Selecciona tu rol:", ("Usuario Anónimo", "Usuario Registrado", "Gestor Financiero"))
st.sidebar.info(f"Actualmente operando como: **{user_role}**")

# --- Interfaz Principal ---
st.write("Escribe una consulta para el asistente financiero. El sistema la analizará antes de generar una respuesta.")
user_prompt = st.text_input("Escribe tu consulta aquí (en español o inglés):", key="prompt_input")

if user_prompt:
    # Preparamos el diccionario para el log de auditoría
    log_data = {
        "user_role": user_role,
        "user_prompt": user_prompt,
    }

    try:
        lang = detect(user_prompt)
        log_data['language_detected'] = lang
        st.info(f"Idioma detectado: **{lang}**")

        # --- Cadena de Agentes ---
        if is_safe(prompt=user_prompt, language=lang):
            log_data['prompt_guard_passed'] = True
            if has_permission(prompt=user_prompt, role=user_role, language=lang):
                log_data['policy_enforcer_passed'] = True
                st.success("✅ Acceso permitido. Generando respuesta...")
                with st.spinner("El asistente de IA está pensando..."):
                    final_prompt = f"Eres un asistente financiero. Responde a la siguiente pregunta: {user_prompt}"
                    response = invoke_model(prompt=final_prompt)
                    log_data['llm_original_response'] = response
                    
                    # Agente 4: Auditor de Salidas
                    if audit_output(response):
                        log_data['output_auditor_passed'] = True
                        st.markdown(response)
                    else:
                        log_data['output_auditor_passed'] = False
                        st.warning("La respuesta generada por el modelo no cumple con las políticas de salida y no puede ser mostrada.")
            else:
                log_data['policy_enforcer_passed'] = False
                st.warning("⚠️ Acceso denegado por políticas de permisos.")
                with st.spinner("Generando explicación..."):
                    reason = get_rejection_reason(user_prompt, "Permisos insuficientes", lang)
                    st.error(reason)
                    log_data['advisory_agent_response'] = reason
        else:
            log_data['prompt_guard_passed'] = False
            st.error("❌ Solicitud bloqueada por contenido inapropiado.")
            with st.spinner("Generando explicación..."):
                reason = get_rejection_reason(user_prompt, "Contenido inapropiado detectado", lang)
                st.warning(reason)
                log_data['advisory_agent_response'] = reason
    
    except LangDetectException:
        log_data['error'] = "LangDetectException"
        st.warning("No se pudo detectar el idioma. Por favor, escribe una frase más larga.")
    except Exception as e:
        log_data['error'] = str(e)
        st.error(f"Ha ocurrido un error inesperado: {e}")
    finally:
        # Agente 5: Registrador de Auditoría - siempre se ejecuta
        log_interaction(log_data)
        st.sidebar.success("La interacción ha sido registrada en el log de auditoría.")