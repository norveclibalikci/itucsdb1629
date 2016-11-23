from flask import Blueprint
from flask import render_template
from flask import  request,url_for
from flask import redirect

from SQL_init import create_user_table
from SQL_init import seed_user_table
from SQL_init import test_user_table
from SQL_init import check_login,create_account,change_password,delete_account



auth = Blueprint('auth', __name__)

def submit():
    if request.method == 'POST':
        return True
    return False


@auth.route("/auth",methods=['GET','POST'])
def main():

    if request.method == 'POST':

            email_var = request.form.get('email')
            pw_var = request.form.get('password')
            if check_login(email_var,pw_var):

                return redirect('/publications')
            else :
                return redirect('/auth')
    return  render_template('login.html')
@auth.route("/create_acc",methods=['GET','POST'])
def create_acc():
    if submit():
        name = request.form.get('name')
        pw = request.form.get('password2')
        mail = request.form.get('email2')
        secret = request.form.get('private')
        create_account(name, pw,mail,secret)
        return redirect('/profile')
    return render_template('create_acc.html')

@auth.route("/change_pw",methods=['GET','POST'])
def change_pw():
    if request.method == 'POST':
            email_var = request.form.get('email2')
            pw_var = request.form.get('password')
            seceret = request.form.get('private')
            change_password(pw_var,seceret,email_var)
            print('?????')
    return render_template('change_pw.html')
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
@auth.route('/delete_acc',methods=['GET','POST'])
def delete_acc():
        if request.method == 'POST':
            email_var = request.form.get('email2')
            pw_var = request.form.get('password')
            seceret = request.form.get('private')
            delete_account(pw_var,email_var,seceret)

        return render_template('delete_acc.html')
@auth.route("/test-user-table")
def testdb():
    count = test_user_table()
    return "number of users in the user table: %d" % count
