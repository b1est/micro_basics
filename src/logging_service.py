from flask import Flask, jsonify, request, make_response
from hazelcast import HazelcastClient
import os
app = Flask(__name__)


@app.route('/log', methods=['POST'])
def post_message():
    msg_id = request.form.get('id')
    msg = request.form.get('msg')
    messages.put(msg_id, msg)
    return make_response(f"Success: POST ({msg_id}, {msg})")

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
    app.run(host = "0.0.0.0", port=8081, debug=True)
    
