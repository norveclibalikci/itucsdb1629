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
   feed=get_all_feed()
   return render_template('publications.html',feed = feed)

@publication.route("/publications", methods=['POST'])
def new_publication_form():
   title = request.form['title']
   publisher = request.form['publisher']
   id = request.form['pub_id']
   
   connection = dbApi.connect(app.config['dsn'])
   with connection:
        
        query = """INSERT INTO
                PUBLICATION (publication_id,  publication_title, publisher)
                VALUES
                    (%s,%s, %s)"""
        with connection.cursor() as cur:
            cur.execute(query,(id,title,publisher))
        
   connection.close()
   
   return redirect("/publications")


@publication.route("/publications/delete" , methods=['POST'] )
def delete_form():
   de_id = request.form['del_id']
   connection = dbApi.connect(app.config['dsn'])
   with connection:
        
        query = """DELETE FROM PUBLICATION 
                    WHERE publication_id = %s"""
        with connection.cursor() as cur:
            cur.execute(query,(de_id,))
        
   connection.close()
   
   return redirect("/publications")

def get_all_feed():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT * FROM PUBLICATION ORDER BY publication_id;"""
        cursor.execute(query)
        connection.commit()
        return cursor

@publication.route("/publications/select" , methods=['POST'] )
def select_from_form():
   sel_id = request.form['sel_id'] 
   with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT publication_title FROM PUBLICATION
                    WHERE publication_id = %s"""

        cursor.execute(query,(sel_id,))
        connection.commit()
        x = cursor.fetchone()[0]
        return x

@publication.route("/publications/update" , methods=['POST'] )
def update_form():
   up_id = request.form['up_id']
   up_tit = request.form['up_tit']
   with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """UPDATE PUBLICATION SET publication_title = %s 
                    WHERE publication_id =%s;"""

        cursor.execute(query,(up_tit,up_id))
        connection.commit()
   return redirect("/publications")

def get_all_feed():
   with dbApi.connect(app.config['dsn']) as connection:
       cursor = connection.cursor()
       query = """SELECT * FROM PUBLICATION;"""
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

