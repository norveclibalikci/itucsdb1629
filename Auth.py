from flask import Blueprint
from flask import render_template
from flask import request, url_for
from flask import redirect
from flask import current_app as app
from flask_login import UserMixin, login_user, current_user
import psycopg2 as dbApi

from SQL_init import create_user_table
from SQL_init import seed_user_table
from SQL_init import test_user_table
from multiprocessing.managers import public_methods

from flask_login import UserMixin
from flask_login.utils import login_required
from flask_login import logout_user


class User(UserMixin):
    def __init__(self, user):
        self.id = user[0]
        self.name = user[1]
        self.mail = user[2]
        self.active = True
        self.is_admin = False

        if user[0] == 1:
            self.is_admin = True

    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return self.active


def get_user(user_id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""SELECT id, name, mail  FROM USERS
                            where id = %s
                            """, [user_id])
        connection.commit()
        user = cursor.fetchone()
        print("name: " + user[1])
        print("mail: " + user[2])
        user = User(user)

        return user


auth = Blueprint('auth', __name__)


def submit():
    if request.method == 'POST':
        return True
    return False


@auth.route("/auth", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':

        email_var = request.form.get('email')
        pw_var = request.form.get('password')
        if check_login(email_var, pw_var):

            with dbApi.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()

                cursor.execute("""SELECT id, name, mail FROM USERS
                                where %s = mail AND %s = password
                                """, (email_var, pw_var))
                connection.commit()

                user_info = cursor.fetchone()
                user = User(user_info)

                login_user(user)

                return redirect('/user_pubs')
        else:
            return redirect('/auth')
    return render_template('login.html')


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/feed")


@auth.route("/create_acc", methods=['GET', 'POST'])
def create_acc():
    if submit():
        name = request.form.get('name')
        pw = request.form.get('password2')
        mail = request.form.get('email2')
        secret = request.form.get('private')
        create_account(name, pw, mail, secret)
        return redirect('/')
    return render_template('create_acc.html')


@auth.route("/change_pw", methods=['GET', 'POST'])
def change_pw():
    if request.method == 'POST':
        email_var = request.form.get('email2')
        pw_var = request.form.get('password')
        seceret = request.form.get('private')
        change_password(pw_var, seceret, email_var)
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


@auth.route('/delete_acc', methods=['GET', 'POST'])
def delete_acc():
    if request.method == 'POST':
        email_var = request.form.get('email2')
        pw_var = request.form.get('password')
        seceret = request.form.get('private')
        delete_account(pw_var, email_var, seceret)

    return render_template('delete_acc.html')


@auth.route("/test-user-table")
def testdb():
    count = test_user_table()
    return "number of users in the user table: %d" % count


def check_login(mail_address, pw):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""select password from USERS
                        WHERE mail = %s """, (mail_address,))
        connection.commit()
        password = cursor.fetchone()[0]
        print(password, pw)
        if pw == password:
            return True
        else:
            return False


def change_password(new_pw, secret_quest, mail_addres):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""SELECT id FROM USERS
                where %s = mail AND %s = secret
                """, (mail_addres, secret_quest))
        connection.commit()
        user_id_change = cursor.fetchone()[0]

        cursor = connection.cursor()
        if user_id_change:

            cursor.execute("""UPDATE USERS SET password = %s
                    where id = %s   AND mail = %s  """, (new_pw, user_id_change, mail_addres,))

            connection.commit()
            return True
        else:
            return False


def create_account(name_, password_, mail_, secret_):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO USERS (name, password,mail,secret) VALUES(%s,%s,%s,%s)
                """, (name_, password_, mail_, secret_,))

        connection.commit()

        return True


def delete_account(password, mail, secret):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""SELECT id FROM USERS
                where mail = %s  AND secret = %s
                """, (mail, secret))
        connection.commit()
        user_id_delete = cursor.fetchone()[0]

        print(user_id_delete)
        cursor = connection.cursor()
        if user_id_delete:

            cursor.execute("""DELETE FROM USERS where id = %s  """, (user_id_delete,))

            connection.commit()
            return True
        else:
            return False


def get_publications(user_id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT publication_id, publication_title FROM PUBLICATION WHERE publication_id in(
                SELECT publication_id FROM USERSPUBS
                WHERE user_id = %s)
                """ % user_id

        cursor.execute(query)
        connection.commit()

    return cursor


def get_no_publications(user_id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT publication_id, publication_title FROM PUBLICATION WHERE publication_id not in (
                SELECT publication_id FROM USERSPUBS
                WHERE user_id = %s)
                """ % user_id

        cursor.execute(query)
        connection.commit()

    return cursor


@auth.route("/user_pubs/follow", methods=['POST'])
def follow():
    user_id = current_user.id
    publication_id = request.form.get('publication_id')
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO USERSPUBS(user_id,publication_id)
                VALUES(%s,%s)
                """, (user_id, publication_id))
        connection.commit()
    return redirect("/user_pubs")


@auth.route("/user_pubs/unfollow", methods=['POST'])
def unfollow():
    user_id = current_user.id

    publication_id = request.form.get('publication_id')

    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""DELETE FROM USERSPUBS WHERE user_id = %s AND publication_id = %s
                """, (user_id, publication_id))
        connection.commit()

    return redirect("/user_pubs")


@auth.route("/user_pubs")
@login_required
def users_publications():
    print(current_user.id)

    if current_user.is_admin:
        print("hello admin")
    print("in userpub funtion")
    users_publications = get_publications(current_user.id)
    users_not_publications = get_no_publications(current_user.id)
    return render_template('users_pub.html', userspubs=users_publications, notuserpubs=users_not_publications)
