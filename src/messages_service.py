from flask import Flask, jsonify
from hazelcast import HazelcastClient
import multiprocessing as mp
import os

app = Flask(__name__)

@app.route('/msg', methods=['GET'])
def get_messages():
    return jsonify(list(dict.values()))



def con_process():
    while True:
        if not queue.is_empty():
            head = queue.take()
            dict.update({head['uuid']: head['message']})

if __name__ == '__main__':
    dict = {}
    client = HazelcastClient(
        cluster_members=[
                os.getenv("HAZELCAST_IP")
            ]
    )
    queue = client.get_queue("queue").blocking()
    
    process = mp.Process(target=con_process)
    process.start()
    app.run(host = "0.0.0.0", port=8000, debug=True)
    process.join()
