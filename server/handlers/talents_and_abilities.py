from server.app import app
from server.db import db
from server import filters
from flask import render_template


@app.route("/talents/")
def all_talents():
    import pymongo

    entries = []
    for item in db.talents.find({}).sort("_id", pymongo.ASCENDING):
        item["name"] = f"<a href='./{item['_id']}'>{title(item['_id'])}</a>"
        item["activation"] = activation(item["activation"])
        entries.append(item)

    return render_template("table.html", title="Talents", header=["Talent", "Activation", "Ranked", "Force Sensitive"],
                           fields=["name", "activation", "ranked", "force"], entries=entries)


@app.route("/abilities/")
def all_abilities():
    import pymongo

    entries = []
    for item in db.abilities.find({}).sort("_id", pymongo.ASCENDING):
        item["name"] = f"<a href='./{item['_id']}'>{title(item['_id'])}</a>"
        item["description"] = filters.description(item["description"])
        entries.append(item)

    return render_template("table.html", title="Abilities", header=["Ability", "Description"],
                           fields=["name", "description"], entries=entries)


@app.route("/talents/<talent_id>")
def get_talent(talent_id):
    item = db.talents.find({"_id": talent_id})[0]
    item["activation"] = activation(item["activation"])

    # todo is there a better way to do this? seems messy
    item["trees"] = [s["_id"].replace("_", " ") for s in db.specializations.find(
        {"tree.talents": {"$elemMatch": {"$elemMatch": {"$in": [talent_id]}}}}, {"_id": 1})]

    return render_template("talent.html", title=item["_id"].replace("_", " "), item=item)


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


# todo not keen on having to do this kind of stuff, change the _id to also be capitalised?
def title(string):
    result = []
    prev_letter = ' '

    for ch in string:
        if ch == "_":
            result.append(" ")
        elif not prev_letter.isalpha() and prev_letter != '\'':
            result.append(ch.upper())
        else:
            result.append(ch.lower())

        prev_letter = ch

    return "".join(result)
