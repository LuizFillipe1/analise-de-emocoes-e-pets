import json
import boto3
from utils.utils import create_response

# Inicializa o cliente do AWS Bedrock
bedrock = boto3.client('bedrock-runtime')

# Gera dicas sobre animais de estimação usando etiquetas detectadas
def generate_pet_tips(pet_labels):
    pet_names = [label['Name'] for label in pet_labels]
    pet_names_text = ','.join(pet_names)

    questions = [
        f"Nível de energia e Necessidade de exercícios para o animal {pet_names_text}.",
        f"Temperamento e comportamento do animal {pet_names_text}.",
        f"Cuidados e necessidades do animal {pet_names_text}.",
        f"Problemas de saúde comuns do animal {pet_names_text}."
    ]
    
    titles = [
        "Nível de Energia e Necessidades de Exercícios:",
        "Temperamento e Comportamento:",
        "Cuidados e Necessidades:",
        "Problemas de Saúde Comuns:"
    ]
    
    all_responses = []

    for i, question in enumerate(questions):
        input_text = f"Responda em português de forma resumida, não mais do que 1-2 frases, sobre: {question}"
        body = json.dumps({"inputText": input_text})

        try:
            # Invoca o modelo para gerar a resposta
            response = bedrock.invoke_model(
                modelId='amazon.titan-text-premier-v1:0',
                contentType='application/json',
                body=body
            )
            
            response_body = response['body'].read().decode('utf-8')
            result = json.loads(response_body)
            
            response_text = result['results'][0]['outputText'].replace('\n', ' ')
            all_responses.append(f"{titles[i]} {response_text}")
        
        except Exception as e:
            # Em caso de erro, adiciona mensagem de erro à resposta
            all_responses.append(f"{titles[i]} Erro ao processar a pergunta: {question}")
            return create_response(500, {'error': str(e)})

    return all_responses
