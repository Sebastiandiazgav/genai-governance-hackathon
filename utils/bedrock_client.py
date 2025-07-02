# utils/bedrock_client.py

import boto3
import json
import streamlit as st

# Ya NO inicializamos el cliente aquí.

@st.cache_data
def invoke_model(prompt: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
    """
    Invoca un modelo de Amazon Bedrock para generar una respuesta.
    (Ahora con inicialización 'perezosa' del cliente de boto3)
    """
    try:
        # Inicializamos el cliente JUSTO ANTES de usarlo.
        # Esto es más robusto en entornos de nube como Streamlit Cloud.
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime', 
            region_name="us-east-1"
        )

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
        # Imprimimos el error real en los logs para poder depurarlo.
        print(f"ERROR al invocar el modelo de Bedrock: {e}")
        # Devolvemos un mensaje de error genérico a la interfaz.
        return "Lo siento, ha ocurrido un error al contactar al modelo de IA."