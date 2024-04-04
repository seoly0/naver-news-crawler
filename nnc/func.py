import requests
import re
import math
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime, timedelta


def get_date(text: str):
    if not text:
        return None

    dateformat = re.match(r'^\d{4}\.\d{2}\.\d{2}\.$', text)
    if dateformat:
        return str(datetime.strptime(dateformat.group(), "%Y.%m.%d.").date())

    n_minute_ago = re.match(r'^(\d+)분\s전$', text)
    if n_minute_ago:
        minute_ago = int(n_minute_ago.group(1))
        return str((datetime.now() - timedelta(minutes=minute_ago)).date())

    n_hour_ago = re.match(r'^(\d+)시간\s전$', text)
    if n_hour_ago:
        hour_ago = int(n_hour_ago.group(1))
        return str((datetime.now() - timedelta(hours=hour_ago)).date())

    n_day_ago = re.match(r'^(\d+)일\s전$', text)
    if n_day_ago:
        days_ago = int(n_day_ago.group(1))
        return str((datetime.now() - timedelta(days=days_ago)).date())

    n_week_ago = re.match(r'^(\d+)주\s전$', text)
    if n_week_ago:
        days_ago = int(n_week_ago.group(1)) * 7
        return str((datetime.now() - timedelta(days=days_ago)).date())


def crawl(query: str, n: int = 100, excludes=[]):

    print(f'"{query}"에 대해 검색...')

    keyword = quote(query)
    initial_url = f'https://s.search.naver.com/p/newssearch/search.naver?start=1&where=news_tab_api&sort=1&query={keyword}'
    response = requests.get(initial_url).json()
    next_url = response['nextUrl']
    contents = response['contents']

    to = math.ceil(n / 10)

    for i in range(1, to):
        response = requests.get(next_url).json()
        next_url = response['nextUrl']
        contents = contents + response['contents']

    data = []

    for content in contents:
        node = BeautifulSoup(content, 'html.parser')
        title_node = node.find('div', class_='news_contents').find('a', class_='news_tit')
        title = title_node.text
        url = title_node.attrs['href']
        info_node = node.find('div', class_='info_group')
        author = info_node.find('a', class_='info').text
        date = list(filter(lambda x: x is not None, map(lambda x: get_date(x.text), info_node.find_all('span', class_='info'))))
        date = date[0] if date else None

        valid = True
        for exclude in excludes:
            if exclude in title:
                valid = False

        if valid:
            data.append({
                'author': author,
                'title': title,
                'url': url,
                'date': date
            })

    data = data[:n]

    ret = {
        'query': query,
        'excludes': excludes,
        'requestedLength': n,
        'timestamp': datetime.now().timestamp(),
        'data': data,
        'length': len(data),
    }

    return ret



