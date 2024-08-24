from utils.utils import create_success_response

def health(event, context):
    return create_success_response("Go Serverless v3.0! Your function executed successfully!", event)
