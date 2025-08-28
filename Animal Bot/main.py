import discord
from discord.ext import commands, tasks
import asyncio
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Store guild-specific channel
drop_channels = {}
# Store leaderboard
leaderboard = {}
# Animals with image URLs
animals = {
    "cat": "https://placekitten.com/300/300",
    "dog": "https://placedog.net/500?id=1",
    "panda": "https://i.imgur.com/4AiXzf8.jpeg",
    "lion": "https://i.imgur.com/1V3Z1Hf.jpeg"
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    drop_animals.start()

@bot.command()
async def setchannel(ctx, channel_id: int):
    """Set the channel where animals will drop"""
    drop_channels[ctx.guild.id] = channel_id
    await ctx.send(f"Drops will now appear in <#{channel_id}>")

@bot.command()
async def leaderboard_cmd(ctx):
    """Show leaderboard"""
    if not leaderboard:
        await ctx.send("No winners yet 😢")
        return

    sorted_lb = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    text = "\n".join([f"{i+1}. <@{uid}> - {score}" for i, (uid, score) in enumerate(sorted_lb)])
    await ctx.send(f"🏆 **Leaderboard** 🏆\n{text}")

@tasks.loop(minutes=random.randint(5, 25))
async def drop_animals():
    await asyncio.sleep(random.randint(10, 60))  # extra randomness
    for guild_id, channel_id in drop_channels.items():
        channel = bot.get_channel(channel_id)
        if channel:
            name, url = random.choice(list(animals.items()))
            await channel.send(f"Guess the animal! 🐾", file=discord.File(fp=await url_to_file(url), filename=f"{name}.jpg"))

async def url_to_file(url: str):
    import aiohttp
    import io
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise ValueError("Could not download image")
            data = await resp.read()
            return io.BytesIO(data)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Check if guessing animal
    for animal in animals.keys():
        if animal in message.content.lower():
            leaderboard[message.author.id] = leaderboard.get(message.author.id, 0) + 1
            await message.channel.send(f"🎉 {message.author.mention} caught the **{animal}** correctly! +1 point")
            break

    await bot.process_commands(message)

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
