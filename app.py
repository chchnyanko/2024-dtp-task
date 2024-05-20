from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/all")
def all():
    return render_template("all.html")


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/sub")
def sub():
    return render_template("sub.html")


@app.route("/special")
def special():
    return render_template("special.html")


@app.route("/type")
def type():
    return render_template("type.html")


if __name__ == "__main__":
    app.run(debug=True)