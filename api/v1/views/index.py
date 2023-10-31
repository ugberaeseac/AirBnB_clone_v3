#!/usr/bin/python3

"""
create a route /status on the object app_views
returns a JSON "status": "OK"
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """
    returns status
    """
    return (jsonify({"status": "OK"}))

@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    retrieves the number of each objects by type
    """
    obj_count = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
    return jsonify(obj_count)
