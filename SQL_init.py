import psycopg2 as dbApi
from flask import current_app as app


# Create and seed all the database tables.
def create_and_seed_database():
    create_feed_table()
    seed_feed_table()

    create_profile_table()
    seed_profile_table()

    create_user_table()
    seed_user_table()

    create_publication_table()
    seed_publication_table()

    create_post_table()
    seed_post_table()

    return


# Create the feed table with two fields, post_id and number_of_likes.
def create_feed_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS FEED"""
        cursor.execute(query)

        query = """CREATE TABLE FEED (
                post_id INTEGER,
                post_title VARCHAR(30),
                author VARCHAR(20),
                number_of_likes INTEGER)"""
        cursor.execute(query)
        connection.commit()
        return True


# Seed the feed table with 3 random values.
def seed_feed_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                FEED (post_id, post_title, author, number_of_likes)
                VALUES
                    (1, 'Living in the Edge', 'Joe Doe', 25),
                    (2, 'A Hard Peace', 'Nick Denton', 35),
                    (5, 'Failed Life', 'Jake Holden', 35)"""
        cursor.execute(query)
        connection.commit()
        return True


# Test the feed table of 3 random values.
def test_feed_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(*) FROM FEED;"""
        cursor.execute(query)
        connection.commit()

        count = cursor.fetchone()[0]
        return count


# Create the profile table with two fields, profile_id, name and surname.
def create_profile_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS PROFILE"""
        cursor.execute(query)
        query = """CREATE TABLE PROFILE (
                profile_id INTEGER,
                name VARCHAR(20),
                surname VARCHAR(20)
        )"""

        cursor.execute(query)
        connection.commit()

        return True


# Seed the profile table with 2 random values.
def seed_profile_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                PROFILE (profile_id, name, surname)
                VALUES
                    (1, 'Sara', 'Benincasa'),
                    (2, 'Chirantha', 'Premathilaka')"""

        cursor.execute(query)
        connection.commit()

        return True


# Test the profile table of 2 random values.
def test_profile_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(*) FROM PROFILE;"""

        cursor.execute(query)
        connection.commit()
        count = cursor.fetchone()[0]

        return count

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
        new_profile_id = last_profile_id+1
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO PROFILE VALUES(%s,%s,%s)
                """ ,(new_profile_id,firstname_,surname_,))

        connection.commit()

        return True

def remove_profile(firstname_):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""DELETE FROM PROFILE
        where name = '%s'""",(firstname_,))
        connection.commit()

        return True

def up_todate_profile(firstname_, newfirstname_):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""UPDATE PROFILE SET name = %s
                where name = %s""",(newfirstname_, firstname_,))
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


def create_user_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS user_"""
        cursor.execute(query)
        query = """CREATE TABLE user_ (
                user_id INTEGER,
                password VARCHAR(40),
                mail VARCHAR(40),
                secret VARCHAR(40)
        )"""

        cursor.execute(query)
        connection.commit()

        return True


def seed_user_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                user_ (user_id, password,mail,secret)
                VALUES
                    (1, 'badpassword','abc@gmail.com','mom1'),
                    (2, 'g00d!p455W0rd*','def@gmail.com','mom2'),
                    (3, 'onemorebadpassword','xyz@gmail.com','mom3')"""

        cursor.execute(query)
        connection.commit()

        return True


def test_user_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(*) FROM user_;"""

        cursor.execute(query)
        connection.commit()
        count = cursor.fetchone()[0]

        return count


def check_login(mail_address, pw):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""select password from user_
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

        cursor.execute("""SELECT user_id FROM user_
                where %s = mail AND %s = secret
                """, (mail_addres, secret_quest))
        connection.commit()
        user_id_change = cursor.fetchone()[0]

        cursor = connection.cursor()
        if user_id_change:

            cursor.execute("""UPDATE user_ SET password = %s
                    where user_id = %s   AND mail = %s  """, (new_pw, user_id_change, mail_addres,))

            connection.commit()
            return True
        else:
            return False


def create_account(password_, mail_, secret_):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT * from user_
                ORDER BY user_id
                DESC
                """

        cursor.execute(query)
        connection.commit()
        last_user_id = cursor.fetchone()[0]
        print(last_user_id)
        new_id = last_user_id + 1
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO user_ VALUES(%s,%s,%s,%s)
                """, (new_id, password_, mail_, secret_,))

        connection.commit()

        return True


def delete_account(password, mail, secret):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("""SELECT user_id FROM user_
                where mail = %s  AND secret = %s
                """, (mail, secret))
        connection.commit()
        user_id_delete = cursor.fetchone()[0]

        print(user_id_delete)
        cursor = connection.cursor()
        if user_id_delete:

            cursor.execute("""DELETE FROM user_ where user_id = %s  """, (user_id_delete,))

            connection.commit()
            return True
        else:
            return False


# Create the publication table  with 2 fields, publication_title, publisher , publication_id
def create_publication_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS PUBLICATION"""
        cursor.execute(query)
        query = """CREATE TABLE PUBLICATION (
                publication_id INTEGER,
                publication_title VARCHAR(40),
                publisher VARCHAR(20))"""

        try:
            cursor.execute(query)
        except:
            return False;
        connection.commit()

        return True


# Seed the publication table with 2 publications.
def seed_publication_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                PUBLICATION (publication_id,  publication_title, publisher)
                VALUES
                    (1,'IoT', 'IEEE'),
                    (2,'AI','Science')"""
        try:
            cursor.execute(query)
        except:
            return False
        connection.commit()

        return True


# Test the publication table
def test_publication_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(*) FROM PUBLICATION;"""

        cursor.execute(query)
        connection.commit()
        count = cursor.fetchone()[0]

        return count


# Create the post table with three variables, post_id, profile_id and category_id
def create_post_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS POST"""
        cursor.execute(query)

        query = """CREATE TABLE POST (
                post_id INTEGER,
                profile_id INTEGER,
                category_id INTEGER
        )"""
        cursor.execute(query)
        connection.commit()
        return True


# Seed the post table with 3 random values.
def seed_post_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                POST (post_id, profile_id, category_id)
                VALUES
                    (1, 22, 3),
                    (5, 41, 1),
                    (7, 71, 2)"""
        cursor.execute(query)
        connection.commit()
        return True


# Testing the post table of 3 random values.
def test_post_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(*) FROM POST;"""
        cursor.execute(query)
        connection.commit()

        count = cursor.fetchone()[0]
        return count


def get_all_feed():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT post_id, post_title, author FROM FEED;"""
        cursor.execute(query)
        connection.commit()
        return cursor


def create_feed_post(post_id, post_title, post_author, post_likes):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO FEED (post_id, post_title, author, number_of_likes) VALUES(%s,'%s','%s',%s)""" % (
            post_id, post_title, post_author, post_likes)

        cursor.execute(query)
        connection.commit()

        return True


def get_feed_post_with_id(id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT * FROM FEED WHERE post_id = %s;""" % id

        cursor.execute(query)
        connection.commit()

        return cursor


def update_feed_post(id, title, author, likes):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """UPDATE FEED
        SET post_id=%s, post_title='%s', author='%s', number_of_likes=%s
        WHERE post_id = %s;""" % (id, title, author, likes, id)
        cursor.execute(query)
        connection.commit()

        return True


def delete_feed_post(id):
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DELETE FROM FEED
        WHERE post_id = %s;""" % id
        cursor.execute(query)
        connection.commit()

        return True
