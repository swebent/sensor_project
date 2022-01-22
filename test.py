import requests
import time
import socket

AGGREGATE_PORT = 32323
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) # socket

i = 0
now = time.perf_counter()

while True:
    i = i +1
    print(i)
    time.sleep(0.05) # hz = 20
    if time.perf_counter() - now > 15: break
    
    msg = 'virtual_sensor1/{}'.format(i)
    sock.sendto(msg.encode('utf-8'), ('127.0.0.1', AGGREGATE_PORT))


