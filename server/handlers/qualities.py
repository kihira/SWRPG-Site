from decorators import get_item
from server.app import app
from server.db import db
from server import filters
from flask import render_template


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


@app.route("/qualities/<item>")
@get_item(db.qualities)
def get_quality(item):
    return render_template("quality.html", item=item)
