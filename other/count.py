# Open the "test.txt" file and count the frequency of each character in the file.
import re
import sys
import math

# GLOBAL VARIABLES
filename = ""

# From: http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
# All in Unicode hex ranges.
# Hiragana: 3040-309F
# Katakana: 30A0-30FF
# Kanji: 4E00-9FAF , common and uncommon
# Ext A: 3400-4DBF , rare
hiragana_regex = r'[\u3040-\u309F]+'
katakana_regex = r'[\u30A0-\u30FF]+'
kanji_regex = r'[\u4E00-\u9FAF\u3400-\u4DBF]+'

all_strings_dict = {}

# FUNCTION DEFINITIONS
def getFrequencyPercent(value, total):
    # Mult. by constant, floor, divide by constant.
    const = 1000000000
    percent = (value / total) * const

    return math.floor(percent) / const

# The following function shall accept matches from a regex and add them to a dictionary.
def addMatchesToDict(matches, dictionary):
    for match in matches:
        if match in dictionary:
            dictionary[match] += 1
        else:
            dictionary[match] = 1

    return dictionary # Not necessary, but good for chaining.


# MAIN LOGIC
# Get filename from args
if len(sys.argv) < 2:
  print("Usage: python3 count.py <filename>")
  exit()

filename = sys.argv[1]

# Read the content of the file AND eliminate all ASCII characters.
# Remove full-width punctuation.
# Split on full hiragana substrings.
with open(filename, "r") as file:
    content = file.read()
    # Below will take megabytes of memory...
    #hiragana_matches = re.findall(hiragana_regex, content)
    #katakana_matches = re.findall(katakana_regex, content)
    kanji_matches = re.findall(kanji_regex, content)
    
    #addMatchesToDict(hiragana_matches, all_strings_dict)
    #addMatchesToDict(katakana_matches, all_strings_dict)
    addMatchesToDict(kanji_matches, all_strings_dict)

    # Sort by frequency
    all_strings_dict = dict(sorted(all_strings_dict.items(), key=lambda item: item[1], reverse=True))
    total = sum(all_strings_dict.values())

    # Print all as CSV file as well as total.
    for key, value in all_strings_dict.items():
        print(f"{key},{value},{getFrequencyPercent(value, total)}")

    print(f"total,{total}")