from server.app import app
from server.db import db
from flask import render_template, url_for


@app.route("/planets/")
def all_planets():
    items = list(db.planets.find({}))

    for item in items:
        item["languages"] = ", ".join(item["languages"])
        item["imports"] = ", ".join(item["imports"])
        item["exports"] = ", ".join(item["exports"])
        item["routes"] = ", ".join(item["routes"])

    return render_template("table.html", title="Planets", name_header="Planet",
                           headers=["Government", "Languages", "Imports", "Exports", "Routes"],
                           fields=["government", "languages", "imports", "exports", "routes"], entries=items)


@app.route("/planet/<planet_id>")
def get_planet(planet_id):
    item = db.planets.find({"_id": planet_id})
    if len(item) != 1:
        return url_for("404")

    return render_template("item.html", title=item["_id"].replace("_", " "), item=item[0])
