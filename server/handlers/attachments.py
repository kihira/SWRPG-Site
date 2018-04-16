from server.decorators import get_item
from server.app import app
from server.db import db
from flask import render_template


@app.route("/attachments/")
def all_attachments():
    items = list(db["attachments"].find({}))

    columns = [
        {"header": "Price", "field": "price", "filter": {"type": "number"}},
        {"header": "Restricted", "field": "restricted", "filter": {"type": "checkbox"}, "hidden": True},
        {"header": "Encumbrance", "field": "encumbrance", "filter": {"type": "number"}},
        {"header": "HP Required", "field": "hardpoints", "filter": {"type": "number"}},
        {"header": "Rarity", "field": "rarity", "filter": {"type": "number"}}
    ]

    return render_template("table.html", title="Attachments", name_header="Attachment", columns=columns, entries=items)


@app.route("/attachments/<item>")
@get_item(db.attachments, True)
def get_attachment(item):
    return render_template("attachments.html", item=item)
