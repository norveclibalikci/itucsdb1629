import psycopg2 as dbApi
from flask import current_app as app


# Create and seed all the database tables.
def create_and_seed_database():
    
    create_user_table()
    seed_user_table()

    create_post_table()
    seed_post_table()

    create_profile_table()
    seed_profile_table()

    create_feed_table()
    seed_feed_table()
    
    create_authors_table()
    seed_authors_table()
    
    create_publication_table()
    seed_publication_table()
    
    return


# Create the feed table with two fields, post_id and number_of_likes.
def create_feed_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS FEED"""
        cursor.execute(query)

        query = """CREATE TABLE FEED (
                feed_id SERIAL PRIMARY KEY,
                post_id INTEGER REFERENCES POSTS ON DELETE CASCADE,
                publication_id INTEGER,
                number_of_likes INTEGER,
                created_at TIMESTAMP)"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS DELETED_FEED"""
        cursor.execute(query)

        query = """CREATE TABLE DELETED_FEED (
                feed_id SERIAL PRIMARY KEY,
                post_id INTEGER,
                publication_id INTEGER,
                number_of_likes INTEGER,
                deleted_at TIMESTAMP)"""
        cursor.execute(query)

        connection.commit()
        return True


# Seed the feed table with 3 random values.
def seed_feed_table():
    with dbApi.connect(app.config['dsn']) as connection:
        # cursor = connection.cursor()

        #        query = """INSERT INTO FEED (post_id, post_title, author, number_of_likes)
        #             VALUES
        #                ('Living in the Edge', 'Joe Doe', 25),
        #               ('A Hard Peace', 'Nick Denton', 35),
        #              ('Failed Life', 'Jake Holden', 35)"""
        #   cursor.execute(query)
        #  connection.commit()
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


def create_user_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS USERS"""
        cursor.execute(query)
        query = """CREATE TABLE USERS (
                id SERIAL PRIMARY KEY,
                name VARCHAR(40),
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
                USERS (name, password,mail,secret)
                VALUES
                    ('John Doe', 'badpassword','abc@gmail.com','mom1'),
                    ('Jack Doe', 'g00d!p455W0rd*','def@gmail.com','mom2'),
                    ('Jamie Doe', 'onemorebadpassword','xyz@gmail.com','mom3')"""

        cursor.execute(query)
        connection.commit()

        return True


def test_user_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(*) FROM USERS;"""

        cursor.execute(query)
        connection.commit()
        count = cursor.fetchone()[0]

        return count


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

        cursor.execute("""SELECT user_id FROM USERS
                where %s = mail AND %s = secret
                """, (mail_addres, secret_quest))
        connection.commit()
        user_id_change = cursor.fetchone()[0]

        cursor = connection.cursor()
        if user_id_change:

            cursor.execute("""UPDATE USERS SET password = %s
                    where user_id = %s   AND mail = %s  """, (new_pw, user_id_change, mail_addres,))

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

        cursor.execute("""SELECT user_id FROM USERS
                where mail = %s  AND secret = %s
                """, (mail, secret))
        connection.commit()
        user_id_delete = cursor.fetchone()[0]

        print(user_id_delete)
        cursor = connection.cursor()
        if user_id_delete:

            cursor.execute("""DELETE FROM USERS where user_id = %s  """, (user_id_delete,))

            connection.commit()
            return True
        else:
            return False



def create_publication_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS PUBLICATION"""
        cursor.execute(query)
        query = """CREATE TABLE PUBLICATION (
                publication_id SERIAL PRIMARY KEY,
                publication_title VARCHAR(40),
                publisher VARCHAR(20),
                author_id INTEGER REFERENCES AUTHORS ON DELETE CASCADE)"""
                
        try:
            cursor.execute(query)
        except:
            return False;
        connection.commit()

        return True


def seed_publication_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                PUBLICATION (publication_title, publisher, author_id)
                VALUES
                    ('IoT', 'IEEE',1),
                    ('AI','Science',2)"""
        try:
            cursor.execute(query)
        except:
            return False
        connection.commit()

        return True



def test_publication_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(*) FROM PUBLICATION;"""

        cursor.execute(query)
        connection.commit()
        count = cursor.fetchone()[0]

        return count


def create_authors_table():
     with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """DROP TABLE IF EXISTS AUTHORS CASCADE"""
        cursor.execute(query)
        query = """CREATE TABLE AUTHORS (
                author_id SERIAL PRIMARY KEY,
                author_name VARCHAR(20) UNIQUE)"""

        try:
            cursor.execute(query)
        except:
            return False;
        connection.commit()

        return True

def seed_authors_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                AUTHORS (author_name)
                VALUES
                    ('Ali'),
                    ('Veli'),
                    ('Mehmet'),
                    ('Samuel')"""
        try:
            cursor.execute(query)
        except:
            return False
        connection.commit()
        
        return True

# Create the post table with four variables, post_id, profile_id, category_id and content
def create_post_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS POSTS"""
        cursor.execute(query)

        query = """CREATE TABLE POSTS (
                post_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                category_id INTEGER,
                title VARCHAR(50),
                content VARCHAR(250)    
        )"""
        cursor.execute(query)
        connection.commit()
        return True


# Seed the post table with 3 random values.
def seed_post_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                POSTS (user_id, category_id, title, content)
                VALUES
                    (1, 3, 'First Post', 'Post 1 is about something that is unique to the post 1.'),
                    (1, 1, 'Second Post', 'Post 2 is about something that is unique to the post 2.'),
                    (2, 2, 'Third Post', 'Post 3 is about something that is unique to the post 3.')"""
        cursor.execute(query)
        connection.commit()
        return True


# Testing the post table of 3 random values.
def test_post_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(*) FROM POSTS;"""
        cursor.execute(query)
        connection.commit()

        count = cursor.fetchone()[0]
        return count
