from server.app import app
from server.db import db
from flask import Markup, render_template


@app.route("/skills/")
def all_skills():
    # Groups all skills by category, then reverses it to present something like you would see in the books
    data = list(db.skills.aggregate([{"$group": {"_id": "$category", "values": {"$push": "$$ROOT"}}}]))
    data.reverse()

    entries = []
    for category in data:
        for skill in category["values"]:
            skill["name"] = Markup("<a href=\"./{0}\">{1}</a>".format(skill["_id"], skill["_id"].replace("_", " ").title()))
            entries.append(skill)

    return render_template("table.html", title="Skills", header=["Skill", "Characteristic"],
                           fields=["name", "characteristic"], entries=entries)


@app.route("/skills/<skill_id>")
def get_skill(skill_id):
    skill = db.skills.find({"_id": skill_id})[0]

    return render_template("item.html", title=skill["_id"].replace("_", " ").title(), item=skill)