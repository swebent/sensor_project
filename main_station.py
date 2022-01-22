import json
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import time

app = Flask(__name__)
api = Api(app)

put_args = reqparse.RequestParser()
put_args.add_argument("Room1", type=list, required=True)

class MainStation(Resource):

    def get(self, room):
        # send current info

        return 200

    def put(self, room):
        # an aggregate put info into general db.

        #args = put_args.parse_args()
        args = request.json
        #json_data = request.get_json(force=True)
        print(room, '\n')
        print(args)
        
        #videos[video_id] = args
        return 200

api.add_resource(MainStation, "/<string:room>")

if __name__ == "__main__":
	
	app.run(debug=True)



	#database()
