

class Phonos:

    def __init__(self, ortho, phono):
        """

        :param ortho: List of (ortho, strongaccent, weakaccent, previous) namedtuples
        :param phono: List of phonetic syllables transcriptions
        """
        self._ortho = ortho
        self._phono = phono

    @property
    def ortho(self):
        return self._ortho

    @property
    def phono(self):
        return self._phono

    @property
    def ortho_word(self):
        return "".join([syl.ortho for syl in self.ortho])

    @property
    def phono_word(self):
        return "".join(self.phono)

    @property
    def ortho_strong_accent(self):
        return self._find_strong_accent(self.ortho)

    @property
    def phono_strong_accent(self):
        return self._find_strong_accent(self.phono)

    @property
    def weak_accents(self):
        return filter(lambda syl: syl.weakaccent, self.ortho)

    def _find_strong_accent(self, transcription):
        if transcription is self.ortho:
            def descriminator(syl): return syl.strongaccent
        if transcription is self.phono:
            def descriminator (syl): return "'" in syl

        syls = filter(descriminator, transcription)
        # todo Maybe switch the assertion with an try/except
        assert len(syls) == 1, """Syllable can't have more than one strong accent"""
        return syls[0]
