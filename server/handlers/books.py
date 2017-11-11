from server.app import app
from server.db import db
from flask import Markup, render_template


@app.route("/books/")
def all_books():
    entries = []
    for book in db.books.find({}):
        book["name"] = Markup("<a href=\"./{0}\">{1}</a>".format(book["_id"], book["name"]))
        entries.append(book)

    return render_template("table.html", title="Books", header=["Book", "System", "Key", "Initials"],
                           fields=["name", "system", "key", "_id"], entries=entries, has_index=False)


@app.route("/books/<book_id>")
def get_book(book_id):
    book = db.books.find({"_id": book_id})[0]

    return render_template("book.html", title="{0}: {1}".format(book["system"], book["name"]), item=book)
