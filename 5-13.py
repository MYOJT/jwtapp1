'''
API GatewayとLambdaを統合し、Lambda内でSQSからメッセージを受信して、POSTリクエストのボディのパラメータに基づいてS3へのファイルアップロードとAuroraへのレコード追加を分岐するコード
'''

import json
import boto3

s3_client = boto3.client('s3')
aurora_client = boto3.client('aurora')

def lambda_handler(event, context):
    # SQSからメッセージを受信
    sqs_messages = receive_messages_from_sqs('YOUR_SQS_QUEUE_URL')
    
    # メッセージがあれば処理を行う
    if sqs_messages:
        for message in sqs_messages:
            # メッセージのボディを取得
            body = json.loads(message['Body'])
            
            # メッセージのボディから必要な情報を取得して処理を分岐
            if 'action' in body:
                action = body['action']
                if action == 'upload_to_s3':
                    upload_to_s3(body['file_content'])
                elif action == 'insert_to_aurora':
                    insert_to_aurora(body['record'])
                else:
                    # 不明なアクションの場合はエラー処理などを行う
                    pass
                
            # 受信したメッセージを削除
            delete_message_from_sqs('YOUR_SQS_QUEUE_URL', message['ReceiptHandle'])

def receive_messages_from_sqs(queue_url):
    # SQSからメッセージを受信
    sqs_client = boto3.client('sqs')
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,  # 1つのメッセージのみを取得
        WaitTimeSeconds=20  # メッセージがない場合の待機時間（秒）
    )
    
    # メッセージがあれば返す
    if 'Messages' in response:
        return response['Messages']
    else:
        return []

def delete_message_from_sqs(queue_url, receipt_handle):
    # SQSからメッセージを削除
    sqs_client = boto3.client('sqs')
    sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

def upload_to_s3(file_content):
    # S3へのファイルアップロード処理
    bucket_name = 'YOUR_S3_BUCKET_NAME'
    key = 'YOUR_S3_OBJECT_KEY'
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=file_content)
    # 必要に応じて成功時の処理を追加

def insert_to_aurora(record):
    # Auroraへのレコード登録処理
    # クエリの実行やトランザクション処理を行う
    pass
