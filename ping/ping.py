import os
import random
import requests
import time
from requests.auth import HTTPDigestAuth
from flask import Flask, jsonify, request
from flask_httpauth import HTTPDigestAuth as realAuth

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = realAuth()

url = 'https://act3pong.herokuapp.com/pong'

users = {
    "vcu" : "rams"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

delayStart = time.time()

r = requests.get(url, auth=HTTPDigestAuth('vcu','rams'))

delayEnd = time.time()

delay = (delayEnd - delayStart) * 1000

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message':'Page Not Found'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'message':'Internal Server Error'}), 500

@app.route('/ping', methods=['GET'])
@auth.login_required
def index():
    return jsonify({'pingpong_t': delay})