from server.decorators import get_item, login_required
from server.model import Model, Field, TextareaField, SelectField
from server.app import app
from server.db import db
from flask import render_template, request, flash

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
    columns = [
        {"header": "System", "field": "system"},
        {"header": "Key", "field": "key"},
        {"header": "Initials", "field": "_id"},
    ]

    return render_template("table.html", title="Books", name_header="Book", categories=False, has_index=False,
                           columns=columns, entries=list(db["books"].find({})))


@app.route("/books/<item>")
@get_item(db.books)
def get_book(item):
    return render_template("book.html", title=f'{item["system"]}: {item["name"]}', item=item)


@app.route("/books/add", methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == "POST":
        item = model.from_form(request.form)
        item["_id"] = db["books"].insert_one(item)
        flash(f'Successfully added item. <a href="{item["_id"]}">View</a><a href="{item["_id"]}/edit">Edit</a>')
    return render_template("edit/add-edit.html", model=model)


@app.route("/books/<item>/edit", methods=['GET', 'POST'])
@login_required
@get_item(db.books)
def edit_book(item):
    if request.method == "POST":
        item = model.from_form(request.form)
        db["books"].update_one({"_id": item["_id"]}, {"$set": item})
        flash(f'Successfully updated item.')
    return render_template("edit/add-edit.html", item=item, model=model)
