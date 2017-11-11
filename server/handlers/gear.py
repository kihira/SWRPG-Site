from server import custom_filters
from server.app import app
from server.db import db
from flask import Markup, render_template
from bson import ObjectId


@app.route("/gear/")
def all_gear():
    entries = []
    for gear in db.gear.find({}):
        gear["name"] = Markup("<a href=\"./{0}\">{1}</a>".format(gear["_id"], gear["name"]))
        gear["price"] = custom_filters.format_price_table(gear["price"], gear["restricted"])
        entries.append(gear)

    return render_template("table.html", title="Items", header=["Item", "Price", "Encumbrance", "Rarity"],
                           fields=["name", "price", "encumbrance", "rarity"], entries=entries)


@app.route("/gear/<object_id>")
def gear_item(object_id):
    gear = db.gear.find({"_id": ObjectId(object_id)})[0]

    return render_template("item.html", title=gear["name"], item=gear)
