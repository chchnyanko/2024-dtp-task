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
    results = cursor.fetchall
    db.close()
    return results


def get_page(table, pagenum):
    offset = (pagenum - 1) * PAGESIZE
    query = "SELECT * FROM %.13s LIMIT ? OFFSET ?;" % (table)
    print(query)
    weapon = connect_database(query, (PAGESIZE, offset))
    return weapon[0]


def select_weapon(query, weaponid):
    weapon = connect_database(query, weaponid)
    if weapon[0] is not None:
        return weapon[0]
    else:
        return None

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/main/<int:page>/<int:weaponID>")
def main(page, weaponID):
    weapons = get_page("MainWeapon", page)
    selected_weapon = select_weapon("SELECT * FROM MainWeapons WHERE MainWeaponID = ?;", (weaponID, ))
    return render_template("main.html", weapons=weapons, selected_weapon=selected_weapon)


if __name__ == "__main__":
    app.run(debug=True)