import os
import common

# LOGIC.
deck_dir = common.getDeckDirOrExit()
decks = os.listdir(deck_dir)

for deck in decks:
  print(deck.replace(".txt", ""))