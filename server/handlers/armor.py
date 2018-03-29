from pymongo.results import InsertOneResult, UpdateResult

from server.decorators import validate_objectid
from server import filters
from server.app import app
from server.db import db
from flask import render_template, abort, request
from bson import ObjectId


@app.route("/armour/")
@app.route("/armor/")
def all_armor():
    items = list(db.armor.find({}))
    for item in items:
        item["price"] = filters.format_price_table(item["price"], item["restricted"])

    return render_template("table.html", title="Armor", name_header="Type", categories=False,
                           headers=["Defense", "Soak", "Price", "Encumbrance", "Hard Points", "Rarity"],
                           fields=["defense", "soak", "price", "encumbrance", "hardpoints", "rarity"],
                           entries=items)


@app.route("/armour/<object_id>")
@app.route("/armor/<object_id>")
@validate_objectid
def armor_item(object_id: str):
    item = db.armor.find({"_id": ObjectId(object_id)})
    if item.count() != 1:
        return abort(404)
    item = item[0]

    return render_template("armor.html", title=item["name"], item=item)


@app.route("/armour/add", methods=['GET', 'POST'])
@app.route("/armor/add", methods=['GET', 'POST'])
def add_armor():
    if request.method == "POST":
        # todo support adding index
        item = {
            "name": request.form["name"],
            "defense": request.form["defense"],
            "soak": request.form["soak"],
            "hardpoints": request.form["hardpoints"],
            "encumbrance": request.form["encumbrance"],
            "price": request.form["price"],
            "restricted": request.form.get("restricted", False),
            "rarity": request.form["rarity"],
            "description": request.form["description"]
        }
        result: InsertOneResult = db.armor.insert_one(item)
        item["_id"] = result.inserted_id
        return render_template("edit/armor.html", item=item, added=True)
    return render_template("edit/armor.html")


@app.route("/armour/<object_id>/edit", methods=['GET', 'POST'])
@app.route("/armor/<object_id>/edit", methods=['GET', 'POST'])
@validate_objectid
def edit_armor(object_id: str):
    item = db.armor.find({"_id": ObjectId(object_id)})
    if item.count() != 1:
        return abort(404)
    item = item[0]

    if request.method == "POST":
        new_item = {
            "name": request.form["name"],
            "defense": request.form["defense"],
            "soak": request.form["soak"],
            "hardpoints": request.form["hardpoints"],
            "encumbrance": request.form["encumbrance"],
            "price": request.form["price"],
            "restricted": request.form.get("restricted", False),
            "rarity": request.form["rarity"],
            "description": request.form["description"]
        }
        result: UpdateResult = db.armor.update_one({"_id": item["_id"]}, new_item)
        return render_template("edit/armor.html", title=item["name"], item=item, updated=(result.modified_count == 1))
    # return the template with values filled out if we haven't received any data
    return render_template("edit/armor.html", title=item["name"], item=item)
