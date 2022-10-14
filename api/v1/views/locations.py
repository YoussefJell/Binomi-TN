#!/usr/bin/python3
""" objects that handle all default RestFul API actions for locations """
from models.location import Location
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/locations', methods=['GET'], strict_slashes=False)
def get_locations():
    """
    Retrieves the list of all location objects
    or a specific location
    """
    all_locations = storage.all(Location).values()
    list_locations = []
    for location in all_locations:
        list_locations.append(location.to_dict())
    return jsonify(list_locations)


@app_views.route('/locations/<location_id>', methods=['GET'], strict_slashes=False)
def get_location(location_id):
    """ Retrieves an location """
    location = storage.get(Location, location_id)
    if not location:
        abort(404)

    return jsonify(location.to_dict())


@app_views.route('/locations/<location_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_location(location_id):
    """
    Deletes a location Object
    """

    location = storage.get(Location, location_id)

    if not location:
        abort(404)

    storage.delete(location)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/locations', methods=['POST'], strict_slashes=False)
def post_location():
    """
    Creates a location
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Location(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/locations/<location_id>', methods=['PUT'], strict_slashes=False)
def put_location(location_id):
    """
    Updates a location
    """
    location = storage.get(Location, location_id)

    if not location:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(location, key, value)
    storage.save()
    return make_response(jsonify(location.to_dict()), 200)
