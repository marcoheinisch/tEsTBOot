# Discord python bot for Konziis!
# 
# Intresting:
#   https://realpython.com/how-to-make-a-discord-bot-python/
#   https://discordpy.readthedocs.io/en/latest/index.html
#   https://github.com/Rapptz/discord.py/tree/v1.7.2/examples

import os
import random
import asyncio

import discord
from discord import activity 
from discord.ext import commands
from discord.ext import tasks
import requests

from mcstatus import MinecraftServer


# DEBUG:
# from dotenv import load_dotenv
# load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MESSAGE_CHANNEL = "📯mitteilungen"
TXT_VOICE_UPDATE = ["is needy and wait's for academic trash talk", 
                    "is lonely and want's to talk", 
                    "is waiting for you ",
                    "is sitting alone here",
                    "<put here some random text stuff>"
                    ]

basic_activity = discord.Game(name="in der Cloud! ☁☁☁")
bot = commands.Bot(command_prefix='!', activity=basic_activity)

# Tasks

@tasks.loop(minutes=5)
async def test():
    # If you know the host and port, you may skip this and use MinecraftServer("example.org", 1234)
    server = MinecraftServer.lookup("ratius99.aternos.me")

    # 'status' is supported by all Minecraft servers that are version 1.7 or higher.
    status = server.status()
    if status.players.online:
        await bot.change_presence(activity = discord.CustomActivity(name="{0} mc players online ({1}ms))".format(status.players.online, status.latency)))
    else:
        await bot.change_presence(activity = basic_activity)

# Events

@bot.event 
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        channel_name=after.channel.name
        print("lonely state")
        await asyncio.sleep(10) # wait to est if user is shy / has misclicked
        if after.channel is not None:
            print("trigger")
            guild = discord.utils.get(bot.guilds, name=GUILD)
            voice_channel = discord.utils.get(guild.voice_channels, name=channel_name)
            print(voice_channel.voice_states)
            if len(voice_channel.voice_states)==1:
                print("t2")
                text_channel = discord.utils.get(guild.text_channels, name=MESSAGE_CHANNEL)
                await text_channel.send(f"Moin! {member.name} "+random.choice(TXT_VOICE_UPDATE)+". Visit him at #"+after.channel.name+".")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, hier ist der nerfffiger Diiscordbot aus Konziis!'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    #read messageses   
    await bot.process_commands(message)

# Commands

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    print("roll event!")
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    print(dice)
    await ctx.send(', '.join(dice))

@bot.command(name='hi', help='Say \"Hi!\" multiple times.')
async def roll(ctx, number_of_hi: int = 1):
    print("hi!")
    for _ in range(number_of_hi):
        await ctx.send('Hi!')

@bot.command(name='echo', help='Echo string.')
async def roll(ctx, txt:str):
    print("echo!")
    await ctx.send(txt)

@bot.command(name='emoji', help='Creates custom server emoji.')
async def roll(ctx, emoji_name: str, image_url:str):
    print("emoji!")
    response = requests.get(image_url)
    img = response.content   
    img = await ctx.guild.create_custom_emoji(name=emoji_name, image=img)
    await ctx.send(">> Emoji created: "+str(img))

@bot.command(name='molec', help='Visualize a given molecule string.', brief='Visualize a given molecule string. Supports MIME and other structural identifier. Note: Triple bonds in SMILES strings represented by \'\#\' have to be URL-escaped as \'%23\' and \'?\' as \'%3F\'. ')
async def roll(ctx, smile_string: str):
    print('molec!')
    url1 = 'http://cactus.nci.nih.gov/chemical/structure/' + smile_string+ '/image'
    await ctx.send(">> Molecule: "+ str(url1))

@bot.event
async def on_command_error(ctx, error):
    print(error.__cause__)
    await ctx.send(">> Error: "+str(error.__cause__))
    

bot.run(TOKEN)


# Custom event example:
# 
# bot.dispatch("custom_event", arg1, arg2)
#
# @bot.event
# async def on_custom_event(arg1, arg2):
#     print("Custom event")
