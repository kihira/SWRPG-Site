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
        for i in item["weapons"]:
            # if type(i) == dict:
            #    equipment += f'{i["quantity"]} '
            #    i = db["weapons"].find_one({"_id": i["id"]})
            # else:
            #    i = db["weapons"].find_one({"_id": i})
            equipment += f'<a href="/weapons/{i["_id"]}">{i["name"]}</a>, '
        for i in item["armor"]:
            equipment += f'<a href="/armor/{i["_id"]}">{i["name"]}</a>, '
        for i in item["gear"]:
            equipment += f'<a href="/gear/{i["_id"]}">{i["name"]}</a>, '
        for i in item["other"]:
            equipment += i + ", "
        item["equipment"] = equipment[:-2]
    return items


@app.route("/adversaries/")
def all_adversaries():
    columns = [
        {"header": "Type", "name": "level"},
        {"header": "Skills", "name": "skills",
         "filter": {"type": "select", "data": [filters.title(x["_id"]) for x in list(db["skills"].find({}))]}},
        {"header": "Talents", "name": "talents",
         "filter": {"type": "select", "data": [filters.title(x["_id"]) for x in list(db["talents"].find({}))]}},
        {"header": "Abilities", "name": "abilities",
         "filter": {"type": "select", "data": [filters.title(x["_id"]) for x in list(db["abilities"].find({}))]}},
        {"header": "Equipment", "name": "equipment", "filter": {"type": "select"}}
    ]

    items = db["adversaries"].aggregate([
        {"$unwind": {"path": "$equipment.weapons", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup":
                {
                    "from": "weapons",
                    "localField": "equipment.weapons",
                    "foreignField": "_id",
                    "as": "weapons"
                }
        },
        {"$unwind": {"path": "$weapons", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$equipment.gear", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup":
                {
                    "from": "gear",
                    "localField": "equipment.gear",
                    "foreignField": "_id",
                    "as": "gear"
                }
        },
        {"$unwind": {"path": "$gear", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$equipment.armor", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup":
                {
                    "from": "armor",
                    "localField": "equipment.armor",
                    "foreignField": "_id",
                    "as": "armor"
                }
        },
        {"$unwind": {"path": "$armor", "preserveNullAndEmptyArrays": True}},
        {
            "$group":
                {
                    "_id": "$_id",
                    "level": {"$first": "$level"},
                    "skills": {"$first": "$skills"},
                    "talents": {"$first": "$talents"},
                    "abilities": {"$first": "$abilities"},
                    "other": {"$first": "$equipment.other"},
                    "index": {"$first": "$index"},
                    "name": {"$first": "$name"},
                    "weapons": {"$addToSet": "$weapons"},  # todo look into why things are duplicating?
                    "armor": {"$addToSet": "$armor"},
                    "gear": {"$addToSet": "$gear"}
                }
        },
        {"$sort": {"name": 1}}
    ])

    return render_template("table.html", title="Adversaries", categories=False, columns=columns,
                           entries=process_items(list(items)))


@app.route("/adversaries/imperials")
@app.route("/adversaries/imperial")
def get_imperials():
    # todo this should probably use a tag system instead of regex search
    return render_template("table.html", title="Adversaries - Imperials",
                           headers=["Type", "Skills", "Talents",
                                    "Abilities", "Equipment"],
                           fields=["level", "skills", "talents",
                                   "abilities", "equipment"],
                           entries=process_items(list(db.adversaries
                                                      .find({"$or": [{"name": {"$regex": "Imperial"}},
                                                                     {"tags": "imperial"}]})
                                                      .sort("name", pymongo.ASCENDING))))


@app.route("/adversaries/alliance")
@app.route("/adversaries/rebels")
def get_rebels():
    # todo this should probably use a tag system instead of regex search
    return render_template("table.html", title="Adversaries - Alliance",
                           headers=["Type", "Skills", "Talents",
                                    "Abilities", "Equipment"],
                           fields=["level", "skills", "talents",
                                   "abilities", "equipment"],
                           entries=process_items(list(db.adversaries
                                                      .find({"$or": [{"name": {"$regex": "Rebel"}},
                                                                     {"name": {
                                                                         "$regex": "Alliance"}},
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
    
