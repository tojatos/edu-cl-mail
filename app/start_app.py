import os
from flask import Flask, request, jsonify
from operator import itemgetter
from app.edu_cl_mail import get_mails

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

@app.route("/api/get_mails/<amount>", methods=['POST'])
def main(amount):
    try:
        username, password = itemgetter('username', 'password')(request.json)
        mails = get_mails(username, password, int(amount))
        return jsonify(mails)
    except:
        return jsonify('invalid credentials or internal error')

if __name__ == "__main__":
    if 'DEBUG' not in os.environ:
        app.run(host=HOST, port=PORT, debug=False, ssl_context=(SSL_CERT_LOCATION, SSL_CERT_KEY_LOCATION))
    else:
        app.run(host=HOST, port=DEBUG_PORT, debug=True)

