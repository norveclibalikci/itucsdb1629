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

from flask_login import current_user
from flask_login.utils import login_required

feed = Blueprint('feed', __name__)


@feed.route("/feed")
@login_required
def main():
    feed = get_all_feed()
    return render_template('feed/feed.html', feed=feed)


@feed.route("/create-feed-table")
@login_required
def create_table():
    if current_user.is_admin:
        create_feed_table()
    return redirect('/')


@feed.route("/seed-feed-table")
@login_required
def seed_table():
    if current_user.is_admin:
        seed_feed_table()
    return redirect('/')


@feed.route("/create-and-seed-feed-table")
@login_required
def create_and_seed():
    if current_user.is_admin:
        create_feed_table()
        seed_feed_table()
    return redirect('/')


@feed.route("/test-feed-table")
@login_required
def testdb():
    if current_user.is_admin:
        count = test_feed_table()
    return "Number of records: %d." % count


@feed.route("/upvote-post/<post_id>/<likes>")
@login_required
def update_post_feed(post_id, likes):
    upvote_feed_post(post_id, likes)
    return redirect('/feed')


@feed.route("/delete-from-feed/<post_id>")
@login_required
def delete_post_feed(post_id):
    delete_feed_post(post_id)
    return redirect('/feed')


@feed.route("/delete-from-posts/<post_id>")
@login_required
def delete_post_from_posts(post_id):
    if current_user.is_admin:
        delete_posts_post(post_id)
    return redirect('/feed')


@feed.route("/add-posts-to-feed", methods=['GET', 'POST'])
@login_required
def list_all_the_posts():
    if request.method == "GET":
        posts = get_all_posts()

        return render_template("feed/list_all_posts.html", posts=posts)
    else:
        id_list = request.form.getlist('selected_posts')

        if id_list:
            insert_into_feed(id_list)
        return redirect('/feed')


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

        query = """SELECT FEED.post_id, title, name, number_of_likes FROM FEED
        JOIN POSTS ON FEED.post_id = POSTS.post_id
        JOIN USERS ON POSTS.user_id = USERS.id
        ORDER BY feed_id"""
        cursor.execute(query)
        connection.commit()
        return cursor


def get_feed_post_with_id(id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT * FROM FEED WHERE post_id = %s;""" % id

        cursor.execute(query)
        connection.commit()

        return cursor


def upvote_feed_post(post_id, likes):
    with dbApi.connect(app.config['dsn']) as connection:
        likes = int(likes) + 1
        cursor = connection.cursor()

        query = """UPDATE FEED
        SET number_of_likes=%s
        WHERE post_id = %s;""" % (likes, post_id)
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


def delete_posts_post(post_id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DELETE FROM POSTS
        WHERE post_id = %s;""" % post_id
        cursor.execute(query)
        connection.commit()

        return True
