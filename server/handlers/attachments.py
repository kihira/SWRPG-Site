from decorators import validate_objectid
from server import filters
from server.app import app
from server.db import db
from flask import render_template, url_for
from bson import ObjectId


@app.route("/attachments/")
def all_attachments():
    items = list(db.attachments.find({}))
    for item in items:
        item["price"] = filters.format_price_table(item["price"], item["restricted"])

    return render_template("table.html", title="Attachments", name_header="Attachment",
                           headers=["Price", "Encumbrance", "HP Required", "Rarity"],
                           fields=["price", "encumbrance", "hardpoints", "rarity"], entries=items)


@app.route("/attachments/<object_id>")
@validate_objectid
def get_attachment(object_id):
    item = db.attachments.find({"_id": ObjectId(object_id)})
    if len(item) != 1:
        return url_for("404")

    return render_template("attachments.html", title=item["name"], item=item[0])
