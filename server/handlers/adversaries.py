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
@app.route("/adversaries/imperial")
def get_imperials():
    # todo this should probably use a tag system instead of regex search
    return render_template("table.html", title="Adversaries - Imperials",
                           headers=["Type", "Skills", "Talents", "Abilities", "Equipment"],
                           fields=["level", "skills", "talents", "abilities", "equipment"],
                           entries=process_items(list(db.adversaries
                                                 .find({"$or": [{"name": {"$regex": "Imperial"}},
                                                                {"tags": "imperial"}]})
                                                 .sort("name", pymongo.ASCENDING))))


@app.route("/adversaries/alliance")
@app.route("/adversaries/rebels")
def get_rebels():
    # todo this should probably use a tag system instead of regex search
    return render_template("table.html", title="Adversaries - Alliance",
                           headers=["Type", "Skills", "Talents", "Abilities", "Equipment"],
                           fields=["level", "skills", "talents", "abilities", "equipment"],
                           entries=process_items(list(db.adversaries
                                                      .find({"$or": [{"name": {"$regex": "Rebel"}},
                                                                     {"name": {"$regex": "Alliance"}},
                                                                     {"tags": "rebel"}]})
                                                      .sort("name", pymongo.ASCENDING))))


@app.route("/adversaries/<object_id>")
def get_adversary(object_id):
    from bson import ObjectId
    item = db.adversaries.find({"_id": ObjectId(object_id)})[0]
    equipment = []
    for i in item["equipment"]:
        if "type" in i:
            if i["type"] == "weapon":
                equipment.append(db.weapons.find({"_id": i["id"]})[0]["name"])
            elif i["type"] == "armor":
                equipment.append(db.armor.find({"_id": i["id"]})[0]["name"])
            elif i["type"] == "gear":
                equipment.append(db.gear.find({"_id": i["id"]})[0]["name"])
        else:
            equipment.append(i)
    item["equipment"] = equipment

    return render_template("adversary.html", title=item["name"], item=item)
