from bson import ObjectId
from flask import render_template, abort, request, flash
from pymongo.collection import Collection

from server import db, app
from server.decorators import login_required
from server.model import Model


class Endpoint:
    url: str
    title: str
    model: Model
    collection: Collection
    objectid: bool

    def __init__(self, url: str, title: str, model: Model, collection: Collection = None, objectid: bool = True):
        self.url = url
        self.title = title
        self.model = model
        self.collection = db[url] if collection is None else collection
        self.objectid = objectid

        app.add_url_rule(f"/{url}/", endpoint=f"table_{url}", view_func=self.view_table)
        app.add_url_rule(f"/{url}/<item>", endpoint=f"item_{url}", view_func=self.view_item)
        app.add_url_rule(f"/{url}/<item>/edit", endpoint=f"edit_{url}", view_func=self.edit_item, methods=["GET", "POST"])
        app.add_url_rule(f"/{url}/add", endpoint=f"add_{url}", view_func=self.add_item, methods=["GET", "POST"])

    def view_table(self):
        return render_template("table-model.html", title=self.title, model=self.model,
                               entries=list(self.collection.find({})))

    def view_item(self, item: str):
        item = self.get_item(item)

        return render_template(f"{self.url}.html", item=item)

    @login_required
    def add_item(self):
        if request.method == "POST":
            item = self.model.from_form(request.form)
            item["_id"] = self.collection.insert_one(item).inserted_id
            flash(f'Successfully added item. <a href="{item["_id"]}">View</a> <a href="{item["_id"]}/edit">Edit</a>')
        return render_template("edit/add-edit.html", model=self.model)

    @login_required
    def edit_item(self, item):
        item = self.get_item(item)

        if request.method == "POST":
            item = self.model.from_form(request.form)
            self.collection.update_one({"_id": item["_id"]}, {"$set": item})
            flash(f'Successfully updated item.')
        return render_template("edit/add-edit.html", item=item, model=self.model)

    def get_item(self, item):
        if self.objectid:
            if len(item) != 24:
                return abort(404)
            item = ObjectId(item)

        item = self.collection.find_one(item)
        if item is None:
            return abort(404)
        return item
