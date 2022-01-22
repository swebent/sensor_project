
import json
from threading import Lock, Thread
import socket

import requests
import time

local_mem = {}
mem_lock = Lock()

with open("state.json", 'r+') as file:
    local_mem = json.load(file)


class Aggregate:
    def __init__(self, base, room, port):
        self.room = room
        self.base = base
        self.db = local_mem
        self.port = port
    

    def start(self):
        thread1 = Thread(target=self.listener)
        thread1.start()

        while True:
            time.sleep(10)

            with mem_lock:
                database = self.db.copy()
            
            with open("state.json", 'r+') as file:
                file.seek(0)
                json.dump(database, file, indent=4)
            

    
    def send(self):
        # send data to main station, freq = 1 / 10min
        while True:

            with mem_lock:
                database = self.db.copy()

            response = requests.put(self.base + self.room, database)
            print(response.json())

            time.sleep(10)

        pass


    def save(self, sensor_name, data):
        # save data to local db
        sensor_exist = False

        with mem_lock:
            database = self.db.copy()

        for i in range(len(database[self.room])):
            if database[self.room][i]['name'] == sensor_name:
                sensor_exist = True

                arrayIsFull = len(database[self.room][i]['data']) >= database[self.room][i]['frequency'] # we have 20 data points in db
                
                with mem_lock:
                    if arrayIsFull: self.db[self.room][i]['data'].pop(0)

                    self.db[self.room][i]['data'].append(data)
                self.db[self.room][i]['average'] = sum(self.db[self.room][i]['data']) / len(self.db[self.room][i]['data'])
                break
        return sensor_exist


    def listener(self):
        # get info from sensors

        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', self.port))  # setup server

        while True:
            msg_bytes, _ = sock.recvfrom(1024)
            msg = msg_bytes.decode("utf-8").split('/')

            if len(msg) != 2: continue

            #print(msg)

            save_thread = Thread(target=self.save, args=[msg[0], int(msg[1])])
            save_thread.start()



if __name__ == "__main__":
    print('hej lisa \033[91m ❤\033[0m')

    BASE = "http://127.0.0.1:5000/"

    aa = Aggregate(BASE, 'Room1', 32323)

    #aa.start()
    #aa.send()


