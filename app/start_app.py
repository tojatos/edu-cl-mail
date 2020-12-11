import os
from functools import wraps

from flask import Flask, request, jsonify, g
from operator import itemgetter
from app.edu_cl_mail import get_mails, get_all_mails, get_amount_inbox, get_all_inbox, check_login, get_page_inbox
from flask_cors import CORS

from dotenv import load_dotenv

load_dotenv()


def get_env(key, fallback):
    try:
        return os.environ[key]
    except KeyError:
        return fallback


HOST = get_env('HOST', '0.0.0.0')
PORT = get_env('PORT', 80)
DEBUG_PORT = get_env('DEBUG_PORT', 8099)
SSL_CERT_LOCATION = get_env('SSL_CERT_LOCATION', 'cert.pem')
SSL_CERT_KEY_LOCATION = get_env('SSL_CERT_KEY_LOCATION', 'key.pem')

app = Flask(__name__)
CORS(app)


@app.before_request
def before_request():
    if request.json:
        g.username, g.password = itemgetter('username', 'password')(request.json)


def try_jsonify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return jsonify(func(*args, **kwargs))
        except:
            return jsonify('invalid credentials or internal error')

    return wrapper


@app.route("/api/login_check", methods=['POST'])
@try_jsonify
def login_check():
    """ returns "true", "false" or "invalid credentials or internal error" """
    return check_login(g.username, g.password)


@app.route("/api/get_mails", methods=['POST'])
@try_jsonify
def get_mails_all():
    """ returns all mails from the default inbox """
    return get_all_mails(g.username, g.password)


@app.route("/api/get_mails/<int:amount>", methods=['POST'])
@try_jsonify
def get_mails_amount(amount):
    """ returns max <amount> mails from the inbox """
    return get_mails(g.username, g.password, amount)


@app.route("/api/inbox/<name>", methods=['POST'])
@try_jsonify
def inbox_all(name):
    """ returns all mails from the inbox <name>"""
    return get_all_inbox(g.username, g.password, name)


@app.route("/api/inbox/<name>/<int:amount>", methods=['POST'])
@try_jsonify
def inbox_amount(name, amount):
    """ returns <amount> mails from the inbox <name>"""
    return get_amount_inbox(g.username, g.password, amount, name)


@app.route("/api/inbox_page/<name>/<int:page>", methods=['POST'])
@try_jsonify
def inbox_page(name, page):
    """ returns max 5 mails from page <page> in the inbox <name>"""
    return get_page_inbox(g.username, g.password, page, name)


if __name__ == "__main__":
    if 'DEBUG' not in os.environ:
        app.run(host=HOST, port=PORT, debug=False, ssl_context=(SSL_CERT_LOCATION, SSL_CERT_KEY_LOCATION))
    else:
        app.run(host=HOST, port=DEBUG_PORT, debug=True)
