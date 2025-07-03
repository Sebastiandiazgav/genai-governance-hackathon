# agents/audit_logger.py
import boto3
import uuid
from datetime import datetime
import os

def log_interaction(log_data: dict):
    """
    Registra la interacción completa en la tabla de DynamoDB.
    
    Args:
        log_data (dict): Un diccionario con toda la información de la interacción.
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        table_name = 'governance_audit_logs'
        table = dynamodb.Table(table_name)
        log_data['log_id'] = str(uuid.uuid4())
        log_data['timestamp'] = datetime.utcnow().isoformat()
        table.put_item(Item=log_data)
        print(f"Registro exitoso en DynamoDB. ID: {log_data['log_id']}")
        return log_data['log_id']

    except Exception as e:
        print(f"ERROR: No se pudo registrar en DynamoDB: {e}")
        return None