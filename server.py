import datetime
import os

from flask import Flask
from flask import render_template
from Feed import user_feed

app = Flask(__name__)

app.register_blueprint(user_feed)

@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
