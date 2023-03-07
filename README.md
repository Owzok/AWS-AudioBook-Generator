# AWS-AudioBook-Generator

## Solution Architecture

## AWS Functions

### Lambda Functions
- TextractPNG
- TxTToDynamo
- ExtranToDynamo

### DynamoDB
- TextoTextract
- ExtranTextract

### Simple Notification Service
- RecibirTextract
- RecibirTextractEx

### S3 Bukets
- ArchivosProyectoFinalCloud
- PollyResultsProyecto

### Simple Queue Service
- ColaTextract
- ColaExranExtract

### Amazon Comprehend
Natural language processing service which uses Machine Learning to find insights in a text. We will be using it to detect the language of the input file.

### Amazon Cloudwatch
Tool used to visualize the registers and check everything is working alright.

### Amazon Polly
Deep Learning Service to recreate human voices. We used id to generate an audio reading the file we sent and to export it to an .mp3 file.

### Amazon Textract
Machine Learning service which extracts texts from images. It's more complex than an OCR because it identifies and comprehends the extracted data. 

### Amazon Translate
AWS Service which uses a neural network to translate between languages in a very accurate way.
