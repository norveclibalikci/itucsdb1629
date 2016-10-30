from flask import Blueprint
from flask import render_template
from flask import redirect
from SQL_init import create_profile_table
from SQL_init import seed_profile_table
from SQL_init import test_profile_table

profile = Blueprint('profile', __name__)

@profile.route("/profile")
def main():
    return render_template('profile.html')

@profile.route("/create-profile-table")
def create_table():
    create_profile_table()
    return "PROFILE table is created"

@profile.route("/seed-profile-table")
def seed_table():
    seed_profile_table()
    return "Entries are added to the PROFILE table!"

@profile.route("/create-and-seed-profile-table")
def create_and_seed():
    create_profile_table()
    seed_profile_table()
    return "PROFILE table is created and the entries are added to it!"

@profile.route("/test-profile-table")
def testdb():
    count = test_profile_table()
    return "Number of records in the PROFILE table: %d." % count

