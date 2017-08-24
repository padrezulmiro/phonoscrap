import requests, lxml
from bs4 import BeautifulSoup as beau

r = requests.get('http://portaldalinguaportuguesa.org/index.php?action=fonetica&act=list&region=lbx')
soup = beau(r.text, 'lxml')
s_rollovertable = beau(str(soup.find(id='rollovertable')), 'lxml')

for i, word in enumerate(s_rollovertable.find_all('tr')):
    print('Word no. ' + str(i))
    print(word.prettify())