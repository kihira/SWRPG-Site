from decorators import get_item
from model import Model, Field, CheckboxField, TextareaField, SelectField
from server.app import app
from server.db import db
from server import filters
from flask import render_template, request, abort

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
    items = list(db.talents.find({}).sort("_id", 1))
    for item in items:
        item["activation"] = activation(item["activation"])
        if "short" in item:
            item["short"] = filters.description(item["short"])

    return render_template("table.html", title="Talents", name_header="Talent", categories=False,
                           headers=["Description", "Activation", "Ranked", "Force Sensitive"],
                           fields=["short", "activation", "ranked", "force"],
                           entries=items)


@app.route("/talents/<item>")
@get_item(db.talents)
def get_talent(item):
    item["activation"] = activation(item["activation"])

    # todo is there a better way to do this? seems messy
    item["trees"] = [s["_id"].replace("_", " ") for s in db.specializations.find(
        {"tree.talents": {"$elemMatch": {"$elemMatch": {"$in": [item]}}}}, {"_id": 1})]

    return render_template("talent.html", title=item["_id"].replace("_", " "), item=item)


# todo auth
@app.route("/talents/<item>/edit", methods=['GET', 'POST'])
@get_item(db.talents)
def edit_talent(item):
    if request.method == "POST":
        db.talents.update_one({"_id": item["_id"]}, {"$set": {
            "ranked": request.form.get("ranked", False),
            "short": request.form["short"].replace("\r\n", " ").replace("\n", " "),
            "description": request.form["description"].replace("\r\n", " ").replace("\n", " ")
        }})

    item["activation"] = activation(item["activation"])
    return render_template("edit/add-item.html", title=item["_id"].replace("_", " "), item=item)


@app.route("/talents/add", methods=['GET', 'POST'])
def add_talent():
    if request.method == "POST":
        # db.talents.insert_one({})
        print(model.from_form(request.form))
    return render_template("edit/add-item.html", model=model)

    # return render_template("edit/add-item.html", title=item["_id"].replace("_", " "), item=item)


@app.route("/abilities/")
def all_abilities():
    items = list(db.abilities.find({}).sort("_id", 1))
    for item in items:
        item["description"] = filters.description(item["description"])

    return render_template("table.html", title="Abilities", name_header="Ability", categories=False,
                           headers=["Description"],
                           fields=["description"], entries=items)


@app.route("/abilities/<item>")
@get_item(db.abilities)
def get_ability(item):
    return render_template("item.html", title=item["_id"].replace("_", " "), item=item)


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
