# The following script outputs all strings of kanji in a file.
import re
import sys
import math

# GLOBAL VARIABLES
input_material_path = ""
output_file_path = ""
all_words = {}

# From: http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
# All in Unicode hex ranges.
# Kanji: 4E00-9FAF , common and uncommon
# Ext A: 3400-4DBF , rare
kanji_regex = r'[\u4E00-\u9FAF\u3400-\u4DBF]+'

# MAIN LOGIC
# Get filename from args
if len(sys.argv) < 3:
    print("Usage: python3 strip.py <input_material_path> <output_file_path>")
    exit()

input_material_path = sys.argv[1]
output_file_path = sys.argv[2]

with open(input_material_path, "r") as input_material:
    for line in input_material:
        kanji_matches = re.findall(kanji_regex, line)
        for match in kanji_matches:
            # I don't care about the count, but maybe useful in the future.
            # The only thing that matters is the key.
            if match in all_words:
                all_words[match] += 1
            else:
                all_words[match] = 1

with open(output_file_path, "w") as output_file:
    for word in all_words:
        output_file.write(word + "\n")