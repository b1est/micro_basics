from flask import Flask, jsonify, request
import requests
import uuid

# Define the URLs for the logging and messages services
logging_service_url = 'http://localhost:8081'
messages_service_url = 'http://localhost:8082'

app = Flask(__name__)


@app.route('/facade_service', methods=['POST'])
def post_message():
    """
    Handle POST requests that log a message to the logging service
    and return a JSON response containing the message ID and message.
    """

    # Extract the message content from the request JSON object
    msg = request.json['msg']

    # Generate a unique identifier for the message using the uuid module
    msg_id = str(uuid.uuid4())
    payload = {'id': msg_id, 'msg': msg}

    # Send a POST request to the logging service with the message ID and message content in the request body
    requests.post(logging_service_url + "/log", data=payload)

    # Return a JSON response containing the message ID and message content
    return jsonify({'id': msg_id, 'msg': msg})


@app.route('/facade_service', methods=['GET'])
def get_messages():
    """
    Handle GET requests to the logging service and the messages service
    and return the combined result as a JSON response.
    """

    logging_response = requests.get(logging_service_url + "/log")
    messages_response = requests.get(messages_service_url + "/msg")

    # Concatenate the two JSON responses and return them as a single response
    return jsonify(logging_response.json() + messages_response.json())


if __name__ == '__main__':
    app.run(port=8080)
