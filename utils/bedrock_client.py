# utils/bedrock_client.py

import boto3
import json
import streamlit as st # <-- AÑADIR ESTA LÍNEA

# ... (el resto del código de inicialización de bedrock_runtime no cambia)
bedrock_runtime = boto3.client(service_name='bedrock-runtime')


# AÑADIMOS EL DECORADOR DE CACHÉ AQUÍ
@st.cache_data
def invoke_model(prompt: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
    """
    Invoca un modelo de Amazon Bedrock para generar una respuesta.
    (Ahora con caché para respuestas instantáneas en prompts repetidos)
    """
    # El resto de la función no cambia en absoluto
    try:
        # ... (código existente de la función)
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ]
        })
        response = bedrock_runtime.invoke_model(
            body=body, 
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        response_body = json.loads(response.get('body').read())
        return response_body.get('content', [{}])[0].get('text', '')
    except Exception as e:
        print(f"ERROR: No se pudo invocar el modelo de Bedrock: {e}")
        return "Lo siento, ha ocurrido un error al contactar al modelo de IA."