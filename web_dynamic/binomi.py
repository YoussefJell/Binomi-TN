#!/usr/bin/python3
""" Starts a Flash Web Application """
from models.user import User
from models.preference import Preference
from models import storage
from os import environ
import uuid
from flask import Flask, render_template
from web_dynamic.auth import auth

app = Flask(__name__)
#secret key for the app, it encrypts cookies
app.config['SECRET_KEY'] = 'dasd13 dream team 12fqwt'

# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True
app.register_blueprint(auth, url_prefix='/')


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
def binomi():
    """ Binomi is alive! """
    #users = storage.all(User).values()
    #users = sorted(users, key=lambda k: k.name)
    #st_ct = []

    #for user in users:
    #    st_ct.append([user, sorted(user.preferences, key=lambda k: k.name)])

    #preferences = storage.all(Preference).values()
    #preferences = sorted(preferences, key=lambda k: k.name)

    return render_template('home.html', cache_id=uuid.uuid4())


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
