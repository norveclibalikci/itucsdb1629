import psycopg2 as dbApi
from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request, url_for
from flask import current_app as app

from SQL_init import test_profile_table

from flask_login import current_user
from flask_login.utils import login_required

profile = Blueprint('profile', __name__)


@profile.route("/profile")
def main():
    profile = list_profiles()
    advertisement = get_all_advertisements()
    return render_template('profile/profile.html', profile=profile, advertisement=advertisement)


@profile.route("/test-profile-table")
def testdb():
    count = test_profile_table()
    return "Number of records in the PROFILE table: %d." % count


@profile.route("/add_profile", methods=['GET', 'POST'])
def add_profile():
    if request.method == 'POST':
        profile_name = request.form.get('first_name')
        profile_surname = request.form.get('surname')
        profile_job = request.form.get('job_id')
        profile_message = request.form.get('mess')
        insert_profile(profile_name, profile_surname, profile_job, profile_message)
        return redirect('/profile')
    else:
        jobs = get_all_jobs()
        return render_template('profile/add_profile.html', jobs=jobs)


@profile.route('/delete_profile', methods=['GET', 'POST'])
@login_required
def delete_profile():
    if request.method == 'POST':
        profile_id = request.form.get('profile_id')
        remove_profile(profile_id)
        return redirect("/profile")
    else:
        profiles = get_all_profiles()
        return render_template('profile/delete_profile.html', profiles=profiles)


@profile.route("/update_profile", methods=['GET', 'POST'])
def update_profile():
    if request.method == 'POST':
        profile_id = request.form.get('profile_id')
        new_mess = request.form.get('new_mess')
        up_todate_profile(profile_id, new_mess)
        return redirect('/profile')
    else:
        profiles = get_all_profiles()
        if profiles.rowcount == 0:
            return redirect("/profile")
        else:
            return render_template('profile/update_profile.html', profiles=profiles)


@profile.route("/advertise", methods=['GET', 'POST'])
def advertise():
    if request.method == 'POST':
        advert_name = request.form.get('advertiser_name')
        advert_product = request.form.get('product')
        advert_description = request.form.get('description')
        insert_advert(advert_name, advert_product, advert_description)
        return redirect('/profile')
    return render_template('profile/advertise.html')


def insert_profile(firstname_, surname_, job_id, message):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO PROFILE(name, surname, job_id, message)
        VALUES(%s, %s, %s,%s)
                """, (firstname_, surname_, job_id, message))

        connection.commit()

        return True


def remove_profile(firstname_):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""DELETE FROM PROFILE
        where id = %s""", (firstname_,))
        connection.commit()

        return True


def up_todate_profile(profileid_, newmess_):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""UPDATE PROFILE SET message = %s
                where id = %s""", (newmess_, profileid_))
        connection.commit()

        return True


def insert_advert(advertname_, advertproduct_, advertdescription_):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO ADVERTISERS(advertiser, product, description)
        VALUES(%s, %s, %s)
                """, (advertname_, advertproduct_, advertdescription_))
        connection.commit()

        return True


def get_all_profiles():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT id, name, surname FROM PROFILE;"""
        cursor.execute(query)
        connection.commit()

        return cursor


def list_profiles():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT PROFILE.name, surname, JOBS.job, message FROM
        PROFILE join JOBS on PROFILE.job_id=JOBS.id;"""
        cursor.execute(query)
        connection.commit()

        return cursor


def get_all_jobs():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT id, job FROM JOBS;"""
        cursor.execute(query)
        connection.commit()

        return cursor


def get_all_advertisements():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT advertiser, product, description FROM ADVERTISERS;"""
        cursor.execute(query)
        connection.commit()

        return cursor
