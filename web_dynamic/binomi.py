#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask_uploads import configure_uploads
from models.location import Location
from models.user import User
from models.preference import Preference
from models import storage
from os import environ
import uuid
from flask import Flask, render_template, send_from_directory, url_for
from web_dynamic.auth import auth
from web_dynamic.profile import photos
from flask_login import LoginManager
from web_dynamic.profile import profile

app = Flask(__name__)
# secret key for the app, it encrypts cookies
app.config['SECRET_KEY'] = 'dasd13 dream team 12fqwt'
app.config['UPLOADED_PHOTOS_DEST'] = 'web_dynamic/uploads'
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(profile, url_prefix='/')

configure_uploads(app, photos)


login_manager = LoginManager()
login_manager.login_view = 'binomi'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return storage.get(User, id)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False, methods=["GET", "POST"])
def binomi():
    """ Binomi is alive! """
    #users = storage.all(User).values()
    #users = sorted(users, key=lambda k: k.name)
    #st_ct = []

    # for user in users:
    #    st_ct.append([user, sorted(user.preferences, key=lambda k: k.name)])

    locations = storage.all(Location).values()
    locations = sorted(locations, key=lambda k: k.name)

    return render_template('home.html', cache_id=uuid.uuid4(), locations=locations)


if __name__ == "__main__":
    """ Main Function """

    app.run(host='0.0.0.0', port=5000)
