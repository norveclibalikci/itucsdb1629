from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from SQL_init import create_post_table
from SQL_init import seed_post_table
from SQL_init import test_post_table
import psycopg2 as dbApi
from flask import current_app as app
from unicodedata import category

from flask_login import current_user
from flask_login.utils import login_required
post = Blueprint('post', __name__)




@post.route("/post")
@login_required
def main():
    return render_template('post.html', text=show_most_recent()[0], category1=str(show_most_relevant()[0]),category2=show_2nd_relevant()[0],category_name=show_most_recent()[1])


@post.route("/edit", methods=['GET', 'POST'])
def edit_post():
    string_to_post = request.form.get('post_string')

    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query= """SELECT post_id FROM POSTS ORDER BY post_id DESC LIMIT 1;"""
        cursor.execute(query)
        counter=cursor.fetchone()[0]
        print(string_to_post)
        query = """UPDATE POSTS SET content = %s WHERE post_id = %s;"""
        cursor.execute(query, (string_to_post, counter))
        connection.commit()
    return render_template('edit-post.html', recent_post=show_most_recent()[0])

@post.route("/edit-category", methods=['GET', 'POST'])
def edit_category1():
    string_to_post = request.form.get('string')
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query= """SELECT category_id FROM CATEGORIES ORDER BY category_id DESC LIMIT 2; """
        cursor.execute(query)
        connection.commit()
        p=cursor.fetchone()
        
        if string_to_post is not None:
            query="""UPDATE CATEGORIES SET category_name = '%s' WHERE category_id = %s;""" %(string_to_post,p[0])
            cursor.execute(query)
            connection.commit()
        
    return render_template('edit-category.html')


@post.route("/edit-category2", methods=['GET', 'POST'])
def edit_category2():
    string_to_post = request.form.get('string')
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query= """SELECT MAX( category_id )
              FROM CATEGORIES
         WHERE category_id< ( SELECT MAX( category_id )
                 FROM CATEGORIES ); """
        cursor.execute(query)
        connection.commit()
        p=cursor.fetchone()
        
        if string_to_post is not None:
            query="""UPDATE CATEGORIES SET category_name = '%s' WHERE category_id = %s;""" %(string_to_post,p[0])
            cursor.execute(query)
            connection.commit()
        
    return render_template('edit-category2.html')



@post.route("/post", methods=['GET','POST'])
def send_form():
    title = request.form.get('title')
    content = request.form.get('post_string')
    category=request.form.get('category')
    connection = dbApi.connect(app.config['dsn'])
    with connection.cursor() as cur:
        query = """SELECT category_id FROM CATEGORIES 
                    WHERE category_name = %s"""
        cur.execute(query,(category,))
        try:
            category_id = cur.fetchone()[0]
        except:
            insert_category(category)
    connection.close()
    connection2 = dbApi.connect(app.config['dsn'])
    with connection2.cursor() as cur:
        query = """SELECT category_id FROM CATEGORIES 
                    WHERE category_name = %s"""
        cur.execute(query,(category,)) 
        category_id = cur.fetchone()[0]
        query = """INSERT INTO
                POSTS (title,content,category_id)
                VALUES
                    (%s, %s, %s)"""
        cur.execute(query,(title, content,category_id))  
    connection2.commit()
    connection2.close()
    return redirect('/post')

def insert_category(category):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """INSERT INTO CATEGORIES (category_name) VALUES
        (%s)"""
        cursor.execute(query,(category,))
        connection.commit() 
        
    return
        
@post.route("/post/delete-most-recent")
def drop_most_recent():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query= """SELECT post_id FROM POSTS ORDER BY post_id DESC LIMIT 1;"""
        cursor.execute(query)
        counter=cursor.fetchone()[0]
        query = """DELETE FROM POSTS WHERE post_id = %s"""
        cursor.execute(query, (counter,))

  
        return redirect('/post')


def show_most_recent():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query= """SELECT post_id FROM POSTS ORDER BY post_id DESC LIMIT 1;"""
        cursor.execute(query)
        counter=cursor.fetchone()[0]
        query = """SELECT content,category_name FROM POSTS,CATEGORIES WHERE (post_id = %s AND POSTS.category_id=CATEGORIES.category_id)"""
        cursor.execute(query, (counter,))
        connection.commit()
        p = cursor.fetchone()
        if p is not None:
            return p
        else:
            return (" ",)
def show_most_relevant():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query= """SELECT category_name FROM CATEGORIES ORDER BY category_id DESC LIMIT 2; """
        cursor.execute(query)
        connection.commit()
        p=cursor.fetchone()
        if p is not None:
            return p
        else:
            return (" ",)
def show_2nd_relevant():
     with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query= """SELECT MAX( category_id )
              FROM CATEGORIES
         WHERE category_id< ( SELECT MAX( category_id )
                 FROM CATEGORIES ); """
        cursor.execute(query)
        connection.commit()
        p=cursor.fetchone()
        if p[0] is not None:
            query= """SELECT category_name FROM CATEGORIES WHERE category_id=%s"""% (p[0])
            cursor.execute(query)
            connection.commit()
            p=cursor.fetchone()
            if p is not None:
                return p
            else:
                return (" ",)
        else:
            return (" ",)
@post.route("/post/delete_most_relevant_category")
def delete_most_relevant():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        todel=show_most_relevant()[0]
        if todel !=" ":
            query = """DELETE FROM CATEGORIES WHERE category_name='%s'""" % (todel)
            cursor.execute(query)
            connection.commit()
    return redirect('/post')
def delete_2nd_relevant():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        todel=show_most_relevant()[0]
        if todel !=" ":
            query = """DELETE FROM CATEGORIES WHERE category_name='%s'""" % (todel)
            cursor.execute(query)
            connection.commit()
    return redirect('/post')
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
