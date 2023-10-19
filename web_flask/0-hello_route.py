#!/usr/bin/python3
"""Starts a Flask Web App on 0.0.0.0:5000"""
from flask import Flask


app = Flask(__name__)


@app.route("/")
def index():
    return ("Hello HBNB!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
