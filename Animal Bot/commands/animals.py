import discord
from discord.ext import commands, tasks
import random

ANIMALS = ["cat", "dog", "sheep", "rabbit", "fox", "panda"]  # add more

class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_ids = []  # fill with IDs of channels you want drops in
        self.drop_animals.start()

    @tasks.loop(minutes=2)  # drops an animal every 2 minutes
    async def drop_animals(self):
        if not self.channel_ids:
            return
        channel_id = random.choice(self.channel_ids)
        channel = self.bot.get_channel(channel_id)
        if channel:
            animal = random.choice(ANIMALS)
            await channel.send(f"Random animal drop! Type **{animal}** first!")

    @drop_animals.before_loop
    async def before_drop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Animals(bot))
