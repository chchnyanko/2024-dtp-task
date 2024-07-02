from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from math import ceil

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB = "splatoon3.db"
LOGINDB = "login.db"

app.config['SECRET_KEY'] = "MyReallySecretKey"


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


def commit_database(query, id=None):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    if id:
        cursor.execute(query, id)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()
    return cursor.lastrowid


def query_db(sql,args=(),one=False):
    '''connect and query- will retun one item if one=true and can accept arguments as tuple'''
    db = sqlite3.connect(LOGINDB)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results


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
    total_pages = ceil(connect_database("SELECT COUNT (*) FROM Weapons")[0][0] / 12)
    if page <= total_pages:
        offset = (page-1)*weapon_amount
        weapon = connect_database("SELECT * FROM Weapons LIMIT ? OFFSET ?;", (weapon_amount, offset))
    else:
        offset = (total_pages - 1) * weapon_amount
        weapon = connect_database("SELECT * FROM Weapons LIMIT ? OFFSET ?;", (weapon_amount, offset))

    selected_weapon = connect_database(f"SELECT * FROM Weapons WHERE WeaponID = '{weaponID}';")
    if selected_weapon:
        selected_weapon = selected_weapon[0]

        if selected_weapon[2]:
            selected_weapon += (int(ceil(int(selected_weapon[2])/12)),)
    else:
        selected_weapon = (0, 0)
    return render_template("all.html", weapon=weapon, page=page, selected_weapon = selected_weapon, total_pages=total_pages)


@app.route("/sub/<int:page>/<int:weaponID>")
def sub(page, weaponID):
    weapon_amount = 12
    offset = (page-1)*weapon_amount
    weapon = connect_database("SELECT * FROM SubWeapon LIMIT ? OFFSET ?", (weapon_amount, offset))
    
    selected_weapon = connect_database(f"SELECT * FROM SubWeapon WHERE SubWeaponID = '{weaponID}';")
    if selected_weapon:
        selected_weapon = selected_weapon[0]
    else:
        selected_weapon.insert(0, 0)
    return render_template("sub.html", weapon=weapon, page=page, selected_weapon=selected_weapon)


@app.route("/special/<int:page>/<int:weaponID>")
def special(page, weaponID):
    weapon_amount = 12
    offset = (page-1)*weapon_amount
    weapon = connect_database("SELECT * FROM SpecialWeapon LIMIT ? OFFSET ?", (weapon_amount, offset))
    
    selected_weapon = connect_database(f"SELECT * FROM SpecialWeapon WHERE SpecialWeaponID = '{weaponID}';")
    if selected_weapon:
        selected_weapon = selected_weapon[0]
    else:
        selected_weapon.insert(0, 0)
    return render_template("special.html", weapon=weapon, page=page, selected_weapon=selected_weapon)


@app.route("/games")
def type():
    return render_template("games.html")


@app.route("/admin", methods=["GET","POST"])
def admin():
    message : str
    #if the user posts a username and password
    if request.method == "POST":
        #get the username and password
        username = request.form['username']
        password = request.form['password']
        #try to find this user in the database- note- just keepin' it simple so usernames must be unique
        sql = "SELECT * FROM Users WHERE Username = ?"
        user = query_db(sql=sql,args=(username,),one=True)
        if user:
            #we got a user!!
            #check password matches-
            try:
                if check_password_hash(user[1], password):
                    #we are logged in successfully
                    #Store the username in the session
                    session['user'] = user
                    message = "login successful"
            except:
                message = "login failed"
        else:
            message = "login failed"
    return render_template("admin.html", message=message)


@app.post("/add_weapon")
def add_weapon():
    print(request.form)
    update = request.form["update"]
    table = request.form["table"]
    id = request.form["id"]
    weapon_name = request.form["weapon_name"]
    main_weapon = request.form["main_weapon"]
    main_weapon_id = connect_database(f"SELECT MainWeaponID FROM MainWeapon WHERE MainWeaponName = '{main_weapon}'")[0][0]
    sub_weapon = request.form["sub_weapon"]
    sub_weapon_id = connect_database(f"SELECT SubWeaponID FROM SubWeapon WHERE SubWeaponName = '{sub_weapon}'")[0][0]
    special_weapon = request.form["special_weapon"]
    special_weapon_id = connect_database(f"SELECT SpecialWeaponID FROM SpecialWeapon WHERE SpecialWeaponName = '{special_weapon}'")[0][0]
    points = request.form["points"]
    version = request.form["version"]
    if update == "update":
        query = f"UPDATE Weapons SET WeaponName = '{weapon_name}', MainWeaponID = '{main_weapon_id}', SubWeaponID = '{sub_weapon_id}', SpecialWeaponID = '{special_weapon_id}', SpecialPoint = '{points}', VersionID = '{version}' WHERE WeaponID = {id}"
    else:
        query = f"INSERT INTO Weapons (WeaponName, MainWeaponID, SubWeaponID, SpecialWeaponID, SpecialPoint, VersionID) VALUES ('{weapon_name}',{main_weapon_id},{sub_weapon_id},{special_weapon_id},{points},{version})"
    commit_database(query)
    return redirect("/")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route('/signup', methods=["GET","POST"])
def signup():
    #if the user posts from the signup page
    if request.method == "POST":
        #add the new username and hashed password to the database
        username = request.form['username']
        password = request.form['password']
        #hash it with the cool secutiry function
        hashed_password = generate_password_hash(password)
        #write it as a new user to the database
        sql = "INSERT INTO Users (Username,Password) VALUES (?,?)"
        query_db(sql,(username,hashed_password))
    return render_template("signup.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("/404.html", error=e), 404


if __name__ == "__main__":
    app.run(debug=True)