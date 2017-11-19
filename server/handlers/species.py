from server.app import app
from server.db import db
from flask import render_template


@app.route("/species/")
def all_species():
    items = list(db.species.find({}).sort("_id", 1))

    return render_template("table.html", title="Species", name_header="Species",
                           headers=["Player"],
                           fields=["player"], entries=items)


@app.route("/species/<species_id>")
def get_species(species_id):
    item = db.species.find({"_id": species_id})[0]

    return render_template("item.html", title=item["_id"].replace("_", " "), item=item)
