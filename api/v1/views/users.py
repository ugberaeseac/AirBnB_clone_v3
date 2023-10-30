#!/usr/bin/python3
"""Import required modules"""
from flask import Flask, make_response
from flask import abort, jsonify, request
from models.user import User
from os import getenv
import json


app = Flask(__name__)


host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')

@app.route('/api/v1/users', methods=['GET'], strict_slashes=False)
def get_list_of_all_states():
    """Retrieves the list of all State objects"""
    from models import storage
    storage.reload
    users_obj = storage.all(User).values()
    users_dict = [user.to_dict() for user in users_obj]
    return jsonify(users_dict)


@app.route('/api/v1/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_state_obj(user_id):
    """Retrieves a State object"""
    from models import storage
    storage.reload
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app.route('/api/v1/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_ob(user_id):
    """Deletes a State object"""
    from models import storage
    storage.reload
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app.route('/api/v1/users', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    try:
        data = request.get_json()
    except Exception:
        return jsonify("Not a JSON"), 400
    if 'email' not in data:
        return jsonify("Missing email"), 400
    if 'password' not in data:
        return jsonify("Missing password"), 400
    new_user = User(**data)
    from models import storage
    new_user.save()
    return (new_user.to_dict()), 201


@app.route('/api/v1/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_state(user_id):
    """Updates a State object"""
    try:
        data = request.get_json()
    except Exception:
        return jsonify({'Not a JSON'}), 400

    from models import storage
    user = storage.get(User, user_id)
    if user:
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return (user.to_dict())
    abort(404)  # If no matching state is found, return a 404 error


if __name__ == "__main__":
    app.run(host=host, port=port)