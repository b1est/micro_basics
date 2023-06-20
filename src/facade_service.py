from flask import Flask, jsonify, request, make_response
from hazelcast import HazelcastClient
import logging
import requests
import random
import uuid
import os

logging.basicConfig(level=logging.INFO)

logging_service_url = ['http://logging-service1:8081/log', 'http://logging-service2:8081/log', 'http://logging-service3:8081/log']
messages_service_url = ['http://messages-service1:8000/msg', 'http://messages-service2:8000/msg']

app = Flask(__name__)


@app.route('/facade_service', methods=['POST'])
def post_message():
    msg = request.json['msg']
    msg_id = str(uuid.uuid4())
    payload = {'id': msg_id, 'msg': msg}
    url_random = random.choice(logging_service_url)
    requests.post(url=url_random, data=payload)
    app.logger.info(f"Message '{payload['id']}' sent to {url_random}")
    queue.put(payload)
    app.logger.info(f"Message '{payload['id']}' added to hazelcast queue")
    return make_response(f"Success")


@app.route('/facade_service', methods=['GET'])
def get_messages():
    try:
        logging_url_random = random.choice(logging_service_url)
        logging_response = requests.get(url=logging_url_random)
        app.logger.info(f"Retrieve messages from '{logging_url_random}' successfully.")
    except:
        app.logger.error(f"Retrieve from '{logging_url_random}' failed with error.")
    
    try:
        messages_url_random = random.choice(messages_service_url)
        messages_response = requests.get(messages_url_random)
        app.logger.info(f"Retrieve messages from '{messages_url_random}' successfully.")
    except:
        app.logger.error(f"Retrieve from '{messages_url_random}' failed with error.")    
   
    app.logger.info(f"Logging-service ({logging_url_random}) response: {logging_response.json()}\nMessages-service ({messages_url_random}) response: {messages_response.json()}.")
    return make_response(f"Logging-service ({logging_url_random}) response: {logging_response.json()}\nMessages-service ({messages_url_random}) response: {messages_response.json()}.")


if __name__ == '__main__':
    client = HazelcastClient(
            cluster_members=[
                os.getenv("HAZELCAST_IP")
            ]
    )
    queue = client.get_queue("queue").blocking()
    app.run(host = "0.0.0.0", port=5000, debug=False)
    client.shutdown()