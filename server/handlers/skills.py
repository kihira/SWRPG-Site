from server.decorators import get_item
from server.app import app
from server.db import db
from flask import render_template


@app.route("/skills/")
def all_skills():
    # Groups all skills by category, then reverses it to present something like you would see in the books
    # todo this could probably be done better
    data = list(db["skills"].aggregate([{"$group": {"_id": "$category", "values": {"$push": "$$ROOT"}}}]))
    data.reverse()

    items = []
    for category in data:
        for skill in category["values"]:
            items.append(skill)

    return render_template("table.html", title="Skills", name_header="Skill",
                           columns=[{"header": "Characteristic", "name": "characteristic"}], entries=items)


@app.route("/skills/<item>")
@get_item(db.skills)
def get_skill(item):
    return render_template("item.html", item=item)
