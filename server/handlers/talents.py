from server.app import app
from server.db import db
from flask import Markup, render_template


@app.route("/talents/")
def all_talents():
    entries = []
    for talent in db.talents.find({}):
        talent["name"] = Markup(
            "<a href=\"./{0}\">{1}</a>".format(talent["_id"], talent["_id"].replace("_", " ").title()))
        if not talent["activation"]:
            talent["activation"] = "Passive"
        elif type(talent["activation"]) == dict:
            talent["activation"] = "Active (" + to_list(talent["activation"]) + ")"
        else:
            talent["activation"] = "Active"
        entries.append(talent)

    return render_template("table.html", title="Items", header=["Talent", "Activation", "Ranked", "Force Sensitive"],
                           fields=["name", "activation", "ranked", "force"], entries=entries)


@app.route("/talents/<talent_id>")
def get_talent(talent_id):
    talent = db.talents.find({"_id": talent_id})[0]

    return render_template("item.html", title=talent["_id"].replace("_", " ").title(), item=talent)


def to_list(dic):
    out = ""
    for key in dic:
        out += key.replace("_", " ").title() + ", "
    return out[:-2]
