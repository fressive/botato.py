from commanding import Phrase
from osu import recent, osudebug
from papergirl import paper

functions = {
    "recent": recent,
    "osudebug": osudebug,
    "paper": paper
}

commands = [
    Phrase("help", ["help me"]),
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
    "number": r"\-?[0-9]+(\.[0-9]+)?"
}