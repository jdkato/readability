import re

from typing import Tuple, List


def is_complex(word: str, syllables: int) -> bool:
    for suffix in ["es", "ed", "ing"]:
        if word.endswith(suffix):
            syllables -= 1
    return syllables > 2


def count_syllables(word: str) -> int:
    """Return the number of syllables in the given word."""
    word = word.lower()
    size = len(word)

    if size < 1:
        return 0
    elif size < 3:
        return 1

    case = cornercases.get(word)
    if case:
        return case

    text, count = clean(word)

    count += len(re_vowels.findall(text))

    count -= len(re_monosyllabic_one.findall(text))
    count -= len(re_monosyllabic_two.findall(text))

    count += len(re_double_syllabic_one.findall(text))
    count += len(re_double_syllabic_two.findall(text))
    count += len(re_double_syllabic_three.findall(text))
    count += len(re_double_syllabic_four.findall(text))

    return 1 if count < 1 else count


def clean(word: str) -> Tuple[str, int]:
    word, prefix = clear_part(word, increment_to_prefix, trim_any_prefixes)
    word, suffix = clear_part(word, increment_to_suffix, trim_any_suffix)
    return word, prefix + suffix


def clear_part(word: str, options: List[List[str]], f) -> Tuple[str, int]:
    old = word
    pos = len(options)

    for i, trim in enumerate(options):
        word = f(word, trim)
        if word != old:
            return word, pos - i

    return word, 0


def trim_any_suffix(word: str, suffixes: List[str]) -> str:
    """Remove the provided suffixes from the given word."""
    for suffix in suffixes:
        if word.endswith(suffix):
            return word.removesuffix(suffix)
    return word


def trim_any_prefixes(word: str, prefixes: List[str]) -> str:
    """Remove the provided prefixes from the given word."""
    for prefix in prefixes:
        if word.startswith(prefix):
            return word.removeprefix(prefix)
    return word


