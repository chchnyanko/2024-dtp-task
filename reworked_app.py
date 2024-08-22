'''Splatoon 3 wiki'''
import sqlite3
from math import ceil
from flask import Flask, render_template, request, redirect, flash


from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB = "splatoon3.db"

app.config['SECRET_KEY'] = "MyReallySecretKey"

LABEL_NAMES: dict = {
    "weapon": ["Weapon ID", "Weapon Name", "Main Weapon", "Sub Weapon", "Special Weapon", "Points for Special", "Introduced Version"],
    "main": ["Weapon ID", "Weapon Name", "Weapon Type", "Damage", "Range", "Attack Rate", "Ink Usage", "Speed While Shooting"],
    "sub": ["Weapon ID", "Weapon Name", "Damage", "Ink Consumption", "Tracking Duration", "Damage Duration"],
    "special": ["Weapon ID", "Weapon Name", "Damage", "Number of Attacks", "Duration"]
}

#the number of weapons shown in 1 page
PAGESIZE = 12 


def connect_database(query, id=None):
    '''Execute queries and commit changes to the database'''
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


def get_page(table, offset):
    '''Get the weapons for the page selected'''
    query = f"SELECT * FROM {table} LIMIT ? OFFSET ?;"
    weapon = connect_database(query, (PAGESIZE, offset))
    return weapon


def select_weapon(query, weapon_id):
    '''Get the data for the selected weapon'''
    weapon = connect_database(query, weapon_id)
    try:
        return weapon[0]
    except:
        return (0, 0)


@app.route("/")
def home():
    '''The homepage'''
    return render_template("home.html")


@app.route("/main/<int:page>/<int:weapon_id>")
def main(page, weapon_id):
    '''The page for main weapons'''
    #get the total number of pages there are for main weapons
    total_pages = ceil(connect_database("SELECT COUNT (*) FROM MainWeapon")[0][0] / 12)
    if page <= total_pages:
        offset = (page - 1) * PAGESIZE
    else:
        #if the page number is greater than the total number of pages, send the user to the last page
        offset = (total_pages - 1) * PAGESIZE
    #get the main weapons that are going to be shown in the current page
    main_weapons = get_page("MainWeapon", offset)
    #if there is a selected weapon, get the data for that weapon
    if weapon_id != 0:
        selected_weapon = select_weapon("SELECT * FROM MainWeapon WHERE MainWeaponID = ?;", (weapon_id, ))
        weapon_type = connect_database("SELECT WeaponType FROM WeaponTypes WHERE WeaponTypeID = ?;", (selected_weapon[2],))
    else:
        selected_weapon = (0, 0)
        weapon_type = 0
    return render_template("reworked_main.html", page=page, total_pages=total_pages, weapons=main_weapons, selected_weapon=selected_weapon, weapon_type=weapon_type, title="main")


@app.route("/sub/<int:page>/<int:weapon_id>")
def sub(page, weapon_id):
    '''The page for sub weapons'''
    #get the total number of pages there are for sub weapons
    total_pages = ceil(connect_database("SELECT COUNT (*) FROM SubWeapon")[0][0] / 12)
    if page <= total_pages:
        offset = (page - 1) * PAGESIZE
    else:
        #if the page number is greater than the total number of pages, send the user to the last page
        offset = (total_pages - 1) * PAGESIZE
    #get the sub weapons that are going to be shown in the current page
    sub_weapons = get_page("SubWeapon", offset)
    #if there is a selected weapon, get the data for that weapon
    if weapon_id != 0:
        selected_weapon = select_weapon("SELECT * FROM SubWeapon WHERE SubWeaponID = ?;", (weapon_id, ))
    else:
        selected_weapon = (0, 0)
    return render_template("reworked_main.html", page=page, total_pages=total_pages, weapons=sub_weapons, selected_weapon=selected_weapon, title="sub")


@app.route("/special/<int:page>/<int:weapon_id>")
def special(page, weapon_id):
    '''The page for special weapons'''
    #get the total number of pages there are for special weapons
    total_pages = ceil(connect_database("SELECT COUNT (*) FROM SpecialWeapon")[0][0] / 12)
    if page <= total_pages:
        offset = (page - 1) * PAGESIZE
    else:
        #if the page number is greater than the total number of pages, send the user to the last page
        offset = (total_pages - 1) * PAGESIZE
    #get the special weapons that are going to be shown in the current page
    special_weapons = get_page("SpecialWeapon", offset)
    #if there is a selected weapon, get the data for that weapon
    if weapon_id != 0:
        selected_weapon = select_weapon("SELECT * FROM SpecialWeapon WHERE SpecialWeaponID = ?;", (weapon_id, ))
    else:
        selected_weapon = (0, 0)
    return render_template("reworked_main.html", page=page, total_pages=total_pages, weapons=special_weapons, selected_weapon=selected_weapon, title="special")


