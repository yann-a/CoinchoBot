import sys
import discord
from discord.ext import commands

from coinche import Coinche
from carte import Carte


# Load the bot token
TOKEN = ""
with open(".token", "r") as f:
    TOKEN = f.readline()

bot = commands.Bot(command_prefix="!")

tables = {}

@bot.command()
async def start(ctx, p2: discord.Member, p3: discord.Member, p4: discord.Member):
    players = [ctx.author, p2, p3, p4]
    await ctx.send("Starting a game with " + ", ".join([p.mention for p in players]), delete_after = 10)

    guild = ctx.guild
    base = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }


    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        players[0] : discord.PermissionOverwrite(read_messages=True),
        players[1] : discord.PermissionOverwrite(read_messages=True),
        players[2] : discord.PermissionOverwrite(read_messages=True),
        players[3] : discord.PermissionOverwrite(read_messages=True)
    }

    category = discord.utils.find(lambda cat: cat.name == "Tables de Coinche", ctx.guild.categories)
    if not category:
        category = await ctx.guild.create_category("Tables de Coinche", overwrites=base)

    channel = await ctx.guild.create_text_channel(
        name="table-coinche",
        category=category,
        overwrites=overwrites
    )

    await channel.send("Hey, ça se passe ici ! " + ", ".join([p.mention for p in players]))
    await channel.send("Phase d'annonce : entrez `!annonce <annonce> <couleur>` pour commencer")

    tables[channel.id] = Coinche(channel, players)
    await tables[channel.id].deal()
    await ctx.message.delete()

@bot.command()
async def annonce(ctx, goal: int, trump: str):
    table = tables[ctx.channel.id]
    await table.annonce(ctx, goal, trump)

@bot.command()
async def play(ctx, value, *args):
    color = args[-1]
    print("Trigger")
    await ctx.channel.send("J'ai compris : " + str(Carte(value, color)))
    table = tables[ctx.channel.id]
    await table.play(ctx, value, color)

bot.run(TOKEN)
