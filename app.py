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
from utils.dynamodb_helpers import update_feedback

# --- Configuración de la Página ---
st.set_page_config(page_title="Sistema de Gobernanza de IA", layout="wide", initial_sidebar_state="expanded")
st.title("Sistema de Gobernanza Multiagente para IA 🤖")
st.header("Asistente Financiero Bilingüe")
st.markdown("Esta es una demostración de un sistema de IA con múltiples agentes de gobernanza que analizan las solicitudes de los usuarios en tiempo real. Selecciona un rol y escribe una consulta para ver cómo reacciona el sistema.")
st.divider()

# --- Simulación de Roles de Usuario ---
st.sidebar.title("Configuración de Simulación")
user_role = st.sidebar.selectbox("Selecciona tu rol:", ("Usuario Anónimo", "Usuario Registrado", "Gestor Financiero"))
st.sidebar.info(f"Actualmente operando como: **{user_role}**")

# --- Lógica de Feedback ---
if 'log_id' not in st.session_state:
    st.session_state.log_id = None

def handle_feedback(feedback_type):
    if st.session_state.log_id:
        if update_feedback(st.session_state.log_id, feedback_type):
            st.toast(f"¡Gracias por tu feedback: {feedback_type}!", icon="👍" if feedback_type == 'positive' else '👎')
        else:
            st.toast("Error al guardar tu feedback.", icon="❌")

# --- Interfaz Principal ---
user_prompt = st.text_input("Escribe tu consulta aquí (en español o inglés):", key="prompt_input")

if user_prompt:
    log_data = {"user_role": user_role, "user_prompt": user_prompt}
    
    try:
        lang = detect(user_prompt)
        log_data['language_detected'] = lang
        with st.expander("Ver detalles técnicos"):
            st.info(f"Idioma detectado: **{lang}**")

        if is_safe(prompt=user_prompt, language=lang):
            log_data['prompt_guard_passed'] = True
            if has_permission(prompt=user_prompt, role=user_role, language=lang):
                log_data['policy_enforcer_passed'] = True
                
                with st.spinner("El asistente de IA está pensando..."):
                    final_prompt = f"Eres un asistente financiero. Responde a la siguiente pregunta: {user_prompt}"
                    response = invoke_model(prompt=final_prompt)
                
                log_data['llm_original_response'] = response
                
                if audit_output(response):
                    log_data['output_auditor_passed'] = True
                    st.success("✅ Respuesta generada exitosamente.", icon="🤖")
                    st.markdown(response)
                    st.session_state.log_id = log_interaction(log_data) # Guardamos el ID del log
                    
                    # --- Botones de Feedback ---
                    col1, col2, _ = st.columns([1, 1, 10])
                    col1.button("👍 Útil", on_click=handle_feedback, args=('positive',))
                    col2.button("👎 No útil", on_click=handle_feedback, args=('negative',))
                else:
                    log_data['output_auditor_passed'] = False
                    st.warning("La respuesta generada por el modelo no cumple con las políticas de salida y no puede ser mostrada.", icon="🛡️")
                    st.session_state.log_id = log_interaction(log_data)
            else:
                log_data['policy_enforcer_passed'] = False
                st.warning("⚠️ Acceso denegado. No tienes los permisos necesarios para realizar esta consulta.", icon="🔒")
                with st.spinner("Generando explicación..."):
                    reason = get_rejection_reason(user_prompt, "Permisos insuficientes", lang)
                st.error(reason, icon="🛡️")
                log_data['advisory_agent_response'] = reason
                st.session_state.log_id = log_interaction(log_data)
        else:
            log_data['prompt_guard_passed'] = False
            st.error("❌ Solicitud bloqueada por contenido inapropiado.", icon="🚫")
            with st.spinner("Generando explicación..."):
                reason = get_rejection_reason(user_prompt, "Contenido inapropiado detectado", lang)
            st.warning(reason, icon="🛡️")
            log_data['advisory_agent_response'] = reason
            st.session_state.log_id = log_interaction(log_data)
    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado: {e}")
        log_data['error'] = str(e)
        st.session_state.log_id = log_interaction(log_data)