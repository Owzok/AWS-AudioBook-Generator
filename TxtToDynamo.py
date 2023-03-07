import json
import boto3

def lambda_handler(event, context):
    x = json.loads(event['Records'][0]['body'])
    msg = json.loads(x['Message'])

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('textoTextract')

    objeto = {
        'tenant_id': msg['tenant_id'],
        'nombre_id': msg['nombre_archivo'],
        'texto': msg['extraccion']
    }
    
    region = 'us-east-1'
    
    print('Insertar en textoTextract\n', 'json:', objeto)
    
    response = table.put_item(Item=objeto)
    
    print('Archivo:', msg['nombre_archivo'])
    print('Texto:', msg['extraccion'])

    polly_client = boto3.client('polly', region_name=region)
    
    response = polly_client.start_speech_synthesis_task(Text=msg['extraccion'], OutputFormat = "mp3",
                                        VoiceId="Joanna", OutputS3BucketName='pollyresultsproyecto')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Polly!')
    }
