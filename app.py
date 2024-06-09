from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

DB = "splatoon3.db"


def connect_database(query, id=None):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    if id:
        cursor.execute(query, id)
    else:
        cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/all/<int:page>/<int:weaponID>")
def all(page, weaponID):
    weapon_amount = 12
    offset = (page-1)*weapon_amount
    weapon = connect_database("SELECT * FROM Weapons LIMIT ? OFFSET ?;", (weapon_amount, offset))
    selected_weapon = connect_database(f"SELECT * FROM Weapons WHERE WeaponID = '{weaponID}';")
    if selected_weapon:
        selected_weapon = selected_weapon[0]
    return render_template("all.html", weapon=weapon, page=page, selected_weapon = selected_weapon)


@app.route("/all")
def main_pppoopoo():
    return redirect(url_for('main', page=1))


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