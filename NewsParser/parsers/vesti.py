import requests
import time

from bs4 import BeautifulSoup
import datetime

from parsers.base import BaseNewsParser


class VestiNewsParser(BaseNewsParser):
    def __init__(self):
        super().__init__()
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
            str_date = date.strftime('%d.%m.%Y')
            date_url = f"{search_url}/{str_date}"
            with requests.get(date_url) as r:
                if r.status_code != 200:
                    continue
                page = BeautifulSoup(r.text, 'lxml')
                item_list = page.findAll('h3', class_='list__title')
                need_news = number_news - len(news_stack)
                news_from_page = self.__parse_all_news(item_list, need_news)
                news_stack.extend(news_from_page)

            if len(news_stack) >= number_news:
                break
            date -= datetime.timedelta(days=1)

        return news_stack[:number_news]

    def __parse_all_news(self, item_list, need_news):
        result = list()
        for item in item_list[:need_news]:
            news = item.find('a')
            news_path = news.get('href')

            news_url = news_path
            if 'http' not in news_url:
                news_url = f"{self.news_url}{news_path}"
            try:
                with requests.get(news_url) as r:
                    if r.status_code != 200:
                        continue
                    text = r.text
            except requests.exceptions.ChunkedEncodingError:
                print(f'Chunk error: {news_url}')
                continue
            except requests.exceptions.ConnectionError:
                print(f'Connection error: {news_url}')
                if self.delay < 0.001:
                    self.delay *= 2
                continue
            except requests.exceptions.InvalidURL:
                print(f'Url Error: {news_url}')
                continue

            page = BeautifulSoup(text, 'lxml')
            title = news.get_text()
            news_text = page.find('div', class_='js-mediator-article')
            if news_text is not None:
                news_text = news_text.get_text()
                news_text = self.drop_special_symbols(news_text)

            tags = page.find_all('a', class_='tags__item')
            if tags:
                tags = [t.get_text() for t in tags]

            if news_text and tags:
                news = {
                    'title': title,
                    'content': news_text,
                    'url': news_url,
                    'tags': tags
                }
                result.append(news)
                time.sleep(self.delay)
        return result
