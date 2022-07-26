import os
from bs4 import BeautifulSoup

dir_files_list = os.listdir()
mega_links = []

for file in dir_files_list:
    if file.rfind('.html') != -1:
        #print(file[-5:])
        #print(file)
        with open(file, 'r', encoding='utf-8') as html:
            soup = BeautifulSoup(html.read(), 'html.parser')
            links = soup.find_all('a')
            #https://mega.nz/file/9UtikSbJ#2zVSlSsI4HYQivFEvVwWZ8wGg_2kt_xt0i0g8LtoMSM
            for link in links:
                if link.get('href').find('https://drive.google.com') == 0:
                    mega_links.append(link.get('href'))


for link in mega_links:
    with open('google_links.txt', 'a', encoding='utf-8') as out_file:
        out_file.write(link + '\n')