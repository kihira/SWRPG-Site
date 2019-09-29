from server import filters

from server.endpoint import Endpoint
from server.model import Model, Field, SelectField, TextareaField, CheckboxField, ArrayField

qualities_endpoint = Endpoint("qualities", "Qualities", Model([
    Field("_id", "Name", table=False),
    SelectField("active", "Active", ["Active", "Passive"]),
    TextareaField("description", "Description", render=filters.description),
    CheckboxField("ranked", "Ranked", render=filters.format_yes_no),
    ArrayField(Field("index", "Index"), table=False),
]), objectid=False)


# @app.route("/qualities/")
# def all_qualities():
#     items = list(db["qualities"].find({}))
#     for quality in items:
#         quality["ranked"] = "Yes" if quality["ranked"] else "No"
#         quality["description"] = filters.description(quality["description"])
#
#     columns = [
#         {"header": "Active", "name": "active", "filter": {"type": "select"}},
#         {"header": "Ranked", "name": "ranked"},
#         {"header": "Effect", "name": "description"}
#     ]
#
#     return render_template("table.html", title="Qualities", name_header="Quality", categories=False,
#                            columns=columns, entries=items)
#
#
# @app.route("/qualities/<item>")
# @get_item(db.qualities)
# def get_quality(item):
#     return render_template("qualities.html", item=item)
