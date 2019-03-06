from server.decorators import get_item
from server.app import app
from server.db import db
from server import filters
from flask import render_template


def process_items(items: list):
    for item in items:
        item["skills"] = filters.format_list(item["skills"], "skills")
        item["talents"] = filters.format_list(item["talents"], "talents")
        item["abilities"] = filters.format_list(item["abilities"], "abilities")
        equipment = ""
        for i in item["equipment"]:
            equipment += f'{i["name"]}, '
        item["equipment"] = equipment[:-2]
    return items


@app.route("/creatures/")
def all_creatures():
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

    items = db["creatures"].find({})

    return render_template("table.html", title="Creatures", categories=False, columns=columns,
                           entries=process_items(list(items)))


@app.route("/creatures/<item>")
@get_item(db.creatures, True)
def get_creature(item):
    item["name"] = f'{item["name"]} [{item["level"]}]'

    return render_template("creature.html", item=item)
