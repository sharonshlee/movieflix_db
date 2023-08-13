"""
Users class
Managing Users' CRUD operations
"""
from typing import List

from movieflix_db.data_manager.data_manager_interface import DataManagerInterface
from movieflix_db.data_manager.data_models import UserMovie


class UsersMovies:
    """
    UsersMovies class
    Implementing UsersMovies' CRUD operations
    """

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager

    @staticmethod
    def __user_to_dict(user) -> dict:
        """
        Convert user from db object to dict format
        """
        movies = []
        for movie in user.movies:
            movies.append(
                {
                    "id": movie.id,
                    "name": movie.movie_name,
                    "director": movie.director,
                    "year": movie.year,
                    "rating": movie.rating,
                    "poster": movie.poster,
                    "website": movie.website
                }
            )
        return {"id": user.id,
                "name": user.user_name,
                "movies": movies}

    def get_all_users_movies(self) -> List[dict] | None:
        """
        Return a list of all users movies
        :return:
            A list of dictionaries representing users movies
        """
        users_query = self._data_manager.get_all_data()
        if users_query is None:
            return None

        users = []
        for user in users_query:
            users.append(self.__user_to_dict(user))
        return users

    @staticmethod
    def __instantiate_user_movie(fav_movie_info):
        return UserMovie(
            user_id=fav_movie_info['user_id'],
            movie_id=fav_movie_info['movie_id']
        )

    def add_user_movie(self, fav_movie_info: dict) -> bool | None:
        """
        Add a movie to a user
        :param fav_movie_info: dict
        :return:
            True for success add (bool) |
            None
        """
        return self._data_manager.add_item(self.__instantiate_user_movie(fav_movie_info))

    def delete_user_movie(self, user_movie_id: int) -> bool | None:
        """
        Delete a user's fav movie given user_movie_id
        :param user_movie_id: int
        :return:
            True for success delete movie (bool) |
            None
        """
        return self._data_manager.delete_item(user_movie_id)
