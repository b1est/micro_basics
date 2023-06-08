from flask import Flask, jsonify
from hazelcast import HazelcastClient
import threading
import logging
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/msg', methods=['GET'])
def get_messages():
    app.logger.info("GET request received.")
    msgs = list(dict.values())
    app.logger.info(f"messages: {msgs}")
    return jsonify(msgs)

def consumer_process():
    app.logger.info(f"TEST")
    while True:
        if not queue.is_empty():
            head = queue.take()
            new_dict = {head['id']: head['msg']}
            dict.update(new_dict)
            app.logger.info(f"Received: {new_dict}")
            app.logger.info(f"All messages: {dict}")



if __name__ == '__main__':
    dict = {}
    client = HazelcastClient(
        cluster_members=[
                os.getenv("HAZELCAST_IP")
            ]
    )
    queue = client.get_queue("queue").blocking()
    
    consumer_thread = threading.Thread(target=consumer_process)
    consumer_thread.start()

    app.run(host="0.0.0.0", port=8000, debug=True)

    consumer_thread.join()
