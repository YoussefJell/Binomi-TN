"""Authentication views"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.preference import Preference
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import json
import requests
from models import storage
import uuid


auth = Blueprint('auth', __name__)


@auth.route('/login',  strict_slashes=False, methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        found = False
        storage.reload()
        users = storage.all(User)

        current = None
        for user in users.values():
            if user.email == email:
                current = user
                found = True
                break

        if found is False:
            flash('Email Not Found', category='error')

        elif check_password_hash(current.password, password) is False:
            flash('Incorrect Password', category='error')
        else:
            login_user(user, remember=True)
            return render_template('home.html')

    return render_template('login.html')


@auth.route('/logout', strict_slashes=False)
@login_required
def logout():
    logout_user()
    return redirect(url_for('binomi'))


def is_valid_email(api_response_obj):
    data = json.load(api_response_obj)
    is_valid_format, is_free_email, is_disposable_email, is_role_email, is_catchall_email, is_mx_found, is_smtp_valid = api_response_obj.values()

    if is_valid_format and is_mx_found and is_smtp_valid:
        if not is_free_email and not is_disposable_email and not is_role_email and not is_catchall_email:
            return True
        else:
            return False
    return False


def send_email_validation_request(email):
    try:
        response = requests.get(
            "https://emailvalidation.abstractapi.com/v1/?api_key=04a15c06802940afbf096f10e9257b42&email={validated_ip_address}")
        return response.content
    except requests.exceptions.RequestException as api_error:
        raise SystemExit(api_error)


@auth.route('/sign-up', strict_slashes=False, methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        found = False
        users = storage.all(User)

        for user in users.values():
            if user.email == email:
                found = True
                break

        if found:
            flash('Email already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        # elif is_valid_email(send_email_validation_request(email)) is False:
           # flash('Email is invalid', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(
                password1, method='sha256'), first_name=first_name, last_name=last_name)
            new_user.save()
            login_user(new_user, remember=True)

            return redirect(url_for("binomi"))

    return render_template("login.html")


@auth.route('/profile', strict_slashes=False, methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        my_dict = {}
        my_dict["first_name"] = request.form.get('first_name')
        my_dict["last_name"] = request.form.get('last_name')
        my_dict["budget"] = request.form.get('budget')
        my_dict["phone"] = request.form.get('phone')
        my_dict["description"] = request.form.get('bio')
        my_dict["sex"] = request.form.get('sex')
        preferences = request.form.getlist('preferences')
        
        
        my_user = storage.get(User, current_user.get_id())
        for key, value in my_dict.items():
            setattr(my_user, key, value)
        my_user.save()
    
    return render_template('profile.html', method="get", prefs=storage.all(Preference).values())


@auth.route('/modify-profile',  strict_slashes=False)
def modify():
    return render_template('modify.html', cache_id=uuid.uuid4())
