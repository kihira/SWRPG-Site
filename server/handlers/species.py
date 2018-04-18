from flask import render_template, request, redirect, flash

from server.decorators import get_item, login_required
from server.model import Model, Field, CheckboxField, FieldGroup, NumberField
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
    return render_template("table.html", title="Species", name_header="Species", categories=False,
                           columns=[{"header": "Player", "field": "player"}],
                           entries=list(db["species"].find({}).sort("_id", ASCENDING)))


@app.route("/species/<item>")
@get_item(db.species)
def get_species(item):
    return render_template("item.html", item=item)


@app.route("/species/add", methods=['GET', 'POST'])
@login_required
def add_species():
    if request.method == "POST":
        item = model.from_form(request.form)
        item["_id"] = db["species"].insert_one(item).inserted_id
        flash(f'Successfully added item. <a href="{item["_id"]}">View</a><a href="{item["_id"]}/edit">Edit</a>')
    return render_template("edit/add-edit.html", model=model)


# todo auth
@app.route("/species/<item>/edit", methods=['GET', 'POST'])
@login_required
@get_item(db.species)
def edit_species(item):
    if request.method == "POST":
        item = model.from_form(request.form)
        db["species"].update_one({"_id": item["_id"]}, {"$set": item})
        flash(f'Successfully updated item.')
    return render_template("edit/add-edit.html", item=item, model=model)

