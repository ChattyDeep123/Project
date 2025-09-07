"""
Main flask project handling all calls from front end and returning required data
using flask and sqlite3 
"""
from flask import Flask, render_template, request, g
import sqlite3

# Convert this file into a flask app
app = Flask(__name__)


# Function to open database
def open_db():
    if "db" not in g:
        g.db = sqlite3.connect("login.db")
        g.db.row_factory = sqlite3.Row
    return g.db

# Closing of database after each route's function has been executed
@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Home page
@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")

# Providing user with sign up page
@app.route("/signup")
def signup():
    return render_template("signup.html")

# Checking if sign up details are valid
@app.route("/check1", methods=["POST"])
def check1():
    name = request.form.get("name")
    pwd1 = request.form.get("pwd1")
    pwd2 = request.form.get("pwd2")
    if not name:
        return render_template("check1.html", fail = "No username")
    elif not pwd1 or not pwd2:
        return render_template("check1.html", fail = "Password missing")
    elif pwd1 != pwd2:
        return render_template("check1.html", fail = "Confirmed password didn't match")
    db = open_db()
    data = db.execute("SELECT name FROM users;")
    data = [row["name"] for row in data]
    if name in data:
        return render_template("check1.html", fail = "This username is already taken")
    db.execute("INSERT INTO users (name, pwd) VALUES (?,?);", (name, pwd1))
    db.execute()
    db.commit()
    return render_template("check1.html", success = "Successfully signed up")

# Providing user with sign in page
@app.route("/signin")
def signin():
    return render_template("signin.html")

# Checking if sign in details are valid
@app.route("/check2", methods=["POST"])
def check2():
    name = request.form.get("name")
    pwd = request.form.get("pwd")
    if not name:
        return render_template("check2.html", fail = "No username")
    elif not pwd:
        return render_template("check2.html", fail = "Password missing")
    db = open_db()
    data = db.execute("SELECT id FROM users WHERE name = ? AND pwd = ?;", (name, pwd)).fetchall()
    if not data:
        return render_template("check2.html", fail = "Incorrect username or password")
    return render_template("check2.html", success = "Logged In")


# To get chat message from browser
@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "POST":
        ques = request.form.get("ques")
        return render_template("chat.html", ques = ques)
    return render_template("chat.html")
