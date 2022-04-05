from core.wordlist.load import load_wordlist


def clean_wordlist(path_file_wordlist: str, path_file_wordstodelete: str):
    wordlist_toclean = load_wordlist(
        path_file_wordlist=path_file_wordlist, shuffle_words=False
    )

    words_todelete = load_wordlist(
        path_file_wordlist=path_file_wordstodelete, shuffle_words=False
    )

    for word in words_todelete:
        wordlist_toclean.remove(word)

    save_wordlist(path_file_wordlist=path_file_wordlist, words=wordlist_toclean)


def save_wordlist(path_file_wordlist: str, words: list[str]):
    with open(path_file_wordlist, "w") as fp:
        fp.writelines(words)
