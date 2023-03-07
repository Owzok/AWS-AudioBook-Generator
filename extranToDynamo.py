import json
import boto3

def lambda_handler(event, context):
    x = json.loads(event['Records'][0]['body'])
    msg = json.loads(x['Message'])

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('extranTextract')

    objeto = {
        'tenant_id': msg['tenant_id'],
        'nombre_id': msg['nombre_archivo'],
        'texto': msg['extraccion']
    }
    
    print('Insertar en textoTextract\n', 'json:', objeto)
    
    response = table.put_item(Item=objeto)
    
    return {
        'statusCode': 200,
        'body': response
    }
