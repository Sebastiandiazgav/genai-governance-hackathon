import config

def has_permission(prompt: str, role: str, language: str) -> bool:
    """
    Verifica si el rol del usuario tiene permiso para la consulta,
    basado en las políticas y palabras clave sensibles.
    
    Args:
        prompt (str): El texto introducido por el usuario.
        role (str): El rol del usuario actual (ej. "Usuario Anónimo").
        language (str): El idioma detectado ('en' o 'es').
        
    Returns:
        bool: True si el usuario tiene permiso, False en caso contrario.
    """
    prompt_lower = prompt.lower()
    
    # Determinar qué lista de palabras clave sensibles usar
    sensitive_keywords_list = config.SENSITIVE_KEYWORDS_EN if language == 'en' else config.SENSITIVE_KEYWORDS_ES
    
    # Iterar sobre las palabras clave del idioma detectado
    for keyword_es_or_en in sensitive_keywords_list:
        if keyword_es_or_en in prompt_lower:
            rule_key = ""
            if language == 'es':
                try:
                    idx = list(config.SENSITIVE_KEYWORDS_ES).index(keyword_es_or_en)
                    rule_key = list(config.SENSITIVE_KEYWORDS_EN)[idx]
                except ValueError:
                    return False 
            else:
                rule_key = keyword_es_or_en 

            if rule_key in config.POLICY_RULES:
                allowed_roles = config.POLICY_RULES[rule_key]
                if role in allowed_roles:
                    continue
                else:
                    print(f"Permiso denegado. Rol '{role}' no autorizado para '{rule_key}'")
                    return False

    return True