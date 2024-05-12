flaskを使用する
pip install flask boto3
export FLASK_APP=main.py
flask run


from flask import Flask, request, render_template
import boto3

app = Flask(__name__)

# AWS S3の設定
S3_BUCKET_NAME = 'YOUR_S3_BUCKET_NAME'
S3_ACCESS_KEY = 'YOUR_S3_ACCESS_KEY'
S3_SECRET_KEY = 'YOUR_S3_SECRET_KEY'

# S3クライアントを作成
s3 = boto3.client('s3',
                  aws_access_key_id=S3_ACCESS_KEY,
                  aws_secret_access_key=S3_SECRET_KEY)
import json
import boto3

def lambda_handler(event, context):
    # SQSからメッセージを受信
    sqs = boto3.client('sqs')
    queue_url = 'YOUR_QUEUE_URL'  # SQSのキューのURLを指定してください
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        VisibilityTimeout=30,
        WaitTimeSeconds=20
    )
    
    messages = response.get('Messages', [])
    
    for message in messages:
        # メッセージの本文を取得
        body = message['Body']
        
        # メッセージを処理するための処理を記述
        # 例えば、メッセージを解析して必要な処理を行います
        
        # 処理が完了したら、メッセージを削除
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('SQSからのメッセージを処理しました')
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    try:
        # S3にファイルをアップロード
        s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
        return 'File uploaded successfully to S3!'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)


