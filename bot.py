#!/usr/bin/env python

import discord
import os
import random
from dotenv import load_dotenv

from discord.ext import commands

import requests
import locale
import datetime
from lxml import html

load_dotenv()

token = os.getenv('TOKEN')

bot = commands.Bot()

# flemme de faire des cogs
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")


@bot.slash_command(name="menu")
async def menu(ctx):
    print(f"Menu demandé par {ctx.author}")
    url = os.getenv("URL")

    response = requests.get(url)
    tree = html.fromstring(response.content)

    dates = tree.xpath('//*[@id="menu-repas"]/ul/li/h3/text()')
    for i, item in enumerate(dates):
        date = item.split()[3:]
        dates[i] = datetime.datetime.strptime(
            f"{'%04d'%int(date[2])}-{date[1]}-{'%02d'%int(date[0])}",
            '%Y-%B-%d')

    menus = []
    for i in range(1, len(dates)+1):
        menu = tree.xpath(
            f'//*[@id="menu-repas"]/ul/li[{i}]/div/div[2]/div/div/ul[1]/li/text()')[1:-1]
        menus.append(menu)

    embed = discord.Embed(title="Menu")
    for date, menu in zip(dates, menus):
        embed.add_field(name=date.strftime(
            '%A %d %B %Y'), value=", ".join(menu), inline=False)
        print(f'{date} {menu}')
    await ctx.respond(embed=embed)

bot.run(token)
