from flask import Flask, jsonify, request, make_response
import requests
import random
import uuid

logging_service_url = ['http://logging-service1:8081/log', 'http://logging-service2:8081/log', 'http://logging-service3:8081/log']
messages_service_url = 'http://messages-service:8000/msg'

app = Flask(__name__)


@app.route('/facade_service', methods=['POST'])
def post_message():
    msg = request.json['msg']
    msg_id = str(uuid.uuid4())
    payload = {'id': msg_id, 'msg': msg}
    url_random = random.choice(logging_service_url)
    requests.post(url=url_random, data=payload)
    app.logger.info(f"Send POST to logging-service ({url_random}) with data: {payload}")
    return make_response("Success")

@app.route('/facade_service', methods=['GET'])
def get_messages():
    while True:
        try:
            url_random = random.choice(logging_service_url)
            app.logger.info(f"Send GET to logging-service ({url_random})")
            logging_response = requests.get(url=url_random)
        except requests.exceptions.ConnectionError:
            app.logger.error(f'GET request failed')
        else:
            break
    
    app.logger.info(f"Send GET to messages-service ({messages_service_url})")
    messages_response = requests.get(messages_service_url)

    return jsonify(logging_response.json() + messages_response.json())


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=5000, debug=True)
