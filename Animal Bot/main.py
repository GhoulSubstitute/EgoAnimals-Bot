import discord
from discord.ext import commands
import asyncio
import random
import aiohttp
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Store drop channels
drop_channels = {}

# Animal images
animals = {
    "Cat": "https://placekitten.com/400/300",
    "Dog": "https://placedog.net/400/300",
    "Panda": "https://i.imgur.com/B0asE0n.jpeg",
    "Fox": "https://i.imgur.com/aC9N9iN.jpeg"
}

# Helper: fetch image from URL
async def url_to_file(url: str, filename: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.read()
            return discord.File(fp=io.BytesIO(data), filename=filename)

# Set channel command
@bot.command()
async def setchannel(ctx, channel_id: int):
    drop_channels[ctx.guild.id] = channel_id
    await ctx.send(f"Drops will now happen in <#{channel_id}> 🎉")

# Background task
async def drop_animals():
    await bot.wait_until_ready()
    while not bot.is_closed():
        wait_time = random.randint(5*60, 25*60)  # 5–25 min
        await asyncio.sleep(wait_time)

        for guild_id, channel_id in drop_channels.items():
            channel = bot.get_channel(channel_id)
            if channel:
                name, url = random.choice(list(animals.items()))
                file = await url_to_file(url, f"{name}.jpg")
                if file:
                    await channel.send(f"🐾 Guess the animal!", file=file)
                else:
                    await channel.send(f"❌ Failed to fetch image for {name}.")

# Start the background loop
bot.loop.create_task(drop_animals())

# Run the bot (Railway style)
bot.run(os.getenv("DISCORD_TOKEN"))
