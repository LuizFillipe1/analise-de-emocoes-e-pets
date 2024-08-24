from utils.utils import create_success_response

# Retorna uma descrição da versão 1 da API VISION
def v1_description(event, context):
    return create_success_response("VISION API version 1.", event)
