#!/usr/bin/env python

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv, dotenv_values
from menu import get_menu
from annuaire import annuaire
from datetime import datetime
from edt import Edt
import locale

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

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

@bot.slash_command(name="timetable")
async def timetable(ctx, group):
    group = group.upper()
    print(f"{ctx.author}: /edt {group}")

    # START TIME 
    start = datetime.now()
    urls = dotenv_values(".env.edt")
    
    if group not in urls.keys():
        print(f"{group} group does not exist")
        embed = discord.Embed(title=f"Emploi du temps")
        embed.add_field(name=f"ERREUR", value="groupe inconnu", inline=False)
        await ctx.respond(embed=embed)
        return

    timet = Edt(urls[group])

    # END TIME
    end = datetime.now()
    rtime = int((end - start).total_seconds() * 1000)

    embed = discord.Embed(title=f"Emploi du temps")
    for cour in timet.getNextNDays():
        # HAHAHHA WTF IS THIS WHY IS THERE NO strftime FOR TIMEDELTA
        time="h".join(str(cour["end"]-cour["start"]).split(":")[:-1])
        embed.add_field(
                name=f"➡️ {', '.join([cour['ressource'], cour['nomRessource']])}"+f" ({cour['typeCours']})",
                value=f"{cour['start'].strftime('%A %d %B %H:%M')} ({time})",
                inline=False,
            )
        embed.add_field(name="Groupes", value=", ".join(cour["groupes"]), inline=True)
        embed.add_field(name="Prof(s)", value=", ".join(cour['prof']), inline=True)
        #embed.add_field(name="", value="", inline=False)
    embed.set_footer(text=f"🗿 Résultat(s) récupéré(s) en {rtime}ms.")
    await ctx.respond(embed=embed)

bot.run(token)
