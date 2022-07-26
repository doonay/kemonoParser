import requests
from bs4 import BeautifulSoup

def mega_parser(link):
    'https://mega.nz/file/lR9wnRyK#-eOWOuzlTOgov6OajytWaD0-2LNpt-_7y4aFBK55ucI'
    'chrome-extension://bigefpfhnfcobdlfbedofhhaibnlghod/mega/secure.html#file/lR9wnRyK#-eOWOuzlTOgov6OajytWaD0-2LNpt-_7y4aFBK55ucI'
    url = link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    print(soup.find('div', {'class': ["title-block", "big-txt"]}))
    '''
    mega = Mega()
    m = mega.login()
    #file = m.find('myfile.doc')
    #m.download(file)
    m.download_url('https://mega.co.nz/#!utYjgSTQ!OM4U3V5v_W4N5edSo0wolg1D5H0fwSrLD3oLnLuS9pc')
    
    m.download(file, '/home/john-smith/Desktop')
    # specify optional download filename (download_url() supports this also)
    m.download(file, '/home/john-smith/Desktop', 'myfile.zip')
    '''
if __name__ == '__main__':
    mega_parser('https://mega.nz/file/lR9wnRyK#-eOWOuzlTOgov6OajytWaD0-2LNpt-_7y4aFBK55ucI')