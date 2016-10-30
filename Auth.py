from flask import Blueprint
from flask import render_template
from SQL_init import create_user_table
from SQL_init import seed_user_table
from SQL_init import test_user_table

auth = Blueprint('auth', __name__)


@auth.route("/auth")
def main():
    return render_template('login.html')

@auth.route("/create-user-table")
def create_table():
    create_user_table()
    return "user table created"

@auth.route("/seed-user-table")
def seed_table():
    seed_user_table()
    return "added sample seeds"

@auth.route("/create-and-seed-user-table")
def create_and_seed():
    create_user_table()
    seed_user_table()
    return "created and added"

@auth.route("/test-user-table")
def testdb():
    count = test_user_table()
    return "number of users in the user table: %d" % count
