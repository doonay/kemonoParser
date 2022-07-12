'''
Перепилить так:
сначала асинхронно парсим только id и ссылку в список словарей
потом проверяем, есть ли этот айди в базе
если есть - дропаем
если нет - парсим всю карточку
'''

#import httplib2
#from urllib.parse import urlparse
#import os
#import asyncio
import requests
from bs4 import BeautifulSoup
import json
import sqlite3

class Card():
    card_id = None
    service_name = None
    card_name = None
    card_link = None
    img_icon = None
    style = None
    card_style = None
    timestrap = None

class Parser():
    def get_json_cards_file(self, page: str):
        r = requests.get(page)
        print(r.status_code)

        with open('data.json', 'w', encoding='utf-8') as json_file:
            json.dump(r.json(), json_file, ensure_ascii=False, indent=4)

    def json_file_parser(self) -> list:
        #открыть файл
        #взять запись
        #создать объект карточки и добавить в список

        #в гуи вывести карточку(временно в консоли распечатать)
        with open('data.json', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        all_cards_list = []
        for card_item in json_data:
            card = Card()
            card.id = card_item.get('id')
            card.indexed = card_item.get('indexed')
            card.name = card_item.get('name')
            card.service = card_item.get('service')
            card.updated = card_item.get('updated')
            card.img_icon = 'https://beta.kemono.party/icons/patreon/' + card.id
            card.img_bg = 'https://beta.kemono.party/banners/patreon/' + card.id
            all_cards_list.append(card)
        return all_cards_list


    def get_patreon_cards(self, all_cards_list: list) -> list:
        patreon_cards_list = []
        for card in all_cards_list:
            if card.service == 'patreon':
                patreon_cards_list.append(card)
        return patreon_cards_list

    def get_pagination(self, site):

        r = requests.get(site)
        print(r.status_code)
        soup = BeautifulSoup(r.text, 'lxml')
        x = soup.small.get_text().strip().rfind(' ') + 1

        return soup.small.get_text().strip()[x:]

    def get_all_cards(self, site):
        baseurl = 'https://beta.kemono.party/artists/updated'
        pagination = self.get_pagination(site)
        '''
        1 = просто
        2 = 25
        3 = 50
        4 = 75
        т.е. шаг цикла = 25
        '''
        for page in range(1, int(pagination), 25):
            url = baseurl + '?o=' + str(page)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            raw_cards = soup.find('div', class_="card-list__items").find_all('a')

        return raw_cards

    def base_creator(self):

        '''
        id INTEGER PRIMARY KEY, #базовый ключ

        card_id TEXT NOT NULL UNIQUE, # айди карты (9746051)
        service_name TEXT, # Название сервиса (Pathreon)
        card_name TEXT, # Имя автора (Joopa)
        card_link TEXT, # Ссылка внутрь карточки (https://beta.kemono.party/fanbox/user/9746051)
        img_icon TEXT, # Ссылка на иконку автора https://beta.kemono.party/icons/fanbox/18893485
        style TEXT, # Цвет бэкграунда карточки, если нет баннера (background-color: #2c333c;)
        card_style TEXT, # Стиль карточки (тут же и бэкграунд) (background-image: linear-gradient(rgb(0 0 0 / 50%)...)
        timestrap DATETIME NOT NULL, # Дата создания поста (2022-07-12 01:32:08.035047)
        '''

        try:
            conn = sqlite3.connect('kemono.db')
            print(conn.total_changes)
            print("База данных подключена к SQLite")

            cursor = conn.cursor()
            sqlite_create_table_query = '''CREATE TABLE kemonocards(
                                        id INTEGER PRIMARY KEY,
                                        card_id TEXT NOT NULL UNIQUE,
                                        service_name TEXT,
                                        card_name TEXT,
                                        card_link TEXT,
                                        img_icon TEXT,
                                        style TEXT,
                                        card_style TEXT,
                                        timestrap DATETIME)
                                        '''

            cursor.execute(sqlite_create_table_query)
            conn.commit()
            print("Таблица SQLite создана")
            cursor.close()

        except sqlite3.Error as error:
            print("Функция создания базы. Ошибка при подключении к sqlite", error)
        finally:
            if (conn):
                conn.close()
                print("Соединение с SQLite закрыто")

    def base_runner(self, card):
        sqlite_connection = sqlite3.connect('kemono.db')
        #card.card_id, card.service_name, card.card_name, card.card_link, card.img_icon, card.style, card.card_style, card.timestrap]

        '''
        id INTEGER PRIMARY KEY, #базовый ключ

        card_id TEXT NOT NULL UNIQUE, # айди карты (9746051)
        service_name TEXT, # Название сервиса (Pathreon)
        card_name TEXT, # Имя автора (Joopa)
        card_link TEXT, # Ссылка внутрь карточки (https://beta.kemono.party/fanbox/user/9746051)
        img_icon TEXT, # Ссылка на иконку автора https://beta.kemono.party/icons/fanbox/18893485
        style TEXT, # Цвет бэкграунда карточки, если нет баннера (background-color: #2c333c;)
        card_style TEXT, # Стиль карточки (тут же и бэкграунд) (background-image: linear-gradient(rgb(0 0 0 / 50%)...)
        timestrap DATETIME NOT NULL, # Дата создания поста (2022-07-12 01:32:08.035047)
        '''

        try:
            conn = sqlite3.connect('kemono.db')
            cursor = conn.cursor()
            print("База данных подключена к SQLite")
            #[card_id, service_name, card_name, card_link, img_icon, style, card_style, timestrap]
            #card[0], card[1], card[2], card[3], card[4], card[5], card[6], card[7]
            data = [card.card_id, card.service_name, card.card_name, card.card_link, card.img_icon, card.style, card.card_style, card.timestrap]
            cursor.execute("INSERT INTO kemonocards(card_id, service_name, card_name, card_link, img_icon, style, card_style, timestrap) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
            print('Данные карты', card.card_name, 'успешно добавлены')
            cursor.close()
            conn.commit()



        except sqlite3.Error as error:
            print("Функция добавления данных. Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def base_reader(self):
        conn = sqlite3.connect("kemono.db")
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM kemonocards").fetchall()
        print(rows)

if __name__ == '__main__':

    # для гуя - фоновый цвет подложки под категорию Patreon - background-color: rgb(250, 87, 66);
    # - стиль бакграундовой картинки - background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.8)), url("/banners/patreon/53460849");
    host = 'https://beta.kemono.party'
    url = host + '/artists/updated'

    parser = Parser()

    print(parser.get_pagination(url))

    raw_all_cards = parser.get_all_cards(url)

    #test
    cards = []
    for raw_card in raw_all_cards: # Создаю объект карты
        card = Card()
        card.card_id = raw_card.get('data-id')      # card_id TEXT NOT NULL UNIQUE, #9746051 айди карты
        card.service_name = raw_card.find('span', class_="user-card__service").get_text().strip() # card_name TEXT, #Название сервиса
        card.card_name = raw_card.find('div', class_="user-card__name").get_text() #Имя автора
        card.card_link = host + raw_card.get('href')  # card_link, # ссылка внутрь карточки https://beta.kemono.party/fanbox/user/9746051
        card.img_icon = host + raw_card.find('img', class_="fancy-image__image").get('src') # img_icon TEXT, #ссылка на иконку автора https://beta.kemono.party/icons/fanbox/18893485
        card.style = raw_card.find('span', class_="user-card__service").get('style') # style TEXT,  #бэкграунд карточки, если нет пикчи. так же в джэйсоне хранить. background-color: #2c333c;
        card.card_style = raw_card.get('data-style')   # card_style TEXT, # стиль карточки (тут же и бэкграунд). почитать, как хранить и возвращать json, background-image: linear-gradient(rgb(0 0 0 / 50%), rgb(0 0 0 / 80%)), url(/banners/fanbox/18893485);
        card.timestrap = raw_card.find('time').get('datetime') # timestrap DATETIME NOT NULL, #datetime 2022-07-12 01:32:08.035047
        cards.append(card)

    print('----')

    parser.base_creator()

    for card in cards:
        parser.base_runner(card)

    #parser.base_reader()







    '''
    #получить переадресацию с основного урла на апи
    artist_search_json_url = 'https://beta.kemono.party/api/creators'

    post_search_url = 'https://beta.kemono.party/posts?q=vam'
    artist_recent_url = 'https://beta.kemono.party/artists/updated'

    parser = Parser()
    #parser.get_json_cards_file(artist_search_json_url)
    print('Json file done!')

    all_cards_list = parser.json_file_parser()
    patreon_cards_list = parser.get_patreon_cards(all_cards_list)
    patreon_card0 = patreon_cards_list[0]
    print(patreon_card0.id)
    print(patreon_card0.indexed)
    print(patreon_card0.name)
    print(patreon_card0.service)
    print(patreon_card0.updated)
    print(patreon_card0.img_icon)
    print(patreon_card0.img_bg)
    print('=======')


    #parser.get_json_cards_file(self, page)
    #parser.json_file_parser()
    #parser.get_patreon_cards(self, all_cards_list)
    '''