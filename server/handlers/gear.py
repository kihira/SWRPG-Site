import re

from server.decorators import get_item, login_required
from server.app import app
from server.db import db
from flask import render_template, request, flash

from server.model import Model, Field, CheckboxField, TextareaField, SelectField, ArrayField, NumberField

model = Model([
    Field("_id", "ID", readonly=True),
    Field("name", "Name"),
    NumberField("encumbrance", "Encumbrance"),
    NumberField("price", "Price"),
    NumberField("rarity", "Rarity"),
    CheckboxField("restricted", "Restricted"),
    TextareaField("description", "Long Description"),
    SelectField("category", "Category", options=[
        "Adversary",
        "Ancient Talismans",
        "Communications",
        "Consumables",
        "Cybernetics",
        "Detection Devices",
        "Droids",
        "Drugs",
        "Field Equipment",
        "Illegal Equipment",
        "Medical",
        "Poison",
        "Recreational",
        "Scanning and Surveillance",
        "Security",
        "Storage",
        "Survival",
        "Tools",
        "Uniforms"
    ]),
    ArrayField(Field("index", "Index"))
])


@app.route("/gear/")
def all_gear():
    items = list(db["gear"].find({"category": {"$not": re.compile("Adversary")}}))

    columns = [
        {"header": "Price", "name": "price", "filter": {"type": "number"}},
        {"header": "Restricted", "name": "restricted", "filter": {"type": "checkbox"}, "hidden": True},
        {"header": "Encumbrance", "name": "encumbrance", "filter": {"type": "number"}},
        {"header": "Rarity", "name": "rarity", "filter": {"type": "number"}}
    ]

    return render_template("table.html", title="Items", name_header="Item", columns=columns, entries=items)


@app.route("/gear/<item>")
@get_item(db.gear, True)
def get_gear(item):
    return render_template("item.html", item=item)


@app.route("/gear/add", methods=['GET', 'POST'])
@login_required
def add_gear():
    if request.method == "POST":
        item = model.from_form(request.form)
        db["gear"].insert_one(item)
        flash(f'Successfully added item. <a href="{item["_id"]}">View</a><a href="{item["_id"]}/edit">Edit</a>')
    return render_template("edit/add-edit.html", model=model)


@app.route("/gear/<item>/edit", methods=['GET', 'POST'])
@login_required
@get_item(db.gear, True)
def edit_gear(item):
    if request.method == "POST":
        item = model.from_form(request.form)
        db["gear"].update_one({"_id": item["_id"]}, {"$set": item})
        flash(f'Successfully updated item.')
    return render_template("edit/add-edit.html", item=item, model=model)