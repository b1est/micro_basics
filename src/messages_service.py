from flask import Flask, jsonify
from hazelcast import HazelcastClient
import netifaces as ni
import threading
import logging
import uuid
import consul


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

lock = threading.Lock()

@app.route('/messages_service', methods=['GET'])
def get_messages():
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
            app.logger.info(f"Received message: {new_dict}.")
            app.logger.info(f"All received messages: {dictionary}.")


if __name__ == '__main__':
    
    consul_client = consul.Consul('consul-server')
    
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    
    consul_client.agent.service.register(name='messages_service', address=ip, service_id='messages-service-'+str(uuid.uuid4()), port=8000)
    hazelcast_service = consul_client.kv.get('app/config/hazelcast/instances')[1]['Value'].decode('utf-8').split(',')
    hazelcast_queue_name = consul_client.kv.get('app/config/hazelcast/queue/name')[1]['Value'].decode('utf-8')
    
    client = HazelcastClient(
            cluster_members=hazelcast_service
    )
    queue = client.get_queue(hazelcast_queue_name).blocking()
    consumer_thread = threading.Thread(target=consumer_process)
    consumer_thread.start()
    
    app.run(host="0.0.0.0", port=8000, debug=False)
    
    client.shutdown()
        