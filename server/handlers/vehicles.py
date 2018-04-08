from server.decorators import get_item
from server import filters
from server.app import app
from server.db import db
from flask import render_template, abort
from bson import ObjectId


@app.route("/vehicles/")
def all_vehicles():
    data = list(db.vehicles.aggregate([{"$group": {"_id": "$category", "values": {"$push": "$$ROOT"}}},
                                       {"$sort": {"_id": 1}}]))

    entries = []
    for category in data:
        for vehicle in category["values"]:
            vehicle["price"] = filters.format_price_table(vehicle["price"], vehicle["restricted"])
            vehicle["crew"] = len(vehicle["crew"])
            if type(vehicle["weapons"]) == list:
                vehicle["weapons"] = len(vehicle["weapons"])

            entries.append(vehicle)

    return render_template("table.html", title="Vehicles",
                           headers=["Silhouette", "Speed", "Handling", "Crew", "Encumbrance", "Passengers",
                                    "Price", "Rarity", "HP", "Weapons"],
                           fields=["silhouette", "speed", "handling", "crew", "encumbrance", "passengers",
                                   "price", "rarity", "hardpoints", "weapons"], entries=entries)


@app.route("/starships/")
def all_starships():
    data = list(db.starships.aggregate([{"$group": {"_id": "$category", "values": {"$push": "$$ROOT"}}},
                                        {"$sort": {"_id": 1}}]))

    entries = []
    for category in data:
        for vehicle in category["values"]:
            vehicle["price"] = filters.format_price_table(vehicle["price"], vehicle["restricted"])
            vehicle["crew"] = len(vehicle["crew"])
            if type(vehicle["weapons"]) == list:
                vehicle["weapons"] = len(vehicle["weapons"])

            entries.append(vehicle)

    return render_template("table.html", title="Starships",
                           headers=["Silhouette", "Speed", "Handling", "Crew", "Encumbrance", "Passengers",
                                    "Price", "Rarity", "HP", "Weapons"],
                           fields=["silhouette", "speed", "handling", "crew", "encumbrance", "passengers",
                                   "price", "rarity", "hardpoints", "weapons"], entries=entries)


@app.route("/vehicles/<item>")
@get_item(db.vehicles, True)
def get_vehicle(item):
    return render_template("vehicle.html", title=item["name"], item=item)


@app.route("/starships/<item>")
@get_item(db.starships, True)
def get_starship(item):
    if type(item["hyperdrive"]) == dict:
        out = "Primary: {0}".format(item["hyperdrive"]["primary"])
        if "backup" in item["hyperdrive"]:
            out += ", Backup: {0}".format(item["hyperdrive"]["backup"])
        item["hyperdrive"] = out

    return render_template("vehicle.html", title=item["name"], item=item)
