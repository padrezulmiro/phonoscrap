import requests
from bs4 import BeautifulSoup as bs
from .htmlparser import HtmlParser


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


def generate_url(search):
    """
    :param search: Dictionary {letter: (start, stop)}

    """
    page_url = '&letter={}&start={}'
    words_per_page = 20

    for letter, word_range in search.items():
        word_ids = range(word_range[0], word_range[1], words_per_page)

        for word_num in word_ids:
            yield page_url.format(letter, word_num)
