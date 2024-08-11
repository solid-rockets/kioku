# Checks for doubles in the input files.
# If two lines start with the same first word,
# the program will print out the line numbers and the word.

import common

# GLOBAL VARIABLES.
word_lines = []

lines_path = common.getLinesPathOrExit()

# HELPER FUNCTIONS.
def getFirstWord(line):
    return line.split(":")[0].strip()

# MAIN LOGIC.
# Open the wordlist file
with open(lines_path, "r") as file:
    word_lines = file.readlines()

# Check for doubles
words = {}
index = 1 # Line numbers start at 1.
for line in word_lines:
    stripped = line.strip()
    if stripped[0] == "#":
        continue

    first_word = getFirstWord(stripped)
    #print(first_word)

    if first_word in words:
        words[first_word] = words[first_word] + [index]
    else:
        words[first_word] = [index]

    index += 1

for word in words:
    if len(words[word]) > 1:
        print(f"Word '{word}' appears on lines {words[word]}.")