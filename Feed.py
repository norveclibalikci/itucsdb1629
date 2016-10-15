from flask import Blueprint

user_feed = Blueprint('user_feed', __name__)


@user_feed.route("/feed")
def MainFeed():
    return "ahanda feed."
