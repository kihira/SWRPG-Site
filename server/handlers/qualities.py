from server.app import app
from server.db import db
from server import filters
from flask import render_template, abort


@app.route("/qualities/")
def all_qualities():
    items = list(db.qualities.find({}))
    for quality in items:
        quality["ranked"] = "Yes" if quality["ranked"] else "No"
        quality["description"] = filters.description(quality["description"])

    return render_template("table.html", title="Qualities", name_header="Quality", categories=False,
                           headers=["Active", "Ranked", "Effect"],
                           fields=["active", "ranked", "description"],
                           entries=items)


@app.route("/qualities/<quality_id>")
def get_quality(quality_id):
    item = db.qualities.find({"_id": quality_id})
    if item.count() != 1:
        return abort(404)
    item = item[0]

    return render_template("quality.html", title=item["_id"].replace("_", " "), item=item)
