import discord
from discord.ext import commands
import inspect

class source(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    # Returns the sourcee of a command
    async def source(self, ctx, *, command: str):
        """Returns the source code of a command
        
        Paramaters
        • command - the name of the command
        """
        source = ctx.bot.get_command(command).callback.__code__
        source = inspect.getsource(source)
        await ctx.send(f"```py\n{source}\n```")

def setup(bot):
    bot.add_cog(source(bot))