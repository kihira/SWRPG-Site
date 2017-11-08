from pymongo import MongoClient
from flask import Flask, Markup, request, redirect, url_for, render_template
from bson.objectid import ObjectId
import os
import custom_filters

app = Flask(__name__)
app.jinja_options = {
    "extensions": ['jinja2.ext.autoescape', 'jinja2.ext.with_'],
    "autoescape": False
}
client = MongoClient(os.environ['DB_CONN'])
db = client.starwars

# Register custom filters
custom_filters.register()


@app.route("/")
def main_page():
    return render_template("table.html", title="Hello", header=["First", "Second"],
                           entries=[["1", "2"]])


@app.route("/skills/")
def skills():
    entries = []
    for skill in db.skills.find({}):
        entry = [Markup("<a href=\"./{0}\">{0}</a>".format(skill["_id"])),
                 skill["characteristic"], skill["type"], skill["index"]]
        entries.append(entry)

    return render_template("table.html", title="Skills", header=["Skill", "Characteristic", "Type", "Index"],
                           entries=entries)


@app.route("/gear/")
def gear():
    entries = []
    for gear in db.gear.find({}):
        gear["name"] = Markup("<a href=\"./{0}\">{1}</a>".format(gear["_id"], gear["name"]))
        gear["price"] = custom_filters.format_price_table(gear["price"], gear["restricted"])
        entries.append(gear)

    return render_template("table.html", title="Items", header=["Item", "Price", "Encumbrance", "Rarity", "Index"],
                           fields=["name", "price", "encumbrance", "rarity"], entries=entries, clazz="gear")


@app.route("/gear/<object_id>")
def gear1(object_id):
    gear = db.gear.find({"_id": ObjectId(object_id)})[0]

    return render_template("item.html", title=gear["name"], item=gear)


@app.route("/add-planet", methods=['GET', 'POST'])
def add_planet():
    if request.method == "POST":
        planet = {
            "_id": request.form["name"],
            "astronavigation": {
                "system": request.form["astronavigation"].split(",")[0][:-7].strip(),
                "sector": request.form["astronavigation"].split(",")[1][:-7].strip(),
                "region": request.form["astronavigation"].split(",")[2][:-7].strip()
            },
            "orbital": {
                "days": int(request.form["orbital"].split("/")[0].strip().split(" ")[0].replace(",", "")),
                "hours": int(request.form["orbital"].split("/")[1].strip().split(" ")[0].replace(",", ""))
            },
            "government": request.form["government"],
            "population": request.form["population"],
            "languages": strip_array(request.form["languages"].split(",")),
            "terrain": request.form["terrain"],
            "cities": {
                "capital": request.form["capital"],
                "others": strip_array(request.form["othercities"].split(","))
            },
            "areas": strip_array(request.form["areas"].split(",")),
            "exports": strip_array(request.form["exports"].split(",")),
            "imports": strip_array(request.form["imports"].split(",")),
            "routes": strip_array(request.form["routes"].split(",")),
            "conditions": request.form["conditions"],
            "background": request.form["background"]
        }
        db.planets.insert(planet)
        print(planet)
        return redirect(url_for("add_planet"))
    return render_template("add-planet.html")


def strip_array(array):
    for i in range(len(array)):
        array[i] = array[i].strip()
    return array
