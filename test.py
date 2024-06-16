import sys
import json
import tkinter

# GLOBAL VARIABLES.
filename = ""
cards = []
testing_cards = []
current_card = None
max_cards = 50 # Default for now; will provide arg in the future.
# TODO: replace max_cards with smaller number if not enought cards.
score = 0
screen_state = "front" # or "back"

root = tkinter.Tk()
root.title("kioku")
root.geometry("800x400")

score_text_var = tkinter.StringVar()
front_text_var = tkinter.StringVar()
back_text_var = tkinter.StringVar()

front_text_var.set("Press any key.")

# score, front, back
tkinter.Label(root, textvariable=score_text_var, font=("Arial", 20)).pack()
tkinter.Label(root, textvariable=front_text_var, font=("Arial", 80)).pack()
tkinter.Label(root, textvariable=back_text_var, font=("Arial", 40)).pack()

# HELPER FUNCTIONS.
def checkAnyLeftToTest():
  for card in testing_cards:
    if not card["was_correct_once"]:
      return True
  return False

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

# Testing cards selected - link them circularly.
for i in range(len(testing_cards)):
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

# Continue the test until all cards are correct once - mark as "was_correct_once".
# Remove the "was_correct_once" mark from all cards after the test.
def key_handler(event):
  global current_card
  global score
  global screen_state

  letter = event.char

  # Make sure a valid card is selected.
  if not checkAnyLeftToTest():
    root.quit()
    return

  while current_card["was_correct_once"]:
    print(current_card)
    current_card = current_card["next"]

  # Update the screen
  if screen_state == "front":
    front_text_var.set(current_card["front"])
    back_text_var.set("")
    # TODO: fix state change
    
  elif screen_state == "back":
    back_text_var.set(current_card["back"].replace("　", "\n"))

    if letter == "y":
      current_card["score"] += 1
      current_card["was_correct_once"] = True
      score += 1
    else:
      current_card["score"] -= 2
    # TODO: fix state change

  # Always update these.
  score_text_var.set(f"Score: {score}/{max_cards}")
  current_card = current_card["next"]

root.bind("<Key>", key_handler)
root.mainloop()

# CLEAN UP AFTER MAIN LOGIC IS COMPLETED.
# Remove the "was_correct_once" and "next" mark from all cards after the test.
for card in testing_cards:
  del card["was_correct_once"]
  del card["next"]

# Save the updated cards to the file.
json_data["cards"] = cards

with open(filename, "w") as file:
  json.dump(json_data, file)
