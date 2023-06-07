from flask import Flask, jsonify, request, make_response
from hazelcast import HazelcastClient
import os
import requests
import random
import uuid

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
    queue.put(payload)
    return make_response(f"Success")


@app.route('/facade_service', methods=['GET'])
def get_messages():
    while True:
        try:
            logging_response = requests.get(url=random.choice(logging_service_url))
        except requests.exceptions.ConnectionError:
            pass
        else:
            break
   
    messages_response = requests.get(random.choice(messages_service_url))

    return jsonify(logging_response.json() + messages_response.json())


if __name__ == '__main__':
    client = HazelcastClient(
            cluster_members=[
                os.getenv("HAZELCAST_IP")
            ]
    )
    queue = client.get_queue("queue").blocking()
    app.run(host = "0.0.0.0", port=5000, debug=True)
