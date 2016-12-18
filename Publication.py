from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request

from SQL_init import create_publication_table
from SQL_init import seed_publication_table
from SQL_init import test_publication_table
from flask import current_app as app

from flask_login import current_user
from flask_login.utils import login_required
import psycopg2 as dbApi
publication = Blueprint('publication', __name__)


@publication.route("/publications")
@login_required
def main():
   pubs=get_all_publications()
   return render_template('publication/publications.html',pubs = pubs)
  
@publication.route("/publications/add", methods=['POST'])
@login_required
def new_publication_form():
    authors  = request.form['author']
    title = request.form['title']
    publisher = request.form['publisher']
    category = request.form['category']
    connection = dbApi.connect(app.config['dsn'])
    with connection.cursor() as cur:
        query = """SELECT author_id FROM AUTHORS 
                    WHERE author_name = %s"""
        cur.execute(query,(authors,))
        try:
            author_id = cur.fetchone()[0]
        except:
            insert_to_authors(authors)
    connection.close()
    
    connection3 = dbApi.connect(app.config['dsn'])
    with connection3.cursor() as cur:
        query = """SELECT category_id FROM category 
                    WHERE category_name = %s"""
        cur.execute(query,(category,))
        try:
            category_id = cur.fetchone()[0]
        except:
            insert_category(category)
    connection3.close()
    
    connection2 = dbApi.connect(app.config['dsn'])
    with connection2.cursor() as cur:
        query = """SELECT author_id FROM AUTHORS 
                    WHERE author_name = %s"""
        cur.execute(query,(authors,)) 
        author_id = cur.fetchone()[0]
        query = """SELECT category_id FROM category 
                    WHERE category_name = %s"""
        cur.execute(query,(category,)) 
        category_id = cur.fetchone()[0]
        query = """INSERT INTO
                PUBLICATION (publication_title, publisher, author_id, category_id)
                VALUES
                    (%s, %s, %s, %s)"""
        cur.execute(query,(title, publisher,author_id,category_id))  
    connection2.commit()
    connection2.close()
   
    return redirect("/publications")

@login_required
def insert_to_authors(author_name):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """INSERT INTO AUTHORS (author_name) VALUES
        (%s)"""
        cursor.execute(query,(author_name,))
        connection.commit()    
    return

@publication.route("/publications/delete" , methods=['POST'] )
@login_required
def delete_from_publication():
   publication_id = request.form['publication_id']
   connection = dbApi.connect(app.config['dsn'])
   with connection:        
        query = """DELETE FROM PUBLICATION 
                    WHERE publication_id = %s"""
        with connection.cursor() as cur:
            cur.execute(query,(publication_id,))
        
   connection.close()
   
   return redirect("/publications")

@publication.route("/publications/select" , methods=['POST'] )
@login_required
def select_from_publication():
   aut_name = request.form['aut_name'] 
   with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(publication_id) FROM PUBLICATION,AUTHORS
                    WHERE  author_name= %s AND PUBLICATION.author_id = AUTHORS.author_id"""

        cursor.execute(query,(aut_name,))
        connection.commit()
        x = cursor.fetchone()[0]
        return str(x)

@publication.route("/publications/update" , methods=['POST'] )
@login_required
def update_publication():
   up_name = request.form['up_name']
   up_tit = request.form['up_tit']
   with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """UPDATE PUBLICATION SET publication_title = %s 
                    WHERE publication_title =%s;"""

        cursor.execute(query,(up_tit,up_name))
        connection.commit()
   return redirect("/publications")


@login_required
def get_all_publications():
   with dbApi.connect(app.config['dsn']) as connection:
       cursor = connection.cursor()
       query = """SELECT publication_id, publication_title, publisher, author_name, category_name FROM PUBLICATION,AUTHORS,category
                            WHERE PUBLICATION.author_id = AUTHORS.author_id AND PUBLICATION.category_id = category.category_id """
       cursor.execute(query)
       connection.commit()
       return cursor
   

@publication.route("/create-publication-table")
@login_required
def create_table():
    var = create_publication_table()
    if var:
        return redirect('/publications')
    else:
        return "Mission Failed: CREATE PUBLICATION TABLE"


@publication.route("/seed-publication-table")
@login_required
def seed_table():
    var = seed_publication_table()
    if var:
        return redirect('/publications')
    else: 
        return "Mission Failed: SEED PUBLICATION TABLE"


@publication.route("/test-publication-table")
@login_required
def test_table():
    count  = test_publication_table() 
    return "Number of records in the Publication table: %d." % count
   
 
@publication.route("/create-and-seed-publication-table")
@login_required
def create_and_seed():
    create_publication_table()
    seed_publication_table()
    return redirect('/publications')

@login_required
def insert_category(category_name):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """INSERT INTO category (category_name)
        VALUES (%s) """
        cursor.execute(query,(category_name,))
        connection.commit()
        
    return




