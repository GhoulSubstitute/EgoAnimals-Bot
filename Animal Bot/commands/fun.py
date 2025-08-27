import discord
from discord.ext import commands, tasks
import aiohttp
import random
import json
import os

LEADERBOARD_FILE = "leaderboard.json"
CHANNEL_ID = 123456789012345678  # Put your target channel ID here

class AnimalDrop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_animal = None
        self.current_image_url = None
        self.leaderboard = self.load_leaderboard()
        self.drop_animal.start()

    def load_leaderboard(self):
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_leaderboard(self):
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(self.leaderboard, f, indent=4)

    async def fetch_animal_image(self, animal):
        urls = {
            "cat": "https://api.thecatapi.com/v1/images/search",
            "dog": "https://dog.ceo/api/breeds/image/random",
            "fox": "https://randomfox.ca/floof/",
            "bird": "https://some-random-api.ml/img/birb",
            "sheep": "https://some-random-api.ml/img/sheep"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(urls[animal]) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                if animal == "cat":
                    return data[0]["url"]
                elif animal == "dog":
                    return data["message"]
                else:
                    return data["link"]

    @tasks.loop(seconds=random.randint(30, 120))
    async def drop_animal(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(CHANNEL_ID)
        animals = ["cat", "dog", "fox", "bird", "sheep"]
        self.current_animal = random.choice(animals)
        self.current_image_url = await self.fetch_animal_image(self.current_animal)
        if self.current_image_url:
            await channel.send(f"🖼️ Guess the animal! First to type it wins!\n{self.current_image_url}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not self.current_animal:
            return
        if message.content.lower() == self.current_animal:
            winner = str(message.author)
            self.leaderboard[winner] = self.leaderboard.get(winner, 0) + 1
            self.save_leaderboard()
            await message.channel.send(f"🎉 {winner} guessed it correctly! It was **{self.current_animal}**.")
            self.current_animal = None
            self.current_image_url = None

    @commands.command()
    async def leaderboard(self, ctx):
        if not self.leaderboard:
            await ctx.send("No scores yet!")
            return
        sorted_lb = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        lb_text = "\n".join([f"{i+1}. {user}: {score}" for i, (user, score) in enumerate(sorted_lb)])
        await ctx.send(f"🏆 **Leaderboard:**\n{lb_text}")

async def setup(bot):
    await bot.add_cog(AnimalDrop(bot))
