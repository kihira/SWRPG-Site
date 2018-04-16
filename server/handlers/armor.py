from model import Model, Field, NumberField, CheckboxField, TextareaField, ObjectIdField
from server.decorators import get_item, login_required
from server import filters
from server.app import app
from server.db import db
from flask import render_template, request, flash

model = Model([
    ObjectIdField("_id", "ID", readonly=True),
    Field("name", "Name"),
    NumberField("defense", "Defense", max=5),
    NumberField("soak", "Soak"),
    NumberField("hardpoints", "Hardpoints"),
    NumberField("encumbrance", "encumbrance"),
    NumberField("price", "Price", max=100000),
    CheckboxField("restricted", "Restricted"),
    NumberField("rarity", "Rarity", max=10),
    TextareaField("description", "Description")
])


@app.route("/armour/")
@app.route("/armor/")
def all_armor():
    items = list(db.armor.find({}))
    for item in items:
        pass
        # item["price"] = filters.format_price_table(item["price"], item["restricted"])

    columns = [
        {"header": "Defense", "field": "defense", "filter": {"type": "number"}},
        {"header": "Soak", "field": "soak", "filter": {"type": "number"}},
        {"header": "Price", "field": "price", "filter": {"type": "number"}},
        {"header": "Restricted", "field": "restricted", "filter": {"type": "checkbox"}, "hidden": True},
        {"header": "Encumbrance", "field": "encumbrance", "filter": {"type": "number"}},
        {"header": "Hard Points", "field": "hardpoints", "filter": {"type": "number"}},
        {"header": "Rarity", "field": "rarity", "filter": {"type": "number"}}
    ]

    return render_template("table.html", title="Armor", name_header="Type", categories=False,
                           columns=columns, entries=items)


@app.route("/armour/<item>")
@app.route("/armor/<item>")
@get_item(db.armor, True)
def get_armor(item):
    return render_template("armor.html", item=item)


@app.route("/armour/add", methods=['GET', 'POST'])
@app.route("/armor/add", methods=['GET', 'POST'])
@login_required
def add_armor():
    if request.method == "POST":
        item = model.from_form(request.form)
        item["_id"] = db["armor"].insert_one(item).inserted_id
        flash(f'Successfully added item. <a href="{item["_id"]}">View</a><a href="{item["_id"]}/edit">Edit</a>')
    return render_template("edit/add-edit.html", model=model)


@app.route("/armour/<item>/edit", methods=['GET', 'POST'])
@app.route("/armor/<item>/edit", methods=['GET', 'POST'])
@login_required
@get_item(db.armor, True)
def edit_armor(item):
    if request.method == "POST":
        item = model.from_form(request.form)
        db["armor"].update_one({"_id": item["_id"]}, {"$set": item})
        flash(f'Successfully updated item.')
    return render_template("edit/add-edit.html", item=item, model=model)
