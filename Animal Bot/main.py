import discord
from discord.ext import commands, tasks
import random
import asyncio
import json
from pathlib import Path
import os

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = Path("animal_data.json")

# Load saved data
if DATA_FILE.exists():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"channels": {}, "scores": {}}

# 🖼️ Animal images
ANIMALS = {
    "dog": "https://place-puppy.com/400x400",
    "cat": "https://placekitten.com/400/400",
    "rabbit": "https://loremflickr.com/400/400/rabbit",
    "fox": "https://loremflickr.com/400/400/fox",
}

current_animals = {}  # guild_id -> (animal, user_caught)


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    animal_drops.start()


@commands.has_permissions(manage_guild=True)
@bot.command(help="Set the channel where animals will drop. Usage: !setchannel <channel_id>")
async def setchannel(ctx, channel_id: int):
    channel = ctx.guild.get_channel(channel_id)
    if not channel:
        await ctx.send("❌ Invalid channel ID.")
        return

    data["channels"][str(ctx.guild.id)] = channel_id
    save_data()
    await ctx.send(f"✅ Animal drop channel set to {channel.mention}")


@bot.command(help="Show the animal catching leaderboard.")
async def leaderboard(ctx):
    guild_scores = data["scores"].get(str(ctx.guild.id), {})
    if not guild_scores:
        await ctx.send("🏆 No catches yet!")
        return

    sorted_scores = sorted(guild_scores.items(), key=lambda x: x[1], reverse=True)
    desc = "\n".join([f"<@{uid}> — **{score}**" for uid, score in sorted_scores[:10]])

    embed = discord.Embed(
        title="🏆 Animal Catch Leaderboard",
        description=desc,
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)


@tasks.loop(minutes=5)
async def animal_drops():
    await bot.wait_until_ready()

    for guild in bot.guilds:
        channel_id = data["channels"].get(str(guild.id))
        if not channel_id:
            continue

        channel = guild.get_channel(channel_id)
        if not channel:
            continue

        # 1 in 3 chance every 5 min → avg ~15 min, max ~25
        if random.random() < 0.33:
            animal, img_url = random.choice(list(ANIMALS.items()))
            embed = discord.Embed(
                title="🐾 A wild animal appeared!",
                description=f"Type **{animal}** to catch it!",
                color=discord.Color.green()
            )
            embed.set_image(url=img_url)
            await channel.send(embed=embed)
            current_animals[guild.id] = (animal, None)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    guild_id = message.guild.id if message.guild else None
    if guild_id and guild_id in current_animals:
        animal, caught_by = current_animals[guild_id]

        if caught_by is None and message.content.lower().strip() == animal:
            current_animals[guild_id] = (animal, message.author.id)

            # Update scores
            guild_scores = data["scores"].setdefault(str(guild_id), {})
            guild_scores[str(message.author.id)] = guild_scores.get(str(message.author.id), 0) + 1
            save_data()

            await message.channel.send(
                f"🎉 {message.author.mention} caught the **{animal}**!"
            )

    await bot.process_commands(message)


bot.run(TOKEN)

