import discord
from discord.ext import commands
from comm import Commands
from events import Events
from discord_slash import SlashCommand, SlashContext
import json


with open('config.json', 'r', encoding='utf-8') as config_file:
    CONFIG = json.load(config_file)

TOKEN = CONFIG['settings']['token']
PREFIX = CONFIG['settings']['prefix']

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents().all())
slash = SlashCommand(bot, sync_commands=True)


bot.add_cog(Commands(bot))
bot.add_cog(Events(bot))

bot.run(TOKEN)
