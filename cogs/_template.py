import discord
from discord.ext import commands
import logging

# Cross platfrom terminal colors
red = "\033[31m"
green = "\033[32m"
cyan = "\033[36m"
purple = "\033[95m"
reset = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"

class Source(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    # Pings and retunrs the latency to Discord
    async def ping(self, ctx):
        """Pings the bot and returns the latency"""
        # Latency is the time it takes to send a message to Discord
        latency = ctx.bot.latency
        # Latency is returned in milliseconds
        latency = latency * 1000
        # Latency is converted to a string
        latency = str(latency)
        # The latency is sent to the user
        await ctx.send(f'Pong! `{latency}ms`')


def setup(bot):
    bot.add_cog(TEMPLATE(bot))