@app.route("/all/<int:page>/<int:weapon_id>")
def weapons(page, weapon_id):
    '''The page for all the weapons and their kits'''
    #get the total number of pages there are for all weapons
    total_pages = ceil(connect_database("SELECT COUNT (*) FROM Weapons")[0][0] / 12)
    if page <= total_pages:
        offset = (page - 1) * PAGESIZE
    else:
        #if the page number is greater than the total number of pages, send the user to the last page
        offset = (total_pages - 1) * PAGESIZE
    #get the weapons that are going to be shown in the current page
    all_weapons = get_page("Weapons", offset)
    #if there is a selected weapon, get the data for that weapon
    if weapon_id != 0:
        selected_weapon = select_weapon("SELECT * FROM Weapons WHERE WeaponID = ?", (weapon_id, ))
        #if the selected weapon exists, add data for the weapon ID's for the main, sub and special weapons to use for links
        if len(selected_weapon) > 2:
            selected_weapon += (int(ceil(int(selected_weapon[2])/12)),)
            selected_weapon += (connect_database("SELECT SubWeaponName FROM SubWeapon WHERE SubweaponID = ?", (selected_weapon[3], ))[0][0],)
            selected_weapon += (connect_database("SELECT SpecialWeaponName FROM SpecialWeapon WHERE SpecialweaponID = ?", (selected_weapon[4], ))[0][0],)
    else:
        selected_weapon = (0, 0)
    return render_template("all.html", page=page, total_pages=total_pages, weapons=all_weapons, selected_weapon=selected_weapon, title="all")


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    '''The admin page for the admin login'''
    try:
        if request.method == "POST":
            #get the inputted username and password
            username = request.form["username"]
            password = request.form["password"]
            query = "SELECT password FROM Users WHERE username = ?"
            correct_password = connect_database(query, (username,))[0][0]
            #check is the inputted password is the same as the correct password
            if check_password_hash(correct_password, password):
                #get the names of all of the weapons
                main_query = "SELECT MainWeaponName FROM MainWeapon"
                mains = connect_database(main_query)
                sub_query = "SELECT SubWeaponName FROM SubWeapon"
                subs = connect_database(sub_query)
                speical_query = "SELECT SpecialWeaponName FROM SpecialWeapon"
                specials = connect_database(speical_query)
                type_query = "SELECT WeaponType FROM WeaponTypes"
                main_types = connect_database(type_query)
                return render_template("admin.html", main_weapons=mains, sub_weapons=subs, special_weapons=specials, main_types=main_types)
    except:
        #if the inputted username or password doesn't match or exist, flash the message
        flash("Username or Password is Incorrect")
    return render_template("admin_login.html")


@app.post("/add_weapon")
def add_weapon():
    '''The admin page for adding and editing data from the database'''
    
    update = request.form["update"]
    table = request.form["table"]
    id = request.form["id"]

    if update == "delete":
        query = "DELETE FROM ? WHERE ? = ?"
        connect_database(query, (id, ))


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
        query = "UPDATE Weapons SET WeaponName = ?, MainWeaponID = ?, SubWeaponID = ?, SpecialWeaponID = ?, SpecialPoint = ?, VersionID = ? WHERE weapon_id = ?"
        connect_database(query, (weapon_name, main_weapon_id, sub_weapon_id, special_weapon_id, points, version, id))
    elif update == "add":
        query = "INSERT INTO Weapons (WeaponName, MainWeaponID, SubWeaponID, SpecialWeaponID, SpecialPoint, VersionID) VALUES (?,?,?,?,?,?)"
        connect_database(query, (weapon_name, main_weapon_id, sub_weapon_id, special_weapon_id, points, version))
    elif update == "delete":
        query = "DELETE FROM Weapons WHERE weapon_id = ?"
        connect_database(query, (id, ))
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    '''The admin page for adding admin users'''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        query = "INSERT INTO Users (Username, Password) VALUES (?,?)"
        connect_database(query, (username, hashed_password))
    return render_template("signup.html")


@app.route("/games")
def games():
    '''This is an easteregg with all of the games that I have made in the past'''
    return render_template("games.html")


@app.errorhandler(404)
def page_not_found(e):
    '''The 404 error page'''
    return render_template("/404.html", error=e), 404


if __name__ == "__main__":
    app.run(debug=True)
