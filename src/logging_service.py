from flask import Flask, jsonify, request, make_response
from hazelcast import HazelcastClient
import logging
import os

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/log', methods=['POST'])
def post_message():
    msg_id = request.form.get('id')
    msg = request.form.get('msg')
    app.logger.info(f"Put key-value {msg_id}-{msg} in the Hazelcast map.")
    messages.put(msg_id, msg)
    app.logger.info(f"Success: ({msg_id}, {msg}) put in the Hazelcast map.")
    return make_response(f"Success")

@app.route('/log', methods=['GET'])
def get_messages():
    return jsonify(list(messages.values()))

if __name__ == '__main__':
    client = HazelcastClient(
            cluster_members=[
                os.getenv("HAZELCAST_IP")
            ]
    )

    messages = client.get_map("messages").blocking()
    app.run(host = "0.0.0.0", port=8081, debug=False)
    client.shutdown()
