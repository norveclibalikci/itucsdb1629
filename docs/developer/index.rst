Developer Guide
===============

Database Design
---------------

In the project, we wanted to create an efficient database structure while keeping the ability to maintain easily. At first, we thought what features would we need, and with the help of this brainstorming, we listed some of the basic needs of our project. At first, we needed a user entity that holds the related information about the users. After this, we needed our posts and feed relations, which are going to keep the posts and feed positions respectively. After this, we decided we would use a publication structure where some authors could be associated with some publications and follow some others. With these additional features, we thought that it would be useful to add *job postings* and *books for sale* sections. Therefore, we deployed the entities into our system on PostgreSQL. Every main feature is connected to user entity some way, and usually, most of the features are related with the posts, except the seperate features such as *job posting* or *Books for Sale*. We tried to use the convention to show the foreign keys in *snake_case* by using the singuler version of the related table name first and the id second, such as an entity related to user table with the id would have the foreign key *"user_id"*. The following is the E/R diagram of the *Feed* and *Books for Sale* features with additional sub-feature entities and relationships:

.. figure:: http://i63.tinypic.com/ehnrlv.png
   :scale: 50 %
   :alt: Burak - E/R diagram
   
The "feed" and "deleted_feed" entities are connected to the "posts" entity with the "post_id" foreign keys. The "deleted_feed" entity is also related to the users table in order to keep the remover of the post. The books table is also related to the user in order to determine the seller of the book, and the "comments" entity is related to both books and users, in order to keep the owner of the comment and where it belongs to.

Code
----

In the project, we used seperate files for seperate features, and used a seperate file for database initialization called `SQL_init.py`. In this file, we implemented the entity generating queries and methods. On top of the file, we have the following self-explanatory file which creates the entities and seeds them:

.. code-block:: python

    def create_and_seed_database():

       drop_foreign_keys()

       create_user_table()
       seed_user_table()

       create_category_table()
       seed_category_table()

       create_post_table()
       seed_post_table()

       create_profile_table()
       seed_universities_table()

       create_feed_table()
       seed_feed_table()

       create_authors_table()
       seed_authors_table()

       create_publication_table()
       seed_publication_table()

       create_and_test_user_publication_table()

       create_products_table()
       create_comments_table()

       add_foreign_keys()

       return


The code drops the existing foreign key constrains first. After this, it starts constructing the entities one by one. Every developer that wants to create an entity needs to put the methods into this file and append the required queries into the `drop_foreign_keys()` and `add_foreign_keys()` methods in order to successfully create the tables on initialization.

In order to XLarge to start working properly, the `/init-db` route can be used. When this route gets a `GET` request, it immediately executes the method `create_and_seed_database()` and after the execution, it redirects to the home page. After this, all of the required entities will be created properly and all of the functionalities of the XLarge can be used without any problem. 

.. toctree::

   Burak Karakan
   member2
   Ahmet Bilal Can
   Uğur Uysal
   member5
