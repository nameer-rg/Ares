import discord
from discord.ext.commands import DefaultHelpCommand


class helpformatter(DefaultHelpCommand):
    def get_ending_note(self):
        return "The shittest selfbot in existence by Daddie#6969\n\nWebsite > https://daddie.dev"