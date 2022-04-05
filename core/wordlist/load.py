import random


def load_wordlist(path_file_wordlist: str, shuffle_words: bool):
    with open(path_file_wordlist, "r") as fp:
        word_list = fp.readlines()
    if shuffle_words:
        random.shuffle(word_list)
    return word_list
