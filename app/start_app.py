import os
from flask import Flask, request, jsonify
from operator import itemgetter
from app.edu_cl_mail import get_mails

HOST = '0.0.0.0'
PORT = 80
DEBUG_PORT = 8099

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
        app.run(host=HOST, port=PORT, debug=False)
    else:
        app.run(host=HOST, port=DEBUG_PORT, debug=True)