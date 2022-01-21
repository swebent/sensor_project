
import json
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

app = Flask(__name__)
api = Api(app)

class Aggregate(Resource):
	def get(self):
		with open("state.json", 'r+') as file:
			file_data = json.load(file)

			return file_data

	def put(self, sensor_name ,sensor_data):
		#args = video_put_args.parse_args()		
		#videos[video_id] = args
		with open("state.json", 'r+') as file:
			file_data = json.load(file)

			sensor_exist = False

			for i in range(len(file_data['Room1'])):
				if file_data['Room1'][i]['name'] == sensor_name:
					sensor_exist = True

					if len(file_data['Room1'][i]['data']) >= file_data['Room1'][i]['frequency']: # we have 20 data points in db
						file_data['Room1'][i]['data'].pop()
					
					file_data['Room1'][i]['data'].append(sensor_data)
					file_data['Room1'][i]['average'] = sum(file_data['Room1'][i]['data']) / len(file_data['Room1'][i]['data'])
					break
			
			file.seek(0)
			json.dump(file_data, file, indent=4)
			file.close()

		return {'sensor_found': sensor_exist, 'value_added': sensor_data}, 200

api.add_resource(Aggregate, "/<string:sensor_name>/<int:sensor_data>")

if __name__ == "__main__":
	print('hej lisa \033[91m ❤\033[0m')
	app.run(debug=True)
	#database()

