# utils/bedrock_client.py

import boto3
import json

# Inicializamos el cliente de Bedrock Runtime una sola vez
bedrock_runtime = boto3.client(service_name='bedrock-runtime')

def invoke_model(prompt: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
    """
    Invoca un modelo de Amazon Bedrock para generar una respuesta.
    
    Args:
        prompt (str): El prompt para enviar al modelo.
        model_id (str): El ID del modelo a usar.
        
    Returns:
        str: La respuesta generada por el modelo.
    """
    try:
        # El cuerpo de la solicitud debe estar en el formato que el modelo espera.
        # Para Claude 3, es un objeto JSON con 'messages' y 'anthropic_version'.
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

        # Invocamos el modelo
        response = bedrock_runtime.invoke_model(
            body=body, 
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )

        # Leemos y parseamos la respuesta
        response_body = json.loads(response.get('body').read())
        
        # Extraemos el texto de la respuesta
        return response_body.get('content', [{}])[0].get('text', '')

    except Exception as e:
        print(f"ERROR: No se pudo invocar el modelo de Bedrock: {e}")
        return "Lo siento, ha ocurrido un error al contactar al modelo de IA."