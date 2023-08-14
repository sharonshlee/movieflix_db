"""
Users class
Managing Users' CRUD operations
"""
from typing import List

from .data_manager_interface import DataManagerInterface
from .data_models import User


class Users:
    """
    Users class
    Implementing Users' CRUD operations
    """

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager

    @staticmethod
    def __user_to_dict(user) -> dict:
        """
        Convert user from db object to dict format
        """
        movies = []
        if user.movies:
            for user_movie in user.movies:
                movies.append(
                    {
                        "user_movie_id": user_movie.id,
                        "id": user_movie.movie.id,
                        "movie_name": user_movie.movie.movie_name,
                        "director": user_movie.movie.director,
                        "year": user_movie.movie.year,
                        "rating": user_movie.movie.rating,
                        "poster": user_movie.movie.poster,
                        "website": user_movie.movie.website
                    }
                )
        return {"id": user.id,
                "user_name": user.user_name,
                "movies": movies}

    def get_all_users(self) -> List[dict] | None:
        """
        Return a list of all users
        :return:
            A list of dictionaries representing users
        """
        users_query = self._data_manager.get_all_data()
        if users_query is None:
            return None

        users = []
        for user in users_query:
            users.append(self.__user_to_dict(user))
        return users

    def get_user(self, user_id: int) -> dict | None:
        """
        Return a specific user given user_id
        :param user_id: int
        :return:
            User (dict) |
            None
        """
        user = self._data_manager.get_item_by_id(user_id)
        if user is None:
            return None
        return self.__user_to_dict(user)

    @staticmethod
    def __validate_user_data(new_user: dict) -> bool:
        #  __ enforce stricter access control
        # accessible to internal class only
        """
        Check if  the new user data is valid
        :param
            new_user: (dict)
        :return:
            True if 'name' and 'movies' fields are present
        """
        return 'user_name' in new_user and 'movies' in new_user

    @staticmethod
    def __instantiate_new_user(name):
        return User(
            user_name=name
        )

    def add_user(self, new_user: dict) -> bool | None:
        """
        Add new user to json file
        :param new_user: (dict)
        :return:
            Successfully add user, True (bool)
            Invalid new user data, None
        """
        if self.__validate_user_data(new_user):
            return self._data_manager.\
                    add_item(self.__instantiate_new_user(new_user['user_name']))
        return None

    def update_user(self, updated_user: dict):
        """
        Update a user info
        :param updated_user: dict
        :return:
            True for success update user (bool) |
            None
        """
        return self._data_manager.update_item(updated_user)

    def delete_user(self, user_id: int) -> bool | None:
        """
        Delete a user
        :param user_id: int
        :return:
            True for success delete user (bool) |
            None
        """
        return self._data_manager.delete_item(user_id)
