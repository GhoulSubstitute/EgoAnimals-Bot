import discord
from discord.ext import commands
import random
import asyncio
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# store channel ID where drops happen
drop_channel_id = None  

# animal images
animals = [
    "https://i.imgur.com/a1.png",
    "https://i.imgur.com/b2.png",
    "https://i.imgur.com/c3.png"
]

# set channel command
@bot.command()
async def setchannel(ctx, channel_id: int):
    global drop_channel_id
    drop_channel_id = channel_id
    await ctx.send(f"✅ Drop channel set to <#{channel_id}>")

# random animal drop task
async def drop_animals():
    await bot.wait_until_ready()
    global drop_channel_id

    while True:
        if drop_channel_id:
            channel = bot.get_channel(drop_channel_id)
            if channel:
                animal = random.choice(animals)
                await channel.send("🐾 A wild animal appeared!")
                await channel.send(animal)

        # wait random time between 5 and 25 minutes
        wait_time = random.randint(300, 1500)
        await asyncio.sleep(wait_time)

# schedule drop_animals in setup_hook
@bot.event
async def setup_hook():
    bot.loop.create_task(drop_animals())

# run bot
bot.run(os.getenv("TOKEN"))
