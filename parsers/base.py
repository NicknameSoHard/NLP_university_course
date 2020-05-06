from abc import ABC, abstractmethod


class BaseNewsParser(ABC):

    @abstractmethod
    def get_news(self, number_news):
        pass
