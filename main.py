import logging
import random

import requests
import time
import json
from requests.sessions import Session
from threading import local

from common.threading_utils import execute_map_threads
from core.wordlist.clean import clean_wordlist
from core.wordlist.load import load_wordlist

PATH_FILE_WORDLIST = "data/wordlist_fr.txt"
THRESHOLD_SCORE = 975
MAX_WORKERS = 200
SHUFFLE_WORDS = True

URL = "https://cemantix.herokuapp.com/score"
THREAD_LOCAL = local()
RESULTS = dict()


def main():
    global RESULTS

    word_list = load_wordlist(
        path_file_wordlist=PATH_FILE_WORDLIST, shuffle_words=SHUFFLE_WORDS
    )

    start = time.time()
    execute_map_threads(func=submit_word, iterable=word_list, max_workers=MAX_WORKERS)
    end = time.time()
    print(f"Total time: {end - start} seconds")

    # Sort & show results
    RESULTS = {
        word: response
        for word, response in sorted(
            RESULTS.items(), key=lambda resp: resp[1]["percentile"], reverse=True
        )
    }

    print(f"{'word':<16}  {'percentile':>10} {'score':>10}")
    for word, response in RESULTS.items():
        print(_format_result(word, response))


def submit_word(word: str):
    word = word.strip()
    session = get_session()
    with session.post(URL, data={"word": word}) as response:
        response = json.loads(response.text)
        if "error" in response.keys():
            logging.warning(response["error"])
        else:
            if response["percentile"] >= THRESHOLD_SCORE:
                RESULTS[word] = response


def get_session() -> Session:
    if not hasattr(THREAD_LOCAL, "session"):
        THREAD_LOCAL.session = requests.Session()
    return THREAD_LOCAL.session


def extract_wrong_word(error_message: str) -> str:
    return error_message.split("<i>")[1][:-5]


def _format_result(word: str, response: dict) -> str:
    return f"{word:<16}:{response['percentile']:>10}‰ {response['score']:>10}"


if __name__ == "__main__":
    main()
