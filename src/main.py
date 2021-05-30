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
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

TXT_VOICE_UPDATE = ["is needy and wait's for academic trash talk", 
                    "is lonely and want's to talk", 
                    "is waiting for you ",
                    "is sitting alone here",
                    "<put here some random text stuff>"
                    ]

# Events

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        print("lonely state")
        await asyncio.sleep(10) # wait to est if user is shy
        if after.channel is not None:
            guild = discord.utils.get(bot.guilds, name=GUILD)
            text_channel = discord.utils.get(guild.text_channels, name="📯mitteilungen")
            await text_channel.send(f"Moin moin! {member.name} "+random.choice(TXT_VOICE_UPDATE)+". Visit him at #"+after.channel.name+".")

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

@bot.command(name='hi', help='Say Hello!')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    print("hi!")
    await ctx.send('Hi!')

@bot.command(name='echo', help='Echos')
async def roll(ctx, txt:str):
    print("echo!")
    await ctx.send(txt)

@bot.command(name='emoji', help='Creates custom server emoji.')
async def roll(ctx, emoji_name: str, image_url:str):
    print("emoji!")
    response = requests.get(image_url)
    img = response.content   
    img = await ctx.guild.create_custom_emoji(name=emoji_name, image=img)
    await ctx.send(">> Emoji erstellt: "+str(img))

@bot.event
async def on_command_error(ctx, error):
    print(error.__cause__)
    await ctx.send(">> Fehler:"+str(error.__cause__))
    

bot.run(TOKEN)


# Custom event example:
# 
# bot.dispatch("custom_event", arg1, arg2)
#
# @bot.event
# async def on_custom_event(arg1, arg2):
#     print("Custom event")
