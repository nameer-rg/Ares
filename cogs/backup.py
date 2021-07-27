import discord
from discord.ext import commands
import logging
import requests
import json
import os 
import time


with open("./data/config.json") as f:
    config = json.load(f)

token = config.get("token")
headers = {"Authorization": token} # Yes I did accidentally forget to remove the token from the last comitt
url = "https://discord.com/api/v9/users/@me/relationships"

class backups(commands.Cog):
    """For when discord hates you the most"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    # Pings and retunrs the latency to Discord
    async def backup(self, ctx):
        """Backups your friendslist to a local file. That way you can still add them back later on!"""


        # Check if is an old backup file at data/backup.json
        if os.path.isfile("./data/backup.json"):
            # If it is rename is to backup.json.bak
            os.rename("./data/backup.json", "./data/backup.json.bak")
        
        # Start timer for metrics
        start = time.time()
        logging.debug("Started timer")

        saved_friends = 0
        # Get the friendslist
        friends = requests.get(url, headers=headers)
        friends_list = []

        # Iterate through the friends
        for friend in friends.json():
            if friend["type"] == 1: # Type 1 means that the user is a friend | Type 2 means that the user is a blocked user | Type 0 means that the user is not a friend
                # Grab relevant information
                # Example: name, discriminator, id
                name = friend["user"]["username"]
                discriminator = friend["user"]["discriminator"]
                id = friend["user"]["id"]
                # Convert ID to int
                id = int(id)


                # Convert the name, discriminator and id to json which will go under friend
                friend_json = {"username": name, "discriminator": discriminator, "id": id}
                # Add the json to the list
                friends_list.append(friend_json)
                saved_friends += 1
        
        logging.info(friends_list)
        # Save the list to a json file
        # Example json: {"friends": {friends_list}}
        with open("./data/backup.json", "w") as f:
            json.dump({"friends": friends_list}, f)
        

        # Remove the backup file if it exists
        if os.path.isfile("./data/backup.json.bak"):
            os.remove("./data/backup.json.bak")

        # Stop timer for metrics
        end = time.time()
        # Calculate the time it took to backup the friends
        time_taken = end - start
        
        # Logs
        logging.info(f"{ctx.author} has saved {saved_friends} friends in {str(time_taken)} seconds.")

    @commands.command()
    async def recover(self, ctx):
        """Prints all the saved friends in the terminal. NOTE: RECOVERING FRIENDS AUTOMATICALLY WILL GET YOUR ACCOUNT LIMITED THATS WHY ITS NOT IMPLEMENTED"""
        await ctx.send("You cannot recover friends automatically, look in your console for a list of your friends")
        # Load friends from data/backup.json
        with open("./data/backup.json", "r") as f:
            friends = json.load(f)["friends"]
        
        # Iterate through friends and print their name + discriminator then id
        # Example: <name>#<discriminator> | <id>
        for friend in friends:
            name = friend["username"]
            discriminator = friend["discriminator"]
            id = friend["id"]
            # Convert the id to string
            id = str(id)
            # Print the name, discriminator and id
            print(f"{name}#{discriminator} | {id}")

def setup(bot):
    bot.add_cog(backups(bot))