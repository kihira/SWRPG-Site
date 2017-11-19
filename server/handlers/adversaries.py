from server.app import app
from server.db import db
from server import filters
from flask import render_template
import pymongo


def process_items(items: list):
    for item in items:
        item["skills"] = filters.format_list(item["skills"], "skills")
        item["talents"] = filters.format_list(item["talents"], "talents")
        item["abilities"] = filters.format_list(item["abilities"], "abilities")
    return items


@app.route("/adversaries/")
def all_adversaries():
    return render_template("table.html", title="Adversaries",
                           headers=["Type", "Skills", "Talents", "Abilities", "Equipment"],
                           fields=["level", "skills", "talents", "abilities", "equipment"],
                           entries=process_items(list(db.adversaries.find({}).sort("name", pymongo.ASCENDING))))


@app.route("/adversaries/imperials")
def get_imperials():
    # todo this should probably use a tag system instead of regex search
    return render_template("table.html", title="Adversaries",
                           headers=["Type", "Skills", "Talents", "Abilities", "Equipment"],
                           fields=["level", "skills", "talents", "abilities", "equipment"],
                           entries=process_items(list(db.adversaries
                                                 .find({"$or": [{"name": {"$regex": "Imperial"}},
                                                                {"tags": "imperial"}]})
                                                 .sort("name", pymongo.ASCENDING))))


@app.route("/adversaries/<object_id>")
def get_adversary(object_id):
    from bson import ObjectId
    item = db.adversaries.find({"_id": ObjectId(object_id)})[0]

    return render_template("adversary.html", title=item["name"], item=item)
