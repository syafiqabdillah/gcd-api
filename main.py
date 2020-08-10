from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
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
    list_titipan = db.get_locations()
    return jsonify({
        'data': list_titipan,
        'message': 'success'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")