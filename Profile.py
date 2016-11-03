from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import  request,url_for
from SQL_init import insert_profile, remove_profile, up_todate_profile, get_all_profiles
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