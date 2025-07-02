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

# --- Diccionario de Textos para UI Bilingüe ---
UI_TEXTS = {
    'lang_selector_label': {'es': "Idioma / Language", 'en': "Language / Idioma"},
    'main_title': {'es': "Sistema de Gobernanza Multiagente para IA 🤖", 'en': "Multi-Agent AI Governance System 🤖"},
    'main_header': {'es': "Asistente Financiero Bilingüe", 'en': "Bilingual Financial Assistant"},
    'main_description': {
        'es': "Esta es una demostración de un sistema de IA con múltiples agentes de gobernanza que analizan las solicitudes de los usuarios en tiempo real. Selecciona un rol y escribe una consulta para ver cómo reacciona el sistema.",
        'en': "This is a demonstration of an AI system with multiple governance agents that analyze user requests in real-time. Select a role and write a query to see how the system reacts."
    },
    'sidebar_title': {'es': "Configuración de Simulación", 'en': "Simulation Settings"},
    'role_selector_label': {'es': "Selecciona tu rol:", 'en': "Select your role:"},
    'role_info': {'es': "Actualmente operando como:", 'en': "Currently operating as:"},
    'roles': {
        'es': ('Usuario Anónimo', 'Usuario Registrado', 'Gestor Financiero'),
        'en': ('Anonymous User', 'Registered User', 'Financial Manager')
    },
    'text_input_label': {'es': "Escribe tu consulta aquí (en español o inglés):", 'en': "Write your query here (in English or Spanish):"},
    'tech_details_expander': {'es': "Ver detalles técnicos", 'en': "View technical details"},
    'lang_detected_info': {'es': "Idioma detectado:", 'en': "Language detected:"},
    'thinking_spinner': {'es': "El asistente de IA está pensando...", 'en': "The AI assistant is thinking..."},
    'explanation_spinner': {'es': "Generando explicación...", 'en': "Generating explanation..."},
    'success_message': {'es': "✅ Respuesta generada exitosamente.", 'en': "✅ Response generated successfully."},
    'permission_denied_warning': {'es': "⚠️ Acceso denegado. No tienes los permisos necesarios para realizar esta consulta.", 'en': "⚠️ Access denied. You do not have the necessary permissions for this query."},
    'inappropriate_content_error': {'es': "❌ Solicitud bloqueada por contenido inapropiado.", 'en': "❌ Request blocked due to inappropriate content."},
    'feedback_thanks': {'es': "¡Gracias por tu feedback:", 'en': "Thanks for your feedback:"},
    'feedback_error': {'es': "Error al guardar tu feedback.", 'en': "Error saving your feedback."},
    'audit_log_success': {'es': "La interacción ha sido registrada en el log de auditoría.", 'en': "Interaction has been logged to the audit trail."},
    'button_useful': {'es': "👍 Útil", 'en': "👍 Useful"},
    'button_not_useful': {'es': "👎 No útil", 'en': "👎 Not Useful"}
}

# --- Configuración de la Página ---
st.set_page_config(page_title="AI Governance System", layout="wide", initial_sidebar_state="expanded")

# --- Selector de Idioma en Sidebar ---
lang_options = {'Español': 'es', 'English': 'en'}
selected_lang_label = st.sidebar.radio(
    label=UI_TEXTS['lang_selector_label']['es'],
    options=lang_options.keys()
)
lang_code = lang_options[selected_lang_label]

# --- Interfaz Principal con Textos Dinámicos ---
# st.title(UI_TEXTS['main_title'][lang_code])
st.title("PRUEBA DE DESPLIEGUE v3 - SI VES ESTO, EL CÓDIGO ESTÁ ACTUALIZADO")
st.header(UI_TEXTS['main_header'][lang_code])
st.markdown(UI_TEXTS['main_description'][lang_code])
st.divider()

