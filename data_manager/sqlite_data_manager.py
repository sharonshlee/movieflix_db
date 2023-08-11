"""
SQLiteDataManager class implemented DataManagerInterface
for managing data from sqlite database
"""
from abc import ABC
from typing import List

from flask_sqlalchemy.query import Query
from sqlalchemy.exc import SQLAlchemyError

from movieflix_db.data_manager.data_manager_interface import DataManagerInterface
from movieflix_db.data_manager.data_models import User, Movie


class SQLiteDataManager(DataManagerInterface, ABC):
    """
    A class for managing data
    from sqlite database
    """

    def __init__(self, id_key, entity, db):
        self.db = db
        self._id_key = id_key
        self._entity = entity

    def get_all_data(self) -> Query | None:
        """
        Return all data from sqlite DB
        :return:
            A query object representing all the data
            None
        """
        try:
            return self._entity.query.all()
        except SQLAlchemyError:
            return None

    def get_item_by_id(self, item_id):
        """
        Return the specific item
        given item_id
        :return:
            item |
            None
        """
        try:
            return self._entity.query. \
                filter(getattr(self._entity, self._id_key) == item_id). \
                one()
        except SQLAlchemyError:
            return None

    def add_item(self, new_item) -> bool | None:
        """
        Add new item to sqlite DB
        :param new_item
        :return:
            Successfully add item, True (bool)
        """
        try:
            self.db.session.add(new_item)
            self.db.session.commit()
            return True
        except SQLAlchemyError:
            self.db.session.rollback()
            return None

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
        pass

    def update_item(self, updated_item: dict) -> bool | None:
        """
        Update item with updated_item
        :param updated_item: dict
        :return:
            True for success update item (bool) |
            None
        """
        try:
            item = self._entity.query.get(updated_item['id'])
            if item:
                for key, value in updated_item.items():
                    # skip id
                    if key == 'id':
                        continue
                    setattr(item, key, value)
                self.db.session.commit()
                return True
        except SQLAlchemyError:
            self.db.session.rollback()
            return None

    def delete_item(self, item_id: int) -> bool | None:
        """
        Delete an item based on item_id
        :param item_id: int
        :return:
            True for success delete item (bool) |
            None
        """

        try:
            item = self._entity.query.get(item_id)
            self.db.session.delete(item)
            self.db.session.commit()
            return True
        except SQLAlchemyError:
            self.db.session.rollback()
            return None
