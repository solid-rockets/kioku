import sys
import json
import os

# GLOBAL VARIABLES.
filename = ""
cards = []
testing_cards = []
max_cards = 50 # Default for now; will provide arg in the future.
termWidth, termHeight = os.get_terminal_size()
score = 0

# HELPER FUNCTIONS.
def checkAnyLeftToTest():
  for card in testing_cards:
    if not card["was_correct_once"]:
      return True
  return False

def clearScreen():
   for i in range(termHeight):
      print()

# MAIN LOGIC
# Get filename from args
if len(sys.argv) < 2:
  print("Usage: python reset.py <filename>")
  exit()

filename = sys.argv[1]

# Load the JSON file cards.
with open(filename, "r") as file:
  json_data = json.load(file)
  cards = json_data["cards"]

# Select the cards for testing.
# Default is 50.
# Ordering is based on the score - worst score goes first.
# Cards of the same score are added in the order they are in the JSON file.

# Get a list of scores, ordered from worst to best.
scores = [card["score"] for card in cards]
scores = list(set(scores))
scores.sort()

# Get the cards with the worst scores.
for score in scores:
  # Break if we have enough cards.
  if len(testing_cards) >= max_cards:
      break
  
  # Otherwise, add the cards with the current score.
  for card in cards:
      if card["score"] == score:
          testing_cards.append(card)
          card["was_correct_once"] = False

          if len(testing_cards) >= max_cards:
              break

# Cards for testing have been prepared.
# Start the test.

# Use tkinter to display the cards.
# The user will be able to flip the card with ENTER and mark it as correct (Y) or incorrect (N).

# The score will be updated +1 for correct, -2 for incorrect.

# The following screens will be shown.
# 1) Front only - show the front of each card in order.
# 2) Both sides - show the front and back of each card in order.

# Continue the test until all cards are correct once - mark as "was_correct_once".
# Remove the "was_correct_once" mark from all cards after the test.
clearScreen()

while checkAnyLeftToTest():
  for card in testing_cards:
    if card["was_correct_once"]:
      continue

    front_text = card["front"]
    score_text = f"{score}/{max_cards}"
    input(f"{front_text} {score_text}")
    letter = input(f"{card['back']}\n\n(y/n) ")

    clearScreen()
    # Update the score.
    if letter == "y":
        card["score"] += 1
        card["was_correct_once"] = True
        score += 1
    else:
        card["score"] -= 2

# Remove the "was_correct_once" mark from all cards after the test.
for card in testing_cards:
  del card["was_correct_once"]

# Save the updated cards to the file.
json_data["cards"] = cards

with open(filename, "w") as file:
  json.dump(json_data, file)
