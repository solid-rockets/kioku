# Opens the wordlist file, transforms into JSON format, and outputs
# the result into a JSON file.

# Input format of flashcard:
# <front>:<back>
# ...

# Output format of a flashcard (JSON):
# {
#   "cards": [
#     {
#       "front": "<front>",
#       "back": "<back>",
#       "score": 0
#     },
#     ...
# }

# TODO
# - Ignore duplicates.

import json
import sys

# GLOBAL VARIABLES.
cards = []
must_read_old_json = False
word_lines = []

input_wordlist_path = ""
input_json_path = ""
output_json_path = ""

# HELPER FUNCTIONS.
def checkCardIsDuplicate(list, front):
    for card in list:
        if card["front"] == front:
            return True
    return False

# MAIN LOGIC.
# Get filenames from args: input of fresh, input of old JSON, and output JSON
# Case of no old JSON file
if len(sys.argv) == 3:
    input_wordlist_path = sys.argv[1]
    output_json_path = sys.argv[2]
    must_read_old_json = False

# Case of old JSON file
if len(sys.argv) == 4:
    input_wordlist_path = sys.argv[1]
    input_json_path = sys.argv[2]
    output_json_path = sys.argv[3]
    must_read_old_json = True

# Inform the user about what filenames need to be provided
if len(sys.argv) < 3:
    print("Usage: python insert.py <input_wordlist_path> <output_json_path>")
    print("Usage: python insert.py <input_wordlist_path> <input_json_path> <output_json_path>")
    exit()

# Open the wordlist file
with open(input_wordlist_path, "r") as file:
    word_lines = file.readlines()

# Load old JSON file
if must_read_old_json:
  with open(input_json_path, "r") as file:
      old_json = json.load(file)
      cards = old_json["cards"]

# Append the new flashcards to the list
for line in word_lines:
    front, back = line.strip().split(":")
    front = front.strip()
    back = back.strip()

    # Ignore duplicates
    if checkCardIsDuplicate(cards, front):
        print(f"Duplicate found: {front}")
        continue

    # All good.
    cards.append({
        "front": front,
        "back": back,
        "score": 0
    })

# Output the result into a JSON file
with open(output_json_path, "w") as file:
    json.dump({"cards": cards}, file)