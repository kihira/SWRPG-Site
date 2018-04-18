from flask import request, redirect, url_for, render_template
from server.app import app
from server.db import db
from server import handlers


if __name__ == '__main__':
    app.run()


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
        db.planets.insert_one(planet)
        print(planet)
        return redirect(url_for("add_planet"))
    return render_template("edit/add-planet.html")


def strip_array(array):
    for i in range(len(array)):
        array[i] = array[i].strip()
    return array
