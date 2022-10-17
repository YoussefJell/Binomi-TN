#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.location import Location
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a user Object
    """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    Updates a user
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/users/<user_id>/preferences', methods=['GET'], strict_slashes=False)
def get_user_preference(user_id):
    """
    Updates a user
    """
    list_preferences = []
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for pref in user.preferences:
        list_preferences.append(pref.to_dict())

    return jsonify(list_preferences)


@app_views.route('/users/<user_id>/location', methods=['GET'], strict_slashes=False)
def get_user_location(user_id):
    """
    Updates a user
    """
    user = storage.get(User, user_id)
    location = storage.get(Location, user.location_id)
    if not user:
        abort(404)
    if not location:
        abort(404)

    return jsonify(location.to_dict())


@app_views.route('/users_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        locations = data.get('locations', None)

    if not data or not len(data) or (not locations):
        users = storage.all(User).values()
        list_users = []
        for user in users:
            list_users.append(user.to_dict())
        return jsonify(list_users)

    list_users = []
    if locations:
        users = storage.all(User).values()
        for user in users:
            if user.location_id in locations:
                list_users.append(user)

    users = []
    for usr in list_users:
        tmp = usr.to_dict()
        users.append(tmp)

    return jsonify(users)
