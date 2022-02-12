import requests
from bs4 import BeautifulSoup

HEADERS = {'Cookie': '_ga=GA1.2.1254197178.1640632463; habr_web_ga_uid=4eeaf5f56703129813def4baa1457eb2; _gid=GA1.2.574329708.1644657632',
            'Accept-Language': 'ru',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Cash-control': 'max-age=0',
            'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
           'sec-sh-ua-module': '?0'
}

url = 'https://habr.com/ru/all/'

response = requests.get(url, headers=HEADERS).text

soup = BeautifulSoup(response, 'html.parser')

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'шахматы']

articles = soup.find_all('article', class_='tm-articles-list__item')

res_title_page = []
res_article_page = []

for article in articles:

    found_elem = article.find('a', class_='tm-article-snippet__title-link')
    header = found_elem.text
    preview = article.find('div', class_='tm-article-body tm-article-snippet__lead').text
    text_for_scrap = set(i.strip(';:.,?!"').lower() for i in (header + preview).split())
    date_create = article.find('time').attrs.get('title').split(',')[0]
    href = 'https://habr.com' + found_elem.attrs.get('href')

    if not set(KEYWORDS).isdisjoint(text_for_scrap):
        res_title_page.append(f'{date_create} - {header} - {href} keywords {set(KEYWORDS).intersection(text_for_scrap)}')
    else:
        response_article = requests.get(href, headers=HEADERS).text
        soup_article = BeautifulSoup(response_article, 'html.parser')
        article_text = soup_article.find('article', class_='tm-article-presenter__content tm-article-presenter__content_narrow').text
        text_for_scrap = set(i.strip(';:.,?!"').lower() for i in article_text.split())

        if not set(KEYWORDS).isdisjoint(text_for_scrap):
            res_article_page.append(
                f'{date_create} - {header} - {href} keywords {set(KEYWORDS).intersection(text_for_scrap)}')

print('Совпадения по заголовкам и аннотациям:')
for el in res_title_page:
    print(el)
print('Совпадения по тексту статьи:')
for el in res_article_page:
    print(el)






