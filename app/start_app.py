import os
from flask import Flask, render_template, Response, jsonify

HOST = '0.0.0.0'
PORT = 80
DEBUG_PORT = 8099

app = Flask(__name__)

@app.route("/")
def main():
    return "it works!"

if __name__ == "__main__":
    if 'DEBUG' not in os.environ:
        app.run(host=HOST, port=PORT, debug=False)
    else:
        app.run(host=HOST, port=DEBUG_PORT, debug=True)