import re

from server.decorators import get_item
from server.app import app
from server.db import db
from flask import render_template


@app.route("/gear/")
def all_gear():
    items = list(db["gear"].find({"category": {"$not": re.compile("Adversary")}}))

    columns = [
        {"header": "Price", "field": "price", "filter": {"type": "number"}},
        {"header": "Restricted", "field": "restricted", "filter": {"type": "checkbox"}, "hidden": True},
        {"header": "Encumbrance", "field": "encumbrance", "filter": {"type": "number"}},
        {"header": "Rarity", "field": "rarity", "filter": {"type": "number"}}
    ]

    return render_template("table.html", title="Items", name_header="Item", columns=columns, entries=items)


@app.route("/gear/<item>")
@get_item(db.gear, True)
def get_gear(item):
    return render_template("item.html", item=item)
