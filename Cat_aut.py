from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request

from flask import current_app as app

from flask_login import current_user
from flask_login.utils import login_required

import psycopg2 as dbApi

cat_aut = Blueprint('cat_aut', __name__)

@cat_aut.route("/cat-aut")
@login_required
def main():
   cat = get_all_cat()
   authors = get_all_authors()
   return render_template('publication/cat_and_authors.html', cat =cat, authors=authors)

@cat_aut.route("/cat-aut/cat-add",  methods= ['POST'])
@login_required
def add_category():
    category_name = request.form['cat_name']
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """INSERT INTO category (category_name)
        VALUES (%s) """
        cursor.execute(query,(category_name,))
        connection.commit()
        
    return redirect("/cat-aut")

@cat_aut.route("/cat-aut/cat-del",  methods= ['POST'])
@login_required
def del_category():
    category_id = request.form['category_id']
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """DELETE FROM category WHERE category_id = %s  """
        cursor.execute(query,(category_id,))
        connection.commit()
        
    return redirect("/cat-aut")


@login_required
def get_all_cat():
      with dbApi.connect(app.config['dsn']) as connection:
       cursor = connection.cursor()
       query = """SELECT * FROM category"""
       cursor.execute(query)
       connection.commit()
       return cursor

@login_required
def get_all_authors():
      with dbApi.connect(app.config['dsn']) as connection:
       cursor = connection.cursor()
       query = """SELECT * FROM AUTHORS"""
       cursor.execute(query)
       connection.commit()
       return cursor

@cat_aut.route('/cat-aut/author-delete', methods=['POST'])
@login_required
def delete_from_authors():
    aut_id = request.form['author_id']
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """DELETE FROM AUTHORS WHERE author_id = %s"""

        cursor.execute(query,(aut_id,))
        connection.commit()
    return redirect("/cat-aut")

@cat_aut.route('/cat-aut/author-add', methods=['POST'])
@login_required
def add_author():
    aut_name = request.form['aut_name']
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """INSERT INTO AUTHORS (author_name)
        VALUES (%s) """
        cursor.execute(query,(aut_name,))
        connection.commit()
    return redirect("/cat-aut")
