
import boto3
import json
import uuid
from flask import Flask, request
from pprint import pprint
app = Flask(__name__)
app.config.from_pyfile('.env')
sqs = boto3.client('sqs')


@app.route('/', methods=['POST', 'GET'])
def index():
    return "Success! Endpoints available: /add, /get, and /delete."


# store an SMS message to SQS FIFO for later sending
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        message = request.get_json()

        kwargs = {}
        for key, value in message.items():
            kwargs[key] = {'DataType': 'String', 'StringValue': value}

        response = sqs.send_message(
            QueueUrl=app.config.get('AWS_SQS_URL'),
            MessageAttributes=kwargs,
            MessageBody=(
                message['text']
            ),
            MessageDeduplicationId=str(uuid.uuid1()),
            MessageGroupId=str(uuid.uuid1())
        )

    if response['MessageId']:
        return "MessageId: " + response['MessageId']
    else:
        return "Error: " + response["error_text"]


@app.route('/get')
def get():
    # get the next message in the queue to send
    message = sqs.receive_message(
        QueueUrl=app.config.get('AWS_SQS_URL'),
        AttributeNames=[
            'SentTimestamp'
        ],
        MessageAttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=1,
        VisibilityTimeout=1,
        WaitTimeSeconds=20
    )

    # send the message
    if message.get("Messages"):
        response = message
    else:
        return "Queue empty!"

    # return status messages and delete from queue
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return json.dumps(response['Messages'][0])
    else:
        return "Error: " + response['Messages'][0]['error-text']


@app.route('/delete', methods=['POST'])
def delete():

    message = request.get_json()
    # return status messages and delete from queue
    if message['receipt_handle']:
        # Delete message from the queue
        response = sqs.delete_message(
            QueueUrl=app.config.get('AWS_SQS_URL'),
            ReceiptHandle=message['receipt_handle']
        )
        return "Message removed from queue, SQS ReceiptHandle: " + message['receipt_handle']
