from server.app import app
from server.db import db
from server import filters
from flask import Markup, render_template
import pymongo


def process_items(items):
    entries = []

    for item in items:
        item["name"] = Markup(f"<a href='./{item['_id']}'>{item['name']}</a>")
        item["skills"] = filters.format_list(item["skills"], "skills")
        item["talents"] = filters.format_list(item["talents"], "talents")
        item["abilities"] = filters.format_list(item["abilities"], "abilities")

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

    return render_template("adversary.html", title=item["name"], item=item)
