from server.decorators import get_item, login_required
from server.model import Model, Field, CheckboxField, TextareaField, SelectField
from server.app import app
from server.db import db
from server import filters
from flask import render_template, request, flash

model = Model([
    Field("_id", "ID"),
    CheckboxField("ranked", "Ranked"),
    TextareaField("short", "Short Description"),
    TextareaField("description", "Long Description"),
    SelectField("activation", "Activation", options=[
        {"display": "Passive", "value": "passive"},
        {"display": "Active (Action)", "value": "active_action"},  # todo this isn't compat with current model
        {"display": "Active (Incidental)", "value": "active_incidental"},
        {"display": "Active (Maneuver)", "value": "active_maneuver"},
        {"display": "Active (Out Of Turn)", "value": "active_oot"},
    ])
])


@app.route("/talents/")
def all_talents():
    items = list(db["talents"].find({}).sort("_id", 1))
    for item in items:
        item["activation"] = activation(item["activation"])
        if "short" in item:
            item["short"] = filters.description(item["short"])

    columns = [
        {"header": "Description", "field": "description"},
        {"header": "Activation", "field": "activation", "filter": {"type": "select"}},
        {"header": "Ranked", "field": "ranked"},
        {"header": "Force Sensitive", "field": "force"}
    ]

    return render_template("table.html", title="Talents", name_header="Talent", categories=False, columns=columns,
                           entries=items)


@app.route("/talents/<item>")
@get_item(db.talents)
def get_talent(item):
    item["activation"] = activation(item["activation"])

    # todo is there a better way to do this? seems messy
    item["trees"] = [s["_id"].replace("_", " ") for s in db.specializations.find(
        {"tree.talents": {"$elemMatch": {"$elemMatch": {"$in": [item]}}}}, {"_id": 1})]

    return render_template("talent.html", title=item["_id"].replace("_", " "), item=item)


@app.route("/talents/add", methods=['GET', 'POST'])
@login_required
def add_talent():
    if request.method == "POST":
        item = model.from_form(request.form)
        item["_id"] = db["talents"].insert_one(item)
        flash(f'Successfully added item. <a href="{item["_id"]}">View</a><a href="{item["_id"]}/edit">Edit</a>')
    return render_template("edit/add-edit.html", model=model)


@app.route("/talents/<item>/edit", methods=['GET', 'POST'])
@login_required
@get_item(db.talents)
def edit_talent(item):
    if request.method == "POST":
        item = model.from_form(request.form)
        db["talents"].update_one({"_id": item["_id"]}, {"$set": item})
        flash(f'Successfully updated item.')
    item["activation"] = activation(item["activation"])
    return render_template("edit/add-edit.html", item=item, model=model)


@app.route("/abilities/")
def all_abilities():
    items = list(db["abilities"].find({}).sort("_id", 1))
    for item in items:
        item["description"] = filters.description(item["description"])

    return render_template("table.html", title="Abilities", name_header="Ability", categories=False,
                           headers=["Description"],
                           fields=["description"], entries=items)


@app.route("/abilities/<item>")
@get_item(db.abilities)
def get_ability(item):
    return render_template("item.html", item=item)


def activation(value):
    if not value:
        return "Passive"
    elif type(value) == dict:
        return "Active (" + to_list(value) + ")"
    else:
        return "Active"


def to_list(dic):
    out = ""
    for key in dic:
        out += key.replace("_", " ") + ", "
    return out[:-2]
