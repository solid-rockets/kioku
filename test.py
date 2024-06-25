import sys
import json
import tkinter

# GLOBAL VARIABLES.
filename = ""
cards = []
testing_cards = []
current_card = None
# TODO: args for the following two lines.
max_cards = 50 # Default for now; will provide arg in the future.
max_correct = 1 # How many times card is shown before it is removed from the test.
num_correct_total = 0
screen_state = "front" # or "back"

root = tkinter.Tk()
root.title("kioku")
root.geometry("800x400")

score_text_var = tkinter.StringVar()
front_text_var = tkinter.StringVar()
back_text_var = tkinter.StringVar()

# score, front, back
tkinter.Label(root, textvariable=score_text_var, font=("Arial", 15)).pack()
tkinter.Label(root, textvariable=front_text_var, font=("Arial", 60)).pack()
tkinter.Label(root, textvariable=back_text_var, font=("Arial", 30)).pack()

# HELPER FUNCTIONS.
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
  return ""

# MAIN LOGIC
# Get filename from args
if len(sys.argv) < 2:
  print("Usage: python reset.py <filename>")
  exit()

filename = sys.argv[1]

# Other args.
# --max=<number> or -m=<number> - number of cards to test.
full_arg = getArgument("--max")
if full_arg != "":
  max_cards = int(full_arg)

# --correct=<number> or -c=<number> - number of times card is shown before it is removed from the test.
full_arg = getArgument("--correct")
if full_arg != "":
  max_correct = int(full_arg)

# Analyze arguments.
# Get max from arg: "--max=<number>" or "-m=<number>"
for arg in sys.argv:
  if arg.startswith("--max="):
    max_cards = int(arg[6:])
  elif arg.startswith("-m="):
    max_cards = int(arg[3:])

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
          card["is_testing_over"] = False
          card["correct_num"] = 0

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

# Continue the test until all cards are correct once - mark as "is_testing_over".
# Remove the "is_testing_over" mark from all cards after the test.
front_text_var.set(current_card["front"])
back_text_var.set("")
score_text_var.set(getScoreString())

def key_handler(event):
  global current_card
  global num_correct_total
  global screen_state

  letter = event.char

  # Update the screen
  if screen_state == "front": # Why? Actions ON any key.
    back_text_var.set(current_card["back"].replace("　", "\n"))
    back_text_var.set(current_card["back"].replace("<br>", "\n"))
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
    screen_state = "front"

  # Always update these.
  score_text_var.set(getScoreString())

root.bind("<Key>", key_handler)
root.mainloop()

# CLEAN UP AFTER MAIN LOGIC IS COMPLETED.
# Remove the "is_testing_over" and "next" mark from all cards after the test.
for card in testing_cards:
  del card["is_testing_over"]
  del card["next"]

# Save the updated cards to the file.
json_data["cards"] = cards

with open(filename, "w") as file:
  json.dump(json_data, file)
