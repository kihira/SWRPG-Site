from pymongo.results import InsertOneResult, UpdateResult

from server.app import app
from server.db import db
from flask import render_template, abort, request


def get_form_data():
    return {
        "_id": request.form.get("_id", ""),
        "sku": request.form.get("sku", ""),
        "isbn": request.form.get("isbn", ""),
        "ffg_url": request.form.get("ffg_url", ""),
        "release_date": request.form.get("release_date", ""),
        "description": request.form.get("description", "")
    }


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
        item = get_form_data()
        result: InsertOneResult = db.books.insert_one(item)
        return render_template("edit/book.html", item=item, added=True)
    return render_template("edit/book.html")


@app.route("/books/<object_id>/edit", methods=['GET', 'POST'])
def edit_book(object_id: str):
    item = db.books.find({"_id": object_id})
    if item.count() != 1:
        return abort(404)
    item = item[0]

    if request.method == "POST":
        new_item = get_form_data()
        result: UpdateResult = db.books.update_one({"_id": item["_id"]}, {"$set": new_item})
        return render_template("edit/book.html", title=item["name"], item=new_item,
                               updated=(result.modified_count == 1))
    # return the template with values filled out if we haven't received any data
    return render_template("edit/book.html", title=item["name"], item=item)
