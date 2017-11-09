from server.app import app
from server.db import db
from flask import Markup, render_template


@app.route("/skills/")
def all_skills():
    entries = []
    for skill in db.skills.find({}):
        entry = [Markup("<a href=\"./{0}\">{0}</a>".format(skill["_id"])),
                 skill["characteristic"], skill["type"], skill["index"]]
        entries.append(entry)

    return render_template("table.html", title="Skills", header=["Skill", "Characteristic", "Type", "Index"],
                           entries=entries)
