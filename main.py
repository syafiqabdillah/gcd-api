from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from datetime import datetime
import db 

load_dotenv()
# JWT_KEY = os.getenv('JWT_KEY')

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello():
    return "Hello, are you trying to hack this ? pls don't"

@app.route('/get-all-sublocations', methods=['GET'])
def get_all_sublocations():
    try:
        sublocation_list = db.get_all_sublocations()
        return jsonify({
            'data': sublocation_list,
            'message': 'success'
        }), 200
    except:
        return jsonify({
            'message': 'server error'
        }), 500

@app.route('/get-crowd-density-information', methods=['GET'])
def get_crowd_density_information():
    try:
        list_location = db.get_crowd_density_information()
        return jsonify({
            'data': list_location,
            'message': 'success'
        }), 200
    except:
        return jsonify({
            'message': 'server error'
        }), 500

@app.route('/get-suggested-locations', methods=['GET'])
def get_suggested_locations():
    try:
        nameslist = db.get_suggested_locations()
        return jsonify({
            'data': nameslist,
            'message': 'success'
        }), 200
    except:
        return jsonify({
            'message': 'server error'
        }), 500

@app.route('/suggest-location', methods=['POST'])
def suggest_location():
    data = request.json
    location_name = data['location_name']
    sublocation_names = data['sublocation_names']
    query_result = db.suggest_location(location_name, sublocation_names)
    message = query_result['message']
    returning_data = query_result['data']
    if message == 'success':
        return jsonify(query_result), 200
    else:
        return jsonify({
            'message': message,
        }), 500

@app.route('/add-location', methods=['POST'])
def add_location():
    data = request.json
    location_name = data['location_name']
    sublocation_names = data['sublocation_names']
    query_result = db.add_location(location_name, sublocation_names)
    message = query_result['message']
    returning_data = query_result['data']
    if message == 'success':
        return jsonify(query_result), 200
    else:
        return jsonify({
            'message': message,
        }), 500

@app.route('/add-sublocation', methods=['POST'])
def add_sublocation():
    data = request.json
    name = data['sublocation_name']
    location_id = data['location_id']
    query_result = db.add_sublocation(location_id, name)
    message = query_result['message']
    returning_data = query_result['data']
    if message == 'success':
        return jsonify(query_result), 200
    else:
        return jsonify({
            'message': message,
        }), 500

@app.route('/add-crowd-data', methods=['POST'])
def add_crowd_data():
    data = request.json

    sublocation_id = data['sublocation_id']
    is_crowded = data['is_crowded']
    created_at = datetime.now()

    query_result = db.add_crowd_data(sublocation_id, is_crowded, created_at)
    message = query_result['message']
    returning_data = query_result['data']
    if message == 'success':
        return jsonify(query_result), 200
    else:
        return jsonify({
            'message': message,
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")