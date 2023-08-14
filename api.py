"""
Movieflix app as a web service.

API endpoints:
Users:
GET /api/users: List all users.
POST /api/users: Add a new user.
GET /api/users/<user_id>/movies: List a user’s favorite movies.
POST /api/users/<user_id>/movies/<movie_id>: Add a new favorite movie for a user.
DELETE /api/users/movies/<user_movie_id>: Delete a favorite movie for a user.

Movies:
GET /api/movies: List all movies.
POST /api/movies: Add a new movie.
PUT /api/movies/update_movie/<int:movie_id>: Update a movie.
DELETE /api/movies/delete_movie/<int:movie_id>: Delete a movie.
GET /movies/<int:movie_id>/reviews: List all movie reviews for a movie
POST /users/<int:user_id>/add_movie_review/<int:movie_id>: Add a movie review for a movie
"""
import requests
from flask import Blueprint, jsonify, g, request

api = Blueprint('api', __name__)

API_KEY = 'd5a88f10'
BASE_URL_KEY = f'http://www.omdbapi.com/?apikey={API_KEY}'
IMDB_BASE_URL = 'https://www.imdb.com/title/'


def jsonify_error_message(message, code: int):
    """
    Return jsonify error message
    and error code
    :param code: int
    :param message: str | list
    :return: error message (json), code (int)
    """
    return jsonify({"error_message": message}), code


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
        return jsonify_error_message("Users not found.", 404)

    return jsonify(users), 200  # ok


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
    user_name = request.json.get('user_name', '')

    error_messages = validate_user_input({'user_name': user_name})
    if len(error_messages) != 0:
        return jsonify_error_message("Invalid user name.", 400)

    new_user = {"user_name": user_name,
                "movies": []}

    if g.users_data_manager.add_user(new_user) is None:
        return jsonify_error_message("Cannot add user.", 500)  # server error

    return jsonify_error_message("User successfully added.", 201)  # created


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
        return jsonify_error_message("User not found.", 404)

    return jsonify(user['movies']), 200


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

    user = g.users_data_manager.get_user(user_id)
    if user is None:
        return jsonify_error_message("User not found.", 404)

    if movie_id in [user_movie['id'] for user_movie in user['movies']]:
        return jsonify_error_message("Cannot add movie as its already added.", 400)

    if g.users_movies_data_manager.add_user_movie(user_movie_info) is None:
        return jsonify_error_message("Cannot add movie.", 500)  # server error

    return jsonify({"message": "Movie successfully added to user."}), 201  # created


@api.route('/users/movies/<int:user_movie_id>', methods=['DELETE'])
def delete_user_movie(user_movie_id: int):
    """
    Delete a fav movie for a user
    given user_movie_id
    :param user_movie_id:
    :return:
        Successfully deleted message |
        Error Message
    """
    user_movie = g.users_movies_data_manager.get_user_movie(user_movie_id)
    if not user_movie:
        return jsonify_error_message("User Movie not found.", 404)

    if g.users_movies_data_manager.delete_user_movie(user_movie_id) is None:
        return jsonify_error_message("Cannot delete movie.", 500)

    return jsonify({"message": "Movie successfully deleted from user."}), 204  # no content


@api.route('/movies', methods=['GET'])
def get_movies():
    """
    Get all the movies from the movies table
    """
    movies = g.movies_data_manager.get_movies()
    if movies is None:
        return jsonify_error_message("Movies not found.", 404)

    return jsonify(movies), 200


def fetch_movie_api_response(title: str) -> dict:
    """
    Fetch api response movie info
    given movie title
    :param title: str
    :return: movie info (dict)
    """
    response = requests.get(f'{BASE_URL_KEY}&t={title}', timeout=5)
    response.raise_for_status()  # check if there was an error with the request

    return response.json()


def isfloat(number: str) -> bool:
    """
    Check if the given number is float type
    :param number:
    :return:
        True or False (bool)
    """
    try:
        float(number)
        return True
    except ValueError:
        return False


