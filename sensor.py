import time
import socket
import random
from threading import Thread

AGGREGATE_PORT = 32323
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) # socket


def sensor1():
    while True:
        time.sleep(0.05) # hz = 20
        
        msg = 'virtual_sensor1/{}'.format(random.randint(1,50))
        sock.sendto(msg.encode('utf-8'), ('127.0.0.1', AGGREGATE_PORT))

def sensor2():
    while True:
        time.sleep(0.1) # hz = 10
        
        msg = 'virtual_sensor2/{}'.format(random.random())
        sock.sendto(msg.encode('utf-8'), ('127.0.0.1', AGGREGATE_PORT))

if __name__ == "__main__":
    t1 = Thread(target=sensor1)
    t2 = Thread(target=sensor2)

    t1.start()
    time.sleep(0.005)
    t2.start()

