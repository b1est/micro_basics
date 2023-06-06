from flask import Flask, jsonify, request, make_response
import requests
import random
import uuid

# Define the URLs for the logging and messages services
logging_service_url = ['http://localhost:8081/log', 'http://localhost::8083/log', 'http://localhost::8082/log']
messages_service_url = 'http://localhost::8084/msg'

app = Flask(__name__)


@app.route('/facade_service', methods=['POST'])
def post_message():

    # Extract the message content from the request JSON object
    msg = request.json['msg']

    # Generate a unique identifier for the message using the uuid module
    msg_id = str(uuid.uuid4())
    payload = {'id': msg_id, 'msg': msg}

    # Send a POST request to the logging service with the message ID and message content in the request body
    requests.post(url=random.choice(logging_service_url), data=payload)
    return make_response("Success")


@app.route('/facade_service', methods=['GET'])
def get_messages():
    while True:
        try:
            logging_response = requests.get(url=random.choice(logging_service_url))
        except requests.exceptions.ConnectionError:
            pass
        else:
            break
   
    messages_response = requests.get(messages_service_url)

    # Concatenate the two JSON responses and return them as a single response
    return jsonify(logging_response.json() + messages_response.json())


if __name__ == '__main__':
    app.run(host = "localhost", port=5000)
