#!/usr/bin/python3
"""Starts a Flask Web App on 0.0.0.0:5000
   routes: "/", "hbnb", "/c/<text>"
"""

from flask import Flask, render_template


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    return ("Hello HBNB!")


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return ("HBNB")


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    return (f"C {text.replace('_', ' ')}")


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is cool"):
    return (f"Python {text.replace('_', ' ')}")


@app.route("/number/<int:n>")
def number(n):
    return (f"{n} is a number")


@app.route("/number_template/<int:n>")
def number_template(n):
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>")
def number_odd_or_even(n):
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
