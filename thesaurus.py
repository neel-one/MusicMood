from bs4 import BeautifulSoup
import requests 

def findRootandSynonyms(word):
    url = 'https://www.merriam-webster.com/dictionary/' + word + '#synonyms'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.content, "html.parser")

    wd = soup.find('h2')
    wd = wd.find('em')
    word = wd.string
    
    l = [word]

    syns = soup.find(class_ = 'mw-list')
    syn_lst = syns.find_all('a')
    for i in syn_lst:
        l.append(i.string)

    return l