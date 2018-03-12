from flask import render_template, request, url_for

from server.app import app
from server.db import db

from pymongo import ASCENDING


@app.route("/species/")
def all_species():
    return render_template("table.html", title="Species", name_header="Species",
                           headers=["Player"],
                           fields=["player"],
                           entries=list(db.species.find({}).sort("_id", ASCENDING)))


@app.route("/species/<species_id>")
def get_species(species_id):
    item = db.species.find({"_id": species_id})
    if len(item) != 1:
        return url_for("404")

    return render_template("item.html", title=item["_id"].replace("_", " "), item=item[0])


# todo auth
@app.route("/species/<species_id>/edit", methods=['GET', 'POST'])
def edit_species(species_id):
    if request.method == "POST":
        db.species.update_one({"_id": species_id}, {"$set": {
            "player": True if "player" in request.form and request.form["player"] else False,
            "wound": int(request.form["wound"]),
            "strain": int(request.form["strain"]),
            "xp": int(request.form["xp"]),
            "characteristics": {
                "brawn": int(request.form["brawn"]),
                "ability": int(request.form["agility"]),
                "intellect": int(request.form["intellect"]),
                "cunning": int(request.form["cunning"]),
                "willpower": int(request.form["willpower"]),
                "presence": int(request.form["presence"])
            }
        }})
    item = db.species.find({"_id": species_id})[0]
    return render_template("edit/species.html", title=item["_id"].replace("_", " "), item=item)
