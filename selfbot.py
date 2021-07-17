# Version and author
__author__ = "Daddie0 || https://daddie.dev"
__version__ = "0.0.1"


import discord
from discord import Color
from discord.ext import commands
from ext import helpformatter
import json
import os
import datetime
import traceback
import sys
import urllib

# start datetime timer
# starttime = datetime.datetime.now()

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

# Try to read data/config.json
# If it fails ask user to run setupWizard.py
try:
    with open("data/config.json") as f:
        data = json.load(f)
except:
    print("\n" + red + "Error: No data/config.json file found!" + reset)
    print("\n" + red + "Please run setupWizard.py to create one!" + reset + "\n")
    sys.exit(1)

# Import all variables from the config file.
with open("data/config.json") as f:
    data = json.load(f)
    token = data["token"]
    prefix = data["prefix"]
    autoupdate = data["autoupdate"]


# Check if autoupdate is enabled.
if autoupdate == True:
    print(green + "Autoupdate is enabled!" + reset)
    print(cyan + "Checking for updates..." + reset)
    # Github repo is https://github.com/GoByeBye/Ares
    # Check the raw file on github https://github.com/GoByeBye/Ares/data/version.json against __version__ of selfbot.py
    # if version differs run update.py and close selfbot.py
    try:
        import urllib.request
        version = urllib.request.urlopen("https://raw.githubusercontent.com/GoByeBye/Ares/master/data/version.json").read()
        
        version = version.decode("utf-8")
        version = json.loads(version)
        version = version["version"]
        if version != __version__:
            print(green + "A new update is available!" + reset)
            print(green + "Updating..." + reset)
            os.system("python update.py")
            sys.exit()
    except Exception as e:
        print(red + "Error checking for updates!" + reset)
        print(red + str(e) + reset)
        sys.exit()



class Selfbot(commands.Bot):
    def __init__(self, **attrs):
        super().__init__(
            command_prefix='self.get_pre',
            self_bot=True,
            help_command=helpformatter(),
            guild_subscriptions=False,
        )
        self.load_extentions()
        
        # Import all commands from cogs folder and traceback the error using traceback. Using colored input Green for successfully loaded and red for error
        def load_extentions(self):
            for extension in os.listdir("cogs"):
                if extension.endswith('.py'):
                    try:
                        self.load_extension("cogs." + extension[:-3])
                        print(green + "Loaded " + extension[:-3] + reset)
                    except Exception as e:
                        print(red + "Failed to load " + extension[:-3] + reset)
                        traceback.print_exc()



    @classmethod
    def init(bot, token=None):
        """Stats the selfbot"""
        selfbot = bot()
        safe_token = token
        try:
            selfbot.run(safe_token, bot=False, reconnect=True)
        except discord.LoginFailure:
            # Token is invalid, ask the user to run the setup wizard again
            print(red + "Invalid Token" + reset)
            print(red + "Please run the setup wizard again" + reset)
            sys.exit(1)
        except KeyboardInterrupt:
            # Bot stopped by the user
            print(red + "Selfbot stopped by the user" + reset)
            sys.exit(0)
        except Exception as e:
            # The bot encountered an error
            print(red + "Encountered an error" + reset)
            traceback.print_exc()
            sys.exit(1)
        finally:
            # Always make sure to close the selfbot
            selfbot.close()
    


