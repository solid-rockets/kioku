# HEADER.
# The following file contains helper functions only.

# IMPORTS.
import os
import sys

# LOGIC.
def getDeckPathOrExit():
  deck_dir  = os.getenv("KIOKU_DECKS")
  deck_name = ""
  deck_path = ""

  if not deck_dir:
    print("Please set the path to decks' directory in the KIOKU_DECKS environment variable.")
    exit()
  
  if len(sys.argv) < 2:
    print("Please provide the deck name.")
    exit()

  deck_name = sys.argv[1]
  deck_path = os.path.join(deck_dir, deck_name + ".json")

  if not os.path.exists(deck_path):
    print(f"Deck '{deck_name}' does not exist: {deck_path}")
    exit()

  return deck_path