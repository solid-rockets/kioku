# HEADER.
# The following file contains helper functions only.

# NOTES
# All decks are text files whose lines are converted into JSON objects.
# 
# There are three types of lines in a deck:
# 1) Empty lines - empty cards; "type": "empty".
# 2) Comment lines - start with "#"; "type": "comment".
# 3) Card lines - contain front, back, and score; "type": "card".

# IMPORTS.
import os
import sys

# LOGIC.
def getDeckNameOrExit():
  if len(sys.argv) < 2:
    print("Please provide the deck name.")
    exit()
  
  return sys.argv[1]

def getDeckDirOrExit():
  deck_dir = os.getenv("KIOKU_PATH")

  if not deck_dir:
    print("Please set the path to decks' directory in the KIOKU_PATH environment variable.")
    exit()

  if not os.path.exists(deck_dir):
    print(f"Directory doesn't exist: {deck_dir}")
    exit()

  return deck_dir

def getDeckPath(makeSureDeckExists = True):
  deck_dir = getDeckDirOrExit()
  deck_name = getDeckNameOrExit() + ".txt"
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

def convertLineIntoCard(line):
  stripped = line.strip()
  
  # Empty line - empty card.
  if len(stripped) == 0:
    return {
      "type": "empty",
    }
  
  # Empty
  if stripped[0] == "#":
    return {
      "type": "comment",
      "text": stripped
    }

  # Otherwise, it's a card.
  fields = stripped.split(":")
  front = fields[0].strip()
  back = fields[1].strip()
  score = 0

  if len(fields) > 2:
    score = int(fields[2].strip())

  return {
    "type": "card",
    "front": front,
    "back": back,
    "score": score
  }

def convertCardIntoLine(card):
  if card["type"] == "empty":
    return ""
  elif card["type"] == "comment":
    return card["text"]
  else:
    return f"{card['front']} : {card['back']} : {card['score']}"

# Read all lines and convert them into cards.
def readDeck():
  deck_path = getDeckPath()
  cards = []
  lines = []

  with open(deck_path, "r") as file:
    lines = file.readlines()

  for line in lines:
    cards.append(convertLineIntoCard(line))

  return cards

# Write all cards back as lines.
def writeDeck(cards):
  deck_path = getDeckPath()

  with open(deck_path, "w") as file:
    for card in cards:
      file.write(convertCardIntoLine(card) + "\n")

def filterForTestCards(cards):
  return [card for card in cards if card["type"] == "card"]