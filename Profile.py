import psycopg2 as dbApi
from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request,url_for
from flask import current_app as app

from SQL_init import create_profile_table
from SQL_init import seed_profile_table
from SQL_init import test_profile_table

profile = Blueprint('profile', __name__)

@profile.route("/profile")
def main():
    profile = get_all_profiles()
    return render_template('profile.html', profile=profile)

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
    return redirect('/profile')

@profile.route("/test-profile-table")
def testdb():
    count = test_profile_table()
    return "Number of records in the PROFILE table: %d." % count

@profile.route("/add_profile",methods=['GET','POST'])
def add_profile():
    if request.method == 'POST':
        profile_name = request.form.get('first_name')
        profile_surname = request.form.get('surname')
        insert_profile(profile_name,profile_surname)
        return redirect('/profile')
    return render_template('add_profile.html')

@profile.route('/delete_profile',methods=['GET','POST'])
def delete_profile():
        if request.method == 'GET':
            profile_name = request.form.get('first_name')
            remove_profile(profile_name)
        else:
            return redirect('/profile')
        return render_template('delete_profile.html')

@profile.route("/update_profile",methods=['GET','POST'])
def update_profile():
    if request.method == 'POST':
            profile_name = request.form.get('first_name')
            new_profile_name = request.form.get('new_first_name')
            up_todate_profile(profile_name,new_profile_name)
            return redirect('/profile')
    return render_template('update_profile.html')


def insert_profile(firstname_, surname_):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT * from PROFILE
                ORDER BY profile_id
                DESC
                """

        cursor.execute(query)
        connection.commit()
        last_profile_id = cursor.fetchone()[0]
        new_profile_id = last_profile_id + 1
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO PROFILE VALUES(%s,%s,%s)
                """, (new_profile_id, firstname_, surname_,))

        connection.commit()

        return True


def remove_profile(firstname_):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""DELETE FROM PROFILE
        where name = '%s'""", (firstname_,))
        connection.commit()

        return True


def up_todate_profile(firstname_, newfirstname_):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""UPDATE PROFILE SET name = %s
                where name = %s""", (newfirstname_, firstname_,))
        connection.commit()

        return True


def get_all_profiles():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT profile_id, name, surname FROM PROFILE;"""
        cursor.execute(query)
        connection.commit()
        for row in cursor:
            profile_id, name, surname = row
            print('{}: {} {}'.format(profile_id, name, surname))
        cursor.close()
        connection.commit()

