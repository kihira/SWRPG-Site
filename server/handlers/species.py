from flask import render_template, request

from decorators import get_item
from model import Model, Field, CheckboxField, FieldGroup, NumberField
from server.app import app
from server.db import db

from pymongo import ASCENDING


model = Model([
    Field("_id", "Name"),
    CheckboxField("player", "Player"),
    FieldGroup("characteristics", "Characteristics", [
        NumberField("brawn", "Brawn", 1, 5, default=1),
        NumberField("agility", "Agility", 1, 5, default=1),
        NumberField("intellect", "Intellect", 1, 5, default=1),
        NumberField("cunning", "Cunning", 1, 5, default=1),
        NumberField("willpower", "Willpower", 1, 5, default=1),
        NumberField("presence", "Presence", 1, 5, default=1),
    ]),
    NumberField("wound", "Wound Threshold"),
    NumberField("strain", "Strain Threshold"),
    NumberField("xp", "Starting XP", required=False)
])


@app.route("/species/")
def all_species():
    return render_template("table.html", title="Species", name_header="Species",
                           headers=["Player"],
                           fields=["player"],
                           entries=list(db.species.find({}).sort("_id", ASCENDING)))


@app.route("/species/<item>")
@get_item(db.species)
def get_species(item):
    return render_template("item.html", title=item["_id"].replace("_", " "), item=item)


# todo auth
@app.route("/species/add", methods=['GET', 'POST'])
def add_species():
    if request.method == "POST":
        item = model.from_form(request.form)
        item["_id"] = db["species"].insert_one(item).inserted_id
        return render_template("edit/add-item.html", item=item, model=model)
    return render_template("edit/add-item.html", model=model)


# todo auth
@app.route("/species/<item>/edit", methods=['GET', 'POST'])
@get_item(db.species)
def edit_species(item):
    if request.method == "POST":
        new_item = model.from_form(request.form)
        db["species"].update_one({"_id": item["_id"]}, {"$set": new_item})
        return render_template("edit/add-item.html", item=new_item, model=model, updated=True)

    return render_template("edit/add-item.html", item=item, model=model)

