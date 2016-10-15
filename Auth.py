from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route("/auth")
def main():
    return "here comes the authentication page."
