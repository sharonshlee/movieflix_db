"""
Movies class
Managing Movies' CRUD operations
"""
from movieflix_db.data_manager.data_manager_interface import DataManagerInterface
from movieflix_db.data_manager.data_models import Movie


class Movies:
    """
    Movies class
    Implementing Users' CRUD operations
    """

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager

    def get_movie(self, movie_id: int) -> dict | None:
        """
        Return a specific user given user_id
        :param movie_id: int
        :return:
            Movie (dict) |
            None
        """
        return self._data_manager.get_item_by_id(movie_id)

    @staticmethod
    def __instantiate_new_movie(new_movie_info, user_id):
        return Movie(
            movie_name=new_movie_info['movie_name'],
            director=new_movie_info['director'],
            year=new_movie_info['year'],
            rating=new_movie_info['rating'],
            poster=new_movie_info['poster'],
            website=new_movie_info['website'],
            user_id=user_id
        )

    def add_user_movie(self, user_id: int, new_movie_info: dict) -> bool | None:
        """
        Add a movie to a user
        :param user_id: int
        :param new_movie_info: dict
        :return:
            True for success add (bool) |
            None
        """
        return self._data_manager.add_item(self.__instantiate_new_movie(new_movie_info, user_id))

    def update_movie(self, updated_movie: dict):
        """
        Update a movie info
        :param updated_movie: dict
        :return:
            True for success update movie (bool) |
            None
        """
        return self._data_manager.update_item(updated_movie)

    def delete_movie(self, movie_id: int) -> bool | None:
        """
        Delete a movie given movie_id
        :param movie_id: int
        :return:
            True for success delete movie (bool) |
            None
        """
        return self._data_manager.delete_item(movie_id)
