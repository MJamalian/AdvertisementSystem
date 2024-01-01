from abc import ABC, abstractmethod


class BaseAdvertising(ABC):

    def __init__(self, id):
        self.__id = id
        self.__views = 0
        self.__clicks = 0

    def inc_views(self):
        self.__views += 1

    def get_views(self):
        return self.__views

    def inc_clicks(self):
        self.__clicks += 1

    def get_clicks(self):
        return self.__clicks

    @abstractmethod
    def describe_me(self):
        """This method describes the functionality of the class"""
