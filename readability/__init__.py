import collections
import html
import string
import re


import bs4
import requests
from requests.sessions import default_headers
import syntok.segmenter as segmenter

from readability.ast import HTMLToAST
from readability.syllables import count_syllables, is_complex
from commonregex import email, link


def fetch(url: str):
    """Get the HTML content of the given URL."""
    r = requests.get(url)
    return html.unescape(r.text)


def parse_html(source: str, sel: dict[str, str], tag="div", from_url=False):
    """Parse an HTML document into a Readability object.

    Supports an HTML string or website URL.
    """
    if from_url:
        source = fetch(source)

    soup = bs4.BeautifulSoup(source, "html.parser")
    body = soup.find(tag, sel)

    return Readability(str(body))


class Readability(object):
    """ """

    parser = HTMLToAST()

    # The number of characters that appear in our document.
    char_count = 0

    # The number of "complex" words that appear in our document.
    #
    # A "complex" word is defined as a multi-syllable word without common
    # suffixes such as "es", "ed", or "ing".
    c_word_count = 0

    # The number of multi-syllable (> 2) words in our document.
    psyll_word_count = 0

    # The number of sentences in our document.
    sent_count = 0

    # The number of syllables in our document.
    syll_count = 0

    # The number of words in our document.
    word_count = 0

    # The number of "long" words in our document.
    #
    # A "long" word is defined as a word with > 6 characters.
    long_word_count = 0

    # A mapping of {word: occurrences}.
    word_freq = collections.defaultdict(int)

    # A list of scopes to process.
    default_scopes = ["paragraph", "list", "blockquote"]

    def __init__(self, html: str, scopes=[]):
        self.parser.feed(html)

        targets = scopes if scopes else self.default_scopes
        for node in self.parser.nodes:
            if node["scope"] not in targets:
                continue

            text = node["text"]
            text = re.sub(email, "", text)
            text = re.sub(link, "", text)

            for paragraph in segmenter.process(text):
                for sentence in paragraph:
                    self.sent_count += 1
                    for token in sentence:
                        word = token.value
                        if word in string.punctuation:
                            continue
                        size = len(word)

                        self.char_count += size
                        self.word_freq[word] += 1

                        if size > 6:
                            self.long_word_count += 1

                        syllables = count_syllables(word)
                        self.syll_count += syllables

                        if syllables > 2:
                            self.psyll_word_count += 1

                        if is_complex(word, syllables):
                            self.c_word_count += 1

                        self.word_count += 1
