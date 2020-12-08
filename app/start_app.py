import os
from flask import Flask, request, jsonify
from operator import itemgetter
from app.edu_cl_mail import get_mails, get_all_mails, get_amount_inbox, get_all_inbox, check_login
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

def get_env(key, fallback):
    try:
        return os.environ[key]
    except:
        return fallback

HOST = get_env('HOST', '0.0.0.0')
PORT = get_env('PORT', 80)
DEBUG_PORT = get_env('DEBUG_PORT', 8099)
SSL_CERT_LOCATION = get_env('SSL_CERT_LOCATION', 'cert.pem')
SSL_CERT_KEY_LOCATION = get_env('SSL_CERT_KEY_LOCATION', 'key.pem')

app = Flask(__name__)
CORS(app)

@app.route("/api/login_check", methods=['POST'])
def login_check():
    """ returns "true", "false" or "invalid credentials or internal error" """
    try:
        username, password = itemgetter('username', 'password')(request.json)
        login_status = check_login(username, password)
        return jsonify(login_status)
    except:
        return jsonify('invalid credentials or internal error')

@app.route("/api/get_mails", methods=['POST'])
def get_mails_all():
    """ returns all mails from the default inbox """
    try:
        username, password = itemgetter('username', 'password')(request.json)
        mails = get_all_mails(username, password)
        return jsonify(mails)
    except:
        return jsonify('invalid credentials or internal error')

@app.route("/api/get_mails/<int:amount>", methods=['POST'])
def get_mails_amount(amount):
    """ returns max <amount> mails from the inbox """
    try:
        username, password = itemgetter('username', 'password')(request.json)
        mails = get_mails(username, password, amount)
        return jsonify(mails)
    except:
        return jsonify('invalid credentials or internal error')


@app.route("/api/inbox/<name>", methods=['POST'])
def inbox_all(name):
    """ returns all mails from the inbox <name>"""
    try:
        username, password = itemgetter('username', 'password')(request.json)
        mails = get_all_inbox(username, password, name)
        return jsonify(mails)
    except:
        return jsonify('invalid credentials or internal error')

@app.route("/api/inbox/<name>/<int:amount>", methods=['POST'])
def inbox_amount(name, amount):
    """ returns <amount> mails from the inbox <name>"""
    try:
        username, password = itemgetter('username', 'password')(request.json)
        mails = get_amount_inbox(username, password, amount, name)
        return jsonify(mails)
    except:
        return jsonify('invalid credentials or internal error')

if __name__ == "__main__":
    if 'DEBUG' not in os.environ:
        app.run(host=HOST, port=PORT, debug=False, ssl_context=(SSL_CERT_LOCATION, SSL_CERT_KEY_LOCATION))
    else:
        app.run(host=HOST, port=DEBUG_PORT, debug=True)
