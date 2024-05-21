import json
import base64
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        file_name = body['fileName']
        file_content = body['fileContent']
        
        # Decode the base64 file content
        file_content_decoded = base64.b64decode(file_content)
        
        # Upload to S3
        s3.put_object(
            Bucket='<your-bucket-name>',
            Key=file_name,
            Body=file_content_decoded
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'File uploaded successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
