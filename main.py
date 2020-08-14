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

@app.route('/get-locations', methods=['GET'])
def get_locations():
    try:
        list_location = db.get_locations()
        return jsonify({
            'data': list_location,
            'message': 'success'
        }), 200
    except:
        return jsonify({
            'message': 'server error'
        }), 500

@app.route('/get-location-names', methods=['GET'])
def get_location_names():
    try:
        nameslist = db.get_location_names()
        return jsonify({
            'data': nameslist,
            'message': 'success'
        }), 200
    except:
        return jsonify({
            'message': 'server error'
        }), 500

@app.route('/add-location', methods=['POST'])
def add_location():
    data = request.json
    name = data['location_name']
    query_result = db.add_location(name)
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
    id_location = data['id_location']
    query_result = db.add_sublocation(id_location, name)
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
    app.run(debug=True)