import json
import boto3
import pymysql

s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')

def lambda_handler(event, context):
    # Aurora DBのエンドポイントと認証情報
    aurora_host = 'YOUR_AURORA_DB_ENDPOINT'
    aurora_user = 'YOUR_AURORA_DB_USERNAME'
    aurora_password = 'YOUR_AURORA_DB_PASSWORD'
    aurora_database = 'YOUR_AURORA_DB_NAME'
    aurora_port = 3306
    queue_url = 'YOUR_SQS_QUEUE_URL'
    
    # メッセージを受信
    for record in event['Records']:
        message = json.loads(record['body'])
        
        # SQSメッセージの受信と削除
        receipt_handle = record['receiptHandle']
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        
        # 条件に応じて処理を分岐
        if message['action'] == 'upload_to_s3':
            # S3へのファイルアップロード処理
            upload_to_s3(message['file_content'])
        elif message['action'] == 'insert_to_aurora':
            # Auroraへのレコード登録処理
            record = message['record']
            insert_to_aurora(aurora_host, aurora_user, aurora_password, aurora_database, aurora_port, record)
        else:
            # 不明なアクションの場合はエラー処理などを行う
            pass

def upload_to_s3(file_content):
    # S3へのファイルアップロード処理
    bucket_name = 'YOUR_S3_BUCKET_NAME'
    key = 'YOUR_S3_OBJECT_KEY'
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=file_content)
    # 必要に応じて成功時の処理を追加

def insert_to_aurora(host, user, password, database, port, record):
    # Auroraへのレコード登録処理
    try:
        # Aurora DBに接続
        conn = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
        cursor = conn.cursor()
        
        # テーブルにレコードを挿入
        sql = "INSERT INTO YOUR_TABLE_NAME (column1, column2, column3) VALUES (%s, %s, %s)"
        val = (record['value1'], record['value2'], record['value3'])
        cursor.execute(sql, val)
        
        # 変更をコミット
        conn.commit()
        
        # 接続を閉じる
        cursor.close()
        conn.close()
        
        # 成功時の処理を追加
    except Exception as e:
        # エラー処理を行う
        print(f"An error occurred: {str(e)}")
