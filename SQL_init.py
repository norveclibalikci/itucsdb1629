import psycopg2 as dbApi
from flask import current_app as app


# Create and seed all the database tables.
def create_and_seed_database():
    create_feed_table()
    seed_feed_table()
    return


# Create the feed table with two fields, post_id and number_of_likes.
def create_feed_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS FEED"""
        cursor.execute(query)

        query = """CREATE TABLE FEED (
                post_id INTEGER,
                number_of_likes INTEGER
        )"""
        cursor.execute(query)
        connection.commit()
        return True


# Seed the feed table with 3 random values.
def seed_feed_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                FEED (post_id, number_of_likes)
                VALUES
                    (1, 25),
                    (2, 35),
                    (5, 17)"""
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

