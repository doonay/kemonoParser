import csv
from html_saver import HTMLSaver


def csv_reader():
    with open('good_links.csv', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter=";")
        count = 0
        for row in file_reader:
            print(row[1])
            html_saver = HTMLSaver(row[0], row[1])
            one_user_all_cards_urls = html_saver.get_all_cards()
            html_saver.html_saver(one_user_all_cards_urls)
            count += 1
        print(f'Всего собрано {count} авторов.')

if __name__ == '__main__':
    csv_reader()