# commands/animals.py
import discord
from discord.ext import commands, tasks
import random
import aiohttp

class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channels = {}  # Stores guild_id: channel_id where drops happen
        self.animal_images = {
            "cat": [
                "https://cdn2.thecatapi.com/images/MTY3ODIyMQ.jpg",
                "https://cdn2.thecatapi.com/images/MTY3ODIzMg.jpg"
            ],
            "dog": [
                "https://images.dog.ceo/breeds/husky/n02110185_1469.jpg",
                "https://images.dog.ceo/breeds/retriever-golden/n02099601_2006.jpg"
            ],
            "sheep": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Ovis_aries_M%C3%A4rchen.jpg/800px-Ovis_aries_M%C3%A4rchen.jpg"
            ]
        }
        self.drop_animals.start()  # start the task loop

    # Task loop to drop random animal images
    @tasks.loop(minutes=5)
    async def drop_animals(self):
        for guild_id, channel_id in self.channels.items():
            guild = self.bot.get_guild(guild_id)
            if not guild:
                continue
            channel = guild.get_channel(channel_id)
            if not channel:
                continue

            animal = random.choice(list(self.animal_images.keys()))
            image_url = random.choice(self.animal_images[animal])
            await channel.send(f"Random {animal} drop!\n{image_url}")

    @commands.command()
    async def setdrop(self, ctx, channel: discord.TextChannel):
        """Set the channel for random animal drops in this server."""
        self.channels[ctx.guild.id] = channel.id
        await ctx.send(f"✅ Random animal drops will now appear in {channel.mention}")

    @commands.command()
    async def addanimal(self, ctx, animal: str, url: str):
        """Add a new animal type or URL to the list."""
        if animal not in self.animal_images:
            self.animal_images[animal] = []
        self.animal_images[animal].append(url)
        await ctx.send(f"✅ Added image for `{animal}`!")

    @commands.command()
    async def animals(self, ctx):
        """Show all animal types currently in the bot."""
        animal_list = ", ".join(self.animal_images.keys())
        await ctx.send(f"Available animals: {animal_list}")

# Setup function required for cogs with setup hook
async def setup(bot):
    await bot.add_cog(Animals(bot))
