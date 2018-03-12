from bson import ObjectId
from decorators import validate_objectid
from server.app import app
from server.db import db
from server import filters
from flask import render_template, url_for
import pymongo


def process_items(items: list):
    for item in items:
        item["skills"] = filters.format_list(item["skills"], "skills")
        item["talents"] = filters.format_list(item["talents"], "talents")
        item["abilities"] = filters.format_list(item["abilities"], "abilities")
        equipment = ""
        for i in item["equipment"]["weapons"]:
            if type(i) == dict:
                equipment += f'{i["quantity"]} '
                print(i["id"])
                i = db.weapons.find({"_id": i["id"]})[0]
            else:
                i = db.weapons.find({"_id": i})[0]
            equipment += f'<a href="/weapons/{i["_id"]}">{i["name"]}</a>, '
        for i in item["equipment"]["armor"]:
            i = db.armor.find({"_id": i})[0]
            equipment += f'<a href="/armor/{i["_id"]}">{i["name"]}</a>, '
        for i in item["equipment"]["gear"]:
            i = db.gear.find({"_id": i})[0]
            equipment += f'<a href="/gear/{i["_id"]}">{i["name"]}</a>, '
        for i in item["equipment"]["other"]:
            equipment += i + ", "
        item["equipment"] = equipment[:-2]
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
@validate_objectid
def get_adversary(object_id: str):
    item = db.adversaries.find({"_id": ObjectId(object_id)})
    if item.count() != 1:
        return url_for("404")
    item = item[0]

    equipment = []
    # Compile it all into one list so we can compile some stuff together
    for weapon in item["equipment"]["weapons"]:
        if type(weapon) == dict:
            quantity = weapon["quantity"]
            weapon = db.weapons.find({"_id": weapon["id"]})[0]
            weapon["quantity"] = quantity
        else:
            weapon = db.weapons.find({"_id": weapon})[0]
        weapon["type"] = "weapon"
        equipment.append(weapon)
    for armor in item["equipment"]["armor"]:
        armor = db.armor.find({"_id": armor})[0]
        armor["type"] = "armor"
        equipment.append(armor)
    for gear in item["equipment"]["gear"]:
        gear = db.gear.find({"_id": gear})[0]
        gear["type"] = "gear"
        equipment.append(gear)
    equipment.extend([other for other in item["equipment"]["other"]])
    item["equipment"] = equipment

    item["name"] = f'{item["name"]} [{item["level"]}]'

    return render_template("adversary.html", title=item["name"], item=item)
