import boto3
import json
from utils.utils import create_response

# Inicializa o cliente do AWS Rekognition
rekognition = boto3.client('rekognition')

# Analisa uma imagem no bucket S3 usando Rekognition para detectar rostos e emoções.
def analyze_image(bucket, image_name):
    try:
        # Detecta rostos na imagem
        response = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': image_name}},
            Attributes=['ALL']
        )

        # Extrai detalhes dos rostos detectados
        faces = response['FaceDetails']
        result_faces = [{
            'position': {
                'Height': face['BoundingBox']['Height'],
                'Left': face['BoundingBox']['Left'],
                'Top': face['BoundingBox']['Top'],
                'Width': face['BoundingBox']['Width']
            },
            'classified_emotion': max(face['Emotions'], key=lambda x: x['Confidence'])['Type'],
            'classified_emotion_confidence': max(face['Emotions'], key=lambda x: x['Confidence'])['Confidence']
        } for face in faces]

        # Se não houver rostos, retorna valores nulos
        if not result_faces:
            result_faces = [{
                'position': {
                    'Height': None,
                    'Left': None,
                    'Top': None,
                    'Width': None
                },
                'classified_emotion': None,
                'classified_emotion_confidence': None
            }]

        # Imprime a resposta do Rekognition
        print(json.dumps(response))
        return result_faces

    except Exception as e:
        # Retorna resposta de erro
        return create_response(500, {'error': str(e)})
    
# Detecta rótulos em uma imagem no bucket S3 usando Rekognition.
def detect_labels(bucket, image_name):
    try:
        # Detecta rótulos na imagem
        response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': image_name}},
            MaxLabels=10,
            MinConfidence=80
        )

        # Filtra os rótulos para incluir apenas aqueles que são animais
        pet_labels = [
            label for label in response['Labels'] 
            if any(parent['Name'].lower() == 'animal' for parent in label['Parents'])
        ]

        # Imprime a resposta do Rekognition
        print(json.dumps(response))
        return pet_labels

    except Exception as e:
        # Retorna resposta de erro
        return create_response(500, {'error': str(e)})