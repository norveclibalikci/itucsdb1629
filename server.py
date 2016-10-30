import os
import json
import re
import psycopg2 as dbApi

from flask import Flask
from Feed import feed
from flask import redirect

from Profile import profile
from Publication import publication
from Auth import auth
from Home import home
from Post import post
from SQL_init import create_and_seed_database


app = Flask(__name__)

# Register the blueprints for different team members, in order to minimize the conflicts.
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(feed)
app.register_blueprint(post)
app.register_blueprint(profile)
app.register_blueprint(publication)


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


# The route to initialize all database tables by creating and seeding.
@app.route('/init-db')
def init_db():
    create_and_seed_database()
    return redirect('/')

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                                   host='localhost' port=5432 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)
