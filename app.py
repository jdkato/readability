from readability import parse_html


if __name__ == "__main__":
    url = "https://developer.cobalt.io/getting-started/sign-in/"
    r = parse_html(url, {"class": "td-content"}, from_url=True)
    print(r.word_freq)
