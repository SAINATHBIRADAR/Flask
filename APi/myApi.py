from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/books", methods=["GET", "POST"])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor = cursor.execute("SELECT * from book")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == "POST":
        new_author = request.form["author"]
        new_language = request.form["language"]
        new_title = request.form["title"]
        sql = """INSERT INTO book(author,language,title)
                VALUES (?,?,?)
              """
        cursor.execute(sql, (new_author, new_language, new_title))
        conn.commit()
        return f"Books with id :{cursor.lastrowid} created successfully"

        # new_obj = {
        #     'author' : new_author,
        #     'country' : new_country,
        #     'language' : new_language,
        #     'title' : new_title,
        #     'year' : new_year
        # }
        # books_list.append(new_obj)
        # return jsonify(books_list)


@app.route("/books/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None

    # GET operation
    if request.method == "GET":
        cursor.execute("SELECT * FROM book WHERE id =?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404

    # UPDATE operation
    if request.method == "PUT":
        sql = """
            UPDATE book
            SET author = ?,
                language = ?,
                title = ?
            WHERE id = ?
        """
        author = request.form["author"]
        language = request.form["language"]
        title = request.form["title"]
        update_book = {
            "id": id,
            "author": author,
            "language": language,
            "title": title
        }
        cursor.execute(sql, (author, language, title, id))
        conn.commit()
        return jsonify(update_book)
        # for book in books_list:
        #     if book["author"] == author:
        #         book['author'] = request.form['author']
        #         updated_book = {
        #             'author': book["author"]
        #         }
        #         return jsonify(updated_book)

        # DELETE operation
    if request.method == "DELETE":
        sql = "DELETE from book WHERE id = ?"
        cursor.execute(sql, (id,))
        conn.commit()
        return "The book with the id {} is successfully deleted".format(id), 200
    # if request.method == "DELETE":
    #     for index , book in  enumerate(books_list):
    #         if book['author'] == author:
    #             books_list.pop(index)
    #             return jsonify(books_list)


if __name__ == "__main__":
    app.run()
