from commanding import Phrase
from osu import recent, osudebug
from papergirl import paper, artist

functions = {
    "recent": recent,
    "osudebug": osudebug,
    "paper": paper,
    "artist": artist
}

commands = [
    Phrase("help", ["help me"]),
    Phrase("artist", ["artist", ["*img", "a"]]),
    Phrase("paper", ["paper"]),
    Phrase("paper", ["paper", ["~query", "a"]]),
    Phrase("paper", ["paper", ["~query", "a"], "x", ["*number", "1"]]),
    Phrase("recent", ["recent"]),
    Phrase("recent", ["recent", ["~query", "a b c"], "-mode", ["~mode", "0"]]),
    Phrase("recent", ["recent", ["~query", "a b c"]]),
    Phrase("osudebug", ["osudebug"]),
]

regexes = {
    "string": r"(?<=\").*?(?=\")",
    "number": r"\-?[0-9]+(\.[0-9]+)?",
    "img": r"\[qq:pic=(\S*)\]"
}