import requests
from bs4 import BeautifulSoup as bs
from .htmlparser import HtmlParser
from ..utils.utils import generate_url


def main():
    parser = 'html5lib'

    search = {
        'a': (0, 200)
    }
    home_url = 'http://portaldalinguaportuguesa.org/index.php?action=fonetica&act=list&region=lbx'
    queries = generate_url(search)

    for query in queries:
        soup = bs(requests.get(home_url + query).text, parser)

        identifiers = ['ortho', 'grammar', 'phono']
        word_table = soup.find(id='rollovertable')('tr')[1:]
        word_dicts = [dict(zip(identifiers, word.contents[1:])) for word in word_table]

        parsed_words = [HtmlParser.word_parse(w) for w in word_dicts]
        print()
