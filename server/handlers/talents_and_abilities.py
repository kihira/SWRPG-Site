from server.app import app
from server.db import db
from server import custom_filters
from flask import Markup, render_template


@app.route("/talents/")
def all_talents():
    import pymongo

    entries = []
    for talent in db.talents.find({}).sort("_id", pymongo.ASCENDING):
        talent["name"] = Markup(
            "<a href=\"./{0}\">{1}</a>".format(talent["_id"], title(talent["_id"])))
        if not talent["activation"]:
            talent["activation"] = "Passive"
        elif type(talent["activation"]) == dict:
            talent["activation"] = "Active (" + to_list(talent["activation"]) + ")"
        else:
            talent["activation"] = "Active"
        entries.append(talent)

    return render_template("table.html", title="Talents", header=["Talent", "Activation", "Ranked", "Force Sensitive"],
                           fields=["name", "activation", "ranked", "force"], entries=entries)


@app.route("/abilities/")
def all_abilities():
    import pymongo

    entries = []
    for ability in db.abilities.find({}).sort("_id", pymongo.ASCENDING):
        ability["name"] = Markup(
            "<a href=\"./{0}\">{1}</a>".format(ability["_id"], title(ability["_id"])))
        ability["description"] = custom_filters.symbol(ability["description"])
        ability["description"] = custom_filters.skill_check(ability["description"])
        entries.append(ability)

    return render_template("table.html", title="Abilities", header=["Ability", "Description"],
                           fields=["name", "description"], entries=entries)


@app.route("/talents/<talent_id>")
def get_talent(talent_id):
    talent = db.talents.find({"_id": talent_id})[0]

    return render_template("item.html", title=talent["_id"].replace("_", " ").title(), item=talent)


@app.route("/abilities/<ability_id>")
def get_ability(ability_id):
    ability = db.abilities.find({"_id": ability_id})[0]

    return render_template("item.html", title=ability["_id"].replace("_", " ").title(), item=ability)


def to_list(dic):
    out = ""
    for key in dic:
        out += key.replace("_", " ").title() + ", "
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
