import json

from flask import request, session, render_template

from server import app


data = open("users.json").read()
users = json.loads(data)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        print(request.form)
        if username in users and request.form.get("password", "") == users[username]:
            session["username"] = request.form["username"]
            print("Logged in")
    return render_template("login.html")
