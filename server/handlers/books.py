from server.app import app
from server.db import db
from flask import render_template


@app.route("/books/")
def all_books():
    return render_template("table.html", title="Books", name_header = "Book",
                           headers=["System", "Key", "Initials"],
                           fields=["system", "key", "_id"], entries=list(db.books.find({})), has_index=False)


@app.route("/books/<book_id>")
def get_book(book_id):
    item = db.books.find({"_id": book_id})[0]

    return render_template("book.html", title=f'{item["system"]}: {item["name"]}', item=item)
