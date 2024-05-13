from flask import Flask, render_template
import sqlite3


# im a pp poo poo :)
app = Flask(__name__)

@app.route("/")
def homely_home():
    return render_template("Index.html")

if __name__ == "__main__":
    app.run(debug=True)

    # i am turning red from turning red the movie