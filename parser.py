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
    img_icon = None
    img_bg = None

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

if __name__ == '__main__':
    # для гуя - фоновый цвет подложки под категорию Patreon - background-color: rgb(250, 87, 66);
    # - стиль бакграундовой картинки - background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.8)), url("/banners/patreon/53460849");
    main_url = 'https://beta.kemono.party/'
    artist_search_url = 'https://beta.kemono.party/artists'
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