from bs4 import (
    Tag,
    NavigableString
)
from .warnings import warn_unequal_syllables
from .phonofactory import PhonoFactory


class HtmlParser:

    @staticmethod
    def word_parse(word_dict):
        """Parse a word dictionary.

        A word dictionary contains the word's orthographic and phonemic transcription embedded
        in HTML. The word's syllables are separated by special symbols and the syllabics are
        denoted by HTML tags such as <u> or <b>.

        A namedtuple is used to represent each syllable, its transcriptions and syllabics; this
        structure eases the construction of a Phono object.

        :param word_dict: Dictionary containing a word's ortho and phono transcriptions
        :return: List of namedtuple's
        """
        ortho_transcription = HtmlParser._ortho_parse(word_dict['ortho'])
        phono_transcription = HtmlParser._phono_parse(word_dict['phono'])

        if not len(ortho_transcription) == len(phono_transcription):
            warn_unequal_syllables(ortho_transcription, phono_transcription)

        phonos = PhonoFactory.create(ortho_transcription, phono_transcription)

        return phonos

    @staticmethod
    def _ortho_parse(td_tag):
        """Parse a <td> ortho tag into a manageable format.

        :param td_tag: <td> Tag of the orthography transcription of a word
        :return: List of OrthoSyl namedtuple
        """

        # OrthoSyl = namedtuple('OrthoSyl', ['ortho', 'strongaccent', 'weakaccent'])
        a_tag = td_tag.find('a')

        syllables = []
        for i, content in enumerate(a_tag.contents):
            syl_str = list(content.stripped_strings)[0] if type(content) is Tag else str(content)

            # Hop out the '·'
            if syl_str in '·':
                continue

            syl_accents = HtmlParser._markup_tags(content)
            has_strong_accent = True if 'b' in syl_accents else False
            has_weak_accent = True if 'u' in syl_accents else False

            assert has_weak_accent if has_strong_accent else True, """If the syllable is 
            strongly accented it also must be weakly accented"""

            s = {
                'ortho': syl_str,
                'strong_accent': has_strong_accent,
                'weak_accent': has_weak_accent
            }
            syllables.append(s)

        syllables = HtmlParser._split_hyphens(syllables)
        #syllables = HtmlParser._agglutinate_hyphens(syllables)
        syllables = HtmlParser._mark_hyphens(syllables)
        return syllables

    @staticmethod
    def _markup_tags(syl_tag):
        """

        :param syl_tag:
        :return:
        """
        if type(syl_tag) is Tag:
            assert len(list(syl_tag.children)) == 1, "Tag doesn't have an only child"
            return HtmlParser._markup_tags(list(syl_tag.children)[0]) + [syl_tag.name]
        elif type(syl_tag) is NavigableString:
            return []
        else:
            return False

    @staticmethod
    def _phono_parse(td_tag):
        """Parse a <td> phono tag into a manageable format.

        :param td_tag: <td> Tag of the phonemic transcription of a word
        :return: List of strings with phonemic transcription of a word
        """

        strings = list(td_tag.stripped_strings)
        if strings:
            phono_str = list(td_tag.stripped_strings)[0]
            return phono_str.split('.')
        else:
            return []

    @staticmethod
    def _split_hyphens(syls):
        """

        :param syls:
        :return:
        """
        splitted = []
        for syl in syls:
            ortho = syl['ortho']
            assert (ortho.count('-') > 1) is False, 'Multiple instances of hyphens'

            hyphen_i = ortho.find('-') # abe-be
            if hyphen_i in range(1, len(ortho)-2):
                before_hyphen = ortho[:hyphen_i+1]
                after_hyphen = ortho[hyphen_i+1:]

                splitted.append({
                    'ortho': before_hyphen,
                    'strong_accent': syl['strong_accent'],
                    'weak_accent': syl['weak_accent']
                })
                splitted.append({
                    'ortho': after_hyphen,
                    'strong_accent': syl['strong_accent'],
                    'weak_accent': syl['weak_accent']
                })
            else:
                splitted.append(syl)

        return splitted

    @staticmethod
    def _agglutinate_hyphens(syls):
        '''

        :param syls:
        :return:
        '''



    @staticmethod
    def _mark_hyphens(syls):
        """Separate two not HTML markup'd hyphenated syllables

        :param syls: List of syls
        :return: List of syls with hyphen property
        """
        # Syls might have hyphens in every combination: -syl, syl-, -syl- or syl-syl

        hyphen_syls = []
        for i, syl in enumerate(syls):
            ortho = syl['ortho']
            hyphen_positions = [i for i, char in enumerate(ortho) if char == '-']

            if 1 in hyphen_positions and not i == 0:
                hyphen_syls.append(i - 1)
            if len(ortho)-1 in hyphen_positions:
                hyphen_syls.append(i)
            
        return syls
