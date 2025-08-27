import discord
from discord.ext import commands

class AnimalGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leaderboard = {}  # {guild_id: {user_id: score}}

    async def record_win(self, guild_id, user_id):
        if guild_id not in self.leaderboard:
            self.leaderboard[guild_id] = {}
        self.leaderboard[guild_id][user_id] = self.leaderboard[guild_id].get(user_id, 0) + 1

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        content = message.content.lower()
        valid_animals = ["cat", "dog", "sheep", "rabbit", "fox", "panda"]
        if any(animal in content for animal in valid_animals):
            await self.record_win(message.guild.id, message.author.id)
            await message.channel.send(f"🏆 {message.author.mention} got a point!")

    @commands.command()
    async def leaderboard(self, ctx):
        guild_id = ctx.guild.id
        if guild_id not in self.leaderboard or not self.leaderboard[guild_id]:
            await ctx.send("No scores yet!")
            return
        sorted_scores = sorted(self.leaderboard[guild_id].items(), key=lambda x: x[1], reverse=True)
        text = "\n".join(f"<@{uid}>: {score}" for uid, score in sorted_scores)
        await ctx.send(f"**Leaderboard:**\n{text}")

async def setup(bot):
    await bot.add_cog(AnimalGame(bot))
