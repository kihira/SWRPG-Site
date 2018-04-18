from server.decorators import get_item
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
        equipment = ""
        for i in item["equipment"]["weapons"]:
            if type(i) == dict:
                equipment += f'{i["quantity"]} '
                i = db["weapons"].find_one({"_id": i["id"]})
            else:
                i = db["weapons"].find_one({"_id": i})
            equipment += f'<a href="/weapons/{i["_id"]}">{i["name"]}</a>, '
        for i in item["equipment"]["armor"]:
            i = db["armor"].find_one({"_id": i}, {"name": True})
            equipment += f'<a href="/armor/{i["_id"]}">{i["name"]}</a>, '
        for i in item["equipment"]["gear"]:
            i = db["gear"].find_one({"_id": i}, {"name": True})
            equipment += f'<a href="/gear/{i["_id"]}">{i["name"]}</a>, '
        for i in item["equipment"]["other"]:
            equipment += i + ", "
        item["equipment"] = equipment[:-2]
    return items


@app.route("/adversaries/")
def all_adversaries():
    columns = [
        {"header": "Type", "field": "level"},
        {"header": "Skills", "field": "skills",
         "filter": {"type": "select", "data": [filters.title(x["_id"]) for x in list(db["skills"].find({}))]}},
        {"header": "Talents", "field": "talents",
         "filter": {"type": "select", "data": [filters.title(x["_id"]) for x in list(db["talents"].find({}))]}},
        {"header": "Abilities", "field": "abilities",
         "filter": {"type": "select", "data": [filters.title(x["_id"]) for x in list(db["abilities"].find({}))]}},
        {"header": "Equipment", "field": "equipment", "filter": {"type": "select"}}
    ]

    return render_template("table.html", title="Adversaries", categories=False, columns=columns,
                           entries=process_items(list(db["adversaries"].find({}).sort("name", pymongo.ASCENDING))))


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


@app.route("/adversaries/<item>")
@get_item(db.adversaries, True)
def get_adversary(item):
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

    return render_template("adversary.html", item=item)
