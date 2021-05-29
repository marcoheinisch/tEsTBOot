# Discord python bot for Konziis!
# 
# Quellen:
# https://realpython.com/how-to-make-a-discord-bot-python/
# https://discordpy.readthedocs.io/en/latest/index.html

import os
import random

import discord 
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# Events

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

@bot.event
async def on_voice_state_update(member, before, after):
    if before.voice_channel is None and after.voice_channel is not None:
        for channel in before.server.channels:
            if channel.name == 'admin':
                await bot.send_message(channel, "Howdy")
        print(str(after))

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

