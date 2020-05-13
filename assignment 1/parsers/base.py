from abc import ABC, abstractmethod


class BaseNewsParser(ABC):
    def __init__(self):
        self.delay = 0.0001

    @abstractmethod
    def get_news(self, number_news):
        pass
