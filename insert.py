# Opens the wordlist file, transforms into JSON format, and outputs
# the result into a JSON file.

import json
import os

import common

# GLOBAL VARIABLES.
cards = []
word_lines = []

deck_path = common.getDeckPath(False)
lines_path = common.getLinesPathOrExit()

# HELPER FUNCTIONS.
def getAnyDuplicate(list, front):
    # TODO: Use a dictionary for faster lookup.
    for card in list:
        if card["front"] == front:
            return card
    return None

# MAIN LOGIC.
# Open the wordlist file
with open(lines_path, "r") as file:
    word_lines = file.readlines()

# Load old JSON file if any.
if not os.path.exists(deck_path):
  with open(deck_path, "w") as file:
    json.dump({"cards": []}, file)

cards = common.readDeck()

# Append the new flashcards to the list
for line in word_lines:
    stripped = line.strip()
    if stripped[0] == "#":
        continue

    front, back = stripped.split(":")
    front = front.strip()
    back = back.strip()

    # Ignore duplicates
    dup = getAnyDuplicate(cards, front)

    if dup:
        dup["back"] = back
    else:
        cards.append({
            "front": front,
            "back": back,
            "score": 0
        })

# Output the result into a JSON file
common.writeDeck(cards)