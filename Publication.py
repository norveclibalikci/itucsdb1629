from flask import Blueprint

publication = Blueprint('publication', __name__)


@publication.route("/publications")
def main():
    return "here comes the publications page."