def get_error_messages(movie_info: dict) -> list:
    """
    Validates user inputs and
    return specific error messages
    based on user input error
    :param movie_info: dict
    :return:
        error messages (list)
    """
    movie_name = movie_info.get('movie_name', '')
    director = movie_info.get('director', '')
    year = movie_info.get('year', '')
    rating = movie_info.get('rating', '')

    error_messages = []
    if len(movie_name) == 0:
        error_messages.append('Movie name cannot be empty')

    if len(movie_name) != 0 and not movie_name[0].isalpha():
        error_messages.append('Movie name must start with letter')

    if len(director) != 0 and not director[0].isalpha():
        error_messages.append('Director name must start with letter')

    if len(year) != 0:
        if not year.isdigit():
            error_messages.append('Year must be number')

        if year.isdigit() and len(year) != 4:
            error_messages.append('Year must be 4 digits')

    if len(rating) != 0:
        if not isfloat(rating):
            error_messages.append('Rating must be a number')
        elif not 1.0 <= float(rating) <= 10.0:
            error_messages.append('Rating must be between 1.0 - 10.0')

    return error_messages


def format_movie_info(response: dict, movie_name: str) -> dict:
    """
    Format movie info
    :param response: dict
    :param movie_name: str
    :return:
        movie info (dict)
    """
    return {'movie_name': response.get('Title', movie_name),
            'director': response.get('Director', ''),
            'year': int(response.get('Year', '0000')[:4]),
            'rating': float(response.get('imdbRating', 0.0)),
            'poster': response.get('Poster', ''),
            'website': IMDB_BASE_URL + response.get('imdbID', '')
            }


def get_empty_info(movie_name: str) -> dict:
    """
    Return empty movie info
    :param movie_name: str
    :return:
        empty movie info (dict)
    """
    return {'movie_name': movie_name,
            'director': '',
            'year': 0,
            'rating': 0.0,
            'poster': '',
            'website': ''
            }


def get_new_movie_info() -> dict | list:
    """
    Get new movie info:
    name from add movie form,
    other movie details from OMDb API
    :return:
        New movie info from OMDb API (dict) |
        New movie name from add movie form (dict)
    """
    movie_name = request.json.get('movie_name', '')

    error_messages = get_error_messages({'movie_name': movie_name})
    if error_messages:
        return error_messages

    try:
        response = fetch_movie_api_response(movie_name)
        return format_movie_info(response, movie_name)

    except (requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException):
        print("Request error. "
              "Check your internet connection "
              "and make sure the website is accessible.")
        return get_empty_info(movie_name)


@api.route('/movies/add_movie', methods=['POST'])
def add_new_movie():
    """
    Add a new movie
    :return:
        Successfully added message |
        Error message
    """
    new_movie_info = get_new_movie_info()
    if isinstance(new_movie_info, list):
        return jsonify_error_message(new_movie_info, 400)

    if g.movies_data_manager.add_new_movie(new_movie_info) is None:
        return jsonify_error_message('Cannot add movie. '
                                     'Movie already exist in the database.', 500)

    return jsonify({'message': 'Movie is successfully added.'}), 201


def get_movie_info() -> dict:
    """
    Get updated movie details
    from request
    :return:
        updated movie details (dict)
    """
    return {'movie_name': request.json.get('movie_name', ''),
            'director': request.json.get('director', ''),
            'year': request.json.get('year', 0),
            'rating': request.json.get('rating', 0.0)
            }


def get_updated_movie_info(movie_id) -> dict | list:
    """
    Get updated movie info
    from request
    :return:
        Updated movie info (dict) |
        List of error messages (list)
    """
    updated_movie_info = get_movie_info()
    error_messages = get_error_messages(updated_movie_info)

    if len(error_messages) != 0:
        return error_messages

    year = updated_movie_info['year']
    if len(year) == 0:
        year = 0

    rating = updated_movie_info['rating']
    if len(rating) == 0:
        rating = 0.0

    return {'id': movie_id,
            'movie_name': updated_movie_info['movie_name'],
            'director': updated_movie_info['director'],
            'year': int(year),
            'rating': float(rating)
            }


