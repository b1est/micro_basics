from flask import Flask, jsonify
from hazelcast import HazelcastClient
from time import sleep
import threading
import logging
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

lock = threading.Lock()

@app.route('/msg', methods=['GET'])
def get_messages():
     
    app.logger.info("GET request received.")
    with lock:
        msgs = list(dictionary.values())
    msgs = list(dictionary.values())
    app.logger.info(f"Messages: {msgs}.")
    return jsonify(msgs)

def consumer_process():
    global dictionary
    dictionary = {}
    while True:
        
        if not queue.is_empty():
            head = queue.take()
            new_dict = {head['id']: head['msg']}
            with lock:
                dictionary.update(new_dict)
            sleep(10)
            app.logger.info(f"Received: {new_dict}.")
            app.logger.info(f"All messages: {dictionary}.")
            sleep(10)


if __name__ == '__main__':
    
    client = HazelcastClient(
        cluster_members=[
                os.getenv("HAZELCAST_IP")
            ]
    )
    queue = client.get_queue("queue").blocking()
    consumer_thread = threading.Thread(target=consumer_process)
    consumer_thread.start()
    
    app.run(host="0.0.0.0", port=8000, debug=True)
    
    client.shutdown()
        