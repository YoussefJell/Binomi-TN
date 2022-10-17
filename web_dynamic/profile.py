#!/usr/bin/python3
from flask import Flask, Blueprint, render_template, request, flash, redirect, send_from_directory, url_for
from models.location import Location
from models.preference import Preference, user_preference
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models import storage
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
profile = Blueprint('profile', __name__)


photos = UploadSet('photos', IMAGES)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed')
        ]
    )
    submit = SubmitField('Upload')


@profile.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory('uploads', filename)


@profile.route('/profile', strict_slashes=False, methods=['GET', 'POST'])
@profile.route('/profile/<uid>', strict_slashes=False, methods=['GET', 'POST'])
def profile_func(uid=None):
    my_user = storage.get(User, request.args.get("uid"))
    form = UploadForm()
    if form.validate_on_submit() and not request.form.get('first_name'):
        filename = photos.save(form.photo.data)
        file_url = url_for('profile.get_file', filename=filename)
        setattr(my_user, 'image_url', file_url)
        my_user.save()
    else:
        file_url = None
    #----------------#

    if request.method == 'POST' and not form.validate_on_submit():
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
            setattr(my_user, key, value)
        my_user.save()

    locations = storage.all(Location).values()
    locations = sorted(locations, key=lambda k: k.name)

    prefs = storage.all(Preference).values()
    prefs = sorted(prefs, key=lambda k: k.name)

    uid = request.args.get("uid")
    storage.reload()
    return render_template('profile.html', prefs=prefs, locations=locations, uid=uid, user=my_user, current=current_user.get_id(), form=form, file_url=file_url)
