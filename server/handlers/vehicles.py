from decorators import validate_objectid
from server import filters
from server.app import app
from server.db import db
from flask import render_template, url_for
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


@app.route("/vehicles/<object_id>")
@validate_objectid
def get_vehicles(object_id):
    item = db.vehicles.find({"_id": ObjectId(object_id)})
    if item.count() != 1:
        return url_for("404")
    item = item[0]

    return render_template("vehicle.html", title=item["name"], item=item)


@app.route("/starships/<object_id>")
@validate_objectid
def get_starship(object_id):
    item = db.starships.find({"_id": ObjectId(object_id)})
    if item.count() != 1:
        return url_for("404")
    item = item[0]

    if type(item["hyperdrive"]) == dict:
        out = "Primary: {0}".format(item["hyperdrive"]["primary"])
        if "backup" in item["hyperdrive"]:
            out += ", Backup: {0}".format(item["hyperdrive"]["backup"])
        item["hyperdrive"] = out

    return render_template("vehicle.html", title=item["name"], item=item)
