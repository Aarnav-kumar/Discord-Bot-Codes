import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="!ticket for support"))

    # Send an embed message with instructions
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title='Support Ticket Bot',
                    description='For support, please type !ticket',
                    color=discord.Color.blue()
                )
                await channel.send(embed=embed)
                break

@bot.command()
async def ticket(ctx, *, issue: str):
    category = discord.utils.get(ctx.guild.categories, name='Tickets')
    ticket_channel = await category.create_text_channel(f'ticket-{ctx.author.name}')

    # Restrict access to "Member" role and administrative roles
    member_role = discord.utils.get(ctx.guild.roles, name='Member')
    admin_roles = [discord.utils.get(ctx.guild.roles, name='Admin'), discord.utils.get(ctx.guild.roles, name='Moderator')]

    for role in ctx.guild.roles:
        if role != member_role and role not in admin_roles:
            await ticket_channel.set_permissions(role, read_messages=False, send_messages=False)

    await ticket_channel.set_permissions(member_role, read_messages=True, send_messages=True)
    await ticket_channel.send(f'{ctx.author.mention}, your ticket has been created. Please describe your issue: {issue}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command. Please check the command and try again.')
    else:
        await ctx.send('An error occurred while running the command.')

bot.run('YOUR_TOKEN')
