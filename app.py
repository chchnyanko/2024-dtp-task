from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

DB = "splatoon3.db"


def connect_database_with_id(query, id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(query, id)
    results = cursor.fetchall()
    conn.close()
    return results


def connect_database(query):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


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
    weepon = connect_database("SELECT * FROM SpecialWeapon;")
    return render_template("special.html", weepon=weepon)


@app.route("/type")
def type():
    return render_template("type.html")


if __name__ == "__main__":
    app.run(debug=True)