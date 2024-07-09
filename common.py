# HEADER.
# The following file contains helper functions only.

# NOTES
# All decks are JSON files.

# IMPORTS.
import os
import sys
import json

# LOGIC.
def getDeckNameOrExit():
  if len(sys.argv) < 2:
    print("Please provide the deck name.")
    exit()
  
  return sys.argv[1]

def getDeckDirOrExit():
  deck_dir = os.getenv("KIOKU_DECKS")

  if not deck_dir:
    print("Please set the path to decks' directory in the KIOKU_DECKS environment variable.")
    exit()

  if not os.path.exists(deck_dir):
    print(f"Directory doesn't exist: {deck_dir}")
    exit()

  return deck_dir

def getDeckPath(makeSureDeckExists = True):
  deck_dir = getDeckDirOrExit()
  deck_name = getDeckNameOrExit() + ".json"
  deck_path = os.path.join(deck_dir, deck_name)

  if makeSureDeckExists and not os.path.exists(deck_path):
    print(f"Deck doesn't exist: {deck_path}")
    exit()

  return deck_path
  
def getLinesPathOrExit():
  # NOTE: doesn't matter whether exists or not - will open anyway.
  deck_dir = getDeckDirOrExit()
  lines_name = getDeckNameOrExit() + ".txt"
  lines_path = os.path.join(deck_dir, lines_name)

  return lines_path

def readDeck():
  deck_path = getDeckPath()
  cards = []

  with open(deck_path, "r") as file:
    json_data = json.load(file)
    cards = json_data["cards"]

  return cards

def writeDeck(cards):
  deck_path = getDeckPath()
  with open(deck_path, "w") as file:
    json.dump({"cards": cards}, file)