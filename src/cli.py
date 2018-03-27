import requests
from bs4 import BeautifulSoup as BS
from .htmlparser import word_parse


def main():
    home_url = 'http://portaldalinguaportuguesa.org/index.php'
    query = '?action=fonetica&act=list&region=lbx'
    parser = 'html5lib'

    soup = BS(requests.get(home_url + query).text, parser)

    identifiers = ['ortho', 'grammar', 'phono']
    word_table = soup.find(id='rollovertable')('tr')[1:]
    word_dicts = [dict(zip(identifiers, word.contents[1:])) for word in word_table]

    print()
    parsed_words = [word_parse(w) for w in word_dicts]



