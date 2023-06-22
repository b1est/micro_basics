from flask import Flask, request, make_response
from hazelcast import HazelcastClient
import netifaces as ni
import logging
import requests
import random
import uuid
import consul

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/facade_service', methods=['POST'])
def post_message():
    msg = request.json['msg']
    msg_id = str(uuid.uuid4())
    payload = {'id': msg_id, 'msg': msg}
    
    url_random = random.choice(get_services_address('logging_service'))
    requests.post(url=url_random, data=payload)
    app.logger.info(f"Message '{payload['id']}' sent to {url_random}")
    queue.put(payload)
    app.logger.info(f"Message '{payload['id']}' added to hazelcast queue")
    return make_response(f"Success")


@app.route('/facade_service', methods=['GET'])
def get_messages():
    try:
        logging_url_random = random.choice(get_services_address('logging_service'))
        logging_response = requests.get(url=logging_url_random)
        app.logger.info(f"Retrieve messages from '{logging_url_random}' successfully.")
    except:
        app.logger.error(f"Retrieve from '{logging_url_random}' failed with error.")
    
    try:
        messages_url_random = random.choice(get_services_address('messages_service'))
        messages_response = requests.get(messages_url_random)
        app.logger.info(f"Retrieve messages from '{messages_url_random}' successfully.")
    except:
        app.logger.error(f"Retrieve from '{messages_url_random}' failed with error.")    
   
    app.logger.info(f"Logging-service ({logging_url_random}) response: {logging_response.json()}\nMessages-service ({messages_url_random}) response: {messages_response.json()}.")
    return make_response(f"Logging-service ({logging_url_random}) response: {logging_response.json()}\nMessages-service ({messages_url_random}) response: {messages_response.json()}.")

def get_services_address(service_name):
    index, req = consul_client.health.service(service_name)
    list_with_services = []
    for element in req:
        address = element.get('Service').get('Address')
        port = element.get('Service').get('Port')
        list_with_services.append("http://"+address + ":" + str(port)+f"/{service_name}")
    app.logger.info(f"List of {service_name} addresses: {list_with_services}")
    return list_with_services

if __name__ == '__main__':
    consul_client = consul.Consul('consul-server')
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    consul_client.agent.service.register(name='facade-service', address=ip, port=5000)
    hazelcast_service = consul_client.kv.get('app/config/hazelcast/instances')[1]['Value'].decode('utf-8').split(',')
    hazelcast_queue_name = consul_client.kv.get('app/config/hazelcast/queue/name')[1]['Value'].decode('utf-8')
    
    client = HazelcastClient(
            cluster_members=hazelcast_service
    )
    queue = client.get_queue(hazelcast_queue_name).blocking()
    
    app.run(host = "0.0.0.0", port=5000, debug=False)
    client.shutdown()