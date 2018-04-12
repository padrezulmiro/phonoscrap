from .phonos import Phonos


class PhonoFactory:

    @staticmethod
    def create(*args):
        if all(args):
            return Phonos(*args)
        else:
            print('Empty transcription')

    @staticmethod
    def _join_ortho_vowels(ortho_syls, phono_syls):
        pass
