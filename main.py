from parser import Parser

artist_search_json_url = 'https://beta.kemono.party/api/creators'

parser = Parser()
#parser.get_json_cards_file(artist_search_json_url)
print('Json file done!')
all_cards_list = parser.json_file_parser()
patreon_cards_list = parser.get_patreon_cards(all_cards_list)

patreon_card0 = patreon_cards_list[0]

for i in range(10):
    print(patreon_cards_list[i].id)
    print(patreon_cards_list[i].indexed)
    print(patreon_cards_list[i].name)
    print(patreon_cards_list[i].service)
    print(patreon_cards_list[i].updated)
    print(patreon_cards_list[i].img_icon)
    print(patreon_cards_list[i].img_bg)
    print('=======')