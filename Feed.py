from flask import Blueprint
from flask import render_template

user_feed = Blueprint('user_feed', __name__)


@user_feed.route("/feed")
def main():
    return render_template('feed.html')
