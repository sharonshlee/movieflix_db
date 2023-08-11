"""
DataManagerInterface:
Data management for file like json, csv or db sources.
"""
from abc import ABC, abstractmethod
from flask_sqlalchemy.query import Query


class DataManagerInterface(ABC):
    """
    An Interface Class that reading file,
    parsing the data into Python
    data structures (lists and dictionaries),
    and providing methods to
    manipulate the data
    (like adding, updating, or removing items)
    """

    @abstractmethod
    def get_all_data(self) -> Query | None:
        """
        Return all the data from db
        :return:
            Query object representing all the data
        """

    @abstractmethod
    def get_item_by_id(self, item_id):
        """
        Return the specific item
        given item_id
        :return:
            item (Query) |
            None
        """

    @abstractmethod
    def add_item(self, new_item: dict) -> bool:
        """
        Add new item to file
        :param new_item: (dict)
        :return:
            Successfully add item, True (bool)
        """

    @abstractmethod
    def generate_new_id(self, items: list, key=None) -> int:
        """
        Return 1 if items is empty
        otherwise, return the highest id_key plus 1
        :param items: list
        :param key: str
        :return:
            new item id (int) |
            1 if items is empty (int)
        """

    @abstractmethod
    def update_item(self, updated_item: dict) -> bool | None:
        """
        Update item with updated_item
        :param updated_item: dict
        :return:
            True for success update item (bool) |
            None
        """

    @abstractmethod
    def delete_item(self, item_id: int) -> bool | None:
        """
        Delete an item based on item_id
        :param item_id: int
        :return:
            True for success delete item (bool) |
            None
        """
