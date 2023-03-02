#!/usr/bin/env python

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from menu import get_menu
from annuaire import annuaire
from datetime import datetime

load_dotenv()

token = os.getenv('TOKEN')

bot = commands.Bot()

@bot.slash_command(name="menu")
async def menu(ctx):
    print(f"{ctx.author}: /menu")

    start = datetime.now()
    menu = get_menu(os.getenv("URL"))
    end = datetime.now()
    rtime = int((end - start).total_seconds() * 1000)

    embed = discord.Embed(title="Menu")
    for jour in menu:
        embed.add_field(name=f"➡️ {jour['date']}", value=", ".join(jour['menu']), inline=False)
        embed.add_field(name="Pastabox", value=", ".join(jour['pastabox']), inline=True)
        embed.add_field(name="Sandwichs", value=", ".join(jour['sandwichs']), inline=True)
        embed.add_field(name="", value="", inline=False)
    embed.set_footer(text=f"🗿 Menu récupéré en {rtime}ms.")
    await ctx.respond(embed=embed)

@bot.slash_command(name="prof")
async def prof(ctx, search):
    print(f"{ctx.author}: /prof {search}")

    start = datetime.now()
    result = annuaire(os.getenv("ANNUAIRE"), search)
    end = datetime.now()
    rtime = int((end - start).total_seconds() * 1000)

    embed = discord.Embed(title=f"Résultat(s) pour: {search}")
    for prof in result:
        embed.add_field(name=f"➡️ {prof['name'].upper()} {prof['surname']}", value=prof["email"], inline=False)
        embed.add_field(name="", value="", inline=False)
    embed.set_footer(text=f"🗿 Résultat(s) récupéré(s) en {rtime}ms.")
    await ctx.respond(embed=embed)

bot.run(token)
