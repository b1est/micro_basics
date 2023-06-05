from hazelcast import HazelcastClient
from multiprocessing import Process
from time import sleep
import os
import yaml

def set_data(num_of_data: int = 1000) -> None:
    client = HazelcastClient() 
    map = client.get_map("my-distributed-map")
    for x in range(1, num_of_data + 1):
        map.set(f"key{x}", x)
        print(f"{x}. key-value pairs have been added.")
    client.shutdown()
    
def check_map_data(num_of_data: int = 1000) -> None:
    client = HazelcastClient()
    map = client.get_map("my-distributed-map").blocking()
    keys = {f"key{i}" for i in range(1, num_of_data + 1)}
    data_dict = map.get_all(keys)
    data_items = sorted(data_dict.values())
    assert len(data_dict) == 1000, "Incorrect data amount!"
    for i, v in zip(data_items, range(1, num_of_data + 1)):
        assert i == v, "Data corrupted!"
    print("Data is OK!")
    client.shutdown()

def update_yaml_file(file_path: str, parameter_path: str, new_value: int) -> None:
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    parameter_list = parameter_path.split('.')
    current_node = data
    for parameter in parameter_list[:-1]:
        current_node = current_node.get(parameter, {})
    parameter_key = parameter_list[-1]
    current_node[parameter_key] = new_value
    with open(file_path, 'w') as file:
        yaml.dump(data, file) 

def no_lock() -> None:
    client = HazelcastClient()
    map = client.get_map("my-distributed-map")
    for i in range(1000):
        map.put('val', map.get('val').result()+1)
    print(f"Result = {map.get('val').result()}")
    client.shutdown()

def pessimistic_lock() -> None:
    client = HazelcastClient()
    map = client.get_map("my-distributed-map")
    for i in range(1000):
        map.lock('val').result()
        try:
            map.put('val', map.get('val').result()+1).result()
        finally:
            map.unlock('val')
    print(f"Result = {map.get('val').result()}")
    client.shutdown()

def optimistic_lock() -> None:
    client = HazelcastClient()
    map = client.get_map("my-distributed-map")
    for i in range(1000):
        while True:
            if map.replace_if_same('val', map.get('val').result(), map.get('val').result()+1).result():
                break
    print(f"Result = {map.get('val').result()}")
    client.shutdown()

def async_write(function) -> None:
    client = HazelcastClient()
    map = client.get_map("my-distributed-map")
    map.put('val', 0).result()

    processes = []
    for _ in range(3):
        p = Process(target=function)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    client.shutdown()

def put_data_in_map_tasks(backup_count: int = 1) -> None:
    update_yaml_file("hazelcast.yaml", 'hazelcast.map.my-distributed-map.backup-count', backup_count)

    if input("Start distributed map and 3 nodes? (y/n): ") == 'y':
        os.system('docker compose up -d')
        print("Distributed map and 3 nodes:")
        set_data()
        check_map_data()
        sleep(180)
        os.system('docker kill hazelcast1 hazelcast2 hazelcast3')
        os.system('docker rm hazelcast1 hazelcast2 hazelcast3')
        os.system('cls')
    if input("Start distributed map and 2 nodes? (y/n): ") == 'y':
        os.system('docker compose up -d')
        print("Distributed map and 2 nodes:")
        os.system('docker kill hazelcast3')
        set_data()
        check_map_data()
        sleep(180)
        os.system('docker kill hazelcast1 hazelcast2')
        os.system('docker rm hazelcast1 hazelcast2 hazelcast3')
        os.system('cls')
    if input("Start distributed map and 1 nodes? (y/n): ") == 'y':
        os.system('docker compose up -d')
        print("Distributed map and 1 nodes:")
        os.system('docker kill hazelcast2 hazelcast3')
        set_data()
        check_map_data()
        sleep(180)
        os.system('docker kill hazelcast1')
        os.system('docker rm hazelcast1 hazelcast2 hazelcast3')
        os.system('cls')
    if backup_count == 1:
        if input("Begin no lock write? (y/n): ") == 'y':
            os.system('docker compose up -d')
            os.system('docker kill hazelcast2 hazelcast3')
            async_write(no_lock)
            sleep(180)
            os.system('docker kill hazelcast1')
            os.system('docker rm hazelcast1 hazelcast2 hazelcast3')
        if input("Begin pessimistic write? (y/n): ") == 'y':
            os.system('docker compose up -d')
            os.system('docker kill hazelcast2 hazelcast3')
            async_write(pessimistic_lock)
            sleep(180)
            os.system('docker kill hazelcast1')
            os.system('docker rm hazelcast1 hazelcast2 hazelcast3')
        if input("Begin optimistic write? (y/n): ") == 'y':
            os.system('docker compose up -d')
            os.system('docker kill hazelcast2 hazelcast3')
            async_write(optimistic_lock)
            sleep(180)
            os.system('docker kill hazelcast1')
    os.system('docker kill hazelcast1 hazelcast2 hazelcast3 hazelcast-management-center')
    os.system('docker rm hazelcast1 hazelcast2 hazelcast3 hazelcast-management-center')
    os.system('cls')

def producer_member() -> None:
    client = HazelcastClient()
    queue = client.get_queue("queue")
    for k in range(1, 20):
        queue.offer(k)
        print(f"Producing: {k}.")
        sleep(2)  
    queue.offer(-1) 
    print("Producer Finished!")
    client.shutdown()

def consumer_member(consumer_string: str) -> None:
    client = HazelcastClient()
    queue = client.get_queue("queue")   
    while True:
        item = queue.take().result()
        print(f"{consumer_string}: consumed {item}.")
        if item == -1:
            queue.put(-1)
            break
        sleep(5)
    print(f"{consumer_string} Finished!")
    client.shutdown()

def async_queue_write(read: bool = True) -> None:
    os.system('docker compose up -d')
    producer = Process(target=producer_member)
   
    if read == True:
        consumer1 = Process(target=consumer_member, args=("Consumer 1", ))
        consumer2 = Process(target=consumer_member, args=("Consumer 2", ))

        producer.start()
        consumer1.start()
        consumer2.start()

        producer.join()
        consumer1.join()
        consumer2.join()
    else:
        producer.start()
        producer.join()
    
    sleep(180)

    os.system('docker kill hazelcast1 hazelcast2 hazelcast3')
    os.system('docker rm hazelcast1 hazelcast2 hazelcast3')


def main() -> None:
    put_data_in_map_tasks(2)
    put_data_in_map_tasks(1)
    put_data_in_map_tasks(0)
    async_queue_write()
    async_queue_write(False)

        
    
if __name__ == "__main__":
    main()
