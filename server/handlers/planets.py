from decorators import get_item
from server.app import app
from server.db import db
from flask import render_template, abort


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


@app.route("/planet/<item>")
@get_item(db.planets)
def get_planet(item):
    return render_template("item.html", item=item)
