#import httplib2
#from urllib.parse import urlparse
#import os
#import asyncio
import requests
from bs4 import BeautifulSoup
import json

class Card():
    id = None
    indexed = None
    name = None
    service = None
    updated = None

class UserPageParser():

    def get_user_id(self, pathreon_user_url):
        with open('data.txt', 'a', encoding='utf-8') as file:
            file.write(pathreon_user_url.split('/')[-1] + '\n')

        return pathreon_user_url.split('/')[-1]


    def get_pagination_count(self, pathreon_user_id):

        ###на вермя тестов
        '''
        with open("pathreon_user_url.html", encoding='utf-8') as f:
            pathreon_user_url = f.read()
            soup = BeautifulSoup(pathreon_user_url, 'lxml')
            pagination_menu = soup.menu.find_all('a')
            last_page = pagination_menu[-2].get('href')
            x = last_page.rfind('=') + 1
            try:
                last_post = int(last_page[x:])
                print('Всего постов:', last_post)
            except:
                print('Пагинация не сконвертилась в целое число. Проверить ссылку на последнюю страницу.')


            for post in range(0, last_post+1, 25):
                pagination_links_list.append(pathreon_user_url + '/?o=' + str(post))
                print('https://beta.kemono.party/patreon/user/31211919?o=' + str(post))
            print()
        return pagination_links_list
        '''

        #боевой вариант
        pathreon_user_url = 'https://beta.kemono.party/patreon/user/' + pathreon_user_id
        r = requests.get(pathreon_user_url)
        soup = BeautifulSoup(r.text, 'lxml')
        text = soup.find('div', {'class': 'paginator', 'id': 'paginator-top'}).small.get_text()
        x = text.strip().rfind(' ') + 1
        pagination_links_list = text.strip()[x:]

        return pagination_links_list


    def get_pages_links(self, pathreon_user_id, last_post):
        pathreon_user_url = 'https://beta.kemono.party/patreon/user/' + pathreon_user_id
        # имеем https://beta.kemono.party/patreon/user/29268099?o=75
        pagination_links_list = []
        # надо все https://beta.kemono.party/patreon/user/29268099/post/39810492
        for post in range(0, int(last_post)+1, 25):
            pagination_links_list.append(pathreon_user_url + '/?o=' + str(post))
        return pagination_links_list


    def get_posts_links(self, posts_list):
        #получаем список страниц с поставми
        #парсим ссылки на посты
        #возвращаем список ссылок на посты
        posts_links_list = []
        for url in posts_list:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            all_articles = soup.find_all('article', class_="post-card")
            for article in all_articles:
                posts_links_list.append('https://beta.kemono.party' + article.a.get('href'))

        return posts_links_list


    def get_content_link(self, posts_urls):
        hrefs = []
        for post_url in posts_urls:
            r = requests.get(post_url)
            soup = BeautifulSoup(r.text, 'lxml')
            posat_body = soup.find('div', class_="post__body")
            all_links = posat_body.find_all('a')
            for link in all_links:
                hrefs.append(link.get('href'))
        return hrefs

    def filewriter(self, string: str):
        if string.find('https://www.patreon.com/') != -1:
            pass
        elif string.find('https://www.youtube.com/') != -1:
            pass
        elif string.find('https://youtu.be/') != -1:
            pass
        else:
            with open('data.txt', 'a', encoding='utf-8') as file:
                file.write(string + '\n')





if __name__ == '__main__':
    host = 'https://beta.kemono.party/'
    #pathreon_user_url = 'https://beta.kemono.party/patreon/user/31211919'
    pathreon_user_url = 'https://beta.kemono.party/patreon/user/2586706'
    #pathreon_user_url = 'https://beta.kemono.party/patreon/user/29268099' #79
    #pathreon_user_url = 'https://beta.kemono.party/patreon/user/50354292'
    #pathreon_user_url = 'https://beta.kemono.party/patreon/user/58933632'

    user_page_parser = UserPageParser()

    pathreon_user_id = user_page_parser.get_user_id(pathreon_user_url)
    print(pathreon_user_id)

    last_post = user_page_parser.get_pagination_count(pathreon_user_id)
    print(last_post)

    posts_list = user_page_parser.get_pages_links(pathreon_user_id, last_post)
    print(posts_list)

    posts_urls = user_page_parser.get_posts_links(posts_list)
    for post_link in posts_urls:
        print(post_link)

    links = user_page_parser.get_content_link(posts_urls)
    for post_link in links:
        user_page_parser.filewriter(post_link)

    '''
    print('Ссылки на страницы с постами:')
    for link in pagination_links_list:
        print(link)
    print()
    '''
    #inner_links = user_page_parser.get_post_inner_links()
    #for inner_link in inner_links:
    #    print(inner_link)






