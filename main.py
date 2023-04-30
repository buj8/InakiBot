# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

audio_files = {"stop inventing": "stop_inventing.mp3"}

responses = {}
with open("responses.txt", "r") as f:
    for line in f:
        trigger, response = line.strip().split()
        responses[trigger] = response


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_message(message):
    response = responses.get(message.content)
    if response:
        await message.channel.send(response)


@bot.command()
async def play(ctx):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("Métete en un canal, bobo.")
        return

    content = ctx.message.content.lower().split()[1]
    filename = audio_files.get(content)
    if not filename:
        await ctx.send("Eso no existe.")
        return

    audio_source = discord.FFmpegPCMAudio(filename)
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if not voice_client:
        voice_client = await voice_channel.connect()
    else:
        await voice_client.move_to(voice_channel)

    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)


bot.run(os.environ["DISCORD_TOKEN"])
