from warnings import warn


def warn_unequal_syllables(ortho, phono, msg=None):
    if msg is None:
        msg = """
        The orthographic and phonemic transcription of the word have different numbers of 
        syllables {num_ortho} ortho ones to {num_phono} phono ones.
        Ortho transcription: {ortho_trans}
        Phono transcription: {phono_trans}
        """

        ortho_trans = ", ".join([syl['ortho'] for syl in ortho])
        phono_trans = ", ".join(phono)

        msg = msg.format(
            num_ortho=str(len(ortho)),
            num_phono=str(len(phono)),
            ortho_trans=ortho_trans,
            phono_trans=phono_trans
        )

    warn(msg, stacklevel=2)
