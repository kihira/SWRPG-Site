from server.app import app
from server.db import db
from server import filters
from flask import render_template, request


@app.route("/talents/")
def all_talents():
    import pymongo

    entries = []
    for item in db.talents.find({}).sort("_id", pymongo.ASCENDING):
        item["name"] = f'<a href="./{item["_id"]}">{item["_id"].replace("_", " ")}</a>'
        item["activation"] = activation(item["activation"])
        if "short" in item:
            item["short"] = filters.description(item["short"])
        entries.append(item)

    return render_template("table.html", title="Talents",
                           header=["Talent", "Description", "Activation", "Ranked", "Force Sensitive"],
                           fields=["name", "short", "activation", "ranked", "force"], entries=entries)


@app.route("/talents/<talent_id>")
def get_talent(talent_id):
    item = db.talents.find({"_id": talent_id})[0]
    item["activation"] = activation(item["activation"])

    # todo is there a better way to do this? seems messy
    item["trees"] = [s["_id"].replace("_", " ") for s in db.specializations.find(
        {"tree.talents": {"$elemMatch": {"$elemMatch": {"$in": [talent_id]}}}}, {"_id": 1})]

    return render_template("talent.html", title=item["_id"].replace("_", " "), item=item)


# todo auth
@app.route("/talents/<talent_id>/edit", methods=['GET', 'POST'])
def edit_talent(talent_id):
    if request.method == "POST":
        print(request.form)
        db.talents.update_one({"_id": talent_id}, {"$set": {
            "ranked": True if "ranked" in request.form and request.form["ranked"] else False,
            "short": request.form["short"].replace("\r\n", " ").replace("\n", " "),
            "description": request.form["description"].replace("\r\n", " ").replace("\n", " ")
        }})
    item = db.talents.find({"_id": talent_id})[0]
    item["activation"] = activation(item["activation"])

    return render_template("edit/talent.html", title=item["_id"].replace("_", " "), item=item)


@app.route("/abilities/")
def all_abilities():
    import pymongo

    entries = []
    for item in db.abilities.find({}).sort("_id", pymongo.ASCENDING):
        item["name"] = f"<a href='./{item['_id']}'>{item['_id'].replace('_', ' ')}</a>"
        item["description"] = filters.description(item["description"])
        entries.append(item)

    return render_template("table.html", title="Abilities", header=["Ability", "Description"],
                           fields=["name", "description"], entries=entries)


@app.route("/abilities/<ability_id>")
def get_ability(ability_id):
    ability = db.abilities.find({"_id": ability_id})[0]
    ability["description"] = filters.description(ability["description"])

    return render_template("item.html", title=ability["_id"].replace("_", " "), item=ability)


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
