import re

from server.decorators import get_item
from server import filters
from server.app import app
from server.db import db
from flask import render_template


@app.route("/gear/")
def all_gear():
    items = list(db.gear.find({"category": {"$not": re.compile("Adversary")}}))
    for item in items:
        item["price"] = filters.format_price_table(item["price"], item["restricted"])

    return render_template("table.html", title="Items", name_header="Item",
                           headers=["Price", "Encumbrance", "Rarity"],
                           fields=["price", "encumbrance", "rarity"],
                           entries=items)


@app.route("/gear/<item>")
@get_item(db.gear, True)
def get_gear(item):
    return render_template("item.html", title=item["name"], item=item)
