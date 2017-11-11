from server import custom_filters
from server.app import app
from server.db import db
from flask import Markup, render_template
from bson import ObjectId


@app.route("/attachments/")
def all_attachments():
    entries = []
    for attachment in db.attachments.find({}):
        attachment["name"] = Markup("<a href=\"./{0}\">{1}</a>".format(attachment["_id"], attachment["name"]))
        attachment["price"] = custom_filters.format_price_table(attachment["price"], attachment["restricted"])
        entries.append(attachment)

    return render_template("table.html", title="Attachments", header=["Attachment", "Price", "Encumbrance",
                                                                      "HP Required", "Rarity"],
                           fields=["name", "price", "encumbrance", "hardpoints", "rarity"], entries=entries, clazz="attachment")


@app.route("/attachments/<object_id>")
def attachment_item(object_id):
    attachment = db.attachments.find({"_id": ObjectId(object_id)})[0]

    return render_template("attachments.html", title=attachment["name"], item=attachment)
