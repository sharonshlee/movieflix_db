"""
Movies class
Managing Movies' CRUD operations
"""
from typing import List

from .data_manager_interface import DataManagerInterface
from .data_models import Movie


class Movies:
    """
    Movies class
    Implementing Movies' CRUD operations
    """

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager


    @staticmethod
    def __movie_to_dict(movie) -> dict:
        """
        Convert movie from db object to dict format
        """
        return {"id": movie.id,
                "movie_name": movie.movie_name,
                "director": movie.director,
                "year": movie.year,
                "rating": movie.rating,
                "poster": movie.poster,
                "website": movie.website
                }

    def get_movies(self) -> List[dict] | None:
        """
        Return a list of movies dict
        :return:
            Movies (List[dict]) |
            None
        """
        movies_query = self._data_manager.get_all_data()
        if movies_query is None:
            return None

        movies = []
        for movie in movies_query:
            movies.append(self.__movie_to_dict(movie))
        return movies

    def get_movie(self, movie_id: int) -> dict | None:
        """
        Return a specific movie given movie_id
        :param movie_id: int
        :return:
            Movie (dict) |
            None
        """
        return self._data_manager.get_item_by_id(movie_id)

    @staticmethod
    def __instantiate_new_movie(new_movie_info):
        return Movie(
            movie_name=new_movie_info['movie_name'],
            director=new_movie_info['director'],
            year=new_movie_info['year'],
            rating=new_movie_info['rating'],
            poster=new_movie_info['poster'],
            website=new_movie_info['website']
        )

    def add_new_movie(self, new_movie_info: dict) -> bool | None:
        """
        Add a new movie
        :param new_movie_info: dict
        :return:
            True for success add (bool) |
            None
        """
        return self._data_manager.add_item(self.__instantiate_new_movie(new_movie_info))

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
