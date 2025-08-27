# commands/animal_game.py
import discord
from discord.ext import commands
import asyncio
import random

class AnimalGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leaderboard = {}  # {guild_id: {user_id: score}}

    async def record_win(self, guild_id, user_id):
        """Increment a user's score in the leaderboard."""
        if guild_id not in self.leaderboard:
            self.leaderboard[guild_id] = {}
        if user_id not in self.leaderboard[guild_id]:
            self.leaderboard[guild_id][user_id] = 0
        self.leaderboard[guild_id][user_id] += 1

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_id = message.guild.id
        content = message.content.lower()

        # Check if the message contains a valid animal
        # Here you could pull from the Animals cog dynamically
        valid_animals = ["cat", "dog", "sheep"]  # add more later
        if any(animal in content for animal in valid_animals):
            await self.record_win(guild_id, message.author.id)
            await message.channel.send(
                f"🏆 {message.author.mention} got a point for spotting an animal!"
            )

    @commands.command()
    async def leaderboard(self, ctx):
        """Show the leaderboard for this server."""
        guild_id = ctx.guild.id
        if guild_id not in self.leaderboard or not self.leaderboard[guild_id]:
            await ctx.send("No scores yet!")
            return

        sorted_scores = sorted(
            self.leaderboard[guild_id].items(), key=lambda x: x[1], reverse=True
        )
        leaderboard_text = "\n".join(
            f"<@{user_id}>: {score}" for user_id, score in sorted_scores
        )
        await ctx.send(f"**Leaderboard:**\n{leaderboard_text}")


async def setup(bot):
    await bot.add_cog(AnimalGame(bot))
