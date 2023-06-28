import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
lockdown_enabled = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if lockdown_enabled and isinstance(message.author, discord.Member) and discord.utils.get(message.author.roles, name="Members"):
        await message.delete()
        await message.channel.send(f'{message.author.mention}, the server is currently in lockdown mode. Please refrain from sending messages.')

    # Auto moderation features
    filtered_words = ['bad_word1', 'bad_word2']
    content = message.content.lower()

    if any(word in content for word in filtered_words):
        await message.delete()
        # Perform additional actions like issuing warnings or punishments

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def add_role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'{role.name} added to {member.name}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'{role.name} removed from {member.name}')

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason: str):
    # Save the warning to a database or file
    await ctx.send(f'{member.name} has been warned for {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str):
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} has been banned for {reason}')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str):
    await member.kick(reason=reason)
    await ctx.send(f'{member.name} has been kicked for {reason}')

@bot.command()
async def ticket(ctx, *, issue: str):
    category = discord.utils.get(ctx.guild.categories, name='Tickets')
    ticket_channel = await category.create_text_channel(f'ticket-{ctx.author.name}')
    await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
    await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
    await ticket_channel.send(f'{ctx.author.mention}, your ticket has been created. Please describe your issue: {issue}')

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx):
    global lockdown_enabled
    lockdown_enabled = not lockdown_enabled

    if lockdown_enabled:
        await ctx.send('Lockdown enabled. Members are not allowed to send messages.')
    else:
        await ctx.send('Lockdown disabled. Members can now send messages.')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command. Please check the command and try again.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the necessary permissions to run this command.')
    else:
        await ctx.send('An error occurred while running the command.')

bot.run('YOUR_TOKEN')
