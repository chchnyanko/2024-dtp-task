from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from math import ceil

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB = "splatoon3.db"
LOGINDB = "login.db"

app.config['SECRET_KEY'] = "MyReallySecretKey"

PAGESIZE = 12


def connect_database(query, id=None):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    if id:
        cursor.execute(query, id)
    else:
        cursor.execute(query)
    db.commit()
    results = cursor.fetchall()
    db.close()
    return results


def get_columns(query):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute(query)
    results = [description[0] for description in cursor.description]
    db.close()
    return results


def get_page(table, offset):
    query = "SELECT * FROM %.13s LIMIT ? OFFSET ?;" % (table)
    weapon = connect_database(query, (PAGESIZE, offset))
    return weapon


def select_weapon(query, weaponid):
    weapon = connect_database(query, weaponid)
    try:
        return weapon[0]
    except:
        return (0, 0)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/main/<int:page>/<int:weaponID>")
def main(page, weaponID):
    total_pages = ceil(connect_database("SELECT COUNT (*) FROM MainWeapon")[0][0] / 12)
    if page <= total_pages:
        offset = (page - 1) * PAGESIZE
    else:
        offset = (total_pages - 1) * PAGESIZE
    weapons = get_page("MainWeapon", offset)
    if weaponID != 0:
        selected_weapon = select_weapon("SELECT * FROM MainWeapon WHERE MainWeaponID = ?;", (weaponID, ))
        columns = get_columns("SELECT * FROM MainWeapon")
    else:
        selected_weapon = (0, 0)
        columns = (0, 0)
    return render_template("reworked_main.html", page=page, total_pages=total_pages, weapons=weapons, selected_weapon=selected_weapon, columns = columns, title="main")


@app.route("/sub/<int:page>/<int:weaponID>")
def sub(page, weaponID):
    total_pages = ceil(connect_database("SELECT COUNT (*) FROM SubWeapon")[0][0] / 12)
    if page <= total_pages:
        offset = (page - 1) * PAGESIZE
    else:
        offset = (total_pages - 1) * PAGESIZE
    weapons = get_page("SubWeapon", offset)
    if weaponID != 0:
        selected_weapon = select_weapon("SELECT * FROM SubWeapon WHERE SubWeaponID = ?;", (weaponID, ))
        columns = get_columns("SELECT * FROM SubWeapon")
    else:
        selected_weapon = (0, 0)
        columns = (0, 0)
    return render_template("reworked_main.html", page=page, total_pages=total_pages, weapons=weapons, selected_weapon=selected_weapon, columns=columns, title="sub")


@app.route("/special/<int:page>/<int:weaponID>")
def special(page, weaponID):
    total_pages = ceil(connect_database("SELECT COUNT (*) FROM SpecialWeapon")[0][0] / 12)
    if page <= total_pages:
        offset = (page - 1) * PAGESIZE
    else:
        offset = (total_pages - 1) * PAGESIZE
    weapons = get_page("SpecialWeapon", offset)
    if weaponID != 0:
        selected_weapon = select_weapon("SELECT * FROM SpecialWeapon WHERE SpecialWeaponID = ?;", (weaponID, ))
        columns = get_columns("SELECT * FROM SpecialWeapon")
    else:
        selected_weapon = (0, 0)
        columns = (0, 0)
    return render_template("reworked_main.html", page=page, total_pages=total_pages, weapons=weapons, selected_weapon=selected_weapon, columns=columns, title="special")


@app.route("/all/<int:page>/<int:weaponID>")
def all(page, weaponID):
    total_pages = ceil(connect_database("SELECT COUNT (*) FROM Weapons")[0][0] / 12)
    if page <= total_pages:
        offset = (page - 1) * PAGESIZE
    else:
        offset = (total_pages - 1) * PAGESIZE
    weapons = get_page("Weapons", offset)
    if weaponID != 0:
        selected_weapon = select_weapon("SELECT * FROM Weapons WHERE WeaponID = ?", (weaponID, ))
        columns = get_columns("SELECT * FROM Weapons")
        if selected_weapon[2]:
            selected_weapon += (int(ceil(int(selected_weapon[2])/12)),)
    else:
        selected_weapon = (0, 0)
        columns = (0, 0)
    return render_template("all.html", page=page, total_pages=total_pages, weapons=weapons, selected_weapon=selected_weapon, columns=columns, title="all")


if __name__ == "__main__":
    app.run(debug=True)