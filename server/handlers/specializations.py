from server.decorators import get_item
from server.app import app
from server.db import db
from flask import render_template


@app.route("/specialisations/")
@app.route("/specializations/")
def all_specializations():
    return render_template("table.html", title="Specializations", headers=["Career"], fields=["career"],
                           entries=db.specializations.find({}).sort("_id", 1))


@app.route("/specialisations/<item>")
@app.route("/specializations/<item>")
@get_item(db.specializations)
def get_specializations(item):
    talents = {}
    for talent in db.talents.find({"_id": {"$in": [entry for row in item["tree"]["talents"] for entry in row]}}):
        talents[talent["_id"]] = talent

    for row in item["tree"]["talents"]:
        for index in range(len(row)):
            talent = talents[row[index]]
            row[index] = talent
            row[index]["name"] = row[index]["_id"]
            if "short" in talent:
                row[index]["description"] = talent["short"]
            elif "description" in talent:
                row[index]["description"] = talent["description"]

    return render_template("specialization.html", title=item["_id"].replace("_", " "), item=item)
