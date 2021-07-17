# Automatically updates the the entire project from the git repo using git pull
# https://github.com/GoByeBye/Ares
#
# Usage: python update.py

import os
import subprocess

# Cross platfrom terminal clearing
def cls():
    os.system('cls' if os.name=='nt' else 'clear')


cls()

# Cross platfrom terminal colors
red = "\033[31m"
green = "\033[32m"
cyan = "\033[36m"
purple = "\033[95m"
reset = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"


# Verify the user has git installed
try:
    subprocess.call(["git", "--version"])
    print(green + "Git is installed!" + reset)
except OSError:
    print(red + "Error: git is not installed. Please install git and try again." + reset)
    print("Windows git download link" + cyan + " https://git-scm.com/download/win" + reset)
    print("Linux install command" + cyan + " sudo apt-get install git" + reset)
    exit()

# Try to pull newest version
try:
    subprocess.call(["git", "pull"])
    print(green + "Updated!" + reset)
    print(green + "You may need to restart the selfbot by running python selfbot.py." + reset)
except OSError:
    print(red + "Error: git pull failed. Please try again." + reset)
    exit()
