from bs4 import (
    Tag,
    NavigableString
)
from collections import namedtuple
from copy import deepcopy
from .warnings import warn_unequal_syllables


class HtmlParser:

    @staticmethod
    def word_parse(word):
        """Parse a word dictionary.

        A word dictionary contains the word's orthographic and phonemic transcription embedded
        in HTML. The word's syllables are separated by special symbols and the syllabics are
        denoted by HTML tags such as <u> or <b>.

        A namedtuple is used to represent each syllable, its transcriptions and syllabics; this
        structure eases the construction of a Phono object.

        :param word: Dictionary containing a word's ortho and phono transcriptions
        :return: List of namedtuple's
        """
        self = HtmlParser()
        Syl = namedtuple('Syl', ['ortho', 'phono', 'strongaccent', 'weakaccent', 'previous'])

        ortho_transcription = self._ortho_parse(word['ortho'])
        phono_transcription = self._phono_parse(word['phono'])

        if not len(ortho_transcription) == len(phono_transcription):
            warn_unequal_syllables(ortho_transcription, phono_transcription)

        # parsed = []
        # for i, ot in enumerate(ortho_transcription):
        #     s = Syl(
        #         ot.ortho,
        #         phono_transcription[i],
        #         ot.strongaccent,
        #         ot.weakaccent,
        #         ot.previous
        #     )
        #     parsed.append(s)
        #
        # return parsed

    def _ortho_parse(self, td_tag):
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

            syl_accents = self._markup_tags(content)
            has_strong_accent = True if 'b' in syl_accents else False
            has_weak_accent = True if 'u' in syl_accents else False
            is_previous = True if i < previous_index else False

            assert has_weak_accent if has_strong_accent else True, """If the syllable is strongly
            accented it also must be weakly accented
            """

            s = OrthoSyl(syl_str, has_weak_accent, has_strong_accent, is_previous)
            syllables.append(s)

        return self._clean_hyphen(syllables)

    def _markup_tags(self, syltag):
        """

        :param syltag:
        :return:
        """
        if type(syltag) is Tag:
            assert len(list(syltag.children)) == 1, "Tag doesn't have just a sole child"
            return self._markup_tags(list(syltag.children)[0]) + [syltag.name]
        elif type(syltag) is NavigableString:
            return []
        else:
            return False

    def _phono_parse(self, td_tag):
        """Parse a <td> phono tag into a manageable format.

        :param td_tag: <td> Tag of the phonemic transcription of a word
        :return: List of strings with phonemic transcription of a word
        """
        phono_str = list(td_tag.stripped_strings)[0]
        return phono_str.split('.')

    def _clean_hyphen(self, syls):
        """Separate two not HTML markup'd hyphenated syllables

        :param syls: List of syls
        :return: Cleaned list of syls
        """

        cleaned_syls = []
        for syl in syls:
            ortho = syl.ortho

            if ortho == '-':
                continue

            if '-' in ortho:
                partition = ortho.partition('-')

                # todo hacking big time with the following if statements
                if partition[0]:
                    first_syl = deepcopy(syl)
                    first_syl = first_syl._replace(ortho=partition[0])
                    cleaned_syls.append(first_syl)

                if partition[2]:
                    second_syl = deepcopy(syl)
                    second_syl = second_syl._replace(ortho=partition[2])
                    cleaned_syls.append(second_syl)

            else:
                cleaned_syls.append(syl)

        return cleaned_syls
