"""
Movieflix app as a web service.

API endpoints:
GET /api/users: List all users.
GET /api/users/<user_id>/movies: List a user’s favorite movies.
POST /api/users/<user_id>/movies: Add a new favorite movie for a user.
"""

from flask import Blueprint, jsonify

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def get_users():
    # Implementation here
    pass
