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


# Create the profile table with two fields, profile_id, name and surname.
def create_profile_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DROP TABLE IF EXISTS PROFILE"""
        cursor.execute(query)
        query = """CREATE TABLE PROFILE (
                profile_id INTEGER,
                name_surname VARCHAR(40)
        )"""
        
        cursor.execute(query)
        connection.commit()
        
        return True
    
# Seed the profile table with 2 random values.
def seed_profile_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                PROFILE (profile_id, name_surname)
                VALUES
                    (1, 'Sara Benincasa'),
                    (2, 'Chirantha Premathilaka')"""
                    
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

        query = """DROP TABLE IF EXISTS USER"""
        cursor.execute(query)
        query = """CREATE TABLE USER (
                user_id INTEGER,
                password VARCHAR(40)
        )"""

        cursor.execute(query)
        connection.commit()

        return True
def seed_user_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO
                USER (user_id, password)
                VALUES
                    (1, 'badpassword'),
                    (2, 'g00d!p455W0rd*'),
                    (3, 'onemorebadpassword')"""

        cursor.execute(query)
        connection.commit()

        return True
def test_user_table():
    with dbApi.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT COUNT(*) FROM USER;"""

        cursor.execute(query)
        connection.commit()
        count = cursor.fetchone()[0]

        return count

    
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
    
    
    
 #Creating post table with three fields, post_id, profile_id, category_id
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
	connection.execute(query)
	connection.commit()
	return True

#Seed the post table with 3 random values
def seed_post_table():
	with dbApi.connection(app.config['dsn']) as connection:
			cursor = connection.cursor()


			query= """INSERT INTO
					POST (post_id, profile_id, category_id)
					VALUES
					(1,22,3),
					(4,11,2),
					(3,33,1)"""
			cursor.execute(query)
			connection.commit()
	return True
#Testing post table with 3 random values
def test_post_table():
	with dbApi.connect(app.config['dsn']) as connection:
		cursor= connection.cursor()

		query= """SELECT COUNT(*) FROM POST;"""

		cursor.execute(query)

		connection.commit()

		count=cursor.fetchone()[0]
		return count
    
