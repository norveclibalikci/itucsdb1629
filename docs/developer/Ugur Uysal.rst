Parts Implemented by Uğur Uysal
******************************

Publicaiton table, author table and category table are crated by Ugur Uysal 

.. code-block:: python
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

 
**************************************************



       