# --- Simulación de Roles de Usuario (CON LA CORRECCIÓN) ---
st.sidebar.title(UI_TEXTS['sidebar_title'][lang_code])
role_options_in_selected_lang = UI_TEXTS['roles'][lang_code]
selected_role_label = st.sidebar.selectbox(
    UI_TEXTS['role_selector_label'][lang_code],
    role_options_in_selected_lang
)
selected_index = role_options_in_selected_lang.index(selected_role_label)
user_role = UI_TEXTS['roles']['es'][selected_index]
st.sidebar.info(f"{UI_TEXTS['role_info'][lang_code]} **{selected_role_label}**")

# --- Lógica de Feedback ---
if 'log_id' not in st.session_state:
    st.session_state.log_id = None

def handle_feedback(feedback_type):
    if st.session_state.log_id:
        if update_feedback(st.session_state.log_id, feedback_type):
            st.toast(f"{UI_TEXTS['feedback_thanks'][lang_code]} {feedback_type}!", icon="👍" if feedback_type == 'positive' else '👎')
        else:
            st.toast(UI_TEXTS['feedback_error'][lang_code], icon="❌")

# --- Bloque Principal de Interacción ---
user_prompt = st.text_input(UI_TEXTS['text_input_label'][lang_code], key="prompt_input")

if user_prompt:
    log_data = {"user_role": user_role, "user_prompt": user_prompt, "ui_language": lang_code}
    
    try:
        detected_lang = detect(user_prompt)
        log_data['prompt_language_detected'] = detected_lang
        
        with st.expander(UI_TEXTS['tech_details_expander'][lang_code]):
            st.info(f"{UI_TEXTS['lang_detected_info'][lang_code]} **{detected_lang}**")

        if is_safe(prompt=user_prompt, language=detected_lang):
            log_data['prompt_guard_passed'] = True
            if has_permission(prompt=user_prompt, role=user_role, language=detected_lang):
                log_data['policy_enforcer_passed'] = True
                
                with st.spinner(UI_TEXTS['thinking_spinner'][lang_code]):
                    if detected_lang == 'es':
                        instruction = "Eres un asistente financiero experto. Responde a la siguiente pregunta de forma clara y concisa en español:"
                    else:
                        instruction = "You are an expert financial assistant. Answer the following question clearly and concisely in English:"
                    
                    final_prompt = f"{instruction} {user_prompt}"
                    response = invoke_model(prompt=final_prompt)
                
                log_data['llm_original_response'] = response
                
                if audit_output(response):
                    log_data['output_auditor_passed'] = True
                    st.success(UI_TEXTS['success_message'][lang_code], icon="🤖")
                    st.markdown(response)
                    st.session_state.log_id = log_interaction(log_data)
                    
                    col1, col2, _ = st.columns([1, 1, 10])
                    col1.button(UI_TEXTS['button_useful'][lang_code], on_click=handle_feedback, args=('positive',))
                    col2.button(UI_TEXTS['button_not_useful'][lang_code], on_click=handle_feedback, args=('negative',))
                else:
                    log_data['output_auditor_passed'] = False
                    st.warning("La respuesta generada por el modelo no cumple con las políticas de salida y no puede ser mostrada.", icon="🛡️")
                    st.session_state.log_id = log_interaction(log_data)
            else:
                log_data['policy_enforcer_passed'] = False
                st.warning(UI_TEXTS['permission_denied_warning'][lang_code], icon="🔒")
                with st.spinner(UI_TEXTS['explanation_spinner'][lang_code]):
                    reason = get_rejection_reason(user_prompt, "Permisos insuficientes", detected_lang)
                st.error(reason, icon="🛡️")
                log_data['advisory_agent_response'] = reason
                st.session_state.log_id = log_interaction(log_data)
        else:
            log_data['prompt_guard_passed'] = False
            st.error(UI_TEXTS['inappropriate_content_error'][lang_code], icon="🚫")
            with st.spinner(UI_TEXTS['explanation_spinner'][lang_code]):
                reason = get_rejection_reason(user_prompt, "Contenido inapropiado detectado", detected_lang)
            st.warning(reason, icon="🛡️")
            log_data['advisory_agent_response'] = reason
            st.session_state.log_id = log_interaction(log_data)

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        log_data['error'] = str(e)
        st.session_state.log_id = log_interaction(log_data)
    finally:
        st.sidebar.success(UI_TEXTS['audit_log_success'][lang_code])