@api.route('/movies/update_movie/<int:movie_id>', methods=['PATCH'])
def update_movie(movie_id: int):
    """
    Update a movie given movie_id
    :param movie_id: int
    :return:
        Successfully updated message |
        Error message
    """
    movie = g.movies_data_manager.get_movie(movie_id)
    if not movie:
        return jsonify_error_message('Movie not found.', 404)

    updated_movie = get_updated_movie_info(movie_id)
    if isinstance(updated_movie, list):
        return jsonify_error_message(updated_movie, 400)

    if g.movies_data_manager.update_movie(updated_movie) is None:
        return jsonify_error_message('Cannot update movie.', 500)

    return jsonify({'message': 'Movie is successfully updated.'}), 201


@api.route('/movies/delete_movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id: int):
    """
    Delete a specific movie given movie_id
    :param movie_id: int
    :return:
        Successfully deleted message |
        Error message
    """
    movie = g.movies_data_manager.get_movie(movie_id)

    if not movie:
        return jsonify_error_message('Movie not found.', 404)

    if g.movies_data_manager.delete_movie(movie_id) is None:
        return jsonify_error_message('Unable to delete movie. It could be favourited.', 500)

    return jsonify({"message": "Movie successfully deleted."}), 204  # no content


@api.route('/movies/<int:movie_id>/reviews', methods=['GET'])
def get_movie_reviews(movie_id: int):
    """
    Get all the movie's reviews
    for that specific movie
    given movie_id
    :param movie_id: int
    :returns:
        Movie reviews json(list[dict])
    """
    movie = g.movies_data_manager.get_movie(movie_id)
    if movie is None:
        return jsonify_error_message("Movie not found.", 404)

    return jsonify(movie["movie_reviews"]), 200  # ok


def get_error_message(user_id: int, movie_id: int):
    """
    Return error messages for any invalid data
    :param user_id: int
    :param movie_id: int
    :return: Error Message (json) |
             False when no errors
    """
    user = g.users_data_manager.get_user(user_id)
    if user is None:
        return jsonify_error_message("User not found.", 404)

    movie = g.movies_data_manager.get_movie(movie_id)
    if not movie:
        return jsonify_error_message("Movie not found.", 404)

    user_movies = user.get('movies')
    if movie_id not in [user_movie['id'] for user_movie in user_movies]:
        return jsonify_error_message("User not favourite this movie cannot make review.", 404)

    movie_reviews = movie["movie_reviews"]
    movie_reviews_user_ids = [movie_review["user_id"] for movie_review in movie_reviews]
    if user_id in movie_reviews_user_ids:
        return jsonify_error_message("Cannot add review as its already added.", 400)

    return False


def get_reviewed_info(user_id: int, movie_id: int) -> dict:
    """
    Get reviewed info from request
    :param user_id: int
    :param movie_id: int
    :return: Reviewed info (dict)
    """
    return {'user_id': user_id,
            'movie_id': movie_id,
            'rating': request.json.get('rating', 0.0),
            'review_text': request.json.get('review_text', '')
            }


@api.route('/users/<int:user_id>/add_movie_review/<int:movie_id>', methods=['POST'])
def add_movie_review(user_id: int, movie_id: int):
    """
    Add a movie review by a user
    given user_id and movie_id
    :param user_id: int
    :param movie_id: int
    """
    if get_error_message(user_id, movie_id):
        return get_error_message(user_id, movie_id)

    if g.movies_reviews_data_manager. \
            add_movie_review(get_reviewed_info(user_id, movie_id)) is None:
        return jsonify_error_message("Cannot add review.", 500)  # server error

    return jsonify({"message": "Movie review successfully added for this user."}), 201  # created
