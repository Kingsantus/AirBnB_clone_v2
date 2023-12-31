#!/usr/bin/python3
""" This script starts a Flask web application """

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def display():
    """ Returns message to be displayed """
    return "Hello HBNB!"

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Returns message to be displayed """
    return "HBNB"

@app.route("/c/<text>", strict_slashes=False)
def display_c(text):
    """ Returns message to be displayed """
    processed_text = text.replace("_", " ")
    return f"C {processed_text}"

@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def display_python(text="is cool"):
    """ Returns message to be displayed """
    processed_text = text.replace("_", " ")
    return f"Python {processed_text}"

@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """ Returns message to be displayed """
    return f"{n} is a number"

@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """ Displays a HTML page """
    return render_template("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
