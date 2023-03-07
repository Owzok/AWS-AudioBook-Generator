import json
import boto3
import time

def start_job(client, s3_bucket_name, object_name):
    response = None
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3_bucket_name,
                'Name': object_name
            }})

    return response["JobId"]


def is_job_complete(client, job_id):
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(1)
        response = client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status


def get_job_results(client, job_id):
    pages = []
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    pages.append(response)
    print("Resultset page received: {}".format(len(pages)))
    next_token = None
    if 'NextToken' in response:
        next_token = response['NextToken']

    while next_token:
        time.sleep(1)
        response = client.\
            get_document_text_detection(JobId=job_id, NextToken=next_token)
        pages.append(response)
        print("Resultset page received: {}".format(len(pages)))
        next_token = None
        if 'NextToken' in response:
            next_token = response['NextToken']

    return pages

def lambda_handler(event, context):
    # === Leer Datos ===
    
    s3_bucket_name = event['Records'][0]['s3']['bucket']['name']
    document_name = event['Records'][0]['s3']['object']['key']
    region = 'us-east-1'
    
    print('Bucket:',s3_bucket_name, '\nFile:',document_name)
    
    # -- Obtener texto usando Amazon Textract --
    
    client = boto3.client('textract', region_name=region)
    
    job_id = start_job(client, s3_bucket_name, document_name)
    print("Empezando a extraer con un id: {}".format(job_id))
    if is_job_complete(client, job_id):
        response = get_job_results(client, job_id)

    text = ""
    
    for result_page in response:
        for item in result_page["Blocks"]:
            if item["BlockType"] == "LINE":
                text += item['Text']
                
    # -- Detectar Idioma usando Amazon Comprehend --
    
    client = boto3.client('comprehend')
    comp = client.detect_dominant_language(Text=text)
    lan = comp['Languages'][0]['LanguageCode']
    
    # -- Traducir usando Amazon Translate --
    
    print('Input Language:', lan)
    print('Output Language: es')
    
    if lan != 'es':
        translate = boto3.client('translate', region_name=region, use_ssl=True)
        trans = translate.translate_text(Text=text, SourceLanguageCode=lan,TargetLanguageCode="es")
        
        print('Translated!! Text changed to translation')
        text = trans['TranslatedText']

    # -- JSON Archivo --
    
    archivo = {
        'tenant_id': lan,
        'nombre_archivo': document_name,
        'extraccion': text
    }
    
    print('-- Archivo --')
    print(archivo)
        
    # -- Enviar al SNS --
    
    sns_client = boto3.client('sns')
    
    # -- Enviar al SNS español
    if lan == 'es':
        print("----- Enviando al SNS Español -----")
        response_sns = sns_client.publish(
            TopicArn = 'arn:aws:sns:us-east-1:992047015027:RecibirTextract',
            Subject = 'Textract Data',
            Message = json.dumps(archivo),
            MessageAttributes = {
                'tenant_id': {'DataType': 'String', 'StringValue': lan}
            }
        )
    
    # -- Enviar al SNS extranjero
    if lan != 'es':
        print("----- Enviando al SNS Extranjero -----")
        response_sns = sns_client.publish(
            TopicArn = 'arn:aws:sns:us-east-1:992047015027:RecibirTextractEx',
            Subject = 'Textract Data',
            Message = json.dumps(archivo),
            MessageAttributes = {
                'tenant_id': {'DataType': 'String', 'StringValue': lan}
            }
        )
    
    # Salida json
    return {
        'statusCode': 200,
        'response': response_sns
    }
