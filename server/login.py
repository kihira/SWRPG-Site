import json
from flask import request, session, render_template
from server import app

users = {}

try:
    data = open("users.json").read()
    users = json.loads(data)
except:
    print("Failed to load users file, you won't be able to login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        print(request.form)
        if username in users and request.form.get("password", "") == users[username]:
            session["username"] = request.form["username"]
            print("Logged in")
    return render_template("login.html")
