
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

POLICY_RULES = {
    "portfolio": ["Usuario Registrado", "Gestor Financiero"],
    "account balance": ["Usuario Registrado", "Gestor Financiero"],
    "transaction history": ["Gestor Financiero"],
    "personal information": ["Usuario Registrado", "Gestor Financiero"]
}

FORBIDDEN_OUTPUT_PHRASES = [
    "i guarantee",
    "i promise",
    "this is financial advice",
    "te garantizo",
    "te prometo",
    "esto es un consejo financiero"
]