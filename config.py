# config.py - VERSIÓN COMPLETA Y CORREGIDA

# --- Reglas para el Agente "Prompt Guard" (Día 3) ---
# Palabras clave que revisarán los prompts de entrada.

PROHIBITED_KEYWORDS_EN = [
    "tax evasion", 
    "insider trading", 
    "money laundering", 
    "illegal",
    "how to make a bomb",
    "buy drugs"
]

PROHIBITED_KEYWORDS_ES = [
    "evasión de impuestos", 
    "información privilegiada", 
    "lavado de dinero", 
    "ilegal",
    "cómo hacer una bomba",
    "comprar drogas"
]


# --- Reglas para el Agente "Policy Enforcer" (Día 4) ---

# Palabras clave que indican un tema sensible
SENSITIVE_KEYWORDS_EN = {
    "portfolio",
    "account balance",
    "transaction history",
    "personal information"
}

SENSITIVE_KEYWORDS_ES = {
    "portafolio",
    "saldo de la cuenta",
    "historial de transacciones",
    "información personal"
}

# Definición de políticas: qué rol se necesita para cada tema sensible.
# Usamos las palabras en inglés como clave estándar para las reglas.
POLICY_RULES = {
    "portfolio": ["Usuario Registrado", "Gestor Financiero"],
    "account balance": ["Usuario Registrado", "Gestor Financiero"],
    "transaction history": ["Gestor Financiero"],
    "personal information": ["Usuario Registrado", "Gestor Financiero"]
}