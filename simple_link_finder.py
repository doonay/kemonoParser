# Парсинг прямых ссылок со страницы кемоно
#file:///C:/data/b6/02/b602c287a73a80106dff5d28d4363e87e7eac1ea7dfe57cffaa3ab75a803c9e4.mp4?f=SlapDoggy%20v1.mp4
#нужно заменить на
#https://beta.kemono.party/data/9a/33/9a33703b22bfb430ff852e515fb80fbf325a7e292bacb8e16d408854fc961bd1.zip?f=jyy.Bunny.1.var
#а именно 'file:///C:' на 'https://beta.kemono.party'
#сначала ищем всё, что начинатеся на 'file:///C:'
import os
from bs4 import BeautifulSoup

def link_finder():
    dir_files_list = os.listdir()
    links = []

    for file in dir_files_list:
        if file.rfind('.html') != -1:
            with open(file, 'r', encoding='utf-8') as html:
                soup = BeautifulSoup(html.read(), 'html.parser')
                a_links = soup.find_all('a')
                for link in a_links:
                    print(link.get('href')) #/data/f8/64/f864ee26fb9cb6193d9358de5295655c6d5de24dedad71438d86addf1550a553.zip?f=jyy.Her_Private_Life.1.var
                    if link.get('href').find('/data') == 0:
                        links.append('https://beta.kemono.party' + link.get('href'))

    print(links)
    for link in links:
        with open('simple_links.txt', 'a', encoding='utf-8') as out_file:
            out_file.write(link + '\n')


link_finder()