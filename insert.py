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

# Global variables
input_wordlist = []
cards = []
must_read_old_json = False

input_wordlist = ""
input_json = ""
output_json = ""

# Get filenames from args: input of fresh, input of old JSON, and output JSON
# Case of no old JSON file
if len(sys.argv) == 3:
    input_wordlist = sys.argv[1]
    output_json = sys.argv[2]
    must_read_old_json = False

# Case of old JSON file
if len(sys.argv) == 4:
    input_wordlist = sys.argv[1]
    input_json = sys.argv[2]
    output_json = sys.argv[3]
    must_read_old_json = True

# Inform the user about what filenames need to be provided
if len(sys.argv) < 3:
    print("Usage: python insert.py <input_wordlist> <output_json>")
    print("Usage: python insert.py <input_wordlist> <input_json> <output_json>")
    exit()

# Open the wordlist file
with open(input_wordlist, "r") as file:
    word_lines = file.readlines()

# Load old JSON file
if must_read_old_json:
  with open(input_json, "r") as file:
      old_json = json.load(file)
      cards = old_json["cards"]

# Append the new flashcards to the list
for line in word_lines:
    front, back = line.strip().split(":")
    cards.append({
        "front": front.rstrip(),
        "back": back.lstrip(),
        "score": 0
    })

# Output the result into a JSON file
with open(output_json, "w") as file:
    json.dump({"cards": cards}, file)