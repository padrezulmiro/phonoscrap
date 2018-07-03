import requests
from bs4 import BeautifulSoup as bs
from src.utils.utils import generate_url

parser = 'html5lib'
home_url = 'http://portaldalinguaportuguesa.org/index.php?action=fonetica&act=list&region=lbx'

search = {
    'b': (0, 2500)
}
queries = generate_url(search)

chars = set()
for query in queries:
    soup = bs(requests.get(home_url + query).text, parser)
    tags = soup('td', title='Fonética')

    for tag in tags:
        stripped = list(tag.stripped_strings)

        if len(stripped) is not 0:
            word = list(tag.stripped_strings)[0]
            word = word.replace('.', '')
            word_chars = set(word)
            chars = chars | word_chars

print(len(chars))
