from flask import Blueprint
from flask import render_template
from SQL_init import create_publication_table
from SQL_init import seed_publication_table
from SQL_init import test_publication_table

publication = Blueprint('publication', __name__)


@publication.route("/publications")
def main():
   return render_template('publications.html')


@publication.route("/create-publication-table")
def create_table():
    var = create_publication_table()
    if var:
        return redirect('/publications')
    else:
        return "Mission Failed: CREATE PUBLICATION TABLE"

@publication.route("/seed-publication-table")
def seed_table():
    var = seed_publication_table()
    if var:
        return redirect('/publications')
    else: 
        return "Mission Failed: SEED PUBLICATION TABLE"


@publication.route("/test-publication-table")
def test_table():
    count  = test_publication_table() 
    return "Number of records in the Publication table: %d." % count
    
@publication.route("/create-and-seed-publication-table")
def create_and_seed():
    create_publication_table()
    seed_publication_table()
    return redirect('/publications')
