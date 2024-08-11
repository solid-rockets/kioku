# Checks for doubles in the input files.
# If two lines start with the same first word,
# the program will print out the line numbers and the word.

import common

# GLOBAL VARIABLES.
word_lines = []
cards = common.readDeck()

# HELPER FUNCTIONS.

# MAIN LOGIC.
# Check for doubles
words = {}
index = 1 # Line numbers start at 1.
for card in cards:
  # Only read lines that are actual flashcards.
  if card["type"] == "card":
    front = card["front"]

    if front in words:
      words[front] = words[front] + [index]
    else:
      words[front] = [index]

  index += 1

for word in words:
    if len(words[word]) > 1:
        print(f"Word '{word}' appears on lines {words[word]}.")