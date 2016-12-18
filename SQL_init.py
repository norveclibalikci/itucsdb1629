import psycopg2 as dbApi
from flask import current_app as app
from passlib.apps import custom_app_context as pwd_context

# Create and seed all the database tables.
def create_and_seed_database():
    drop_foreign_keys()

    create_user_table()
    seed_user_table()

    create_category_table()
    seed_category_table()

    create_post_table()
    seed_post_table()

    create_profile_table()
    seed_jobs_table()

    create_feed_table()
    seed_feed_table()
    
    create_pubcategory_table()
    seed_pubcategory_table()
    
    create_authors_table()
    seed_authors_table()

    create_publication_table()
    seed_publication_table()

    create_and_test_user_publication_table()

    create_products_table()
    create_comments_table()
    create_jobs_table()
    add_foreign_keys()

    return


def drop_foreign_keys():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ALTER TABLE IF EXISTS PROFILE DROP CONSTRAINT IF EXISTS profile_job_id_fkey;"""
        cursor.execute(query)
        query = """ALTER TABLE IF EXISTS FEED DROP CONSTRAINT IF EXISTS feed_post_id_fkey;"""
        cursor.execute(query)
        query = """ALTER TABLE IF EXISTS DELETED_FEED DROP CONSTRAINT IF EXISTS deleted_feed_remover_id_fkey;"""
        cursor.execute(query)
        query = """ALTER TABLE IF EXISTS DELETED_FEED DROP CONSTRAINT IF EXISTS deleted_feed_post_id_fkey;"""
        cursor.execute(query)
        query = """ALTER TABLE IF EXISTS PUBLICATION DROP CONSTRAINT IF EXISTS publication_author_id_fkey;"""
        cursor.execute(query)
        query = """ALTER TABLE IF EXISTS POSTS DROP CONSTRAINT IF EXISTS posts_category_id_fkey;"""
        cursor.execute(query)
        query = """ALTER TABLE IF EXISTS USERSPUBS DROP CONSTRAINT IF EXISTS userpubs_user_id_fkey;"""
        cursor.execute(query)
        query = """ALTER TABLE IF EXISTS USERSPUBS DROP CONSTRAINT IF EXISTS userpubs_publication_id_fkey;"""
        cursor.execute(query)
        query = """ALTER TABLE IF EXISTS BOOKS DROP CONSTRAINT IF EXISTS products_user_id_fkey;"""
        cursor.execute(query)
        query = """ALTER TABLE IF EXISTS COMMENTS DROP CONSTRAINT IF EXISTS comments_user_id_fkey;"""
        cursor.execute(query)
        query = """ALTER TABLE IF EXISTS COMMENTS DROP CONSTRAINT IF EXISTS comments_book_id_fkey;"""
        cursor.execute(query)
        query = """ALTER TABLE IF EXISTS PUBLICATION DROP CONSTRAINT IF EXISTS publication_category_id_fkey;"""
        cursor.execute(query)

        connection.commit()


def add_foreign_keys():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ALTER TABLE PROFILE ADD FOREIGN KEY (job_id) REFERENCES JOBS(id);"""
        cursor.execute(query)
        query = """ALTER TABLE FEED ADD FOREIGN KEY (post_id) REFERENCES POSTS(post_id) ON DELETE CASCADE;"""
        cursor.execute(query)
        query = """ALTER TABLE DELETED_FEED ADD FOREIGN KEY (post_id) REFERENCES POSTS(post_id) ON DELETE CASCADE;"""
        cursor.execute(query)
        query = """ALTER TABLE DELETED_FEED ADD FOREIGN KEY (remover_id) REFERENCES USERS(id) ON DELETE CASCADE;"""
        cursor.execute(query)
        query = """ALTER TABLE PUBLICATION ADD FOREIGN KEY (author_id) REFERENCES AUTHORS(author_id) ON DELETE CASCADE;"""
        cursor.execute(query)
        query = """ALTER TABLE POSTS ADD FOREIGN KEY (category_id) REFERENCES CATEGORIES(category_id) ON DELETE CASCADE;"""
        cursor.execute(query)
        query = """ALTER TABLE USERSPUBS ADD FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE CASCADE;"""
        cursor.execute(query)
        query = """ALTER TABLE USERSPUBS ADD FOREIGN KEY (publication_id) REFERENCES PUBLICATION(publication_id) ON DELETE CASCADE;"""
        cursor.execute(query)
        query = """ALTER TABLE BOOKS ADD FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE CASCADE;"""
        cursor.execute(query)
        query = """ALTER TABLE COMMENTS ADD FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE CASCADE;"""
        cursor.execute(query)
        query = """ALTER TABLE COMMENTS ADD FOREIGN KEY (book_id) REFERENCES BOOKS(id) ON DELETE CASCADE;"""
        cursor.execute(query)
        query = """ALTER TABLE PUBLICATION ADD FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE;"""
        cursor.execute(query)

        connection.commit()


