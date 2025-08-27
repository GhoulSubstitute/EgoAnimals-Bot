import os
import discord
from discord.ext import commands

# Get token from environment variable
TOKEN = os.getenv("TOKEN") 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load commands from commands folder
bot.load_extension("commands.fun")
bot.load_extension("commands.animals")
bot.load_extension("commands.moderation")


bot.run(TOKEN)
