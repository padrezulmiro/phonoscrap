import requests
from bs4 import (
    BeautifulSoup as Beau,
    Tag,
    NavigableString
)
from collections import namedtuple

def main():
    url = 'http://portaldalinguaportuguesa.org/index.php?action=fonetica&act=list&region=lbx'
    p = 'html5lib'

    soup = Beau(requests.get(url).text, p)
    identifiers = ['ortho', 'grammar', 'phono']
    wordtable = soup.find(id='rollovertable')('tr')[1:]
    worddicts = [dict(zip(identifiers, word.contents[1:])) for word in wordtable]
    for word in worddicts:
        word['ortho'] = ortho_parse(word['ortho'])
        word['grammar'] = list(word['grammar'].stripped_strings)[0]
    print()


def ortho_parse(td_tag):
    """Parse a <td> ortho tag into a manageable format

    :param td_tag: <td> Tag of the orthography transcription of a word
    :return: List of Syllable namedtuple
    """
    a_tag = td_tag.find('a')
    Syllable = namedtuple('Syllable', ['ortho', 'strongaccent', 'weakaccent', 'previous'])
    syllables = []
    previous_index = ''.join(a_tag.stripped_strings).find('-')
    for i, content in enumerate(a_tag.contents):
        syl_str = list(content.stripped_strings)[0] if type(content) is Tag else str(content)

        # Filter out '·' and '-'
        syl_str = syl_str.replace('-', '')
        if syl_str in '·':
            continue

        syl_accents = markup_tags(content)
        has_strongaccent = True if 'b' in syl_accents else False
        has_weakaccent = True if 'u' in syl_accents else False
        is_previous = True if i < previous_index else False

        assertion = has_weakaccent if has_strongaccent else True
        assert_msg = 'If the syllable is strongly accented it also must be weakly accented'
        assert assertion, assert_msg

        s = Syllable(syl_str, has_weakaccent, has_strongaccent, is_previous)
        syllables.append(s)

    return syllables

def markup_tags(syltag):
    """

    :param syltag:
    :return:
    """
    if type(syltag) is Tag:
        assert len(list(syltag.children)) == 1, "Tag doesn't have just a sole child"
        return markup_tags(list(syltag.children)[0]) + [syltag.name]
    elif type(syltag) is NavigableString:
        return []
    else:
        return False
    

def phono_parse(td_tag):
    pass

main()


