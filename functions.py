from commanding import Phrase
from osu import recent

functions = {
    "recent": recent
}

commands = [
    Phrase("paper", ["paper"]),
    Phrase("recent", ["recent"]),
	Phrase("recent", ["recent", ["~query", "$self"]])
]

regexes = {
    
}