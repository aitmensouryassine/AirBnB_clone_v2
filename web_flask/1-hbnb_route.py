#!/usr/bin/python3
"""Starts a Flask Web App on 0.0.0.0:5000
   routes: "/", "hbnb"
"""

from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    return ("Hello HBNB!")


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return ("HBNB")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
