from pymongo.results import InsertOneResult, UpdateResult

from model import Model, Field, TextareaField, SelectField
from server.app import app
from server.db import db
from flask import render_template, abort, request

model = Model([
    Field("_id", "Index"),
    Field("name", "Name"),
    SelectField("system", "System", [
        "Edge of the Empire",
        "Age of Rebellion",
        "Force and Destiny",
        "Star Wars Roleplaying"
    ]),
    Field("key", "SKU"),
    Field("isbn", "ISBN"),
    Field("ffg_url", "Product Page", html_type="url"),
    Field("release_date", "Release Date", html_type="date"),
    TextareaField("description", "Description")
])


@app.route("/books/")
def all_books():
    return render_template("table.html", title="Books", name_header="Book", categories=False, has_index=False,
                           headers=["System", "Key", "Initials"],
                           fields=["system", "key", "_id"], entries=list(db.books.find({})))


@app.route("/books/<book_id>")
def get_book(book_id):
    item = db.books.find({"_id": book_id})
    if item.count() != 1:
        return abort(404)
    item = item[0]

    return render_template("book.html", title=f'{item["system"]}: {item["name"]}', item=item)


@app.route("/books/add", methods=['GET', 'POST'])
def add_book():
    if request.method == "POST":
        item = model.from_form(request.form)
        result: InsertOneResult = db.books.insert_one(item)
        return render_template("edit/add-item.html", item=item, model=model, added=True)
    return render_template("edit/add-item.html", model=model)


@app.route("/books/<object_id>/edit", methods=['GET', 'POST'])
def edit_book(object_id: str):
    item = db.books.find({"_id": object_id})
    if item.count() != 1:
        return abort(404)
    item = item[0]

    if request.method == "POST":
        new_item = model.from_form(request.form)
        result: UpdateResult = db.books.update_one({"_id": item["_id"]}, {"$set": new_item})
        return render_template("edit/add-item.html", title=item["name"], item=new_item, model=model,
                               updated=(result.modified_count == 1))

    return render_template("edit/add-item.html", title=item["name"], item=item, model=model)
