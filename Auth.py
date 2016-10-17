from flask import Blueprint
from flask import render_template

auth = Blueprint('auth', __name__)


@auth.route("/auth")
def main():
    return render_template('login.html')
