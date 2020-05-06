import re

import requests
import time

from bs4 import BeautifulSoup
import datetime

from parsers.base import BaseNewsParser


class VestiNewsParser(BaseNewsParser):
    def __init__(self):
        self.news_url = 'http://www.vesti.ru'
        self.search_by_date = 'news/index/date'

        self.default_args = {
            'project': 'rbcnews',
            'material': 'short_news'
        }

    def get_news(self, number_news, date=None):
        if date is None:
            date = datetime.datetime.today().date()

        news_stack = list()
        search_url = f"{self.news_url}/{self.search_by_date}"
        while True:
            '04.05.2020'
            str_date = date.strftime('%d.%m.%Y')
            date_url = f"{search_url}/{str_date}"
            r = requests.get(date_url)
            if r.status_code != 200:
                continue

            page = BeautifulSoup(r.text, 'lxml')
            item_list = page.findAll('h3', class_='b-item__title')
            need_news = number_news - len(news_stack)
            news_from_page = self.__parse_all_news(item_list, need_news)
            news_stack.extend(news_from_page)

            if len(news_stack) >= number_news:
                break
            date -= datetime.timedelta(days=1)

        return news_stack[:number_news]

    def __parse_all_news(self, item_list, need_news):
        result = list()
        for item in item_list:
            if len(result) >= need_news:
                break

            news = item.find('a')
            news_path = news.get('href')
            news_url = f"{self.news_url}{news_path}"
            r = requests.get(news_url)
            if r.status_code != 200:
                continue

            page = BeautifulSoup(r.text, 'lxml')
            title = news.get_text()
            news_text = page.find('div', class_='js-mediator-article').get_text()
            news_text = self.__drop_special_symbols(news_text)
            if news_text:
                news = {
                    'title': title,
                    'content': news_text
                }
                result.append(news)
            time.sleep(0.000001)
        return result

    @staticmethod
    def __drop_special_symbols(string):
        return re.sub(r'/[^a-zа-яA-ZА-Я ]/ui', '', string).replace('\n', ' ')
