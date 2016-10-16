from flask import Blueprint
from flask import render_template

profile = Blueprint('profile', __name__)


@profile.route("/profile")
def main():
    return "here comes the profile page."
