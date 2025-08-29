import discord
from discord.ext import commands, tasks
import random
import os
from discord import Embed

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Store channel for drops
drop_channel_id = None

# Store leaderboard {user_id: score}
scores = {}

# Current drop
current_animal = None

# Animals + gifs (make sure they are .gif links from tenor/media.tenor)
animals = {
    "cat": "https://media.tenor.com/4y-1KJdP4xQAAAAC/cat-cute.gif",
    "dog": "https://media.tenor.com/5Rmbz9t5XQ0AAAAC/dog-smirk.gif",
    "fox": "https://media.tenor.com/ZpH_Z-7rOZQAAAAC/fox-snow.gif",
    "panda": "https://media.tenor.com/8Vy6bFp0tXwAAAAC/panda-cute.gif"
}


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    drop_animals.start()


# Command to set drop channel
@bot.command()
async def setchannel(ctx, channel_id: int):
    global drop_channel_id
    channel = bot.get_channel(channel_id)
    if channel:
        drop_channel_id = channel.id
        await ctx.send(f"✅ Drops will now appear in {channel.mention}")
    else:
        await ctx.send("❌ Invalid channel ID.")


# Leaderboard
@bot.command()
async def leaderboard(ctx):
    if not scores:
        await ctx.send("No catches yet!")
        return

    sorted_lb = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    msg = "**🏆 Leaderboard:**\n"
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

        # Embed with forced gif preview
        embed = Embed(title=f"🐾 A wild {animal} appeared!")
        embed.set_image(url=img)
        await channel.send(embed=embed)


# Detect guesses
@bot.event
async def on_message(message):
    global current_animal

    if message.author == bot.user:
        return

    if current_animal and message.channel.id == drop_channel_id:
        if message.content.lower().strip() == current_animal:
            scores[message.author.id] = scores.get(message.author.id, 0) + 1
            await message.channel.send(
                f"🎉 {message.author.mention} caught the {current_animal}!"
            )
            current_animal = None  # reset

    await bot.process_commands(message)


# Run bot (Railway / local)
bot.run(os.getenv("TOKEN"))
