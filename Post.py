from flask import Blueprint

post = Blueprint('post', __name__)


@post.route("/post")
def main():
    return "here comes the post page."
