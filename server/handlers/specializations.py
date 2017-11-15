from server.app import app
from server.db import db
from flask import Markup, render_template


@app.route("/specialisations/")
@app.route("/specializations/")
def all_specializations():
    import pymongo

    entries = []
    for item in db.species.find({}).sort("_id", pymongo.ASCENDING):
        item["name"] = Markup(
            "<a href=\"./{0}\">{1}</a>".format(item["_id"], item["_id"]).replace("_", " "))
        entries.append(item)

    return render_template("table.html", title="Specializations", header=["Specializations", "Career"],
                           fields=["name", "career"], entries=entries)


@app.route("/specialisations/<species_id>")
@app.route("/specializations/<species_id>")
def get_specializations(species_id):
    item = db.specializations.find({"_id": species_id})[0]
    talents = {}
    for talent in db.talents.find({"_id": {"$in": [entry for row in item["tree"]["talents"] for entry in row]}}):
        talents[talent["_id"]] = talent

    for row in item["tree"]["talents"]:
        for index in range(len(row)):
            row[index] = talents[row[index]]
            row[index]["name"] = row[index]["_id"]
            if "short" in talent:
                row[index]["description"] = talent["short"]
            elif "description" in talent:
                row[index]["description"] = talent["description"]

    return render_template("specialization.html", title=item["_id"].replace("_", " "), item=item)
