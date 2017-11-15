from server.app import app
from server.db import db
from flask import Markup, render_template


@app.route("/species/")
def all_species():
    import pymongo

    entries = []
    for species in db.species.find({}).sort("_id", pymongo.ASCENDING):
        species["name"] = Markup(
            "<a href=\"./{0}\">{1}</a>".format(species["_id"], species["_id"]).replace("_", " "))
        entries.append(species)

    return render_template("table.html", title="Species", header=["Species", "Player"],
                           fields=["name", "player"], entries=entries)


@app.route("/species/<species_id>")
def get_species(species_id):
    species = db.species.find({"_id": species_id})[0]

    return render_template("item.html", title=species["_id"].replace("_", " "), item=species)