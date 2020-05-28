# sms-aws-sqs-python-receiver
Python function to store bulk messages to AWS SQS without consideration of source.

## Prerequisites
* Python 3.8 (update `serverless.yml` if higher version is desired)
* Pip
* [Node.js](https://nodejs.org/en/) and npm
* [Serverless Framework](https://serverless.com/framework/docs/getting-started/)
* [AWS account](https://aws.amazon.com/)

## Setup Instructions
Clone this repo from GitHub, and navigate into the newly created directory to proceed.

### Environment
Rename `.env.default` to `.env` and add values to `VONAGE_API_KEY` and `VONAGE_API_SECRET` provided by your [Vonage API Dashboard](https://dashboard.nexmo.com/).

### AWS Setup
You will need to create [AWS credentials](https://www.serverless.com/framework/docs/providers/aws/guide/credentials/) as indicated by Serverless. Update the `.env` file with these.

Also, create a new [SQS FIFO queue](https://aws.amazon.com/sqs/) using the default settings, and update `.env` with the SQS queue URL. By using FIFO, it ensures messages are sent in the order they were stored.

### Usage
To start, create a virtualenv from within the project root to contain the project as you proceed. Then activate it as follows:

```bash
virtualenv venv --python=python3
source venv/bin/activate
```

Next, initialize npm and follow the prompts selecting the defaults. Unless you desire to change any of them. Also, use npm to install needed dependencies for dev to enable Serverless and Lambda to work with the Flask app.

```bash
npm init
npm install --save-dev serverless-wsgi serverless-python-requirements
```

Now you can use pip to install the required Python dependencies. The dependencies are already listed in the requirements.txt, so instruct pip to use it.

```bash
pip install -r requirements.txt
```

#### Running Local
Should you wish to run the app locally and test things out, before deploying to AWS Lambda, you can serve it with the following command:

```bash
sls wsgi serve
```

By default this will serve the app at `http://localhost:5000`. Hitting `Ctrl+c` will close it down.

#### Deploy to Lambda
With all the above finished successfully, you can now use `Serverless` to deploy the app to AWS Lambda.

```bash
sls deploy
```

> IMPORTANT: This application does not contain any authentication for use. Therefore, ensure you add authentication in front of it to prevent public usage. By leaving it open to the public, it could result in usage charges at AWS and Vonage.

#### Available Endpoints
There are 4 URL endpoints available with this client:

1 HTTP GET request to `/`

* Doesn't perform any actions, but provides a quick way to test

2 HTTP POST request to `/add`

* This action stores the message in SQS.
* Pass a POST with a JSON body like the following. Substitute the placeholders, indicated with `<>` with your data.
* The result contains the SQS `MessageId`.

```json
{
    "from": "<your_name_or_number>",
    "message": "<sms_message_contents>",
    "to": "<recipients_number>"
}
```

3 HTTP GET request to `/get`

* Retrieves the message from SQS FIFO queue.
* Once received, the `ReceiptHandle` can be used to remove it from queue.
    
```text
location=None, media_mode=relayed, archive_mode=manual
```

4 HTTP POST request to `/delete`

* This action deletes the message from SQS.
* Pass a POST with a JSON body like the following. Substitute the placeholders, indicated with `<>` with your data.

```json
{
    "receipt_handle": "<your_receipt_handle>",
}
```

##### Examples:
Go to the URL provided by the deploy process. Below are some examples of what sample requests may look like: (Your URL will vary.)

GET `https://7ulasfasdasdfw4.execute-api.us-east-1.amazonaws.com/dev/`

The `/` endpoint returns the generic message.

POST `https://7ulasfasdasdfw4.execute-api.us-east-1.amazonaws.com/dev/add`

The `add` endpoint will return the SQS `MessageId`.

GET `https://7ulasfasdasdfw4.execute-api.us-east-1.amazonaws.com/dev/get`

The `get` endpoint will return a message for use.

GET `https://7ulasfasdasdfw4.execute-api.us-east-1.amazonaws.com/dev/delete`

The `delete` endpoing will delete a message from SQS.

#### Deactivating Virtualenv
To exit the virtualenv you can deactivate it, when desired.

```bash
deactivate
```

> NOTE: Depending on OS, you may need to prepend `virtualenv` to the command above.

## Contributing

We love questions, comments, issues - and especially pull requests. Either open an issue to talk to us, or reach us on twitter: <https://twitter.com/VonageDev>.
