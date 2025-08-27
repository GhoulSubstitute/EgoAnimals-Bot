import discord
from discord.ext import commands, tasks
import aiohttp
import random
import json
import os

LEADERBOARD_FILE = "leaderboard.json"

class AnimalGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_animal = None
        self.current_image_url = None
        self.leaderboard = self.load_leaderboard()

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
        if animal not in urls:
            return None
        async with aiohttp.ClientSession() as session:
            async with session.get(urls[animal]) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                # Handle APIs differently
                if animal == "cat":
                    return data[0]["url"]
                elif animal == "dog":
                    return data["message"]
                else:
                    return data["link"]

    @commands.command()
    async def start_animal_game(self, ctx):
        animals = ["cat", "dog", "fox", "bird", "sheep"]
        self.current_animal = random.choice(animals)
        self.current_image_url = await self.fetch_animal_image(self.current_animal)

        if not self.current_image_url:
            await ctx.send("Couldn't fetch an animal image. Try again later.")
            return

        await ctx.send(f"🖼️ Guess the animal! First to type the correct animal wins!\n{self.current_image_url}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not self.current_animal:
            return

        if message.content.lower() == self.current_animal:
            winner = str(message.author)
            self.leaderboard[winner] = self.leaderboard.get(winner, 0) + 1
            self.save_leaderboard()
            await message.channel.send(f"🎉 {winner} guessed it correctly! The animal was **{self.current_animal}**.")
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
    await bot.add_cog(AnimalGame(bot))
