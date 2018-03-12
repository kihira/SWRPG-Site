from decorators import validate_objectid
from server.app import app
from server.db import db
from flask import render_template, url_for


@app.route("/books/")
def all_books():
    return render_template("table.html", title="Books", name_header="Book", categories=False, has_index=False,
                           headers=["System", "Key", "Initials"],
                           fields=["system", "key", "_id"], entries=list(db.books.find({})))


@app.route("/books/<book_id>")
def get_book(book_id):
    item = db.books.find({"_id": book_id})
    if len(item) != 1:
        return url_for("404")

    return render_template("book.html", title=f'{item["system"]}: {item["name"]}', item=item[0])
