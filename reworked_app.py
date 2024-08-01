from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
from math import ceil

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB = "splatoon3.db"

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
        print("hello", selected_weapon)
        if len(selected_weapon) > 2:
            selected_weapon += (int(ceil(int(selected_weapon[2])/12)),)
            selected_weapon += (connect_database("SELECT SubWeaponName FROM SubWeapon WHERE SubWeaponID = ?", (selected_weapon[3], ))[0][0],)
            selected_weapon += (connect_database("SELECT SpecialWeaponName FROM SpecialWeapon WHERE SpecialWeaponID = ?", (selected_weapon[4], ))[0][0],)
    else:
        selected_weapon = (0, 0)
        columns = (0, 0)
    return render_template("all.html", page=page, total_pages=total_pages, weapons=weapons, selected_weapon=selected_weapon, columns=columns, title="all")


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    try:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            query = "SELECT password FROM Users WHERE username = ?"
            print(connect_database(query, (username,)))
            correct_password = connect_database(query, (username,))[0][0]
            if check_password_hash(correct_password, password):
                print("password correct")
                main_query = "SELECT MainWeaponName FROM MainWeapon"
                mains = connect_database(main_query)
                sub_query = "SELECT SubWeaponName FROM SubWeapon"
                subs = connect_database(sub_query)
                speical_query = "SELECT SpecialWeaponName FROM SpecialWeapon"
                specials = connect_database(speical_query)
                return render_template("admin.html", main_weapons=mains, sub_weapons=subs, special_weapons=specials)
    except:
        flash("Username or Password is Incorrect")
    return render_template("admin_login.html")


@app.post("/add_weapon")
def add_weapon():
    print(request.form)
    update = request.form["update"]
    table = request.form["table"]
    id = request.form["id"]

    weapon_name = request.form["weapon_name"]
    main_weapon = request.form["main_weapon"]

    main_weapon_id = connect_database("SELECT MainWeaponID FROM MainWeapon WHERE MainWeaponName = ?", (main_weapon,))[0][0]
    sub_weapon = request.form["sub_weapon"]
    sub_weapon_id = connect_database("SELECT SubWeaponID FROM SubWeapon WHERE SubWeaponName = ?", (sub_weapon,))[0][0]
    special_weapon = request.form["special_weapon"]
    special_weapon_id = connect_database("SELECT SpecialWeaponID FROM SpecialWeapon WHERE SpecialWeaponName = ?", (special_weapon, ))[0][0]
    
    points = request.form["points"]
    version = request.form["version"]
    if update == "update":
        query = "UPDATE Weapons SET WeaponName = ?, MainWeaponID = ?, SubWeaponID = ?, SpecialWeaponID = ?, SpecialPoint = ?, VersionID = ? WHERE WeaponID = ?"
        connect_database(query, (weapon_name, main_weapon_id, sub_weapon_id, special_weapon_id, points, version, id))
    elif update == "add":
        query = "INSERT INTO Weapons (WeaponName, MainWeaponID, SubWeaponID, SpecialWeaponID, SpecialPoint, VersionID) VALUES (?,?,?,?,?,?)"
        connect_database(query, (weapon_name, main_weapon_id, sub_weapon_id, special_weapon_id, points, version))
    elif update == "delete":
        query = "DELETE FROM Weapons WHERE WeaponID = ?"
        connect_database(query, (id, ))
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        query = "INSERT INTO Users (Username, Password) VALUES (?,?)"
        connect_database(query, (username, hashed_password))
    return render_template("signup.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("/404.html", error=e), 404


if __name__ == "__main__":
    app.run(debug=True)