# Create the feed table with two fields, post_id and number_of_likes.
def create_feed_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS FEED"""
        cursor.execute(query)

        query = """CREATE TABLE FEED (
                feed_id SERIAL PRIMARY KEY,
                post_id INTEGER,
                publication_id INTEGER,
                number_of_likes INTEGER,
                created_at TIMESTAMP)"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS DELETED_FEED"""
        cursor.execute(query)

        query = """CREATE TABLE DELETED_FEED (
                id SERIAL PRIMARY KEY,
                remover_id INTEGER,
                post_id INTEGER,
                publication_id INTEGER,
                number_of_likes INTEGER)"""
        cursor.execute(query)

        connection.commit()
        return True


def create_comments_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS COMMENTS"""
        cursor.execute(query)

        query = """CREATE TABLE COMMENTS (
                id SERIAL PRIMARY KEY,
                book_id INTEGER,
                user_id INTEGER,
                comment VARCHAR(255))"""
        cursor.execute(query)
        connection.commit()
        return True
def create_jobs_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """ DROP TABLE IF EXISTS JOBS"""
        cursor.execute(query)
        query ="""CREATE TABLE JOBS ( 
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                job_title VARCHAR(255),
                description VARCHAR(255),
                location VARCHAR(255),
                salary NUMERIC,
                is_remote BOOLEAN)
                """
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


# Create the feed table with two fields, post_id and number_of_likes.
def create_products_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS BOOKS"""
        cursor.execute(query)

        query = """CREATE TABLE BOOKS (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                title VARCHAR(255),
                description VARCHAR(255),
                author VARCHAR (255),
                price NUMERIC,
                is_used BOOLEAN,
                created_at TIMESTAMP)"""
        cursor.execute(query)

        connection.commit()
        return True


# Create the profile and jobs tables.
def create_profile_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS JOBS"""
        cursor.execute(query)
        query = """CREATE TABLE JOBS (id SERIAL PRIMARY KEY,job VARCHAR(50))"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS PROFILE"""
        cursor.execute(query)
        query = """CREATE TABLE PROFILE (
                id SERIAL PRIMARY KEY,
                name VARCHAR(20),
                surname VARCHAR(20),
                job_id INTEGER,
                message VARCHAR(80)
        )"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS ADVERTISERS"""
        cursor.execute(query)
        query = """CREATE TABLE ADVERTISERS (
                advertiser VARCHAR(20),
                product VARCHAR(20),
                description VARCHAR(120)
        )"""
        cursor.execute(query)
        connection.commit()

        return True


