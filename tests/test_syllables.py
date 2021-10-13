import json

import syllables as alt_syll

from readability.syllables import syllables
from hyphen import Hyphenator

HYP_COUNTER = Hyphenator("en_US")


def test_syllables():
    with open("data/syllables.json") as f:
        for word, count in json.load(f).items():
            assert count == syllables(word), word


def test_n_syllables():
    total = 9462.0
    right = 0

    comp = {"pyhyphen": 0, "syllables": 0}

    for n in range(1, 8):
        with open(f"data/{n}-syllable-words.txt") as f:
            for line in f.readlines():
                word = line.strip()
                if syllables(word) == n:
                    right += 1

                hc = max(1, len(HYP_COUNTER.syllables(word)))
                if hc == n:
                    comp["pyhyphen"] += 1

                if alt_syll.estimate(word) == n:
                    comp["syllables"] += 1

    ratio = round(right / total, 2)
    assert ratio >= 0.93, "Less than 93% accurate on NSyllables!"

    hyp_ratio = round(comp["pyhyphen"] / total, 2)
    assert ratio > hyp_ratio, f"Less accurate than pyhyphen {hyp_ratio}!"

    syll_ratio = round(comp["syllables"] / total, 2)
    assert ratio > syll_ratio, f"Less accurate than syllables {syll_ratio}!"
