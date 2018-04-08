from pymongo.results import InsertOneResult, UpdateResult

from model import Model, Field, NumberField, CheckboxField, TextareaField, ObjectIdField
from server.decorators import get_item
from server import filters
from server.app import app
from server.db import db
from flask import render_template, request

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
        item["price"] = filters.format_price_table(item["price"], item["restricted"])

    return render_template("table.html", title="Armor", name_header="Type", categories=False,
                           headers=["Defense", "Soak", "Price", "Encumbrance", "Hard Points", "Rarity"],
                           fields=["defense", "soak", "price", "encumbrance", "hardpoints", "rarity"],
                           entries=items)


@app.route("/armour/<item>")
@app.route("/armor/<item>")
@get_item(db.armor, True)
def get_armor(item):
    return render_template("armor.html", item=item)


@app.route("/armour/add", methods=['GET', 'POST'])
@app.route("/armor/add", methods=['GET', 'POST'])
def add_armor():
    if request.method == "POST":
        item = model.from_form(request.form)
        item["_id"] = db["armor"].insert_one(item).inserted_id
        return render_template("edit/add-item.html", item=item, model=model, added=True)
    return render_template("edit/add-item.html", model=model)


@app.route("/armour/<item>/edit", methods=['GET', 'POST'])
@app.route("/armor/<item>/edit", methods=['GET', 'POST'])
@get_item(db.armor, True)
def edit_armor(item):
    if request.method == "POST":
        new_item = model.from_form(request.form)
        result: UpdateResult = db["armor"].update_one({"_id": item["_id"]}, {"$set": new_item})
        return render_template("edit/add-item.html", item=new_item, model=model, updated=(result.modified_count == 1))

    return render_template("edit/add-item.html", item=item, model=model)
