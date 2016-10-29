from flask import Blueprint
from flask import render_template

publication = Blueprint('publication', __name__)


@publication.route("/publications")
def main():
   return render_template('publications.html')