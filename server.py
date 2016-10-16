import datetime
import os

from flask import Flask
from Feed import user_feed
from Profile import profile
from Publication import publication
from Auth import auth
from Home import home
from Post import post


app = Flask(__name__)

# Register the blueprints for different team members, in order to minimize the conflicts.
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(user_feed)
app.register_blueprint(post)
app.register_blueprint(profile)
app.register_blueprint(publication)


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
