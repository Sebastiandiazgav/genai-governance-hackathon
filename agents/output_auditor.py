# agents/output_auditor.py
import config

def audit_output(llm_response: str) -> bool:
    """
    Revisa la respuesta del LLM para asegurar que no contenga frases prohibidas.
    
    Args:
        llm_response (str): La respuesta generada por el LLM.
        
    Returns:
        bool: True si la salida es segura, False si no lo es.
    """
    response_lower = llm_response.lower()
    for phrase in config.FORBIDDEN_OUTPUT_PHRASES:
        if phrase in response_lower:
            print(f"Auditoría de salida fallida. Frase encontrada: '{phrase}'")
            return False
    return True