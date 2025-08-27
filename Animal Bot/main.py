import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

class AnimalBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.load_extension("commands.animals")
        await self.load_extension("commands.animal_game")
        await self.load_extension("commands.moderation")

bot = AnimalBot()
bot.run(TOKEN)
