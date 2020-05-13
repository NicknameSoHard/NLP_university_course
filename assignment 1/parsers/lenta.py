import re
import requests
import time

from bs4 import BeautifulSoup
import datetime

from parsers.base import BaseNewsParser


class LentaNewsParser(BaseNewsParser):
    def __init__(self):
        super().__init__()
        self.news_by_date_url = "https://lenta.ru"
        self.news_started = datetime.date(year=1999, month=9, day=1)

    def get_news(self, number_news, date=None, start_from_latest=True):
        if date is None:
            date = datetime.datetime.today().date()
        if not start_from_latest:
            date = self.news_started

        news_stack = list()
        load_more = True
        while load_more:
            str_date = str(date).replace('-', '/')
            news_for_date_url = f"{self.news_by_date_url}/news/{str_date}"
            r = requests.get(news_for_date_url)
            if r.status_code != 200:
                continue

            page = BeautifulSoup(r.text, 'lxml')
            longrid_columns = page.findAll('section', class_='b-longgrid-column')
            for longrid in longrid_columns:
                need_news = number_news - len(news_stack)
                news_from_page = self.__parse_longrid(longrid, need_news)
                news_stack.extend(news_from_page)

                if len(news_stack) >= number_news:
                    load_more = False
                    break

            date -= datetime.timedelta(days=1)

        return news_stack[:number_news]

    def __parse_longrid(self, longrid, need_news):
        result = list()
        tabloids_news = longrid.findAll('a')
        for div_news in tabloids_news:
            if len(result) >= need_news:
                break

            news_path = div_news.get('href')
            news_url = f"{self.news_by_date_url}/{news_path}"
            r = requests.get(news_url)
            if r.status_code != 200:
                continue

            page = BeautifulSoup(r.text, 'lxml')
            title = div_news.string
            news_text = ''
            for p in page.findAll('p'):
                news_text += p.get_text()
            news_text = self.__drop_special_symbols(news_text)

            if news_text:
                news = {
                    'title': title,
                    'content': news_text
                }
                result.append(news)
            time.sleep(self.delay)
        return result

    @staticmethod
    def __drop_special_symbols(string):
        return re.sub(r'/[^a-zа-я ]/ui', '', string).replace('\n', ' ')
