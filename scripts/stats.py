# Calculates statistics for the cards in the deck.
# Two types of statistics are calculated:
# 1. Total number of cards.
# 2. Percentage of cards at given scores.

import common

# GLOBAL VARIABLES.
total_cards = 0
cards = common.readDeck()

# MAIN LOGIC.
# Count the total number of cards.
total_cards = len(cards)

# Count the number of cards at each score.
scores = {}
for card in cards:
  if card["type"] == "card":
    score = card["score"]

    if score in scores:
      scores[score] = scores[score] + 1
    else:
      scores[score] = 1

# Print the statistics.
print(f"Total number of cards: {total_cards}")
for score in scores:
  number = scores[score]
  percentage = number / total_cards * 100
  print(f"Score {score}: {number} ({percentage:.2f}%)")