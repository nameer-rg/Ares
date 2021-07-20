import json
import logging
import os
import sys
import urllib

import discord
from discord.ext import commands

# Cross platfrom terminal colors
red = "\033[31m"
green = "\033[32m"
cyan = "\033[36m"
purple = "\033[95m"
reset = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"
class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    # Returns the latency of the selfbot
    @commands.command(name='ping', aliases=['latency'])
    async def ping(self, ctx):
        """Pong! Returns your ping"""
        # Get the latency
        latency = self.bot.latency
        # Create the embed
        embed = discord.Embed(title="Pong!", description=f"Latency: {latency * 1000:.0f}ms", color=0x00ff00)
        # Send the embed
        await ctx.send(embed=embed)
        # Log the command
        logging.info("Pinged the bot with latency: " + latency)

    @commands.command()
    #Restarts the Bot
    async def restart(self, ctx):
        """Restarts the bot"""
        await ctx.send(f"Restarting...")
        os.execv(sys.executable, ['python'] + sys.argv)

    # Checks the bot for updates using autoupdater in selfbot.py
    @commands.command()
    async def update(self, ctx):
        """Checks the selfbot for updates"""
        logging.info("Grabbing current version number")
        # Load the version number from data/version.json
        with open('data/version.json') as f:
            data = json.load(f)
            __version__ = data['version']
            logging.info("Current version: " + __version__)

        logging.info("Grabbing latest version number" )
        # Github repo is https://github.com/GoByeBye/Ares
        # Check the raw file on github https://github.com/GoByeBye/Ares/data/version.json against __version__ of selfbot.py
        # if version differs run update.py and close selfbot.py
        try:
            import urllib.request
            version = urllib.request.urlopen("https://raw.githubusercontent.com/GoByeBye/Ares/master/data/version.json").read()
            version = version.decode("utf-8")
            version = json.loads(version)
            version = version["version"]
            logging.info("Newest version is: " + str(version))
            if version != __version__:
                logging.info("A new update is available!")
                logging.info("Updating...")
                os.system("python update.py")
                sys.exit()
            else:
                logging.info("You are running the latest version!")
        except:
            logging.error("Error: Could not check for updates.")
            logging.error("Please check your internet connection")
            sys.exit()

def setup(bot):
    bot.add_cog(utils(bot))
