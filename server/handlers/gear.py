from server import filters
from server.app import app
from server.db import db
from flask import render_template
from bson import ObjectId


@app.route("/gear/")
def all_gear():
    items = list(db.gear.find({}))
    for item in items:
        item["price"] = filters.format_price_table(item["price"], item["restricted"])

    return render_template("table.html", title="Items", name_header="Item",
                           headers=["Price", "Encumbrance", "Rarity"],
                           fields=["price", "encumbrance", "rarity"], entries=items)


@app.route("/gear/<object_id>")
def get_gear(object_id):
    item = db.gear.find({"_id": ObjectId(object_id)})[0]

    return render_template("item.html", title=item["name"], item=item)
