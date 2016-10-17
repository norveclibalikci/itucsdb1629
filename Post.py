from flask import Blueprint
from flask import render_template

post = Blueprint('post', __name__)


@post.route("/post")
def main():
    return render_template("post.html")
