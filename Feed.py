from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request

from SQL_init import create_feed_table
from SQL_init import seed_feed_table
from SQL_init import test_feed_table
from SQL_init import get_all_feed
from SQL_init import create_feed_post
from SQL_init import get_feed_post_with_id
from SQL_init import update_feed_post
from SQL_init import delete_feed_post

feed = Blueprint('feed', __name__)


@feed.route("/feed")
def main():
    feed = get_all_feed()
    return render_template('feed.html', feed=feed)


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


@feed.route("/create-feed-post", methods=['GET','POST'])
def create_post_feed():
    if request.method == "POST":
        id = request.form.get('post_id')
        title = request.form.get('post_title')
        author = request.form.get('author')
        likes = request.form.get('number_of_likes')
        create_feed_post(id, title, author, likes)
        return redirect('/feed')
    return render_template("create_feed_post.html")


@feed.route("/update-post/<post_id>", methods=['GET','POST'])
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
        return render_template("update_feed_post.html", data=data)


@feed.route("/delete-post/<post_id>")
def delete_post_feed(post_id):
    delete_feed_post(post_id)
    return redirect('/feed')
