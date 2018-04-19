from flask import Markup, render_template

from server.decorators import get_item
from server import filters
from server.app import app
from server.db import db


@app.route("/weapons/")
def all_weapons():
    items = list(db["weapons"].find({}))
    for item in items:
        item["special"] = filters.format_list(item["special"], "qualities")
        item["skill"] = Markup(f'<a href="/skills/{item["skill"]}">{item["skill"].replace("_", " ")}</a>')

    columns = [
        {"header": "Skill", "field": "skill"},
        {"header": "Dam", "field": "damage", "filter": {"type": "number"}},
        {"header": "Crit", "field": "critical", "filter": {"type": "number"}},
        {"header": "Range", "field": "range", "filter": {"type": "select"}},
        {"header": "HP", "field": "hardpoints", "filter": {"type": "number"}},
        {"header": "Price", "field": "price", "filter": {"type": "number"}},
        {"header": "Restricted", "field": "restricted", "filter": {"type": "checkbox"}, "hidden": True},
        {"header": "Rarity", "field": "rarity", "filter": {"type": "number"}},
        {"header": "Special", "field": "special", "filter": {"type": "select"}},
    ]

    return render_template("table.html", title="Weapons", columns=columns, entries=items)


@app.route("/weapons/<item>")
@get_item(db.weapons, True)
def get_weapon(item):
    item["skill"] = Markup(f"<a href=\"/skills/{item['skill']}\">{item['skill'].replace('_', ' ')}</a>")

    return render_template("weapon.html", item=item)
