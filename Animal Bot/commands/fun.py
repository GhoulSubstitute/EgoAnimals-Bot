import discord
from discord.ext import commands
import random
import pandas as pd


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}!")

    @commands.command(name="joke")
    async def joke(self, ctx):
        jokes = pd.read_csv("data/jokes.csv")["Joke"].tolist()
        await ctx.send(random.choice(jokes))

def setup(bot):
    bot.add_cog(Fun(bot))
