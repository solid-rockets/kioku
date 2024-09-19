import sys
import tkinter
import random
import math

import common

# CONSTANTS.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# GLOBAL VARIABLES.
raw_cards = common.readDeck()
cards = common.filterForTestCards(raw_cards)
testing_cards = []
current_card = None

deck_path = common.getDeckPath()

max_cards = 50
max_correct = 1 # How many times card is shown before it is removed from the test.

min_score = 0 # Minimum score for a card to be included in the test.

num_correct_total = 0
screen_state = "front" # or "back"

seen_cards_num = 0

root = tkinter.Tk()
root.title("kioku")
root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
root.configure(bg="black")

score_text_var = tkinter.StringVar()
seen_text_var = tkinter.StringVar()
cards_remaining_var = tkinter.StringVar()
trans_test_score_var = tkinter.StringVar()

front_text_var = tkinter.StringVar()
back_text_var = tkinter.StringVar()

# score, front, back
# TODO: remove repetition.
tkinter.Label(root, textvariable=score_text_var, font=("Arial", 15), bg="black", fg="white").place(x=10, y=10)
tkinter.Label(root, textvariable=seen_text_var, font=("Arial", 15), bg="black", fg="white").place(x=10, y=35)
tkinter.Label(root, textvariable=cards_remaining_var, font=("Arial", 15), bg="black", fg="white").place(x=SCREEN_WIDTH - 135, y=10)
tkinter.Label(root, textvariable=trans_test_score_var, font=("Arial", 15), bg="black", fg="white").place(x=SCREEN_WIDTH - 135, y=35)

tkinter.Label(root, textvariable=front_text_var, font=("Arial", 60), bg="black", fg="white").pack()
tkinter.Label(root, textvariable=back_text_var, font=("Arial", 30), bg="black", fg="white").pack()

# HELPER FUNCTIONS.
def countLeftToTest():
  count = 0

  for card in testing_cards:
    if not card["is_testing_over"]:
      count += 1

  return count

def checkAnyLeftToTest():
  for card in testing_cards:
    if not card["is_testing_over"]:
      return True
  return False

def getScoreString():
  global num_correct_total
  global max_cards
  global max_correct
  return f"Score: {num_correct_total}/{max_cards * max_correct}"

def getArgument(arg_name):
  arg_name = arg_name + "="

  for arg in sys.argv:
    if arg_name in arg:
      return arg.split("=")[1]
    
  return None

def randomizeOrder(list):
  halved_len = int(math.floor(len(list) / 2))

  for i in range(0, halved_len): # Only to half of the list.
    anti_i = len(list) - 1 - i

    if random.randint(0, 1) >= 1:
      list[i], list[anti_i] = list[anti_i], list[i]

def addNewlinesToBackString(string):
  return string.replace(";", "\n")
  
def filterScores(scores, min_score):
  filtered_scores = []

  for s in scores:
    if s >= min_score:
      filtered_scores.append(s)

  return filtered_scores

# MAIN LOGIC
# Other args.
# --max=<number> or -m=<number> - number of cards to test.
full_arg = getArgument("--max") or getArgument("-m")
if full_arg is not None:
  max_cards = int(full_arg)

# --correct=<number> or -c=<number> - number of times card is shown before it is removed from the test.
full_arg = getArgument("--correct") or getArgument("-c")
if full_arg is not None:
  max_correct = int(full_arg)

# --title - title of the deck.
full_arg = getArgument("--title") or getArgument("-t")
if full_arg is not None:
  root.title(f"kioku - {full_arg.replace('--', ' ')}")

# --min=<number> or -n=<number> - minimum score for a card to be included in the test.
full_arg = getArgument("--min") or getArgument("-n")
if full_arg is not None:
  min_score = int(full_arg)

# Select the cards for testing.
# Default is 50.
# Ordering is based on the score - worst score goes first.
# Cards of the same score are added in the order they are in the JSON file.

# Get a list of scores, ordered from worst to best.
scores = [card["score"] for card in cards]
scores = list(set(scores))
scores.sort()
scores = filterScores(scores, min_score)

# Get the cards with the worst scores.
for score in scores:
  # Break if we have enough cards.
  if len(testing_cards) >= max_cards:
    break
  
  # Otherwise, add the cards with the current score.
  for card in cards:
    if card["score"] == score:
      testing_cards.append(card)
      card["is_testing_over"] = False
      card["correct_num"] = 0

      if len(testing_cards) >= max_cards:
        break
          
# Introduce light randomness.
randomizeOrder(testing_cards)

# Testing cards selected - link them circularly.
for i in range(len(testing_cards)):
  testing_cards[i]["index"] = i + 1

  if i == len(testing_cards) - 1:
    testing_cards[i]["next"] = testing_cards[0]
  else:
    testing_cards[i]["next"] = testing_cards[i + 1]

current_card = testing_cards[0]
max_cards = len(testing_cards) # For proper score in case of small decks.

# Cards for testing have been prepared.
# Start the test.

# Use tkinter to display the cards.
# The user will be able to flip the card with ENTER and mark it as correct (Y) or incorrect (N).

# The score will be updated +1 for correct, -2 for incorrect.

# The following screens will be shown.
# 1) Front only - show the front of each card in order.
# 2) Both sides - show the front and back of each card in order.

# Continue the test until all cards are correct once - mark as "is_testing_over".
# Remove the "is_testing_over" mark from all cards after the test.
front_text_var.set(current_card["front"])
back_text_var.set("")
trans_test_score_var.set(f"Card score: {current_card['score']}")

score_text_var.set(getScoreString())
seen_text_var.set(f"Seen: {seen_cards_num}")
cards_remaining_var.set(f"Remaining: {max_cards}")

def key_handler(event):
  global current_card
  global num_correct_total
  global screen_state
  global seen_cards_num

  letter = event.char

  # Update the screen
  if screen_state == "front": # Why? Actions ON any key.
    back_text_var.set(addNewlinesToBackString(current_card["back"]))
    seen_cards_num += 1
    screen_state = "back"
    
  elif screen_state == "back":
    if letter == "y":
      current_card["score"] += 1
      current_card["correct_num"] += 1
      num_correct_total += 1

      if current_card["correct_num"] == max_correct:
        current_card["is_testing_over"] = True

    else:
      current_card["score"] -= 1

    # Make sure a valid card is selected.
    if not checkAnyLeftToTest():
      root.quit()
      return

    current_card = current_card["next"]

    while current_card["is_testing_over"]:
      current_card = current_card["next"]

    front_text_var.set(current_card["front"])
    back_text_var.set("")
    trans_test_score_var.set(f"Card score: {current_card['score']}")
    
    screen_state = "front"

  # Always update these.
  score_text_var.set(getScoreString())
  seen_text_var.set(f"Seen: {seen_cards_num}")
  cards_remaining_var.set(f"Remaining: {countLeftToTest()}")

root.bind("<Key>", key_handler)
root.mainloop()

# CLEAN UP AFTER MAIN LOGIC IS COMPLETED.
# Remove the "is_testing_over" and "next" mark from all cards after the test.
for card in testing_cards:
  del card["is_testing_over"]
  del card["correct_num"]
  del card["next"]

# Save the updated cards to the file.
# Using raw cards because:
# 1) The scores will be updated in the filtered cards with "raw_cards" keeps track of.
# 2) We need to keep the comments and empty lines.
common.writeDeck(raw_cards)
