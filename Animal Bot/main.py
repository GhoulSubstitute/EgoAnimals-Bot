import discord
from discord.ext import commands
import os


class AnimalBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.TOKEN = os.getenv("TOKEN")

    async def setup_hook(self):
        # Load all cogs
        await self.load_extension("commands.fun")        # your random image drops cog
        await self.load_extension("commands.animals")    # other animal commands
        await self.load_extension("commands.moderation") # moderation cog if needed

bot = AnimalBot()
bot.run(bot.TOKEN)

