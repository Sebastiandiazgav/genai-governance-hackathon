# config.py (añadir al final)

# --- Reglas para el Agente "Policy Enforcer" ---

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