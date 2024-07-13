# NOTE: gets kanji from Chinese loanwords in a text.

# Kanji frequency list was obtained from:
# https://scriptin.github.io/kanji-frequency/

# Kanji dictionary can be obtained from:
# https://www.edrdg.org/wiki/index.php/KANJIDIC_Project

# Open the "test.txt" file and count the frequency of each character in the file.

# IMPORTS
import re

# CONSTANTS
MAX_KANJI = 3000

# GLOBAL VARIABLES
kanjidic_path = "/home/ado/kanjidic"
kanji_src_path = "/home/ado/wiki_freq.txt" # Will read any source, line by line, kanji by kanji.

all_kanjidic_lines = []

# From: http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
# All in Unicode hex ranges.
# Hiragana: 3040-309F
# Katakana: 30A0-30FF
# Kanji: 4E00-9FAF , common and uncommon
# Ext A: 3400-4DBF , rare
katakana_regex = r'[\u30A0-\u30FF]+'
kanji_word_regex = r'[\u4E00-\u9FAF\u3400-\u4DBF]{2,}'
kanji_regex = r'[\u4E00-\u9FAF\u3400-\u4DBF]'

all_kanji_dict = {}

kanji_count = 0

# FUNCTION DEFINITIONS
def addMatchesToDict(matches, dictionary):
  for match in matches:
    if not match in dictionary:
      dictionary[match] = []

  return dictionary # Not necessary, but good for chaining.

def stringKatakanaReadings(readings):
  return "<br>".join(readings)

# MAIN LOGIC
# Load the whole dictionary into memory for convenience.
with open(kanjidic_path, "r") as file:
  all_kanjidic_lines = file.readlines()

# Read all unique kanji from each line.
with open(kanji_src_path, "r") as file:
  for line in file:
    kanji_words = re.findall(kanji_word_regex, line)

    for word in kanji_words:
      kanji_matches = re.findall(kanji_regex, word)
      addMatchesToDict(kanji_matches, all_kanji_dict)

# Get katakana readings from kanjidic.
for kanji in all_kanji_dict:
  for line in all_kanjidic_lines:
    if kanji in line:
      # Get all katakana readings and attach each to the array.
      #katakana_match = re.search(katakana_regex, line)
      katakana_matches = re.findall(katakana_regex, line)

      for match in katakana_matches:
        all_kanji_dict[kanji].append(match)

for kanji in all_kanji_dict:
  if kanji_count >= MAX_KANJI:
    break

  if len(all_kanji_dict[kanji]) > 0:
    print(f"{kanji}:{stringKatakanaReadings(all_kanji_dict[kanji])}")
    kanji_count += 1

