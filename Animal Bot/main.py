import os
import discord
from discord.ext import commands

# Get token from environment variable
TOKEN = os.getenv("TOKEN") 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load commands from commands folder
async def setup_extensions():
    await bot.load_extension("commands.fun")
    await bot.load_extension("commands.animals")
    await bot.load_extension("commands.moderation")

bot.loop.run_until_complete(setup_extensions())



bot.run(TOKEN)

