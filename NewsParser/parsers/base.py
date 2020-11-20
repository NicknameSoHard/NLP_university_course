import re
from abc import ABC, abstractmethod


class BaseNewsParser(ABC):
    def __init__(self):
        self.delay = 0.0001

    @abstractmethod
    def get_news(self, number_news):
        pass

    @staticmethod
    def drop_special_symbols(string):
        return re.sub(r'/[^a-zа-яA-ZА-Я ]/ui', '', string).replace('\n', ' ')