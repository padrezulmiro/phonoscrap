def generate_url(search):
    """
    :param search: Dictionary {letter: (start, stop)}

    """
    page_url = '&letter={}&start={}'
    words_per_page = 20

    for letter, word_range in search.items():
        word_ids = range(word_range[0], word_range[1], words_per_page)

        for word_num in word_ids:
            yield page_url.format(letter, word_num)

