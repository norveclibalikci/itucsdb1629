Parts Implemented by Burak Karakan
================================

Feed
----

The Feed is actually one of the most important parts of the user experience in XLarge. The Feed is a simple entity that connects some existing posts to the feed by referencing them with their ID. Also, a user seeing the post on the Feed page can upvote it, and in order to keep the likes counter, the `feed` entity is used again. An admin can delete posts from Feed, and in order to keep track of these deleted posts, there is the `deleted_feed` entity. This entity holds the removed feed posts by the remover user ID, and is connected to the posts by the post ID. The E/R diagram of the feed structure is as follows:

.. figure:: http://i67.tinypic.com/drba13.png
   :scale: 50 %
   :alt: Feed E/R diagram
   


