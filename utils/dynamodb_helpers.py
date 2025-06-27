# utils/dynamodb_helpers.py
import boto3

def update_feedback(log_id: str, feedback: str):
    """
    Actualiza un item en DynamoDB para añadir el feedback del usuario.
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('governance_audit_logs')

        table.update_item(
            Key={'log_id': log_id},
            UpdateExpression='SET user_feedback = :feedback',
            ExpressionAttributeValues={':feedback': feedback}
        )
        print(f"Feedback '{feedback}' guardado para el log ID: {log_id}")
        return True
    except Exception as e:
        print(f"ERROR: No se pudo actualizar el feedback en DynamoDB: {e}")
        return False