# Seed the jobs table.
def seed_jobs_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                JOBS (id, job)
                VALUES
                    (1, 'Accountant'),
                    (2, 'Architect'),
                    (3, 'Chef'),
                    (4, 'Computer Programmer'),
                    (5, 'Director'),
                    (6, 'Engineer'),
                    (7, 'Lawyer'),
                    (8, 'Student'),
                    (9, 'Teacher'),
                    (10, 'Teacher Assistant')"""
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

        query = """DROP TABLE IF EXISTS USERS CASCADE"""
        cursor.execute(query)
        query = """CREATE TABLE USERS (
                id SERIAL PRIMARY KEY,
                name VARCHAR(40),
                password CHAR(120),
                mail VARCHAR(40),
                secret VARCHAR(40)
        )"""

        cursor.execute(query)
        connection.commit()

        return True


def seed_user_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        hashed_admin = pwd_context.encrypt('admin')
        hashed_1 = pwd_context.encrypt('badpassword')
        hashed_2= pwd_context.encrypt('g00d!p455W0rd*')
        hashed_3 = pwd_context.encrypt('onemorebadpassword')
        print(hashed_admin)
        query = """INSERT INTO
                USERS (name, password,mail,secret)
                VALUES
                    ('admin','%s','admin@admin.com','admin'),
                    ('John Doe','%s','abc@gmail.com','mom1'),
                    ('Jack Doe', '%s','def@gmail.com','mom2'),
                    ('Jamie Doe', '%s','xyz@gmail.com','mom3')
                     """ % (hashed_admin,hashed_1,hashed_2,hashed_3)

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


def create_pubcategory_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS category"""
        cursor.execute(query)
        query = """CREATE TABLE category (
                category_id SERIAL PRIMARY KEY,
                category_name VARCHAR(20) UNIQUE)"""
        try:
            cursor.execute(query)
        except:
            return False;
        connection.commit()

        return True
    
def seed_pubcategory_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                category (category_name)
                VALUES
                    ('Science'),
                    ('Sports'),
                    ('Health'),
                    ('Economy'),
                    ('Technology'),
                    ('Literature')"""
        try:
            cursor.execute(query)
        except:
            return False
        connection.commit()

        return True
    
def create_publication_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS PUBLICATION CASCADE"""
        cursor.execute(query)
        query = """CREATE TABLE PUBLICATION (
                publication_id SERIAL PRIMARY KEY,
                publication_title VARCHAR(40),
                publisher VARCHAR(20),
                author_id INTEGER,
                category_id INTEGER)"""

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
                PUBLICATION (publication_title, publisher, author_id, category_id)
                VALUES
                    ('IoT', 'IEEE Spectrum',1,5),
                    ('AI','Science',2,1),
                    ('Six pack','Mans Health',4,2),
                    ('Poems', 'Best Poems', 3, 6),
                    ('Cancer', 'Your Life', 4, 3)"""
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


def create_category_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS CATEGORIES CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE CATEGORIES (
                category_id SERIAL PRIMARY KEY,
                category_name VARCHAR(40)  UNIQUE,
                related_category VARCHAR(40)
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
                    (1, 1, 'First Post', 'Post 1 is about something that is unique to the post 1.'),
                    (2, 2, 'Second Post', 'Post 2 is about something that is unique to the post 2.'),
                    (3, 3, 'Third Post', 'Post 3 is about something that is unique to the post 3.')"""
        cursor.execute(query)
        connection.commit()
        return True


def seed_category_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """INSERT INTO
                CATEGORIES (category_name, related_category)
                VALUES
                    ('Artifical Intelligence', 'Machine Learning'),
                    ('IoT', 'Computer Networks'),
                    ('Cyber Security', 'Computer Networks')"""
        cursor.execute(query)
        connection.commit()
        return True


def test_post_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(*) FROM POSTS;"""
        cursor.execute(query)
        connection.commit()

        count = cursor.fetchone()[0]
        return count


def create_and_test_user_publication_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS USERSPUBS CASCADE """
        cursor.execute(query)
        query = """CREATE TABLE USERSPUBS (
                 user_id INTEGER,
                 publication_id INTEGER
                )"""

        cursor.execute(query)
        connection.commit()

        query = """INSERT INTO
                USERSPUBS (user_id,publication_id)
                VALUES
                ('1','2'),
                ('1','1'),
                ('2','1')
                    """

        cursor.execute(query)
        connection.commit()

        return "okay"
