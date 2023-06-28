import discord
from discord.ext import commands, tasks
import random
import asyncio

token_secret = os.environ['TOKEN']
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Pandy Coins!"))

@bot.event
async def on_guild_join(guild):
    print(f'Bot joined guild: {guild.name}')

@bot.event
async def on_guild_remove(guild):
    print(f'Bot left guild: {guild.name}')

@bot.command()
async def ping(ctx):
    """Check the bot's latency"""
    latency = bot.latency
    await ctx.send(f'Pong! Latency: {latency * 1000}ms')

@bot.command()
async def daily(ctx):
    """Claim daily Pandy coins"""
    user_id = ctx.author.id
    #Adding Pandy coins
    await ctx.send(f'200 Pandy coins added to your balance, {ctx.author.mention}!')

@tasks.loop(hours=24)
async def remove_coins():
    """Remove coins from every server member's balance"""
    #remove 120 Pandy coins from every server member's balance
    #remove coins from user's balance goes here

@bot.command()
@commands.has_permissions(administrator=True)
async def admincommand(ctx):
    """An admin command that can only be used by administrators"""
    await ctx.send('This is an admin command!')

@bot.command()
async def roll(ctx, sides: int = 6):
    """Roll a dice with the specified number of sides (default: 6)"""
    if sides < 2:
        await ctx.send("The dice must have at least 2 sides.")
    else:
        result = random.randint(1, sides)
        await ctx.send(f"You rolled a {result}!")

@bot.command()
async def flip(ctx):
    """Flip a coin"""
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"The coin landed on **{result}**!")

@bot.command()
async def giveaway(ctx, duration: int, *, prize: str):
    """Start a giveaway with the specified duration in minutes and prize"""
    await ctx.send(f"A giveaway for **{prize}** is starting now! React with 🎉 to participate!")

    giveaway_msg = await ctx.send(f"🎉 **GIVEAWAY** 🎉\nPrize: {prize}\nTime remaining: {duration} minutes")
    await giveaway_msg.add_reaction("🎉")

    await asyncio.sleep(duration * 60)

    updated_giveaway_msg = await ctx.fetch_message(giveaway_msg.id)
    reaction = discord.utils.get(updated_giveaway_msg.reactions, emoji="🎉")
    participants = await reaction.users().flatten()
    winner = random.choice(participants)

    await ctx.send(f"🎉 **GIVEAWAY ENDED** 🎉\nPrize: {prize}\nWinner: {winner.mention}")

remove_coins.start()
bot.run('token_secret')
