from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from SQL_init import create_post_table
from SQL_init import seed_post_table
from SQL_init import test_post_table
import psycopg2 as dbApi
from flask import current_app as app

post = Blueprint('post', __name__)

counter=3

@post.route("/post")
def main():
    return render_template('post.html',text=show_most_recent()[0])

@post.route("/edit", methods=['GET','POST'])
def edit_post():
    string_to_post=request.form.get('post_string')

    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        global counter
        query = """UPDATE POST SET content = %s WHERE post_id = %s;"""
        cursor.execute(query,(string_to_post,counter)   )
        connection.commit()
    return render_template('edit-post.html',recent_post=show_most_recent()[0])


@post.route("/post", methods=['POST'])
def send_form():
    string_to_post=request.form['post_string']

    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        global counter
        counter=counter+1
        query = """INSERT INTO
                POST (post_id, profile_id, category_id, content)
                VALUES
                    (%s, 22, 3,%s)"""
        cursor.execute(query,(counter,string_to_post))
        connection.commit()
    return redirect('/post')

@post.route("/post/delete-most-recent")
def drop_most_recent():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        global counter
        
        query = """DELETE FROM POST WHERE post_id = %s"""
        cursor.execute(query,(counter,))
        
        counter=counter-1
        return redirect('/post')

def show_most_recent():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        global counter
        query= """SELECT content FROM POST WHERE post_id = %s"""
        cursor.execute(query,(counter,))
        connection.commit()
        p = cursor.fetchone()
        if p is not None:
            return p
        else:
             return (" ",)
    
@post.route("/create-post-table")
def create_table():
    create_post_table()
    return redirect('/')


@post.route("/seed-post-table")
def seed_table():
    seed_post_table()
    return redirect('/')


@post.route("/create-and-seed-post-table")
def create_and_seed():
    create_post_table()
    seed_post_table()
    return redirect('/')


@post.route("/test-post-table")
def testdb():
    count = test_post_table()
    return "Number of records at database: %d." % count

