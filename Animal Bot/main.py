import discord
from discord.ext import commands, tasks
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Store channel for drops
drop_channel_id = None

# Store leaderboard {user_id: score}
leaderboard = {}

# Current drop
current_animal = None

# Animals + images
animals = {
    "cat": "https://placekitten.com/300/300",
    "dog": "https://placedog.net/400/400",
    "fox": "https://randomfox.ca/images/1.jpg",
    "panda": "https://cdn.pixabay.com/photo/2017/08/01/00/39/panda-2568857_1280.jpg"
}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    drop_animals.start()


# Command to set channel
@bot.command()
async def setchannel(ctx, channel_id: int):
    global drop_channel_id
    channel = bot.get_channel(channel_id)
    if channel:
        drop_channel_id = channel.id
        await ctx.send(f"Drops will now appear in {channel.mention}")
    else:
        await ctx.send("Invalid channel ID.")


# Leaderboard command
@bot.command()
async def leaderboard(ctx):
    if not leaderboard:
        await ctx.send("No catches yet!")
        return

    sorted_lb = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    msg = "**Leaderboard:**\n"
    for i, (user_id, score) in enumerate(sorted_lb, 1):
        user = await bot.fetch_user(user_id)
        msg += f"{i}. {user.name} - {score} animals\n"
    await ctx.send(msg)


# Drop animals every 1 min
@tasks.loop(minutes=1)
async def drop_animals():
    global current_animal
    if drop_channel_id is None:
        return

    channel = bot.get_channel(drop_channel_id)
    if channel:
        animal, img = random.choice(list(animals.items()))
        current_animal = animal
        await channel.send("🐾 A wild animal appeared! Type its name to catch it!")
        await channel.send(img)


# Detect guesses
@bot.event
async def on_message(message):
    global current_animal

    if message.author == bot.user:
        return

    if current_animal and message.channel.id == drop_channel_id:
        if message.content.lower().strip() == current_animal:
            leaderboard[message.author.id] = leaderboard.get(message.author.id, 0) + 1
            await message.channel.send(f"🎉 {message.author.mention} caught the {current_animal}!")
            current_animal = None  # reset after catch

    await bot.process_commands(message)


# Run bot (Railway env)
bot.run(os.getenv("TOKEN"))    
