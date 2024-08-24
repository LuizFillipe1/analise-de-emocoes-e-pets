import json

# Cria uma resposta HTTP com o status e o corpo fornecidos
def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }

# Cria uma resposta de sucesso com uma mensagem e o evento recebido
def create_success_response(message, event):
    body = {
        "message": message,
        "input": event,
    }
    return create_response(200, body)
