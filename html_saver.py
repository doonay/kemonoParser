import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

class HTMLSaver():

    def __init__(self, url, name='OtherVAM'):
        self.url = url #'https://hub.virtamate.com/resources/categories/paid.5/'
        self.name = name
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}
        self.cookies = {'vamhubconsent': 'yes'}
        self.session = requests.Session()
        self.r = self.session.get(self.url, headers=self.headers, cookies=self.cookies) # подсунули свой кук с согласием
        self.soup = BeautifulSoup(self.r.text, 'lxml')
        self.last_page = None

    def get_pagination(self):
        x = self.soup.find('small').get_text().strip().rfind(' ') + 1
        last_page = self.soup.find('small').get_text().strip()[x:]
        return int(last_page)

    def get_all_cards(self):
        baseurl = self.url
        try:
            pagination = self.get_pagination()
        except AttributeError:
            pagination = str(1)

        all_content_links = []
        for page in range(0, int(pagination), 25):
            url = baseurl + '?o=' + str(page)
            #print(url)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            raw_cards = soup.find_all('article', class_='post-card')

            for card in raw_cards:
                link = 'https://beta.kemono.party' + card.a.get('href')
                all_content_links.append(link)
        return all_content_links



    def parse_content_links(self):
        self.last_page = self.get_pagination()
        url_prefix = 'https://hub.virtamate.com/resources/categories/paid.5/?page='

        pages = []
        for url_suffix in range(1, self.last_page + 1):
            pages.append(url_prefix + str(url_suffix))
        return pages

    def dir_maker(self, name: str):
        try:
            os.mkdir(name)
        except FileExistsError:
            pass

    def html_saver(self, one_user_all_cards_urls, contentdir='content'):

        progess_one_user_all_cards_urls = tqdm(one_user_all_cards_urls)
        for one_card_url in progess_one_user_all_cards_urls:

            filename = os.path.split(one_card_url)[1]
            #dirname = os.path.split(os.path.split(os.path.split(one_card_url)[0])[0])[1]
            dirname = self.name

            #name = os.path.split(one_card_url)[1]
            self.dir_maker(contentdir)
            self.dir_maker(contentdir + '/' + dirname)
            #print(name)
            while True:
                try:
                    r = requests.get(one_card_url) #url - ссылка
                    break
                except requests.exceptions.ConnectionError:
                    time.sleep(5)

            html = r.text

            isexist = os.path.exists(contentdir + '/' + dirname + '/' + filename + '.html')
            if isexist:
                pass
            else:
                with open(contentdir + '/' + dirname + '/' + filename + '.html', 'w', encoding='utf-8') as html_file:
                    html_file.write(html)
                    progess_one_user_all_cards_urls.set_description("Processing %s" % one_card_url)

if __name__ == ('__main__'):
    #htmlSaver = HTMLSaver('https://beta.kemono.party/patreon/user/50768560', 'OtherVAM')
    htmlSaver = HTMLSaver('https://beta.kemono.party/patreon/user/8261834','s p l i n e VR')
    one_user_all_cards_urls = htmlSaver.get_all_cards()
    htmlSaver.html_saver(one_user_all_cards_urls)
    #print(htmlSaver.get_pagination())


