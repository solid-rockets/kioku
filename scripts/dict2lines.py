# PLEASE NOTE: will be replaced with a direct interface to the EDICT file.

# The following code automatically analyzes the output from the gjiten dictionary
# and outputs lines into a file that agree with the input format of kioku.

# The general format is as follows:
# <JP word in kanji or hiragana> (<hiragana>) (<class attr.>)* <English definition>

import re
import common

# GLOBAL VARIABLES.
running = True
input_file_path = common.getLinesPathOrExit()

# HELPER FUNCTIONS.
def getJapaneseWord(input_line):
  # First couple of bytes followed by a space.
  return re.match(r"^[^ ]+ ", input_line).group(0)

def getAllClassAttributes(input_line):
  # Find all class attributes.
  str_of_class_attrs = re.findall(r"(\(.+\) )+", input_line)
  class_attrs = str_of_class_attrs[0].strip().split(" ")
  return class_attrs

def extractHiragana(group):
  # Get hiragana out if any.
  matches = re.findall(r"[ぁ-ん]+", group)

  return matches[0] if matches else ""

def removeAllGroups(input_line, groups):
  # Remove all groups from the input line.
  output_line = input_line

  for group in groups:
    output_line = output_line.replace(group, "")

  return output_line
  
def convertToKiokuLine(input_line):
  # Get the raw extracts.
  first_letter = input_line[0]
  jpWord = getJapaneseWord(input_line)
  classAttrs = getAllClassAttributes(input_line)
  reading = extractHiragana(classAttrs[0])

  # Remove the raw extracts from the line.
  output_line = input_line.replace(jpWord, "")
  enDefinition = removeAllGroups(output_line, classAttrs).strip()

  # Clean the raw extracts.
  jpWord = jpWord.strip()

  if reading:
    reading = reading.strip().replace("(", "").replace(")", "")

  # Build the line and return.
  breakpoint = ";" if reading != "" else ""

  if first_letter == "　":
    # For special cases, where both kanji and reading are present, but I need the reading only.
    return f"{reading}:{enDefinition}"
  else:
    return f"{jpWord}:{reading}{breakpoint}{enDefinition}"

# MAIN LOGIC.
with open(input_file_path, "a") as file:
  while running:
    input_line = input()
    if input_line == "exit":
      break

    output_line = convertToKiokuLine(input_line)
    file.write(output_line + "\n")
    file.flush()