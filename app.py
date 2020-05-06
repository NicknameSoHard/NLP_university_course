import sys
from argparse import ArgumentParser

import pandas
from parsers import MeduzaNewsParser, LentaNewsParser, VestiNewsParser


news_parsers = (VestiNewsParser, LentaNewsParser, MeduzaNewsParser,)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-n', '--number', default=5)
    arg_parser.add_argument('-f', '--file', default='news.csv')

    args = arg_parser.parse_args(sys.argv[1:])
    total_news_to_download = int(args.number)
    filename = args.file

    news_parsers = [parser() for parser in news_parsers]
    number_of_parsers = len(news_parsers)

    news_on_one_source = total_news_to_download // number_of_parsers
    added_news = total_news_to_download % number_of_parsers

    all_news = pandas.DataFrame()
    for parser in news_parsers:
        news_to_download = news_on_one_source
        if added_news:
            news_to_download += added_news
            added_news = 0

        news = parser.get_news(news_to_download)
        new_news = pandas.DataFrame(news)
        new_news['source'] = parser.__class__.__name__
        all_news = pandas.concat([all_news, new_news])

    all_news.to_csv(filename, sep=';', index=False)
