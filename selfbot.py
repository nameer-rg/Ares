# Version and author
__author__ = "Daddie0 || https://daddie.dev"
__version__ = "0.1.0"


import discord
from discord import Color
from discord.ext import commands
from ext.context import CustomContext
from ext.helpformatter import helpformatter
import json
import os
import datetime
import traceback
import sys
import urllib
import re

# Logging libraries
import logging
import coloredlogs


# Import logger configuration from data/logger.json
# if the configuration is empy or does not exist overwrite with default configuration
# { "level": "ERROR" }
def initLogger():
    try:
        with open('data/logger.json', 'r') as f:
            config = json.load(f)
            if not config['level']:
                config['level'] = 'WARNING'
            else:
                config['level'] = config['level'].upper()
                # Initialize coloredlogs
                coloredlogs.install(level=config['level'])
    except:
        with open('data/logger.json', 'w') as f:
            config = {
                'level': 'WARNING'
            }
            json.dump(config, f)
            # restart the bot
            print("Restarting")
            os.execv(sys.executable, ['python'] + sys.argv)



initLogger()

# Cross platfrom terminal colors
red = "\033[31m"
green = "\033[32m"
cyan = "\033[36m"
purple = "\033[95m"
reset = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"


# start datetime timer
starttime = datetime.datetime.now()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


cls()


# Try to read data/config.json
# If it fails ask user to run setupWizard.py using logging level error
try:
    with open("data/config.json") as f:
        data = json.load(f)
except:
    logging.critical("Failed to read data/config.json\nRunning the setup wizard")
    # Run setupWizard.py
    os.system("python setupWizard.py")
    # Gracefully exit
    sys.exit(1)



# autoupdate script 
def autoupdater():
    logging.info("Autoupdater is enabled")
    logging.info("Checking for updates")
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
            logging.warning("A new version of the selfbot is available.")
            logging.warning("Attempting to update automatically")
            os.system("python update.py")
            sys.exit()
        else:
            logging.info("You're already running the latest version")
    except:
        logging.error("Could not check for update")
        logging.error("Please check your internet connection") 
        sys.exit()





# Import all variables from the config file.
with open("data/config.json") as f:
    data = json.load(f)
    token = data["token"]
    prefix = data["prefix"]
    autoupdate = data["autoupdate"]


# Check if autoupdate is enabled. If yes run the update
if autoupdate == True:
    autoupdater()




class Selfbot(commands.Bot):
    def __init__(self, **attrs):
        super().__init__(
            command_prefix=prefix,
            self_bot=True,
            help_command=helpformatter(),
            guild_subscriptions=False,
        )
        self.load_extensions()

    # Recursivley load cogs from cogs folder. Ignore cogs starting with "_" then import extension
    # Green = Success | Red = Error
    def load_extensions(self):
        for extension in os.listdir("cogs"):
            if extension.startswith("_"):
                continue
            # Remove .py from extension
            extension = extension.replace(".py", "")
            # Import the extension
            try:
                self.load_extension("cogs." + extension)
                logging.info("Loaded cog: " + extension)
            except Exception as e:
                logging.error("Error loading cog: " + extension)
                logging.error(e)
                


    @property
    def token(self):
        """Returns your token wherever it is"""
        with open("data/config.json") as f:
            config = json.load(f)
            if config.get("token") == "":
                if not os.environ.get("token"):
                    # Automatically run setupWizard.py in case no token is set
                    logging.critical("No token found, running setupWizard.py")
                    os.system("python3 setupWizard.py")
                    sys.exit()
            else:
                token = config.get("token").strip('"')
        return os.environ.get("token") or token


    @classmethod
    def init(bot, token=None):
        """Stats the selfbot"""
        selfbot = bot()
        safe_token = token or selfbot.token.strip("")
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

    async def on_connect(self):
        
        cls()
        guilds = len(self.guilds)
        channels = len([c for c in self.get_all_channels()])
        
        # Get elapsed time since the selfbot started in seconds and ms. Rounded to the last 3 decimals.
        elapsed = datetime.datetime.now() - starttime
        elapsed = elapsed.seconds + (elapsed.microseconds / 10**6)
        elapsed = round(elapsed, 3)


        # Check if user is on the blacklist which can be found here https://gobyebye.github.io/cdn/b.json
        # If true exit the Selfbot else run like normal
        try:
            print(cyan + "Checking the blacklist" + reset)
            r = urllib.request.urlopen("https://gobyebye.github.io/cdn/b.json").read()
            r = r.decode("utf-8")
            r = json.loads(r)
            if r == self.user.id:
                blacklisted = True
                logging.critical("You are blacklisted from running the bot")
                sys.exit(1)
        except:
            blacklisted = False

        cls()

        # Print ascii art of Ares
        print(f"""
{red}
              ...                            
             ;::::;                           
           ;::::; :;                          
         ;:::::'   :;           {reset}Your time has come {red}          
        ;:::::;     ;.                        
       ,:::::'       ;           OOO\         
       ::::::;       ;          OOOOO\        
       ;:::::;       ;         OOOOOOOO       
      ,;::::::;     ;'         / OOOOOOO      
    ;:::::::::`. ,,,;.        /  / DOOOOOO    
  .';:::::::::::::::::;,     /  /     DOOOO   
 ,::::::;::::::;;;;::::;,   /  /        DOOO  
:`:::::::`;::::::;;::: ;::#  /            DOOO
::`:::::::`;:::::::: ;::::# /              DOOO
`:`:::::::`;:::::: ;::::::#/               DOOO
 :::`:::::::`;; ;:::::::::##                OOO
 ::::`:::::::`;::::::::;:::#                OO
 `:::::`::::::::::::;'`:;::#                O 
  `:::::`::::::::;' /  / `:#                  
   ::::::`:::::;'  /  /   `#   
{green}
        Version > {reset}{__version__}
        {green}Made by > {reset}{__author__}

{green}________________________________________________________________________________________________________

Logged in as: {reset}{self.user.name}#{self.user.discriminator}{green} - {reset}{self.user.id}
{green}Prefix: {reset}{self.command_prefix}
{green}Guilds: {reset}{guilds}
{green}Channels: {reset}{channels}
{green}Total Servers: {reset}{len(self.guilds)}
{green}Total Commands: {reset}{len(self.commands)}


{cyan}Finished starting up in {reset}{elapsed} second(s)
{green}________________________________________________________________________________________________________{reset}
        """)
        logging.info("Connected to the discord API")


    # Process the message using CustomContext subclass of discord.Context
    async def process_commands(self, message):
        """Utilises the CustomContext subclass of discord.Context"""
        ctx = await self.get_context(message, cls=CustomContext)
        if ctx.command is None:
            return
        await self.invoke(ctx)
    
    async def on_message(self, message):
            if message.author.id == self.user.id:
                if message.content.startswith(self.command_prefix):
                    await message.delete()
                    await self.process_commands(message)
    
    # Error handling for commands
    async def on_command_error(self, ctx, exception):
        # Really general error handling for commands
        logging.error(exception)

if __name__ == "__main__":
    Selfbot.init()


