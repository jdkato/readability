import collections
import html


import bs4
import requests
import syntok.segmenter as segmenter

from readability.ast import HTMLToAST


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

    def __init__(self, html: str):
        self.parser.feed(html)
        for node in self.parser.nodes:
            for paragraph in segmenter.analyze(node["text"]):
                for sentence in paragraph:
                    self.sent_count += 1
                    for token in sentence:
                        word = token.value
                        size = len(word)

                        self.char_count += size
                        self.word_freq[word] += 1

                        if size > 6:
                            self.long_word_count += 1
