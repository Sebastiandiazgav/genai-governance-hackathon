# agents/advisory_agent.py

from utils.bedrock_client import invoke_model

def get_rejection_reason(original_prompt: str, rejection_reason: str, language: str) -> str:
    """
    Usa el LLM para generar una explicación amigable cuando un prompt es rechazado.
    
    Args:
        original_prompt (str): El prompt original del usuario.
        rejection_reason (str): La razón interna del bloqueo (ej. "Contenido inapropiado").
        language (str): El idioma para la respuesta ('es' o 'en').
        
    Returns:
        str: Una explicación amigable generada por el LLM.
    """
    instructional_prompt = f"""
    Act as a helpful and polite governance assistant. A user's request was blocked. 
    Your task is to explain why, in a clear, educational, and non-judgmental way.

    - **User's original prompt:** "{original_prompt}"
    - **Internal reason for blocking:** "{rejection_reason}"
    - **Language for the response:** "{language}"

    Please generate a brief, helpful explanation for the user in the specified language.
    """
    
    return invoke_model(prompt=instructional_prompt)