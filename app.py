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


@app.route("/main/<int:page>/<int:weaponID>")
def main(page, weaponID):
    weapon_amount = 12
    offset = (page-1)*weapon_amount
    weapon = connect_database("SELECT * FROM MainWeapon LIMIT ? OFFSET ?", (weapon_amount, offset))

    selected_weapon = connect_database(f"SELECT * FROM MainWeapon WHERE MainWeaponID = '{weaponID}';")
    if selected_weapon:
        selected_weapon = selected_weapon[0]
    else:
        selected_weapon.insert(0, 0)
    return render_template("main.html", weapon=weapon, page=page, selected_weapon=selected_weapon)


@app.route("/all/<int:page>/<int:weaponID>")
def all(page, weaponID):
    weapon_amount = 12
    offset = (page-1)*weapon_amount
    weapon = connect_database("SELECT * FROM Weapons LIMIT ? OFFSET ?;", (weapon_amount, offset))

    selected_weapon = connect_database(f"SELECT * FROM Weapons WHERE WeaponID = '{weaponID}';")
    if selected_weapon:
        selected_weapon = selected_weapon[0]
    else:
        selected_weapon.insert(0, 0)
    return render_template("all.html", weapon=weapon, page=page, selected_weapon = selected_weapon)


@app.route("/sub/<int:page>")
def sub(page):
    weapon_amount = 12
    offset = (page-1)*weapon_amount
    weapon = connect_database("SELECT * FROM SubWeapon LIMIT ? OFFSET ?", (weapon_amount, offset))
    return render_template("sub.html", weapon=weapon, page=page)


@app.route("/special/<int:page>")
def special(page):
    weapon_amount = 12
    offset = (page-1)*weapon_amount
    weapon = connect_database("SELECT * FROM SpecialWeapon LIMIT ? OFFSET ?", (weapon_amount, offset))
    return render_template("special.html", weapon=weapon, page=page)


@app.route("/type")
def type():
    return render_template("type.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("/404.html", error = e), 404


if __name__ == "__main__":
    app.run(debug=True)