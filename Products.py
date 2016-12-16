import psycopg2 as dbApi
import re
from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import current_app as app

from flask_login import current_user
from flask_login.utils import login_required

product = Blueprint('product', __name__)


@product.route("/books-for-sale")
@login_required
def main():
    books = get_all_books()
    return render_template('books/books.html', books=books)


@product.route("/delete-book/<book_id>")
@login_required
def delete_book_ad(book_id):
    if current_user.is_admin:
        delete_book(book_id)
    return redirect('/books-for-sale')


@product.route("/update-book/<book_id>", methods=['GET', 'POST'])
@login_required
def update_book_ad(book_id):
    if request.method == "GET":
        object = get_book_with_id(book_id).fetchone()
        if object:
            title = object[0]
            description = object[1]
            author = object[2]
            price = object[3]
            is_used = object[4]
            return render_template("books/update_book.html",
                                   object=object, title=title, description=description, author=author, price=price,
                                   is_used=is_used)
        else:
            return redirect('books-for-sale')
    else:
        if current_user.is_admin:
            title = request.form.get('book_title')
            description = request.form.get('description')
            author = request.form.get('author')
            price = request.form.get('price')
            is_used = request.form.get('is_used')
            update_book(book_id, title, description, author, price, is_used);
    return redirect('/books-for-sale')


@product.route("/sell-new-book", methods=['GET', 'POST'])
@login_required
def sell_new_book():
    if request.method == "GET":
        return render_template("books/sell_new_book.html")
    else:
        title = request.form.get('book_title')
        description = request.form.get('description')
        author = request.form.get('author')
        price = request.form.get('price')
        is_used = request.form.get('is_used')
        create_new_book_ad(title, description, author, price, is_used)
        return redirect('/books-for-sale')


@product.route("/book/<book_id>", methods=["GET", "POST"])
@login_required
def display_book(book_id):
    if request.method == "POST":
        comment = request.form.get('comment')
        create_comment(book_id, comment)
        return redirect("/book/%s" % book_id)
    else:
        book = get_book_with_id(book_id).fetchone()
        title = book[0]
        description = book[1]
        author = book[2]
        price = book[3]
        is_used = book[4]
        comments = get_comments_with_book_id(book_id)
        return render_template("/books/display_book.html", title=title, description=description,
                               author=author, price=price, comments=comments)


@product.route("/book/<book_id>/remove-comment/<comment_id>")
@login_required
def remove_comment_route(book_id, comment_id):
    if current_user.is_admin:
        remove_comment(comment_id)
        return redirect("book/%s" % book_id)


@product.route("/book/<book_id>/edit-comment/<comment_id>", methods=["POST"])
@login_required
def edit_comment_route(book_id, comment_id):
    if current_user.is_admin:
        new_comment = request.form.get("edited-comment")
        edit_comment(comment_id, new_comment)
        return redirect("book/%s" % book_id)


def get_all_books():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT BOOKS.id,
        u.name, title, description, author, price,
        is_used, created_at
        from BOOKS JOIN USERS as u
        ON u.id = BOOKS.user_id
        ORDER BY price;"""
        cursor.execute(query)
        connection.commit()
        return cursor


def get_book_with_id(id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT title, description, author, price,
        is_used
        from BOOKS where id=%s""" % id
        cursor.execute(query)
        connection.commit()
        return cursor


def delete_book(id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DELETE FROM BOOKS
        WHERE id = %s;""" % id
        cursor.execute(query)
        connection.commit()

        return True


def update_book(id, title, description, author, price, is_used):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        if is_used == "on":
            is_used = True
        else:
            is_used = False

        cursor.execute("""UPDATE BOOKS SET
        title=%s,
        description=%s,
        author=%s,
        price=%s,
        is_used=%s
        WHERE id = %s;""", (title, description, author, price, is_used, id))
        connection.commit()

        return True


def create_new_book_ad(title, description, author, price, is_used):
    with dbApi.connect(app.config['dsn']) as connection:
        now = datetime.now()
        if is_used == "on":
            is_used = True
        else:
            is_used = False

        cursor = connection.cursor()
        cursor.execute("""INSERT INTO BOOKS (user_id, title, description, author, price, is_used, created_at)
VALUES (%s, %s, %s, %s, %s, %s, %s);""", (
            current_user.id, title, description, author, price, is_used, now.strftime('%Y-%m-%d %H:%M:%S')))
        connection.commit()
        return True


def create_comment(book_id, comment):
    with dbApi.connect(app.config['dsn']) as connection:
        now = datetime.now()

        cursor = connection.cursor()
        cursor.execute("""INSERT INTO COMMENTS (user_id, book_id, comment)
VALUES (%s, %s, %s);""", (current_user.id, book_id, comment))
        connection.commit()
        return True


def get_comments_with_book_id(book_id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COMMENTS.id, book_id, comment, USERS.name FROM COMMENTS
        JOIN USERS ON COMMENTS.user_id=USERS.id
        WHERE book_id=%d""" % int(book_id)
        cursor.execute(query)
        connection.commit()
        return cursor


def remove_comment(comment_id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DELETE FROM COMMENTS WHERE id=%s""" % comment_id
        cursor.execute(query)
        connection.commit()
        return True


def edit_comment(comment_id, new_comment):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""UPDATE COMMENTS SET comment = %s WHERE id = %s""", (new_comment, comment_id))
        connection.commit()
        return True
