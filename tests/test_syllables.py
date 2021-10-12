import json

from readability.syllables import syllables


def test_syllables():
    with open("data/syllables.json") as f:
        for word, count in json.load(f).items():
            assert count == syllables(word), word
