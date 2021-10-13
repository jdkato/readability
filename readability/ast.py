import html.parser
import re

INLINE_TAGS = [
    "b",
    "big",
    "i",
    "small",
    "abbr",
    "acronym",
    "cite",
    "dfn",
    "em",
    "kbd",
    "strong",
    "a",
    "br",
    "img",
    "span",
    "sub",
    "sup",
    "code",
    "tt",
]
HEADING = re.compile(r"^h\d$")
SKIP_TAGS = ["script", "style", "pre", "figure"]
TAG_TO_SCOPE = {
    "th": "table.heading",
    "td": "table.cell",
    "li": "list",
    "blockquote": "blockquote",
}


def codify(text):
    """Add markup-specific inline code makers."""
    return "{0}".format(text)


def clean(text, is_skip):
    """ """
    if is_skip:
        text = codify("*" * len(text))
        is_skip = False
    return text, is_skip


def make_node(text, history):
    """ """
    for tag in history:
        scope = TAG_TO_SCOPE.get(tag)
        if scope or HEADING.match(tag):
            if scope:
                scope = scope
            else:
                scope = "heading"
            return {"scope": scope, "text": text}
        elif tag in SKIP_TAGS:
            return {"scope": "ignore", "text": text}

    if "p" in history:
        return {"scope": "paragraph", "text": text}

    return {"scope": history[-1], "text": text}


class HTMLToAST(html.parser.HTMLParser):
    """Convert an HTML document into an AST."""

    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.block = False
        self.skip = False
        self.history = []
        self.buf = []
        self.nodes = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.block = True
        else:
            self.skip = tag == "tt" or tag == "code"

        self.history.append(tag)
        for k, val in dict(attrs).items():
            if k in ("alt", "id"):
                self.nodes.append({"scope": "ignore", "text": val})
            elif k == "href":
                self.nodes.append({"scope": "href", "text": val})

    def handle_endtag(self, tag):
        if self.block and tag in SKIP_TAGS:
            self.block, self.skip = False, False

        content = "".join(self.buf).strip()
        if tag not in INLINE_TAGS and content:
            node = make_node(content, self.history)
            self.nodes.append(node)
            self.buf = []
            self.history = []

    def handle_data(self, data):
        if not self.block:
            if self.skip:
                self.nodes.append({"scope": "code", "text": data})
            data, self.skip = clean(data, self.skip)
        self.buf.append(data)
