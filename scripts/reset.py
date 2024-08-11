import common

# Global variables
cards = common.readDeck()

# Load JSON, reset scores, and save.
for card in cards:
  if card["type"] == "card":
    card["score"] = 0

common.writeDeck(cards)

