import json
import datetime
from services.rekognition_service import analyze_image
from utils.utils import create_response

# Analisa a imagem usando o serviço de reconhecimento v1
def v1_analyze(event, context):
    try:
        body = json.loads(event['body'])  # Carrega o corpo da requisição
        bucket = body['bucket']  # Obtém o bucket do S3
        image_name = body['imageName']  # Obtém o nome da imagem
        url_to_image = f"https://{bucket}.s3.amazonaws.com/{image_name}"  # Cria a URL da imagem
        
        result_faces = analyze_image(bucket, image_name)  # Analisa a imagem e obtém detalhes dos rostos

        response_body = {
            'url_to_image': url_to_image,  # URL da imagem analisada
            'created_image': datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),  # Data e hora da análise
            'faces': result_faces  # Detalhes dos rostos encontrados
        }

        return create_response(200, response_body)  # Retorna a resposta com sucesso

    except Exception as e:
        return create_response(500, {'error': str(e)})  # Retorna erro em caso de exceção
