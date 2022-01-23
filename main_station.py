import json
from flask import Flask, request
from threading import Lock
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import time

app = Flask(__name__)

db_lock = Lock()

with open("main_station_db.json", 'r+') as file:
    local_mem = json.load(file)

@app.route("/post_data/<string:room>", methods=["POST"])
def post_data(room):
    json_data = request.get_json()

    with db_lock:
        with open("main_station_db.json", 'r+') as file:
            database = json.load(file)
            database[room] = json_data
            file.seek(0)
            json.dump(database, file, indent=4)
            file.close()
    return 'done!',200

info = {'test': 23}
@app.route("/rooms/<string:room>", methods=["GET"])
def send_info(room):
    database = {}
    return_data = {}
    with db_lock:
        with open("main_station_db.json", 'r+') as file:
            database = json.load(file)

    for r, r_db in database.items():
        if r == room:
            for sensor in r_db:
                name = sensor['name']
                return_data[name] = sensor
                del return_data[name]['name']
                del return_data[name]['recent_data']
            break

    return return_data, 200


if __name__ == "__main__":
	
	app.run(debug=True)
