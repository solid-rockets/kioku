# Formats of files are discussed in "insert.py"
import common

# Global variables
cards = common.readDeck()

# Load JSON, reset scores, and save.
for card in cards:
  card["score"] = 0

common.writeDeck(cards)

