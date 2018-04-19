from server.decorators import get_item
from server.app import app
from server.db import db
from flask import render_template


@app.route("/vehicles/")
def all_vehicles():
    entries = list(db["vehicles"].aggregate([{"$group": {"_id": "$category", "values": {"$push": "$$ROOT"}}},
                                             {"$sort": {"_id": 1}}]))

    items = []
    for category in entries:
        for vehicle in category["values"]:
            vehicle["crew"] = len(vehicle["crew"])
            if type(vehicle["weapons"]) == list:
                vehicle["weapons"] = len(vehicle["weapons"])
            items.append(vehicle)

    columns = [
        {"header": "Silhouette", "name": "silhouette", "filter": {"type": "number"}},
        {"header": "Speed", "name": "speed", "filter": {"type": "number"}},
        {"header": "Handling", "name": "handling", "filter": {"type": "number"}},
        {"header": "Crew", "name": "crew", "filter": {"type": "number"}},
        {"header": "Encumbrance", "name": "encumbrance", "filter": {"type": "number"}},
        {"header": "Passengers", "name": "passengers", "filter": {"type": "number"}},
        {"header": "Price", "name": "price", "filter": {"type": "number"}},
        {"header": "Restricted", "name": "restricted", "filter": {"type": "checkbox"}, "hidden": True},
        {"header": "Rarity", "name": "rarity", "filter": {"type": "number"}},
        {"header": "HP", "name": "hardpoints", "filter": {"type": "number"}},
        {"header": "Weapons", "name": "weapons", "filter": {"type": "number"}},
    ]

    return render_template("table.html", title="Vehicles", columns=columns, entries=items)


@app.route("/starships/")
def all_starships():
    entries = list(db["starships"].aggregate([{"$group": {"_id": "$category", "values": {"$push": "$$ROOT"}}},
                                              {"$sort": {"_id": 1}}]))

    items = []
    for category in entries:
        for vehicle in category["values"]:
            vehicle["crew"] = len(vehicle["crew"])
            if type(vehicle["weapons"]) == list:
                vehicle["weapons"] = len(vehicle["weapons"])
            items.append(vehicle)

    columns = [
        {"header": "Silhouette", "field": "silhouette", "filter": {"type": "number"}},
        {"header": "Speed", "field": "speed", "filter": {"type": "number"}},
        {"header": "Handling", "field": "handling", "filter": {"type": "number"}},
        {"header": "Crew", "field": "crew", "filter": {"type": "number"}},
        {"header": "Encumbrance", "field": "encumbrance", "filter": {"type": "number"}},
        {"header": "Passengers", "field": "passengers", "filter": {"type": "number"}},
        {"header": "Price", "field": "price", "filter": {"type": "number"}},
        {"header": "Restricted", "field": "restricted", "filter": {"type": "checkbox"}, "hidden": True},
        {"header": "Rarity", "field": "rarity", "filter": {"type": "number"}},
        {"header": "HP", "field": "hardpoints", "filter": {"type": "number"}},
        {"header": "Weapons", "field": "weapons", "filter": {"type": "number"}},
    ]

    return render_template("table.html", title="Starships", columns=columns, entries=items)


@app.route("/vehicles/<item>")
@get_item(db.vehicles, True)
def get_vehicle(item):
    return render_template("vehicle.html", item=item)


@app.route("/starships/<item>")
@get_item(db.starships, True)
def get_starship(item):
    if type(item["hyperdrive"]) == dict:
        out = "Primary: {0}".format(item["hyperdrive"]["primary"])
        if "backup" in item["hyperdrive"]:
            out += ", Backup: {0}".format(item["hyperdrive"]["backup"])
        item["hyperdrive"] = out

    return render_template("vehicle.html", item=item)
