# Formats of files are discussed in "insert.py"

import sys
import json

import common

# Global variables
deck_path = common.getDeckPathOrExit()
cards = []

# Load the JSON file and reset all cards to 0.
with open(deck_path, "r") as file:
    json_data = json.load(file)
    cards = json_data["cards"]
    for card in cards:
        card["score"] = 0

# Replace the file with the updated JSON data
with open(deck_path, "w") as file:
    json.dump(json_data, file)

