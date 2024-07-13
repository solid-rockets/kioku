# The following script is used to install "kioku"
# on a Un*x system.
#
# The following changes are made:
# 1) KIOKU_PATH is appended to the .bashrc file.
# 2) The executable scripts are copied to $KIOKU_PATH/scripts.
# 3) Scipts are made executable.

# TODO:
# - support files other than .bashrc

import os
import sys

# GLOBAL VARIABLES
kioku_path = input("Please input the path for kioku: (default is ~/kioku):")
scripts_path = ""
rc_path = os.path.expanduser("~/.bashrc")

# from commandline, get first argument only
arg = ""
if len(sys.argv) > 1:
  arg = sys.argv[1]

common = ["common.py"]
scripts = ["dict2lines.py", "reset.py", "test.py", "check4doubles.py"]

# HELPER FUNCTIONS
def ensureKiokuPathExists():
  global scripts_path
  global kioku_path

  if kioku_path == "":
    kioku_path = os.path.expanduser("~/kioku")
  scripts_path = os.path.join(kioku_path, "scripts")

  os.makedirs(kioku_path, exist_ok=True)
  os.makedirs(scripts_path, exist_ok=True)

def checkForKiokuPathInRcFile():
  with open(rc_path, "r") as file:
    for line in file:
      if "KIOKU_PATH" in line:
        print("KIOKU_PATH already exists in .bashrc")
        print("Please also delete the append to PATH.")
        print("Exiting...")
        exit()

def appendToRcFile():
  with open(rc_path, "a") as file:
    file.write(f"\nexport KIOKU_PATH={kioku_path}")
    file.write("\nexport PATH=$PATH:$KIOKU_PATH/scripts")

def copyScriptsToKiokuPath():
  global scripts_path

  os.makedirs(scripts_path, exist_ok=True)

  # Copy the scripts.
  for lib in common:
    os.system(f"cp {lib} {scripts_path}")

  for script in scripts:
    os.system(f"cp {script} {scripts_path}")
    
def installKiokuShellScript():
  global scripts_path

  os.system(f"cp kioku.sh {scripts_path}/kioku")
  os.system(f"chmod +x {scripts_path}/kioku")

# MAIN LOGIC
ensureKiokuPathExists()
if arg == "full":
  checkForKiokuPathInRcFile()
  appendToRcFile()
copyScriptsToKiokuPath()
installKiokuShellScript()
