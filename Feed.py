import psycopg2 as dbApi
from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import current_app as app

from SQL_init import create_feed_table
from SQL_init import seed_feed_table
from SQL_init import test_feed_table

feed = Blueprint('feed', __name__)


@feed.route("/feed")
def main():
    feed = get_all_feed()
    return render_template('feed/feed.html', feed=feed)


@feed.route("/create-feed-table")
def create_table():
    create_feed_table()
    return redirect('/')


@feed.route("/seed-feed-table")
def seed_table():
    seed_feed_table()
    return redirect('/')


@feed.route("/create-and-seed-feed-table")
def create_and_seed():
    create_feed_table()
    seed_feed_table()
    return redirect('/')


@feed.route("/test-feed-table")
def testdb():
    count = test_feed_table()
    return "Number of records: %d." % count


@feed.route("/create-feed-post", methods=['GET', 'POST'])
def create_post_feed():
    if request.method == "POST":
        id = request.form.get('post_id')
        title = request.form.get('post_title')
        author = request.form.get('author')
        likes = request.form.get('number_of_likes')
        create_feed_post(id, title, author, likes)
        return redirect('/feed')
    return render_template("feed/create_feed_post.html")


@feed.route("/update-post/<post_id>", methods=['GET', 'POST'])
def update_post_feed(post_id):
    if request.method == "POST":
        id = request.form.get('post_id')
        title = request.form.get('post_title')
        author = request.form.get('author')
        likes = request.form.get('number_of_likes')
        update_feed_post(id, title, author, likes)
        return redirect('/feed')
    else:
        data = get_feed_post_with_id(post_id)
        return render_template("feed/update_feed_post.html", data=data)


@feed.route("/delete-post/<post_id>")
def delete_post_feed(post_id):
    delete_feed_post(post_id)
    return redirect('/feed')


@feed.route("/add-posts-to-feed", methods=['GET', 'POST'])
def list_all_the_posts():
    if request.method == "GET":
        posts = get_all_posts()
        return render_template("feed/list_all_posts.html", posts=posts)
    else:
        id_list = request.form.getlist('selected_posts')
        insert_into_feed(id_list)
        return redirect('/add-posts-to-feed')


def insert_into_feed(id_list):
    with dbApi.connect(app.config['dsn']) as connection:
        now = datetime.now()
        query = "INSERT INTO FEED (post_id, publication_id, number_of_likes, created_at) VALUES "
        for id in id_list:
            query += "(" + id + ", 0, 0, '" + now.strftime('%Y-%m-%d %H:%M:%S') + "'),"

        query = query[:-1]
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        return True


def get_all_posts():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT post_id, title, name FROM POSTS
        JOIN USERS ON POSTS.user_id = USERS.id
        WHERE post_id NOT IN (
            SELECT post_id FROM FEED)
        ORDER BY post_id;"""
        cursor.execute(query)
        connection.commit()
        return cursor


def get_all_feed():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT title, name FROM FEED
        JOIN POSTS ON FEED.post_id = POSTS.post_id
        JOIN USERS ON POSTS.user_id = USERS.id
        ORDER BY feed_id"""
        cursor.execute(query)
        connection.commit()
        return cursor


def create_feed_post(post_id, post_title, post_author, post_likes):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO FEED (post_id, post_title, author, number_of_likes) VALUES(%s,'%s','%s',%s)""" % (
            post_id, post_title, post_author, post_likes)

        cursor.execute(query)
        connection.commit()

        return True


def get_feed_post_with_id(id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT * FROM FEED WHERE post_id = %s;""" % id

        cursor.execute(query)
        connection.commit()

        return cursor


def update_feed_post(id, title, author, likes):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """UPDATE FEED
        SET post_id=%s, post_title='%s', author='%s', number_of_likes=%s
        WHERE post_id = %s;""" % (id, title, author, likes, id)
        cursor.execute(query)
        connection.commit()

        return True


def delete_feed_post(id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DELETE FROM FEED
        WHERE post_id = %s;""" % id
        cursor.execute(query)
        connection.commit()

        return True
