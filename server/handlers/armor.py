from server import custom_filters
from server.app import app
from server.db import db
from flask import Markup, render_template
from bson import ObjectId


@app.route("/armor/")
def all_armor():
    entries = []
    for armor in db.armor.find({}):
        armor["name"] = Markup("<a href=\"./{0}\">{1}</a>".format(armor["_id"], armor["name"]))
        armor["price"] = custom_filters.format_price_table(armor["price"], armor["restricted"])
        entries.append(armor)

    return render_template("table.html", title="Armor",
                           header=["Type", "Defense", "Soak", "Price", "Encumbrance", "Hard Points", "Rarity"],
                           fields=["name", "defense", "soak", "price", "encumbrance", "hardpoints", "rarity"],
                           entries=entries, clazz="armor")


@app.route("/armor/<object_id>")
def armor_item(object_id):
    armor = db.armor.find({"_id": ObjectId(object_id)})[0]

    return render_template("armor.html", title=armor["name"], item=armor)
