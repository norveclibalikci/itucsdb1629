from flask import Blueprint
from flask import render_template
from flask import redirect
from SQL_init import create_post_table
from SQL_init import seed_post_table
from SQL_init import test_post_table

post = Blueprint('post', __name__)


@post.route("/post")
def main():
    return render_template('post.html')


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

