import requests
from bs4 import (
    BeautifulSoup as Beau,
    Tag,
    NavigableString
)
from collections import namedtuple


def main():
    homeurl = 'http://portaldalinguaportuguesa.org/index.php'
    query = '?action=fonetica&act=list&region=lbx'
    p = 'html5lib'

    soup = Beau(requests.get(homeurl+query).text, p)
    identifiers = ['ortho', 'grammar', 'phono']
    wordtable = soup.find(id='rollovertable')('tr')[1:]
    worddicts = [dict(zip(identifiers, word.contents[1:])) for word in wordtable]
    parsed_words = [word_parse(w) for w in worddicts]
    print()


def word_parse(word):
    """Parse a word dictionary.

    A word dictionary contains the word's orthographic and phonemic transcription embedded in
    HTML. The word's syllables are separated by special symbols and the syllabics are denoted
    by HTML tags such as <u> or <b>.

    A namedtuple is used to represent each syllable, its transcriptions and syllabics; this
    structure eases the construction of a Phono object.

    :param word: Dictionary containing a word's ortho and phono transcriptions
    :return: List of namedtuple's
    """
    Syl = namedtuple('Syl', ['ortho', 'phono', 'strongaccent', 'weakaccent', 'previous'])
    otrans = ortho_parse(word['ortho'])
    ptrans = phono_parse(word['phono'])
    assert len(otrans) == len(ptrans), """The orthographic and phonemic transcriptions 
    of the word have a different number of syllables.
    """

    parsed = []
    for i, ot in enumerate(otrans):
        s = Syl(
            ot.ortho,
            ptrans[i],
            ot.strongaccent,
            ot.weakaccent,
            ot.previous
        )
        parsed.append(s)

    return parsed


def ortho_parse(td_tag):
    """Parse a <td> ortho tag into a manageable format.

    :param td_tag: <td> Tag of the orthography transcription of a word
    :return: List of OrthoSyl namedtuple
    """

    a_tag = td_tag.find('a')
    OrthoSyl = namedtuple('OrthoSyl', ['ortho', 'strongaccent', 'weakaccent', 'previous'])
    previous_index = ''.join(a_tag.stripped_strings).find('-')

    syllables = []
    for i, content in enumerate(a_tag.contents):
        syl_str = list(content.stripped_strings)[0] if type(content) is Tag else str(content)

        # Hop out the '·'
        if syl_str in '·':
            continue


        syl_accents = markup_tags(content)
        has_strongaccent = True if 'b' in syl_accents else False
        has_weakaccent = True if 'u' in syl_accents else False
        is_previous = True if i < previous_index else False

        assert has_weakaccent if has_strongaccent else True, """If the syllable is strongly
        accented it also must be weakly accented
        """

        s = OrthoSyl(syl_str, has_weakaccent, has_strongaccent, is_previous)
        syllables.append(s)

    return clean_hyphen(syllables)


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
    """Parse a <td> phono tag into a manageable format.

    :param td_tag: <td> Tag of the phonemic transcription of a word
    :return: List of strings with phonemic transcription of a word
    """
    phono_str = list(td_tag.stripped_strings)[0]
    return phono_str.split('.')


def clean_hyphen(syls):
    """Separate two not HTML markup'd hyphenated syllables

    :param syls: List of syls
    :return: Cleaned list of syls
    """
    cleaned_syls = []
    for syl in syls:
        if '-' in syl:
            partition = syl.partition('-')
            cleaned_syls.append(partition[0])
            cleaned_syls.append(partition[2])
        else:
            cleaned_syls.append()
main()


