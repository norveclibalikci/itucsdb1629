from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from SQL_init import create_publication_table
from SQL_init import seed_publication_table
from SQL_init import test_publication_table
from flask import current_app as app
import psycopg2 as dbApi
publication = Blueprint('publication', __name__)


@publication.route("/publications")
def main():
   pubs=get_all_publications()
   authors=get_all_authors()
   return render_template('publications.html',pubs = pubs,authors=authors)
  
@publication.route("/publications/add", methods=['POST'])
def new_publication_form():
    authors  = request.form['author']
    title = request.form['title']
    publisher = request.form['publisher']

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
    connection2 = dbApi.connect(app.config['dsn'])
    with connection2.cursor() as cur:
        query = """SELECT author_id FROM AUTHORS 
                    WHERE author_name = %s"""
        cur.execute(query,(authors,)) 
        author_id = cur.fetchone()[0]
        query = """INSERT INTO
                PUBLICATION (publication_title, publisher, author_id)
                VALUES
                    (%s, %s, %s)"""
        cur.execute(query,(title, publisher,author_id))  
    connection2.commit()
    connection2.close()
   
    return redirect("/publications")

def insert_to_authors(author_name):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """INSERT INTO AUTHORS (author_name) VALUES
        (%s)"""
        cursor.execute(query,(author_name,))
        connection.commit()    
    return

@publication.route("/publications/delete" , methods=['POST'] )
def delete_from_publication():
   de_name = request.form['del_tit']
   connection = dbApi.connect(app.config['dsn'])
   with connection:        
        query = """DELETE FROM PUBLICATION 
                    WHERE publication_title = %s"""
        with connection.cursor() as cur:
            cur.execute(query,(de_name,))
        
   connection.close()
   
   return redirect("/publications")

@publication.route("/publications/select" , methods=['POST'] )
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

@publication.route('/publications/author-delete', methods=['POST'])
def delete_from_authors():
    aut_name = request.form['aut_name']
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """DELETE FROM AUTHORS WHERE author_name = %s"""

        cursor.execute(query,(aut_name,))
        connection.commit()
    return redirect("/publications")

@publication.route('/publications/author-add', methods=['POST'])
def add_author():
    aut_name = request.form['aut_name']
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """INSERT INTO AUTHORS (author_name)
        VALUES (%s) """
        cursor.execute(query,(aut_name,))
        connection.commit()
    return redirect("/publications")

@publication.route('/publications/author-update', methods= ['POST'])
def update_author():
    up_name = request.form['up_name']
    aut_name = request.form['aut_name']
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """UPDATE AUTHORS SET author_name = %s 
                    WHERE author_name =%s;"""
        cursor.execute(query,(aut_name,up_name))
        connection.commit()
    return redirect("/publications")

def get_all_publications():
   with dbApi.connect(app.config['dsn']) as connection:
       cursor = connection.cursor()
       query = """SELECT publication_id, publication_title, publisher, author_name FROM PUBLICATION,AUTHORS 
                            WHERE PUBLICATION.author_id = AUTHORS.author_id"""
       cursor.execute(query)
       connection.commit()
       return cursor

def get_all_authors():
      with dbApi.connect(app.config['dsn']) as connection:
       cursor = connection.cursor()
       query = """SELECT * FROM AUTHORS"""
       cursor.execute(query)
       connection.commit()
       return cursor
   
@publication.route("/create-publication-table")
def create_table():
    var = create_publication_table()
    if var:
        return redirect('/publications')
    else:
        return "Mission Failed: CREATE PUBLICATION TABLE"


@publication.route("/seed-publication-table")
def seed_table():
    var = seed_publication_table()
    if var:
        return redirect('/publications')
    else: 
        return "Mission Failed: SEED PUBLICATION TABLE"


@publication.route("/test-publication-table")
def test_table():
    count  = test_publication_table() 
    return "Number of records in the Publication table: %d." % count
   
 
@publication.route("/create-and-seed-publication-table")
def create_and_seed():
    create_publication_table()
    seed_publication_table()
    return redirect('/publications')




