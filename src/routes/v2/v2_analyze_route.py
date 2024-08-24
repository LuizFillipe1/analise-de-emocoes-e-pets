import json
import datetime
from services.rekognition_service import analyze_image, detect_labels
from services.bedrock_service import generate_pet_tips
from utils.utils import create_response

# Analisa a imagem, detecta rostos e rótulos de animais, e gera dicas para os animais
def v2_analyze(event, context):
    try:
        body = json.loads(event['body'])
        bucket = body['bucket']
        image_name = body['imageName']
        url_to_image = f"https://{bucket}.s3.amazonaws.com/{image_name}"
        
        result_faces = analyze_image(bucket, image_name)
        pet_labels = detect_labels(bucket, image_name)
        result_tip = generate_pet_tips(pet_labels)
        
        pet_info = {
            "labels": [{'Confidence': label['Confidence'], 'Name': label['Name']} for label in pet_labels],
            "Dicas": result_tip
        }

        response_body = {
            'url_to_image': url_to_image,
            'created_image': datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        }

        # Filtrar faces para incluir apenas aquelas com valores não nulos
        if result_faces is not None:
            filtered_faces = []
            for face in result_faces:
                position = face.get('position', {})
                if any(value is not None for value in position.values()) or face.get('classified_emotion') is not None or face.get('classified_emotion_confidence') is not None:
                    filtered_faces.append(face)
            if filtered_faces:
                response_body['faces'] = filtered_faces
   
        response_body['pets'] = [pet_info] if pet_labels else []
        return create_response(200, response_body)

    except Exception as e:
        return create_response(500, {'error': str(e)})
