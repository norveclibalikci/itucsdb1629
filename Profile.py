import psycopg2 as dbApi
from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request,url_for
from flask import current_app as app

from SQL_init import test_profile_table

profile = Blueprint('profile', __name__)

@profile.route("/profile")
def main():
    profile = list_profiles()
    return render_template('profile/profile.html', profile=profile)

@profile.route("/test-profile-table")
def testdb():
    count = test_profile_table()
    return "Number of records in the PROFILE table: %d." % count

@profile.route("/add_profile",methods=['GET','POST'])
def add_profile():
    if request.method == 'POST':
        profile_name = request.form.get('first_name')
        profile_surname = request.form.get('surname')
        profile_university = request.form.get('uni_id')
        profile_message = request.form.get('mess')
        insert_profile(profile_name,profile_surname, profile_university, profile_message)
        return redirect('/profile')
    
    else:
        universities = get_all_universities() 
        return render_template('profile/add_profile.html', universities=universities)

@profile.route('/delete_profile',methods=['GET','POST'])
def delete_profile():
        if request.method == 'POST':
            profile_id = request.form.get('profile_id')
            remove_profile(profile_id)
            return redirect("/profile")
        else:
            profiles = get_all_profiles()
            return render_template('profile/delete_profile.html', profiles=profiles)

@profile.route("/update_profile",methods=['GET','POST'])
def update_profile():
    if request.method == 'POST':
            profile_name = request.form.get('first_name')
            new_profile_name = request.form.get('new_first_name')
            up_todate_profile(profile_name,new_profile_name)
            return redirect('/profile')
    return render_template('profile/update_profile.html')


def insert_profile(firstname_, surname_, uni_id, message):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO PROFILE(name, surname, uni_id, message) 
        VALUES(%s, %s, %s,%s)
                """, (firstname_, surname_,uni_id, message))

        connection.commit()

        return True


def remove_profile(firstname_):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""DELETE FROM PROFILE
        where id = %s""", (firstname_,))
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

        query = """SELECT id, name, surname FROM PROFILE;"""
        cursor.execute(query)
        connection.commit()
        
        return cursor


def list_profiles():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT PROFILE.name, surname, UNIVERSITIES.name, country, message FROM 
        PROFILE join UNIVERSITIES on PROFILE.uni_id=UNIVERSITIES.id;"""
        cursor.execute(query)
        connection.commit()
        
        return cursor



def get_all_universities():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT id, name FROM UNIVERSITIES;"""
        cursor.execute(query)
        connection.commit()
        
        return cursor