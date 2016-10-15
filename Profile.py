from flask import Blueprint

profile = Blueprint('profile', __name__)


@profile.route("/profile")
def main():
    return "here comes the profile page."
