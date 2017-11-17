from server.app import app
from server.db import db
from flask import Markup, render_template
import pymongo


def process_items(items):
    entries = []

    for item in items:
        item["name"] = Markup(f"<a href='./{item['_id']}'>{item['name']}</a>")

        skills = ""
        for talent in item["skills"]:
            if type(talent) == dict:
                skills += f"<a href='/skills/{talent['id']}'>{talent['id'].replace('_', ' ')}</a> {talent['value']}, "
            else:
                skills += f"<a href='/skills/{talent}'>{talent.replace('_', ' ')}</a>, "
        item["skills"] = skills[:-2]

        talents = ""
        for talent in item["talents"]:
            if type(talent) == dict:
                talents += f"<a href='/talents/{talent['id']}'>{talent['id'].replace('_', ' ')}</a> {talent['value']}, "
            else:
                talents += f"<a href='/talents/{talent}'>{talent.replace('_', ' ')}</a>, "
        item["talents"] = talents[:-2]

        abilities = ""
        for ability in item["abilities"]:
            abilities += f"<a href='/abilities/{ability}'>{ability.replace('_', ' ')}</a>, "
        item["abilities"] = abilities[:-2]

        entries.append(item)
    return entries


@app.route("/adversaries/")
def all_adversaries():
    return render_template("table.html", title="Adversaries",
                           header=["Name", "Type", "Skills", "Talents", "Abilities", "Equipment"],
                           fields=["name", "level", "skills", "talents", "abilities", "equipment"],
                           entries=process_items(db.adversaries.find({}).sort("name", pymongo.ASCENDING)))


@app.route("/adversaries/imperials")
def get_imperials():
    # todo this should probably use a tag system instead of regex search
    return render_template("table.html", title="Adversaries",
                           header=["Name", "Type", "Skills", "Talents", "Abilities", "Equipment"],
                           fields=["name", "level", "skills", "talents", "abilities", "equipment"],
                           entries=process_items(db.adversaries
                                                 .find({"$or": [{"name": {"$regex": "Imperial"}},
                                                                {"tags": "imperial"}]})
                                                 .sort("name", pymongo.ASCENDING)))


@app.route("/adversaries/<object_id>")
def get_adversary(object_id):
    from bson import ObjectId
    item = db.adversaries.find({"_id": ObjectId(object_id)})[0]
    if item["level"] == "Minion":
        item["skills"] = [f'<a href="/skills/{skill}">{skill.replace("_", " ")}</a>'
                          for skill in item["skills"]]
    else:
        item["skills"] = [f'<a href="/skills/{skill["id"]}">{skill["id"].replace("_", " ")}</a> {skill["value"]}'
                          for skill in item["skills"]]

    return render_template("adversary.html", title=item["name"], item=item)
