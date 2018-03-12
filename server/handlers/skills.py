from server.app import app
from server.db import db
from flask import render_template, abort


@app.route("/skills/")
def all_skills():
    # Groups all skills by category, then reverses it to present something like you would see in the books
    # todo this could probably be done better
    data = list(db.skills.aggregate([{"$group": {"_id": "$category", "values": {"$push": "$$ROOT"}}}]))
    data.reverse()

    items = []
    for category in data:
        for skill in category["values"]:
            items.append(skill)

    return render_template("table.html", title="Skills", name_header="Skill",
                           headers=["Characteristic"],
                           fields=["characteristic"], entries=items)


@app.route("/skills/<skill_id>")
def get_skill(skill_id):
    item = db.skills.find({"_id": skill_id})
    if item.count() != 1:
        return abort(404)
    item = item[0]

    return render_template("item.html", title=item["_id"].replace("_", " "), item=item)
