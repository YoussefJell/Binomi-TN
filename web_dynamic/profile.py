#!/usr/bin/python3
import uuid
from flask import Flask, Blueprint, abort, render_template, request, flash, redirect, send_from_directory, url_for
from models.location import Location
from models.preference import Preference, user_preference
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models import storage
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms import SubmitField
profile = Blueprint('profile', __name__)


photos = UploadSet('photos', IMAGES)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileSize(8000000, 0, 'Max file size is 8mb')
        ]
    )
    submit = SubmitField('Upload')


@profile.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory('uploads', filename)


@profile.route('/profile', strict_slashes=False, methods=['GET', 'POST'])
@profile.route('/profile/<uid>', strict_slashes=False, methods=['GET', 'POST'])
def profile_func(uid=None):
    my_user = storage.get(User, request.args.get(
        "uid", current_user.get_id()))
    if not my_user:
        abort(404, 'Invalid Profile, Log in or Click on a User\'s image in the home page')
    form = UploadForm()
    if form.validate_on_submit() and request.form.get('submit') == 'Upload':
        filename = photos.save(form.photo.data)
        file_url = url_for('profile.get_file', filename=filename)
        setattr(my_user, 'image_url', file_url)
        my_user.save()
    else:
        file_url = None
    #----------------#

    if request.method == 'POST' and not request.form.get('submit'):
        my_user = storage.get(User, current_user.get_id())
        my_dict = {}
        my_dict["first_name"] = request.form.get('first_name')
        my_dict["last_name"] = request.form.get('last_name')
        my_dict["budget"] = request.form.get('budget')
        my_dict["phone"] = request.form.get('phone')
        my_dict["description"] = request.form.get('bio')
        my_dict["sex"] = request.form.get('sex')
        my_dict["location_id"] = request.form.get('location')
        curr_loc = storage.get(Location, request.form.get('location'))
        if curr_loc:
            my_dict["location_name"] = curr_loc.name
        preferences = request.form.getlist('preferences')
        dont_delete = ("first_name", "last_name", "sex", "location_id")

        # removing the deselected preferences
        for pref_user in my_user.preferences:
            if pref_user.id not in preferences:
                my_user.preferences.remove(pref_user)
                pref_user.users.remove(my_user)
                pref_user.save()
        # populate the many to many "user_preference" table
        for pref_id in preferences:
            pref_obj = storage.get(Preference, pref_id)
            if pref_obj not in my_user.preferences:
                my_user.preferences.append(pref_obj)
                pref_obj.users.append(my_user)
                pref_obj.save()

        for key, value in my_dict.items():
            if (key in dont_delete) and (len(value) is not 0):
                setattr(my_user, key, value)
        my_user.save()

    locations = storage.all(Location).values()
    locations = sorted(locations, key=lambda k: k.name)

    prefs = storage.all(Preference).values()
    prefs = sorted(prefs, key=lambda k: k.name)

    uid = request.args.get("uid")
    storage.reload()
    return render_template('profile.html', cache_id=uuid.uuid4(), prefs=prefs, locations=locations, uid=uid, user=my_user, current=current_user.get_id(), form=form, file_url=file_url)
