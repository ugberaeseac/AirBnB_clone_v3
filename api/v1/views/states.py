#!/usr/bin/python3
"""Import required modules"""
from flask import Flask, make_response
from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from os import getenv
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_list_of_all_states():
    """Retrieves the list of all State objects"""
    from models import storage
    storage.reload
    states_obj = storage.all(State).values()
    states_dict = [state.to_dict() for state in states_obj]
    return jsonify(states_dict)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_obj(state_id):
    """Retrieves a State object"""
    from models import storage
    storage.reload
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_ob(state_id):
    """Deletes a State object"""
    from models import storage
    storage.reload
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    data = request.get_json()
    new_state = State(**data)
    from models import storage
    new_state.save()
    return (new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    data = request.get_json()
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    from models import storage
    state = storage.get(State, state_id)
    if state:
        state.name = data['name']
        state.save()
        return (state.to_dict())
    abort(404)  # If no matching state is found, return a 404 error
