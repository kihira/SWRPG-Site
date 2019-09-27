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
    status = None
    if request.method == "POST":
        username = request.form.get("username", "")
        if username in users and request.form.get("password", "") == users[username]:
            session["username"] = request.form["username"]
            status = "success"
        else:
            status = "failed"
    return render_template("login.html", status=status)
