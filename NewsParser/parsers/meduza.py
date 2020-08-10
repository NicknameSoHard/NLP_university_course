import requests
import time

from bs4 import BeautifulSoup

from parsers.base import BaseNewsParser


class MeduzaNewsParser(BaseNewsParser):
    def __init__(self):
        super().__init__()
        self.api_url = "https://meduza.io/api/v3"

        self.search_path = 'search'
        self.base_params = {'chrono': 'news',
                            'locale': 'ru',
                            'per_page': 30  # Max value 30
                            }

    def get_news(self, number_news):
        list_news_url = f"{self.api_url}/{self.search_path}"

        news_stack = list()
        page_number = 0
        while True:
            r = requests.get(list_news_url, params={
                'page': page_number,
                **self.base_params
            })
            if r.status_code != 200:
                continue

            news_urls = [path for path in r.json()['collection'] if 'news/' in path]
            need_news = number_news - len(news_stack)
            news_list = self.__get_full_news(news_urls, need_news)
            news_stack.extend(news_list)

            if len(news_stack) >= number_news:
                break
            page_number += 1

        return news_stack[:number_news]

    def __get_full_news(self, news_urls: list, need_news):
        result = list()
        for news_path in news_urls:
            if len(result) >= need_news:
                break
            news_url = f"{self.api_url}/{news_path}"
            r = requests.get(news_url)
            if r.status_code != 200:
                continue

            root = r.json()['root']
            body = root['content']['body']
            body_text = self.__get_news_text(body)
            title = root['title']

            news = {
                'title': title,
                'content': body_text,
                'url': news_url
            }
            result.append(news)
            time.sleep(self.delay)
        return result

    @staticmethod
    def __get_news_text(body):
        parsed_body = BeautifulSoup(body, 'lxml')
        news_text = parsed_body.get_text()
        drop_position = news_text.find('Читайте также')
        if drop_position != -1:
            news_text = news_text[:drop_position]
        return news_text.replace('\n', ' ')
