#!/usr/bin/python3
""" objects that handle all default RestFul API actions for preferences """
from models.preference import Preference
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/preferences', methods=['GET'], strict_slashes=False)
def get_preferences():
    """
    Retrieves the list of all preference objects
    or a specific preference
    """
    all_preferences = storage.all(Preference).values()
    list_preferences = []
    for preference in all_preferences:
        list_preferences.append(preference.to_dict())
    return jsonify(list_preferences)


@app_views.route('/preferences/<preference_id>', methods=['GET'], strict_slashes=False)
def get_preference(preference_id):
    """ Retrieves an preference """
    preference = storage.get(Preference, preference_id)
    if not preference:
        abort(404)

    return jsonify(preference.to_dict())


@app_views.route('/preferences/<preference_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_preference(preference_id):
    """
    Deletes a preference Object
    """

    preference = storage.get(Preference, preference_id)

    if not preference:
        abort(404)

    storage.delete(preference)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/preferences', methods=['POST'], strict_slashes=False)
def post_preference():
    """
    Creates a preference
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Preference(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/preferences/<preference_id>', methods=['PUT'], strict_slashes=False)
def put_preference(preference_id):
    """
    Updates a preference
    """
    preference = storage.get(Preference, preference_id)

    if not preference:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(preference, key, value)
    storage.save()
    return make_response(jsonify(preference.to_dict()), 200)
