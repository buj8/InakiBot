# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

responses = {}
with open('responses.txt', 'r') as f:
    for line in f:
        trigger, response = line.strip().split()
        responses[trigger] = response


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command()
async def respond(ctx):
    response = responses.get(ctx.message.content)
    if response:
        await ctx.send(response)


bot.run(os.environ["DISCORD_TOKEN"])
