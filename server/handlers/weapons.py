from flask import Markup, render_template

from server.decorators import get_item
from server import filters
from server.app import app
from server.db import db


@app.route("/weapons/")
def all_weapons():
    items = list(db.weapons.find({}))
    for item in items:
        item["price"] = filters.format_price_table(item["price"], item["restricted"])
        item["special"] = filters.format_list(item["special"], "qualities")
        item["skill"] = Markup(f'<a href="/skills/{item["skill"]}">{item["skill"].replace("_", " ")}</a>')

    return render_template("table.html", title="Weapons",
                           headers=["Skill", "Dam", "Crit", "Range", "Encum", "HP", "Price", "Rarity", "Special"],
                           fields=["skill", "damage", "critical", "range", "encumbrance", "hardpoints", "price", "rarity", "special"],
                           entries=items)


@app.route("/weapons/<item>")
@get_item(db.weapons, True)
def get_weapon(item):
    item["skill"] = Markup("<a href=\"/skills/{0}\">{1}</a>".format(item["skill"], item["skill"].replace("_", " ")))

    return render_template("weapon.html", item=item)
