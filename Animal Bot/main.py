import discord
from discord.ext import commands, tasks
import random
import os
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

drop_channel_id = None
current_animal = None
current_rarity = None

# JSON file for saving scores
SCORES_FILE = "scores.json"

# Load scores
if os.path.exists(SCORES_FILE):
    with open(SCORES_FILE, "r") as f:
        scores = json.load(f)
else:
    scores = {}

# Local animals grouped by rarity
animals = {
    "common": {
        "cat": "cat.gif",
        "dog": "dog.gif",
        "panda": "panda.gif",
        "fox": "fox.gif"
    },
    "rare": {
        "tiger": "tiger.gif",
        "eagle": "eagle.gif",
        "einstein": "einstein.gif",
        "pikachu": "pikachu.gif"
    },
    "ultra rare": {
        "dragon": "dragon.gif",
        "zeus": "zeus.gif",
        "cerberus": "cerberus.gif",
        "leviathan": "leviathan.gif"
    }
}

def save_scores():
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=4)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    drop_animals.start()


@bot.command()
async def setchannel(ctx, channel_id: int):
    global drop_channel_id
    channel = bot.get_channel(channel_id)
    if channel:
        drop_channel_id = channel.id
        await ctx.send(f"Drops will now appear in {channel.mention}")
    else:
        await ctx.send("❌ Invalid channel ID.")


@bot.command()
async def leaderboard(ctx):
    if not scores:
        await ctx.send("No catches yet!")
        return

    # Sort by total animals caught
    sorted_lb = sorted(scores.items(), key=lambda x: x[1]["total"], reverse=True)

    embed = discord.Embed(
        title="🏆 Leaderboard",
        description="Top 10 Animal Catchers",
        color=discord.Color.gold()
    )

    for i, (user_id, data) in enumerate(sorted_lb[:10], 1):
        user = await bot.fetch_user(int(user_id))
        embed.add_field(
            name=f"{i}. {user.name}",
            value=(
                f"**Total:** {data['total']}\n"
                f"Common: {data['common']} | Rare: {data['rare']} | Ultra Rare: {data['ultra rare']}"
            ),
            inline=False
        )

    # Show the stats of the user who called the command
    user_id = str(ctx.author.id)
    if user_id in scores:
        user_data = scores[user_id]
        rank = [u for u, _ in sorted_lb].index(user_id) + 1
        embed.add_field(
            name=f"✨ Your Rank: #{rank}",
            value=(
                f"**Total:** {user_data['total']}\n"
                f"Common: {user_data['common']} | Rare: {user_data['rare']} | Ultra Rare: {user_data['ultra rare']}"
            ),
            inline=False
        )

    await ctx.send(embed=embed)


@tasks.loop(minutes=30)
async def drop_animals():
    global current_animal, current_rarity
    if drop_channel_id is None:
        return

    channel = bot.get_channel(drop_channel_id)
    if channel:
        roll = random.randint(1, 100)
        if roll <= 80:
            rarity = "common"
        elif roll <= 95:
            rarity = "rare"
        else:
            rarity = "ultra rare"

        animal, filepath = random.choice(list(animals[rarity].items()))
        current_animal = animal
        current_rarity = rarity

        if os.path.exists(filepath):
            file = discord.File(filepath, filename=os.path.basename(filepath))
            await channel.send(
                content=f"🌟 A **{rarity.title()}** animal appeared: **{animal}**!\nType `{animal}` to catch it!",
                file=file
            )
        else:
            await channel.send(f"⚠️ Missing file for {animal} ({filepath})")


@bot.event
async def on_message(message):
    global current_animal, current_rarity

    if message.author == bot.user:
        return

    if current_animal and message.content.lower() == current_animal.lower():
        user_id = str(message.author.id)

        if user_id not in scores:
            scores[user_id] = {"total": 0, "common": 0, "rare": 0, "ultra rare": 0}

        scores[user_id]["total"] += 1
        scores[user_id][current_rarity] += 1
        save_scores()

        await message.channel.send(
            f"✅ {message.author.mention} caught the **{current_rarity.title()} {current_animal}**!"
        )

        current_animal = None
        current_rarity = None

    await bot.process_commands(message)


bot.run(os.getenv("TOKEN"))