cornercases = {
    "abalone": 4,
    "abare": 3,
    "abed": 2,
    "abruzzese": 4,
    "abbruzzese": 4,
    "aborigine": 5,
    "aborigines": 5,
    "acreage": 3,
    "adame": 3,
    "adieu": 2,
    "adobe": 3,
    "anemone": 4,
    "apache": 3,
    "aphrodite": 4,
    "apostrophe": 4,
    "ariadne": 4,
    "cafe": 2,
    "cafes": 2,
    "calliope": 4,
    "catastrophe": 4,
    "chile": 2,
    "chloe": 2,
    "circe": 2,
    "coyote": 3,
    "epitome": 4,
    "facsimile": 4,
    "forever": 3,
    "gethsemane": 4,
    "guacamole": 4,
    "hyperbole": 4,
    "jesse": 2,
    "jukebox": 2,
    "karate": 3,
    "machete": 3,
    "maybe": 2,
    "people": 2,
    "recipe": 3,
    "sesame": 3,
    "shoreline": 2,
    "simile": 3,
    "syncope": 3,
    "tamale": 3,
    "yosemite": 4,
    "daphne": 2,
    "eurydice": 4,
    "euterpe": 3,
    "hermione": 4,
    "penelope": 4,
    "persephone": 4,
    "phoebe": 2,
    "zoe": 2,
}
re_monosyllabic_one = re.compile(
    "cia(l|$)|"
    + "tia|"
    + "cius|"
    + "cious|"
    + "[^aeiou]giu|"
    + "[aeiouy][^aeiouy]ion|"
    + "iou|"
    + "sia$|"
    + "eous$|"
    + "[oa]gue$|"
    + ".[^aeiuoycgltdb]{2,}ed$|"
    + ".ely$|"
    + "^jua|"
    + "uai|"
    + "eau|"
    + "^busi$|"
    + "("
    + "[aeiouy]"
    + "("
    + "b|"
    + "c|"
    + "ch|"
    + "dg|"
    + "f|"
    + "g|"
    + "gh|"
    + "gn|"
    + "k|"
    + "l|"
    + "lch|"
    + "ll|"
    + "lv|"
    + "m|"
    + "mm|"
    + "n|"
    + "nc|"
    + "ng|"
    + "nch|"
    + "nn|"
    + "p|"
    + "r|"
    + "rc|"
    + "rn|"
    + "rs|"
    + "rv|"
    + "s|"
    + "sc|"
    + "sk|"
    + "sl|"
    + "squ|"
    + "ss|"
    + "th|"
    + "v|"
    + "y|"
    + "z"
    + ")"
    + "ed$"
    + ")|"
    + "("
    + "[aeiouy]"
    + "("
    + "b|"
    + "ch|"
    + "d|"
    + "f|"
    + "gh|"
    + "gn|"
    + "k|"
    + "l|"
    + "lch|"
    + "ll|"
    + "lv|"
    + "m|"
    + "mm|"
    + "n|"
    + "nch|"
    + "nn|"
    + "p|"
    + "r|"
    + "rn|"
    + "rs|"
    + "rv|"
    + "s|"
    + "sc|"
    + "sk|"
    + "sl|"
    + "squ|"
    + "ss|"
    + "st|"
    + "t|"
    + "th|"
    + "v|"
    + "y"
    + ")"
    + "es$"
    + ")"
)
re_monosyllabic_two = re.compile(
    "[aeiouy]"
    + "("
    + "b|"
    + "c|"
    + "ch|"
    + "d|"
    + "dg|"
    + "f|"
    + "g|"
    + "gh|"
    + "gn|"
    + "k|"
    + "l|"
    + "ll|"
    + "lv|"
    + "m|"
    + "mm|"
    + "n|"
    + "nc|"
    + "ng|"
    + "nn|"
    + "p|"
    + "r|"
    + "rc|"
    + "rn|"
    + "rs|"
    + "rv|"
    + "s|"
    + "sc|"
    + "sk|"
    + "sl|"
    + "squ|"
    + "ss|"
    + "st|"
    + "t|"
    + "th|"
    + "v|"
    + "y|"
    + "z"
    + ")"
    + "e$",
)
re_double_syllabic_one = re.compile(
    "(?:"
    + "[^aeiouy]ie"
    + "("
    + "r|"
    + "st|"
    + "t"
    + ")|"
    + "[aeiouym]bl|"
    + "eo|"
    + "ism|"
    + "asm|"
    + "thm|"
    + "dnt|"
    + "uity|"
    + "dea|"
    + "gean|"
    + "oa|"
    + "ua|"
    + "eings?|"
    + "[aeiouy]sh?e[rsd]"
    + ")$"
)
re_double_syllabic_two = re.compile("[^gq]ua[^auieo]|[aeiou]{3}|^(ia|mc|coa[dglx].)")
re_double_syllabic_three = re.compile(
    "[^aeiou]y[ae]|"
    + "[^l]lien|"
    + "riet|"
    + "dien|"
    + "iu|"
    + "io|"
    + "ii|"
    + "uen|"
    + "real|"
    + "iell|"
    + "eo[^aeiou]|"
    + "[aeiou]y[aeiou]",
)
re_double_syllabic_four = re.compile("[^s]ia")
re_vowels = re.compile("[aeiouy]+")

increment_to_prefix = [
    [
        "above",
        "anti",
        "ante",
        "counter",
        "hyper",
        "afore",
        "agri",
        "infra",
        "intra",
        "inter",
        "over",
        "semi",
        "ultra",
        "under",
        "extra",
        "dia",
        "micro",
        "mega",
        "kilo",
        "pico",
        "nano",
        "macro",
    ],
    [
        "un",
        "fore",
        "ware",
        "none",
        "non",
        "out",
        "post",
        "sub",
        "pre",
        "pro",
        "dis",
        "side",
    ],
]
increment_to_suffix = [
    ["ology", "ologist", "onomy", "onomist"],
    ["fully", "berry", "woman", "women"],
    [
        "ly",
        "less",
        "some",
        "ful",
        "er",
        "ers",
        "ness",
        "cian",
        "cians",
        "ment",
        "ments",
        "ette",
        "ettes",
        "ville",
        "villes",
        "ships",
        "ship",
        "side",
        "sides",
        "port",
        "ports",
        "shire",
        "shires",
        "tion",
        "tioned",
    ],
]
