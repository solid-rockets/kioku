# Insert words by displaying the following interface:
# F: <front>
# B: <back>
# -----... # to cover the whole line in the console.
# 
# NO HELPER FUNCTIONS - just implement a simple loop.

import common

# GLOBAL VARIABLES.
running = True

lines_path = common.getDeckPath(False)

# HELPER FUNCTIONS.
def checkIfExit(text):
  if text == "!exit":
    exit()
    
# MAIN LOGIC.
with open(lines_path, "a") as file:
  while running:
    front = input("F: ")
    checkIfExit(front)
    
    back = input("B: ")
    checkIfExit(back)

    line = f"{front} : {back} : 0"
    print("-" * 80)

    file.write(line + "\n")
    file.flush()