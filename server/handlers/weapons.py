from server import filters
from server.app import app
from server.db import db
from flask import Markup, render_template
from bson import ObjectId


@app.route("/weapons/")
def all_weapons():
    entries = []
    for weapon in db.weapons.find({}):
        weapon["name"] = Markup("<a href=\"./{0}\">{1}</a>".format(weapon["_id"], weapon["name"]))
        weapon["price"] = filters.format_price_table(weapon["price"], weapon["restricted"])
        weapon["special"] = filters.format_list(weapon["special"], "qualities")
        weapon["skill"] = Markup("<a href=\"/skills/{0}\">{1}</a>".format(weapon["skill"],
                                                                          weapon["skill"].replace("_", " ")))
        entries.append(weapon)

    return render_template("table.html", title="Weapons",
                           header=["Name", "Skill", "Dam", "Crit", "Range", "Encum", "HP", "Price", "Rarity", "Special"],
                           fields=["name", "skill", "damage", "critical", "range", "encumbrance", "hardpoints", "price", "rarity", "special"], entries=entries)


@app.route("/weapons/<object_id>")
def get_weapon(object_id):
    weapon = db.weapons.find({"_id": ObjectId(object_id)})[0]
    weapon["skill"] = Markup("<a href=\"/skills/{0}\">{1}</a>".format(weapon["skill"],
                                                                      weapon["skill"].replace("_", " ")))

    return render_template("weapon.html", title=weapon["name"], item=weapon)
