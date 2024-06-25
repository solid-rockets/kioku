# Opens the following files and transforms a list of words into
# local line format.

# Edict format:
# <JP word> [reading] /<ENG translation>/.../
# Removes (...) groups from front of each /.../ section.

# Output format of local line:
# <front>:<back>
# ...

import sys
import re

# GLOBAL VARIABLES.
cards = []

input_words = []

edict_path = ""
input_words_path = ""
output_lines_path = ""

kanji_ranges = '\u4E00-\u9FAF\u3400-\u4DBF'

# MAIN LOGIC.
# Get filenames from args: edict, input of words, and output lines
if len(sys.argv) == 3:
    edict_path = sys.argv[1]
    input_words_path = sys.argv[2]
    output_lines_path = sys.argv[3]

# Inform the user about what filenames need to be provided
if len(sys.argv) < 3:
    print("Usage: python with_edict.py <edict_path> <input_words_path> <output_lines_path>")
    exit()

edict_path = sys.argv[1]
input_words_path = sys.argv[2]
output_lines_path = sys.argv[3]

# The idea is to obtain the definitions of words from the edict file.
with open(input_words_path, "r") as file:
    input_words = file.readlines()

with open(output_lines_path, "w") as file:
    with open(edict_path, "r") as edict:
        for word in input_words:
            found = False

            for line in edict: # The dictionary file is too big to load into memory.
                # OPTI IDEA: save the seeker.

                # The entry is followed by a space and a reading.
                # PLEASE NOTE: FIFO - first definition only.
                word_re = f"^{word}[{kanji_ranges}]+ " # 
                word_match = re.match(word_re, line)
                if re.match(word_re, line):
                    jp_word = word_match.group(0)
                    reading = re.search(r"\[([^\]]+)\]", line).group(1)
                    translation = re.search(r"/([^/]+)/", line).group(1)

                    file.write(f"{word}:{reading}<br>{translation}\n")
                    found = True
                    break

            if not found:
                # Print to standard error.
                print(f"{word}", file=sys.stderr)

            edict.seek(0)     