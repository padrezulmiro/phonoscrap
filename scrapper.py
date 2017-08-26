import requests, lxml
from bs4 import BeautifulSoup as beau

url = 'http://portaldalinguaportuguesa.org/index.php?action=fonetica&act=list&region=lbx'
parser = 'lxml'

r = requests.get(url)
soup = beau(r.text, parser)

soup_wordtable = beau(str(soup.find(id='rollovertable')), parser)

for i, word in enumerate(soup_wordtable.find_all('tr')[1:]):
    word_dict = {}

    for content in word.contents[1:]:
        print(content.prettify())