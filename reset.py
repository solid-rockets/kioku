# Formats of files are discussed in "insert.py"

import sys
import json

# Global variables
filename = ""
cards = []

# Get filename from args
if len(sys.argv) < 2:
    print("Usage: python reset.py <filename>")
    exit()

filename = sys.argv[1]

# Load the JSON file and reset all cards to 0.
with open(filename, "r") as file:
    json_data = json.load(file)
    cards = json_data["cards"]
    for card in cards:
        card["score"] = 0

# Replace the file with the updated JSON data
with open(filename, "w") as file:
    json.dump(json_data, file)

