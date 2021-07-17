import discord
from discord.ext import commands

class utils(commands.Cog):
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

    @commands.command()
    # Restarts the selfbot
    async def restart(self, ctx):
        """Restarts the bot"""
        # Restarts the bot
        await ctx.send('Restarting...')
        await ctx.bot.logout()
        await ctx.bot.close()
        await ctx.bot.start()
        

def setup(bot):
    bot.add_cog(utils(bot))