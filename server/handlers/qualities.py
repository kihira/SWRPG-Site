from server.app import app
from server.db import db
from server import filters
from flask import Markup, render_template


@app.route("/qualities/")
def all_qualities():
    entries = []
    for quality in db.qualities.find({}):
        quality["name"] = Markup(f'<a href="./{quality["_id"]}">{quality["_id"].replace("_", " ")}</a>')
        quality["ranked"] = "Yes" if quality["ranked"] else "No"
        quality["description"] = filters.symbol(quality["description"])
        entries.append(quality)

    return render_template("table.html", title="Qualities", header=["Quality", "Active", "Ranked", "Effect"],
                           fields=["name", "active", "ranked", "description"], entries=entries)


@app.route("/qualities/<quality_id>")
def get_quality(quality_id):
    quality = db.qualities.find({"_id": quality_id})[0]

    return render_template("quality.html", title=quality["_id"].replace("_", " "), item=quality)
