from decorators import validate_objectid
from server.app import app
from server.db import db
from flask import render_template, abort


@app.route("/specialisations/")
@app.route("/specializations/")
def all_specializations():
    return render_template("table.html", title="Specializations", headers=["Career"], fields=["career"],
                           entries=db.specializations.find({}).sort("_id", 1))


@app.route("/specialisations/<object_id>")
@app.route("/specializations/<object_id>")
@validate_objectid
def get_specializations(object_id):
    item = db.specializations.find({"_id": object_id})
    if item.count() != 1:
        return abort(404)
    item = item[0]

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
