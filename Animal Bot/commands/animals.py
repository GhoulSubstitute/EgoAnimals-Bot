import discord
from discord.ext import commands
import random

animal_images = {
    "cat": [
        "https://cataas.com/cat",
        "https://placekitten.com/400/400"
    ],
    "dog": [
        "https://random.dog/woof.json",
        "https://placedog.net/400/400"
    ],
    "sheep": [
        "https://place-sheep.com/400/400"
    ],
    # Add more animals here
    "fox": ["https://randomfox.ca/images/1.jpg"],
    "bird": ["https://some-random-api.ml/img/birb"]
}


class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="animal")
    async def animal(self, ctx, kind: str):
        kind = kind.lower()
        if kind not in animal_images:
            await ctx.send(f"Sorry, I don’t have images for {kind}.")
            return
        img = random.choice(animal_images[kind])
        embed = discord.Embed(title=f"{kind.capitalize()} for you!")
        embed.set_image(url=img)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Animals(bot))
