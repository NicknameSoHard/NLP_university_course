import sys
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

import pandas

from parsers import MeduzaNewsParser, LentaNewsParser, VestiNewsParser

news_parsers = (VestiNewsParser, LentaNewsParser, MeduzaNewsParser)


def get_news_dataframe(parser, count_to_download):
    parser_name = parser.__class__.__name__
    print(f'{parser_name}:  Work started.')
    news = parser.get_news(count_to_download)
    news_frame = pandas.DataFrame(news)
    news_frame['source'] = parser_name
    print(f'{parser_name}: Work done.')
    return news_frame


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-n', '--number', default=15)
    arg_parser.add_argument('-f', '--file', default='news.csv')

    args = arg_parser.parse_args(sys.argv[1:])
    filename = args.file

    news_parsers = [parser() for parser in news_parsers]
    number_of_parsers = len(news_parsers)

    total_news_to_download = int(args.number)
    news_on_one_source = total_news_to_download // number_of_parsers
    added_news = total_news_to_download % number_of_parsers

    all_news = pandas.DataFrame()
    result = list()
    with ThreadPoolExecutor(max_workers=number_of_parsers) as executor:
        for parser in news_parsers:
            news_to_download = news_on_one_source
            if added_news:
                news_to_download += added_news
                added_news = 0

            future_result = executor.submit(get_news_dataframe, parser, news_to_download)
            result.append(future_result)

        for res in result:
            parsed_news = res.result()
            all_news = pandas.concat([all_news, parsed_news])

    all_news.to_csv(filename, sep=';', index=False)
