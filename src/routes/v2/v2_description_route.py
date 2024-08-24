from utils.utils import create_success_response

# Retorna uma resposta de sucesso indicando a versão 2 da API de visão
def v2_description(event, context):
    return create_success_response("VISION API version 2.", event)
