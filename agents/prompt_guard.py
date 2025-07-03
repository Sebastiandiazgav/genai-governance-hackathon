import config

def is_safe(prompt: str, language: str) -> bool:
    """
    Verifica si un prompt es seguro basado en palabras clave prohibidas.
    
    Args:
        prompt (str): El texto introducido por el usuario.
        language (str): El código del idioma detectado ('en' o 'es').
        
    Returns:
        bool: True si el prompt es seguro, False si contiene palabras prohibidas.
    """
    prompt_lower = prompt.lower()

    if language == 'en':
        keyword_list = config.PROHIBITED_KEYWORDS_EN
    elif language == 'es':
        keyword_list = config.PROHIBITED_KEYWORDS_ES
    else:
        return False
        
    # Comprobamos si alguna palabra clave prohibida está en el prompt
    for keyword in keyword_list:
        if keyword in prompt_lower:
            print(f"Peligro detectado. Palabra clave: '{keyword}'") 
            return False # No es seguro

    return True