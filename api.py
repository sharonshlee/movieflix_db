"""
Movieflix app as a web service.

API endpoints:
GET /api/users: List all users.
POST /api/users: Add a new user.
GET /api/users/<user_id>/movies: List a user’s favorite movies.
POST /api/users/<user_id>/movies/<movie_id>: Add a new favorite movie for a user.
DELETE /api/users/delete_user_movie/<user_movie_id>: Delete a favorite movie for a user.
"""
import requests
from flask import Blueprint, jsonify, g, request

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def get_users():
    """
    Return all the users
    :returns
        List of Users dictionary |
        Error Message
    """
    users = g.users_data_manager.get_all_users()
    if users is None:
        return jsonify({"error_message": "Users not found."}), 404

    return jsonify(users)


def validate_user_input(user_info: dict) -> list:
    """
    Validates user inputs and
    return specific error messages
    based on user input error
    :param user_info: dict
    :return:
        error messages (list)
    """
    user_name = user_info['user_name']
    error_messages = []
    if len(user_name) == 0:
        error_messages.append('User name cannot be empty')
    else:
        # check first letter is digit or special chars
        if not user_name[0].isalpha():
            error_messages.append('User name must start with letter')
    return error_messages


@api.route('/users', methods=['POST'])
def add_user():
    """
    Add a new user
    :return:
        Successfully added message |
        Error message
    """
    user_name = request.json['user_name']

    error_messages = validate_user_input({'user_name': user_name})
    if len(error_messages) != 0:
        return jsonify({"error_message": "Invalid user name."}), 400

    new_user = {"user_name": user_name,
                "movies": []}

    if g.users_data_manager.add_user(new_user) is None:
        return jsonify({"error_message": "Cannot add user."}), 500  # server error

    return jsonify({"message": "User successfully added."}), 201  # created


@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id: int):
    """
    Get user movies given user id
    :param
        user_id: int
    :return:
        List of user's movies dictionary |
        Error Message
    """
    user = g.users_data_manager.get_user(user_id)

    if user is None:
        return jsonify({"error_message": "User not found."}), 404

    return jsonify(user['movies'])


@api.route('/users/<int:user_id>/movies/<int:movie_id>', methods=['POST'])
def add_user_movie(user_id: int, movie_id: int):
    """
    Add a favourite movie to a user
    given user_id and movie id
    :param user_id: int
    :param movie_id: int
    :return:
        Successful added message |
        Error message
    """
    user_movie_info = {
        'user_id': user_id,
        'movie_id': movie_id
    }

    user_movies = g.users_data_manager.get_user(user_id)['movies']

    if movie_id in [user_movie['id'] for user_movie in user_movies]:
        return jsonify({"error_message": "Cannot add movie as its already added."}), 400

    if g.users_movies_data_manager.add_user_movie(user_movie_info) is None:
        return jsonify({"error_message": "Cannot add movie."}), 500  # server error

    return jsonify({"message": "Movie successfully added to user."}), 201  # created


@api.route('/users/delete_user_movie/<int:user_movie_id>', methods=['DELETE'])
def delete_user_movie(user_movie_id: int):
    """
    Delete a fav movie for a user
    given user_movie_id
    :param user_movie_id:
    :return:
        Successfully deleted message |
        Error Message
    """
    if g.users_movies_data_manager.delete_user_movie(user_movie_id) is None:
        return jsonify({"error_message": "Cannot delete movie."}), 500

    return jsonify({"message": "Movie successfully deleted from user."}), 204  # no content
