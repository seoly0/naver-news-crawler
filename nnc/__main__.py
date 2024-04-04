import json
import os
import argparse
from .func import crawl
from datetime import datetime


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', type=int)
    parser.add_argument('-d', type=str)
    parser.add_argument('-e', type=str)
    parser.add_argument('params', nargs='*')

    args = parser.parse_args()

    n = args.n if args.n else 100
    d = args.d if args.d else ''
    e = args.e.split(',') if args.e else ''

    keywords = args.params if args.params else []

    if len(keywords) < 1:
        print('There is no keywords...')
        exit(1)

    keyword_combined = '+'.join(keywords)

    try:
        result = crawl(keyword_combined, n, e)
    except Exception as e:
        print(e)
        print('Crawling Fail...')
        exit(1)

    try:
        if not os.path.isabs(d):
            d = os.path.abspath(d)
        os.makedirs(d, exist_ok=True)
        file_path = os.path.join(d, f'''result-{keyword_combined}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json''')
        f = open(file_path, 'w', encoding='utf-8')
        json.dump(result, f, ensure_ascii=False)
    except:
        print('Writing file Fail...')
        exit(1)

    exit(0)
