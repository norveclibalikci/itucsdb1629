from flask import Blueprint
from flask import render_template
from flask import redirect
from SQL_init import create_feed_table
from SQL_init import seed_feed_table

feed = Blueprint('feed', __name__)


@feed.route("/feed")
def main():
    return render_template('feed.html')


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