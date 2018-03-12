from decorators import validate_objectid
from server import filters
from server.app import app
from server.db import db
from flask import render_template, url_for
from bson import ObjectId


@app.route("/armour/")
@app.route("/armor/")
def all_armor():
    items = list(db.armor.find({}))
    for item in items:
        item["price"] = filters.format_price_table(item["price"], item["restricted"])

    return render_template("table.html", title="Armor", name_header="Type", categories=False,
                           headers=["Defense", "Soak", "Price", "Encumbrance", "Hard Points", "Rarity"],
                           fields=["defense", "soak", "price", "encumbrance", "hardpoints", "rarity"],
                           entries=items)


@app.route("/armour/<object_id>")
@app.route("/armor/<object_id>")
@validate_objectid
def armor_item(object_id: str):
    item = db.armor.find({"_id": ObjectId(object_id)})
    if item.count() != 1:
        return url_for("404")
    item = item[0]

    return render_template("armor.html", title=item["name"], item=item)
