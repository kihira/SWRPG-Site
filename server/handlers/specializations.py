from copy import deepcopy
from werkzeug.datastructures import MultiDict
from server.decorators import get_item
from server.app import app
from server.db import db
from flask import render_template, request
from server.filters import title, to_id


def generate_talent_tree(talents: list):
    return [[talents[index] for index in range(row * 4, row * 4 + 4)] for row in range(0, 5)]


def generate_talent_connection(form: MultiDict, name: str, rows: int, cols: int):
    return [[form.get(f"{name}_{row}_{col}", False) is not False for col in range(0, cols)] for row in range(0, rows)]


@app.route("/specialisations/")
@app.route("/specializations/")
def all_specializations():
    return render_template("table.html", title="Specializations", columns=[{"header": "Career", "name": "career"}],
                           entries=db["specializations"].find({}).sort("_id", 1))


@app.route("/specialisations/add", methods=["GET", "POST"])
@app.route("/specializations/add", methods=["GET", "POST"])
def add_edit_specialization():
    if request.method == "POST":
        spec = {
            "_id": to_id(request.form.get("name")),
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "career": request.form.get("career"),
            "universal": request.form.get("universal"),
            "skills": request.form.getlist("skills"),
            "tree": {
                "talents": generate_talent_tree(request.form.getlist("talent")),
                "hoz": generate_talent_connection(request.form, "talent_hoz", 5, 3),
                "vert": generate_talent_connection(request.form, "talent_vert", 4, 4),
            },
            "index": request.form.getlist("index[]"),
        }
        print(spec)
        db["specializations"].insert_one(spec)

    talents = list(db["talents"].find({}))
    skills = list(db["skills"].find({}))
    return render_template("edit/edit-spec.html", talents=talents, skills=skills)


@app.route("/specialisations/<item>")
@app.route("/specializations/<item>")
@get_item(db.specializations)
def get_specializations(item):
    talents = {}
    for talent in db.talents.find({"_id": {"$in": [entry for row in item["tree"]["talents"] for entry in row]}}):
        talents[talent["_id"]] = talent

    for row_index in range(0, 5):
        for col_index in range(0, 4):
            talent = deepcopy(talents[item["tree"]["talents"][row_index][col_index]])
            talent["name"] = title(talent["_id"])
            if "short" in talent:
                talent["description"] = talent["short"]
            talent["vert"] = row_index < 4 and item["tree"]["vert"][row_index][col_index]
            talent["hoz_left"] = col_index > 0 and item["tree"]["hoz"][row_index][col_index - 1]
            talent["hoz_right"] = col_index < 3 and item["tree"]["hoz"][row_index][col_index]

            item["tree"]["talents"][row_index][col_index] = talent

    return render_template("specialization.html", item=item)
