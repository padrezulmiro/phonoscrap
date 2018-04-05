import requests
from bs4 import BeautifulSoup as bs
from .htmlparser import HtmlParser


def main():
    home_url = 'http://portaldalinguaportuguesa.org/index.php'
    query = '?action=fonetica&act=list&region=lbx'
    parser = 'html5lib'

    soup = bs(requests.get(home_url + query).text, parser)

    identifiers = ['ortho', 'grammar', 'phono']
    word_table = soup.find(id='rollovertable')('tr')[1:]
    word_dicts = [dict(zip(identifiers, word.contents[1:])) for word in word_table]

    word_example = word_dicts[12]  # abrogatório
    print(word_example)
    parsed_example = HtmlParser.word_parse(word_example)
    parsed_words = [HtmlParser.word_parse(w) for w in word_dicts]



