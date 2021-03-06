#Очень долго. Попробовать спарсить с помощью asyncio
#Добавить результат в базу (отдельная таблица)

import requests
from bs4 import BeautifulSoup as bs

class PaidParser():

    def __init__(self):
        self.url = 'https://hub.virtamate.com/resources/categories/paid.5/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}
        self.cookies = {'vamhubconsent': 'yes'}
        self.session = requests.Session()
        self.r = self.session.get(self.url, headers=self.headers, cookies=self.cookies) # подсунули свой кук с согласием
        self.soup = bs(self.r.text, 'lxml')
        self.last_page = None

    def get_pagination(self):
        last_page = self.soup.find('ul', class_="pageNav-main").find_all('li')[3].div.div.div.div.div.input.get('max')
        return int(last_page)

    def parse_authors(self):
        self.last_page = self.get_pagination()
        url_prefix = 'https://hub.virtamate.com/resources/categories/paid.5/?page='

        pages = []
        for url_suffix in range(1, self.last_page + 1):
            pages.append(url_prefix + str(url_suffix))
        return pages

    def parse_page(self, page):
        r = self.session.get(page, headers=self.headers, cookies=self.cookies) # подсунули свой кук с согласием
        soup = bs(r.text, 'lxml')

        print(page.replace('https://hub.virtamate.com/resources/categories/paid.5/?page=', ''), 'of', self.last_page)
        authors = soup.find_all('div', class_="structItem")

        one_page_author_list = []
        for author in authors:
            if author.get('data-author') not in one_page_author_list:
                one_page_author_list.append(author.get('data-author'))
                #print(author.get('data-author'), 'added.')
        return one_page_author_list

    def parse_pages(self, pages):
        all_author_list = []
        for page in pages:
            for author in self.parse_page(page):
                if author not in all_author_list:
                    all_author_list.append(author)
                    print(author, 'added.')
        return all_author_list

    def export_data(self, authors):
        for author in authors:
            with open('vam_authors', 'a') as file:
                file.write(author + '\n')


if __name__ == ('__main__'):
    paidParser = PaidParser()

    pages = paidParser.parse_authors()
    page = pages[-1] #test
    #paidParser.parse_pages(page)
    authors = paidParser.parse_pages(pages)
    paidParser.export_data(authors)
